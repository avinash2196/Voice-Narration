"""Owner-consented sample admission and authenticated original playback."""
from copy import deepcopy
from datetime import timedelta, datetime
import io
from secrets import token_urlsafe
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile
from starlette.datastructures import Headers
from starlette.formparsers import MultiPartParser, MultiPartException
from python_multipart.multipart import parse_options_header

from voice_narration._enrollment import model, owner, principal, query, serializer
from voice_narration._http import bearer, install_errors, timestamp
from voice_narration._sql import PersistenceError, duration, fail, identity, instant
from voice_narration.voices.quality import decode, duration_bounds, rounded


MIME = {"wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}


class MemoryUploadParser(MultiPartParser):
    """Parse arbitrary part order without writing unconsented file bytes to disk."""
    def __init__(self, headers, stream, maximum):
        super().__init__(headers, stream, max_files=1, max_fields=3)
        self.maximum = maximum
        self.file_bytes = 0

    def on_headers_finished(self):
        disposition, options = parse_options_header(self._current_part.content_disposition)
        if disposition != b"form-data" or b"name" not in options:
            fail("INVALID_INPUT")
        try:
            name = options[b"name"].decode("utf-8", errors="strict")
        except UnicodeError:
            raise PersistenceError("INVALID_INPUT") from None
        if name not in {"consent_id", "model_id", "model_version", "file"}:
            fail("INVALID_INPUT")
        self._current_part.field_name = name
        if b"filename" in options:
            self._current_files += 1
            if self._current_files > 1 or name != "file":
                fail("INVALID_INPUT")
            memory = io.BytesIO()
            self._files_to_close_on_error.append(memory)
            self._current_part.file = UploadFile(file=memory, size=0, filename="sample",
                                                headers=Headers(raw=self._current_part.item_headers))
        else:
            self._current_fields += 1
            if self._current_fields > 3 or name == "file":
                fail("INVALID_INPUT")
            self._current_part.file = None

    def on_part_data(self, data, start, end):
        if self._current_part.file is not None:
            self.file_bytes += end - start
            if self.file_bytes > self.maximum:
                fail("LIMIT_EXCEEDED")
        super().on_part_data(data, start, end)


def create_app(*, repository, authenticate, validate_consent, capability, settings, clock):
    required = {"max_upload_bytes", "max_samples_per_profile", "sample_min_seconds", "sample_max_seconds",
                "signed_link_seconds", "sample_days", "default_page_size", "max_page_size"}
    if not isinstance(settings, dict) or set(settings) != required:
        fail("INVALID_CONFIGURATION")
    for key in required - {"sample_min_seconds", "sample_max_seconds"}:
        duration(settings[key])
    duration_bounds({"sample_min_seconds": settings["sample_min_seconds"],
                     "sample_max_seconds": settings["sample_max_seconds"]})
    if not all(callable(value) for value in (authenticate, validate_consent, capability, clock)):
        fail("INVALID_CONFIGURATION")
    settings = deepcopy(settings)
    serialized = serializer()
    links = {}
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    install_errors(app, clock)

    def instant_from_text(value):
        return instant(datetime.fromisoformat(value.replace("Z", "+00:00")))

    @serialized
    def sample(account, artifact_id, owner_id=None):
        who = principal(account)
        reader = owner(account)
        if owner_id is not None:
            identity(owner_id)
            if who["role"] != "Administrator":
                fail("FORBIDDEN")
            repository.permit(who, owner_id, "samples:read", instant(clock()))
            reader = who
        record = repository.read(reader, identity(artifact_id), now=instant(clock()))
        if owner_id is not None and record["owner_id"] != owner_id:
            fail("FORBIDDEN")
        payload = record["payload"]
        if record["category"] != "sample" or "artifact" not in payload:
            fail("ARTIFACT_UNAVAILABLE")
        artifact = deepcopy(payload["artifact"])
        if instant(clock()) >= instant_from_text(artifact["expires_at"]):
            fail("ARTIFACT_UNAVAILABLE")
        consent_account = dict(account, user_id=record["owner_id"], role="User")
        validate_consent(consent_account, record["consent_id"])
        return record, artifact, reader

    @serialized
    def enrollment_samples(account, consent_id, ids):
        owner(account)
        validate_consent(account, identity(consent_id))
        if (not isinstance(ids, list) or not ids or len(ids) > settings["max_samples_per_profile"] or
                any(not isinstance(value, str) for value in ids) or len(set(ids)) != len(ids)):
            fail("INVALID_INPUT")
        result = []
        for artifact_id in ids:
            try:
                record, artifact, reader = sample(account, artifact_id)
            except PersistenceError as exc:
                if exc.code == "NOT_FOUND":
                    fail("ARTIFACT_UNAVAILABLE")
                raise
            if record["consent_id"] != consent_id:
                fail("INVALID_INPUT")
            chunks = repository.read_bytes(reader, artifact_id, now=instant(clock()))
            if len(chunks) != 1:
                fail("ARTIFACT_UNAVAILABLE")
            decoded = decode(chunks[0], artifact["format"])
            result.append({"artifact_id": artifact_id, "bytes": chunks[0],
                           "stream_index": decoded["stream_index"], "artifact": artifact})
        return result

    @serialized
    def admit(account, consent_id, selected, data, fmt):
        who = owner(account)
        validate_consent(account, consent_id)
        cap = capability(selected)
        bounds = duration_bounds(cap, settings)
        decoded = decode(data, fmt)
        if not bounds[0] <= decoded["duration_seconds"] <= bounds[1]:
            fail("INVALID_AUDIO")
        now, artifact_id = instant(clock()), str(uuid4())
        expires = now + timedelta(days=settings["sample_days"])
        artifact = {"artifact_id": artifact_id, "owner_id": who["user_id"], "kind": "sample",
                    "consent_id": consent_id, "profile_id": None, "job_id": None,
                    "format": fmt, "size_bytes": len(data),
                    "duration_seconds": rounded(decoded["duration_seconds"]),
                    "sample_rate_hz": decoded["sample_rate_hz"], "created_at": timestamp(now),
                    "expires_at": timestamp(expires), "availability": "available"}
        validate_consent(account, consent_id)
        repository.publish_sample(
            {"id": artifact_id, "owner_id": who["user_id"], "profile_id": artifact_id,
             "consent_id": consent_id, "category": "sample", "created_at": now,
             "payload": {"artifact": artifact, "stream_index": decoded["stream_index"]}},
            data, validate=lambda: validate_consent(account, consent_id))
        return artifact

    @app.post("/api/v1/artifacts/upload")
    async def upload(request: Request):
        account = await run_in_threadpool(authenticate, bearer(request))
        content_type, _ = parse_options_header(request.headers.get("content-type", ""))
        if content_type != b"multipart/form-data":
            fail("INVALID_INPUT")
        try:
            form = await MemoryUploadParser(request.headers, request.stream(), settings["max_upload_bytes"]).parse()
        except (MultiPartException, UnicodeError, ValueError):
            raise PersistenceError("INVALID_INPUT") from None
        try:
            expected = {"consent_id", "model_id", "model_version", "file"}
            if set(form) != expected or any(len(form.getlist(k)) != 1 for k in form):
                fail("INVALID_INPUT")
            if any(not isinstance(form[k], str) for k in expected - {"file"}):
                fail("INVALID_INPUT")
            consent_id = identity(form["consent_id"])
            selected = model({"model_id": form["model_id"], "version": form["model_version"]})
            item = form["file"]
            if not isinstance(item, UploadFile):
                fail("INVALID_INPUT")
            fmt = next((key for key, value in MIME.items() if item.content_type == value), None)
            if fmt is None:
                fail("INVALID_AUDIO")
            await run_in_threadpool(validate_consent, account, consent_id)
            await run_in_threadpool(capability, selected)
            data = await item.read(settings["max_upload_bytes"] + 1)
            if len(data) > settings["max_upload_bytes"]:
                fail("LIMIT_EXCEEDED")
            artifact = await run_in_threadpool(admit, account, consent_id, selected, data, fmt)
            return JSONResponse(status_code=201, content=artifact)
        finally:
            await form.close()

    @serialized
    def link(account, artifact_id, params, disposition):
        if "format" in params:
            fail("UNSUPPORTED_FORMAT")
        record, artifact, _ = sample(account, artifact_id, params.get("owner_id"))
        expires = timestamp(instant(clock()) + timedelta(seconds=settings["signed_link_seconds"]))
        signature = token_urlsafe(32)
        parameters = {"signature": signature, "expires_at": expires,
                      "disposition": disposition, "format": artifact["format"]}
        links[signature] = (principal(account), artifact_id, deepcopy(parameters), params.get("owner_id"))
        return {"url": "/api/v1/artifacts/" + artifact_id + "/content?" + urlencode(parameters),
                "expires_at": expires, "artifact": artifact}

    @app.get("/api/v1/artifacts/{artifact_id}/preview-url")
    def preview(request: Request, artifact_id: str):
        return link(authenticate(bearer(request)), artifact_id, query(request, {"owner_id"}), "inline")

    @app.get("/api/v1/artifacts/{artifact_id}/download-url")
    def download(request: Request, artifact_id: str):
        return link(authenticate(bearer(request)), artifact_id, query(request, {"owner_id", "format"}), "attachment")

    @app.get("/api/v1/artifacts/{artifact_id}/content")
    def content(request: Request, artifact_id: str):
        account = authenticate(bearer(request))
        params = query(request, {"signature", "expires_at", "disposition", "format"})
        saved = links.get(params.get("signature"))
        if saved is None or saved[1] != artifact_id or saved[2] != params:
            fail("INVALID_LINK")
        if saved[0] != principal(account):
            fail("FORBIDDEN")
        if instant(clock()) >= instant_from_text(params["expires_at"]):
            fail("INVALID_LINK")
        if "range" in request.headers:
            fail("INVALID_INPUT")
        record, artifact, reader = sample(account, artifact_id, saved[3])
        chunks = repository.read_bytes(reader, artifact_id, now=instant(clock()))
        if len(chunks) != 1:
            fail("ARTIFACT_UNAVAILABLE")
        return Response(chunks[0], media_type=MIME[artifact["format"]],
                        headers={"Content-Disposition": params["disposition"]})

    app.state.enrollment_samples = enrollment_samples
    app.state.effective_settings = lambda: deepcopy(settings)
    app.state.close = repository.close
    return app
