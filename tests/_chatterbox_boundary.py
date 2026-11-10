"""Test-only stand-ins for the boundaries of the inference service's voice cloning call.

Used by the CRM-4 tests of work item chatterbox-cloud-run (API-Contract.md). Nothing here is
production code, and nothing here decides what the inference service answers:

- ``FakeBackend`` serves, on one loopback port, a stand-in OAuth 2.0 token endpoint (the
  ``token_uri`` of a test-generated service-account key) and a stand-in Chatterbox
  ``POST /v1/synthesize`` that answers the way the approved contract and Cloud Run do.
- ``write_service_account_key`` writes a service-account key file with a newly generated RSA
  key whose ``token_uri`` points at the stand-in token endpoint.
- ``isolate_network`` clears proxy settings and blocks, and records, every connection and DNS
  lookup that is not loopback.
"""

from __future__ import annotations

import asyncio
import base64
import contextlib
import ipaddress
import json
import socket
import threading
import time
import uuid
from pathlib import Path

import uvicorn
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from starlette.datastructures import UploadFile

SERVICE_ACCOUNT_EMAIL = "crm4-test-invoker@crm4-test-project.iam.gserviceaccount.com"
JWT_BEARER_GRANT = "urn:ietf:params:oauth:grant-type:jwt-bearer"
SAMPLE_PATH_DETAIL = "sample_path is not supported; send the voice sample as sample_audio"
PROXY_VARIABLES = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "no_proxy",
)
TRICKLE_PIECES = 12


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(segment: str) -> bytes:
    return base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))


def jwt_parts(token: str) -> tuple[dict, dict, bytes, bytes]:
    """Split a compact JWT into header, claims, signature and signing input, without verifying it."""
    header_segment, claims_segment, signature_segment = token.split(".")
    header = json.loads(b64url_decode(header_segment))
    claims = json.loads(b64url_decode(claims_segment))
    signing_input = f"{header_segment}.{claims_segment}".encode("ascii")
    return header, claims, b64url_decode(signature_segment), signing_input


class ServiceAccountKey:
    """A test-generated service-account key file and the public half of its RSA key."""

    def __init__(self, path: Path, email: str, public_key) -> None:
        self.path = path
        self.email = email
        self.public_key = public_key

    def verify(self, assertion: str) -> dict:
        """Verify an RS256 JWT signed with this key and return its claims."""
        header, claims, signature, signing_input = jwt_parts(assertion)
        assert header.get("alg") == "RS256", header
        self.public_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())
        return claims


def write_service_account_key(path: Path, token_uri: str, email: str = SERVICE_ACCOUNT_EMAIL) -> ServiceAccountKey:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")
    info = {
        "type": "service_account",
        "project_id": "crm4-test-project",
        "private_key_id": uuid.uuid4().hex,
        "private_key": pem,
        "client_email": email,
        "client_id": "100000000000000000000",
        "token_uri": token_uri,
        "universe_domain": "googleapis.com",
    }
    path.write_text(json.dumps(info), encoding="utf-8")
    return ServiceAccountKey(path, email, private_key.public_key())


class NetworkGuard:
    """Records every non-loopback connection or DNS lookup attempted while it is installed."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.blocked: list[str] = []

    def record(self, attempt: str) -> None:
        with self._lock:
            self.blocked.append(attempt)

    def assert_no_network(self) -> None:
        assert self.blocked == [], f"non-loopback network access was attempted: {self.blocked}"


def _is_loopback(host) -> bool:
    if host is None:
        return True
    if isinstance(host, bytes):
        host = host.decode("ascii", "replace")
    host = str(host)
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host.split("%", 1)[0]).is_loopback
    except ValueError:
        return False


def isolate_network(monkeypatch) -> NetworkGuard:
    """Clear proxy settings and block every connection and DNS lookup that is not loopback."""
    guard = NetworkGuard()
    for name in PROXY_VARIABLES:
        monkeypatch.delenv(name, raising=False)

    real_getaddrinfo = socket.getaddrinfo
    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex

    def guarded_getaddrinfo(host, *args, **kwargs):
        if not _is_loopback(host):
            guard.record(f"getaddrinfo {host!r}")
            raise socket.gaierror(socket.EAI_NONAME, f"blocked by the CRM-4 test network guard: {host!r}")
        return real_getaddrinfo(host, *args, **kwargs)

    def _check(address) -> None:
        if isinstance(address, tuple) and not _is_loopback(address[0]):
            guard.record(f"connect {address!r}")
            raise ConnectionRefusedError(f"blocked by the CRM-4 test network guard: {address!r}")

    def guarded_connect(self, address):
        _check(address)
        return real_connect(self, address)

    def guarded_connect_ex(self, address):
        _check(address)
        return real_connect_ex(self, address)

    monkeypatch.setattr(socket, "getaddrinfo", guarded_getaddrinfo)
    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", guarded_connect_ex)
    return guard


class FakeBackend:
    """Stand-in token endpoint and stand-in Chatterbox, served together on one loopback port.

    ``POST /token`` answers the service-account ID-token grant with a new token whose ``aud`` is the
    assertion's ``target_audience``. ``POST /v1/synthesize`` answers, in this order: a forced
    ``401``/``403`` (as Cloud Run would); ``401`` unless the ``Authorization`` header carries a token
    this endpoint issued (as Cloud Run would); any other forced status; ``422`` unless the body is
    ``multipart/form-data`` with form fields ``text`` and ``language`` and file part ``sample_audio``;
    ``400`` for a ``sample_path`` part; otherwise, after the configured delay, the configured body
    and media type, trickled over ``trickle_seconds`` when that is set.
    """

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.base_url = ""
        self.token_requests: list[dict] = []
        self.token_grants: list[dict] = []
        self.synthesize_calls: list[dict] = []
        self.audio = b"RIFF" + uuid.uuid4().bytes + b"WAVEfake-cloned-audio"
        self.status = 200
        self.media_type: str | None = "audio/wav"
        self.body: bytes | None = None
        self.delay_seconds = 0.0
        self.trickle_seconds = 0.0
        self.token_status = 200
        self.token_delay_seconds = 0.0
        self.app = self._build_app()

    @property
    def token_uri(self) -> str:
        return f"{self.base_url}/token"

    def _issued(self) -> set[str]:
        with self.lock:
            return {grant["id_token"] for grant in self.token_grants}

    async def _trickle(self, body: bytes):
        step = max(1, -(-len(body) // TRICKLE_PIECES))
        pieces = [body[index : index + step] for index in range(0, len(body), step)] or [b""]
        interval = self.trickle_seconds / len(pieces)
        for piece in pieces:
            await asyncio.sleep(interval)
            yield piece

    def _build_app(self) -> FastAPI:
        app = FastAPI(title="CRM-4 fake token endpoint and Chatterbox")

        @app.post("/token")
        async def token(request: Request):
            form = await request.form()
            fields = {name: value for name, value in form.multi_items() if isinstance(value, str)}
            await form.close()
            with self.lock:
                self.token_requests.append(fields)
            if self.token_delay_seconds:
                await asyncio.sleep(self.token_delay_seconds)
            if self.token_status != 200:
                return JSONResponse(
                    status_code=self.token_status,
                    content={"error": "invalid_grant", "error_description": "refused by the CRM-4 test token endpoint"},
                )
            try:
                _, claims, _, _ = jwt_parts(fields.get("assertion", ""))
            except Exception:
                return JSONResponse(status_code=400, content={"error": "invalid_request"})
            now = int(time.time())
            id_claims = {
                "iss": "https://accounts.google.com",
                "aud": claims.get("target_audience"),
                "email": claims.get("iss"),
                "iat": now,
                "exp": now + 3600,
                "jti": uuid.uuid4().hex,
            }
            id_token = ".".join(
                [
                    b64url_encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode("utf-8")),
                    b64url_encode(json.dumps(id_claims).encode("utf-8")),
                    b64url_encode(b"crm4-test-signature"),
                ]
            )
            with self.lock:
                self.token_grants.append({"fields": fields, "id_token": id_token})
            return {"id_token": id_token}

        @app.post("/v1/synthesize")
        async def synthesize(request: Request):
            authorization = request.headers.get("authorization")
            content_type = request.headers.get("content-type", "")
            parts: list[dict] = []
            if content_type.lower().startswith("multipart/form-data"):
                form = await request.form()
                for name, value in form.multi_items():
                    if isinstance(value, UploadFile):
                        parts.append({"name": name, "is_file": True, "content": await value.read()})
                    else:
                        parts.append({"name": name, "is_file": False, "content": value})
                await form.close()
            else:
                await request.body()
            with self.lock:
                self.synthesize_calls.append(
                    {"authorization": authorization, "content_type": content_type, "parts": parts}
                )

            if self.status in (401, 403):
                return JSONResponse(status_code=self.status, content={"detail": "denied by the CRM-4 test platform"})
            if authorization is None or authorization not in {f"Bearer {issued}" for issued in self._issued()}:
                return JSONResponse(status_code=401, content={"detail": "no valid identity token"})
            if self.status != 200:
                return JSONResponse(status_code=self.status, content={"detail": f"forced by the CRM-4 test ({self.status})"})

            by_name = {part["name"]: part for part in parts}
            well_formed = (
                by_name.get("text", {}).get("is_file") is False
                and by_name.get("language", {}).get("is_file") is False
                and by_name.get("sample_audio", {}).get("is_file") is True
            )
            if not well_formed:
                return JSONResponse(
                    status_code=422,
                    content={"detail": [{"type": "missing", "loc": ["body"], "msg": "text, language, sample_audio"}]},
                )
            if "sample_path" in by_name:
                return JSONResponse(status_code=400, content={"detail": SAMPLE_PATH_DETAIL})

            if self.delay_seconds:
                await asyncio.sleep(self.delay_seconds)
            body = self.audio if self.body is None else self.body
            if self.trickle_seconds:
                return StreamingResponse(self._trickle(body), media_type=self.media_type)
            return Response(content=body, media_type=self.media_type)

        return app


@contextlib.contextmanager
def running_app(app):
    """Serve an ASGI app with uvicorn on a dynamically allocated loopback port, in a daemon thread."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", lifespan="off", timeout_graceful_shutdown=5))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started:
            if not thread.is_alive() or time.monotonic() > deadline:
                raise RuntimeError("CRM-4 test server did not start")
            time.sleep(0.05)
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()


@contextlib.contextmanager
def running_fake_backend():
    backend = FakeBackend()
    with running_app(backend.app) as base_url:
        backend.base_url = base_url
        yield backend


def closed_loopback_url() -> str:
    """A loopback URL on a port that was just allocated and released, so nothing listens on it."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return f"http://127.0.0.1:{port}"


class TruncatingServer:
    """Reads each request, answers with headers promising 1000 body bytes, sends fewer, and closes."""

    def __init__(self) -> None:
        self.requests: list[str] = []
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.bind(("127.0.0.1", 0))
        self._listener.listen(5)
        self._listener.settimeout(0.2)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self.base_url = f"http://127.0.0.1:{self._listener.getsockname()[1]}"

    def _serve(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self._listener.accept()
            except (TimeoutError, socket.timeout):
                continue
            except OSError:
                return
            with conn:
                conn.settimeout(5)
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data += chunk
                head, _, body = data.partition(b"\r\n\r\n")
                length = 0
                for line in head.split(b"\r\n")[1:]:
                    name, _, value = line.partition(b":")
                    if name.strip().lower() == b"content-length":
                        length = int(value.strip())
                while len(body) < length:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    body += chunk
                self.requests.append(head.split(b"\r\n", 1)[0].decode("latin-1"))
                conn.sendall(
                    b"HTTP/1.1 200 OK\r\nContent-Type: audio/wav\r\nContent-Length: 1000\r\n\r\nRIFF-partial"
                )
                conn.shutdown(socket.SHUT_WR)

    def __enter__(self) -> "TruncatingServer":
        self._thread.start()
        return self

    def __exit__(self, *exc_info) -> None:
        self._stop.set()
        self._thread.join(timeout=5)
        self._listener.close()
