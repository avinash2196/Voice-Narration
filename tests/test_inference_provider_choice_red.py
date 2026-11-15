"""OAM-4 RED: provider choice, the four pre-call Chatterbox failures, the provider list and waiting.

Contract: docs/.ai/chatterbox-original-app/API-Contract.md (Inference Generation,
Generation Waiting, Inference Service Chatterbox Call steps 1-3, Chatterbox Failure
Causes OAF-1 to OAF-4, Inference Provider List, Inference Service Settings).

No test fakes or calls Chatterbox (requirements COA-16). In every test the identity
token cannot be obtained, because GOOGLE_APPLICATION_CREDENTIALS never names a usable
service-account key, so the Chatterbox call (contract step 4) cannot be reached.
CHATTERBOX_URL is absent, blank or http://127.0.0.1:0, never the deployed service.
Each test sets or removes every setting it depends on, so values loaded from a local
.env file do not apply, and any name lookup of a host outside this machine is blocked
and fails the test (Plan OAR-8).
"""

from __future__ import annotations

import asyncio
import io
import ipaddress
import json
import math
import socket
import struct
import threading
import time
import wave
from contextlib import ExitStack, contextmanager
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
import uvicorn

from voice_narration.inference import application as inference_application
from voice_narration.inference.providers.mock import MockInferenceProvider
from voice_narration.simple_voices.application import create_app as create_voice_app

CLOSING = "Please retry, or choose another provider."
NOT_CONFIGURED = f"Chatterbox voice cloning is not configured. {CLOSING}"
INVALID_TIME_LIMIT = (
    "The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; "
    f"it must be a positive whole number of seconds. {CLOSING}"
)
SAMPLE_UNREADABLE = f"The voice sample for the selected voice could not be read. {CLOSING}"
TOKEN_UNAVAILABLE = f"Could not obtain an identity token for Chatterbox. {CLOSING}"
UNSUPPORTED_PROVIDER = {"error": "Unsupported provider. Choose google or chatterbox."}
UNSUPPORTED_LANGUAGE = {"error": "language must be en or hi for a chatterbox generation."}
MISSING_FIELDS = {"error": "Missing required fields: script, voice_id"}
CHATTERBOX_DESCRIPTION = "Chatterbox voice cloning (deployed Cloud Run service)"
BASELINE_DESCRIPTIONS = {
    "azure": "Azure Cognitive Services Speech (requires AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)",
    "google": "Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS)",
    "mock": "Deterministic mock for testing (no external deps)",
}
PRELOADED_VOICE = "en-US-Neural2-A"
UNKNOWN_VOICE = "voice-00000000"
UNUSABLE_URL = "http://127.0.0.1:0"
SETTINGS_REMOVED = (
    "CHATTERBOX_TIMEOUT_SECONDS",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "INFERENCE_PROVIDER",
    "AUDIO_RETENTION_DAYS",
)

# Placeholders in the failure cases, replaced by Harness.resolve.
MISSING_KEY = "<missing key file>"
NOT_JSON_KEY = "<key file that is not JSON>"
AUTHORIZED_USER_KEY = "<authorized-user key file>"
PADDED_VOICE_SERVICE_URL = "<voice service URL with spaces and a trailing slash>"


def pcm_wav(seconds: float = 0.5, rate: int = 16_000) -> bytes:
    """A PCM WAV voice sample, which the voice service stores byte-identical (OAM-3)."""
    frames = b"".join(
        struct.pack("<h", int(12_000 * math.sin(2 * math.pi * 440 * index / rate)))
        for index in range(int(seconds * rate))
    )
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(frames)
    return buffer.getvalue()


VOICE_SAMPLE = pcm_wav()


def host_name(host) -> str | None:
    """The host as text; asynchronous lookups pass it as bytes."""
    if host is None:
        return None
    return host.decode() if isinstance(host, bytes) else str(host)


def is_on_this_machine(name: str | None) -> bool:
    if name is None:
        return True
    if name.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(name.strip("[]")).is_loopback
    except ValueError:
        return False


class StartupProvider(MockInferenceProvider):
    """The mock the inference service starts with, recording each generation and optionally slowed."""

    def __init__(self, delay: float = 0.0):
        super().__init__()
        self.delay = delay
        self.calls: list[SimpleNamespace] = []
        self.in_flight = 0
        self.max_in_flight = 0
        self._lock = threading.Lock()

    async def generate(self, script: str, voice_id: str, **kwargs) -> dict:
        with self._lock:
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
        started = time.monotonic()
        try:
            if self.delay:
                await asyncio.sleep(self.delay)
            return await super().generate(script, voice_id, **kwargs)
        finally:
            with self._lock:
                self.in_flight -= 1
                self.calls.append(SimpleNamespace(voice_id=voice_id, start=started, end=time.monotonic()))


class RefusingDatabase:
    """Refuses every database use, so no test writes to the local PostgreSQL.

    The contract says a database failure does not fail a generation (Saving a success).
    """

    def __init__(self):
        self.attempts = 0

    def refuse(self, *args, **kwargs):
        self.attempts += 1
        raise RuntimeError("the database is not used by these tests")


@contextmanager
def serve(app):
    """Run an ASGI app with uvicorn on a loopback socket bound before start, so no other process can take its port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", timeout_graceful_shutdown=2))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started:
        assert thread.is_alive() and time.monotonic() < deadline, "local server did not start"
        time.sleep(0.01)
    try:
        yield f"http://127.0.0.1:{sock.getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(15)
        sock.close()


def upload_voice(client: httpx.Client, name: str) -> str:
    response = client.post("/voice/upload", data={"name": name},
                           files={"file": ("voice.wav", VOICE_SAMPLE, "audio/wav")})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def generate(client: httpx.Client, job_id: str, **body) -> httpx.Response:
    return client.post(f"/inference/jobs/{job_id}/infer", json=body)


def wait_until(condition, message: str, seconds: float = 15) -> None:
    deadline = time.monotonic() + seconds
    while not condition():
        assert time.monotonic() < deadline, message
        time.sleep(0.02)


def post_in_background(client: httpx.Client, job_id: str, results: dict, **body) -> threading.Thread:
    """Send a generation request from its own thread, recording its answer and when it arrived."""

    def post():
        response = generate(client, job_id, **body)
        results[job_id] = SimpleNamespace(response=response, answered=time.monotonic())

    thread = threading.Thread(target=post)
    thread.start()
    return thread


class Harness:
    def __init__(self, voices, root: Path, database: RefusingDatabase, monkeypatch):
        self.voices = voices
        self.root = root
        self.database = database
        self.monkeypatch = monkeypatch

    def resolve(self, value: str) -> str:
        if value == MISSING_KEY:
            return str(self.root / "no-such-key.json")
        if value == NOT_JSON_KEY:
            path = self.root / "not-json-key.json"
            path.write_text("this is not a key file")
            return str(path)
        if value == AUTHORIZED_USER_KEY:
            path = self.root / "authorized-user-key.json"
            path.write_text(json.dumps({"type": "authorized_user", "client_id": "1",
                                        "client_secret": "s", "refresh_token": "r"}))
            return str(path)
        if value == PADDED_VOICE_SERVICE_URL:
            return f"  {self.voices.url}/  "
        return value

    def settings(self, **values) -> None:
        for name, value in values.items():
            if value is None:
                self.monkeypatch.delenv(name, raising=False)
            else:
                self.monkeypatch.setenv(name, self.resolve(value))

    def voice(self, which: str) -> str:
        return {"uploaded": self.voices.uploaded, "deleted": self.voices.deleted,
                "preloaded": PRELOADED_VOICE, "unknown": UNKNOWN_VOICE}[which]

    @contextmanager
    def inference(self, startup: StartupProvider | None = None):
        startup = startup or StartupProvider()
        app = inference_application.create_app(provider=startup)
        assert app.state.inference.storage_root == (self.root / "audio").resolve()
        with serve(app) as url, httpx.Client(base_url=url, trust_env=False, timeout=60) as client:
            yield SimpleNamespace(url=url, client=client, startup=startup)

    def stored_files(self) -> list[str]:
        audio = self.root / "audio"
        return sorted(str(path.relative_to(audio)) for path in audio.rglob("*") if path.is_file())


@pytest.fixture(autouse=True)
def stay_on_this_machine(monkeypatch):
    """Block, record and fail any name lookup of a host outside this machine (Plan OAR-8)."""
    attempts: list[str] = []
    real_getaddrinfo = socket.getaddrinfo

    def guarded_getaddrinfo(host, *args, **kwargs):
        name = host_name(host)
        if not is_on_this_machine(name):
            attempts.append(name)
            raise socket.gaierror(f"blocked by the OAM-4 tests: {name} is outside this machine")
        return real_getaddrinfo(host, *args, **kwargs)

    monkeypatch.setattr(socket, "getaddrinfo", guarded_getaddrinfo)
    yield attempts
    assert attempts == [], f"a test tried to reach {attempts}, outside this machine"


@pytest.fixture(scope="module")
def voices(tmp_path_factory):
    with serve(create_voice_app(root=tmp_path_factory.mktemp("voice-store"))) as url:
        with httpx.Client(base_url=url, trust_env=False, timeout=30) as client:
            uploaded = upload_voice(client, "Cloned voice")
            deleted = upload_voice(client, "Deleted voice")
            assert client.delete(f"/voices/{deleted}").status_code == 200
            assert client.get(f"/voices/{uploaded}/sample").content == VOICE_SAMPLE
        yield SimpleNamespace(url=url, uploaded=uploaded, deleted=deleted)


@pytest.fixture
def harness(voices, tmp_path, monkeypatch):
    database = RefusingDatabase()
    monkeypatch.setattr(inference_application, "SessionLocal", database.refuse)
    monkeypatch.setattr(inference_application, "create_all_tables", database.refuse)
    for name in SETTINGS_REMOVED:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CHATTERBOX_URL", UNUSABLE_URL)
    monkeypatch.setenv("VOICE_SERVICE_URL", voices.url)
    monkeypatch.setenv("AUDIO_STORAGE_PATH", str(tmp_path / "audio"))
    return Harness(voices, tmp_path, database, monkeypatch)


def test_each_generation_uses_the_provider_it_names(harness):
    with harness.inference() as service:
        for job_id, choice in [("named-google", {"provider": "google", "language": "fr"}),
                               ("no-provider", {}), ("null-provider", {"provider": None}),
                               ("empty-provider", {"provider": ""})]:
            response = generate(service.client, job_id, script="Namaste", voice_id=PRELOADED_VOICE, **choice)
            assert response.status_code == 200, response.text
            assert response.json()["status"] == "complete"
        assert [call.voice_id for call in service.startup.calls] == [PRELOADED_VOICE] * 4
        assert harness.database.attempts > 0, "the generations did not use the test's database"
        cloned = generate(service.client, "named-chatterbox", script="Hello there",
                          voice_id=harness.voices.uploaded, provider="chatterbox", language="en")
        assert cloned.status_code == 503, cloned.text
        assert cloned.json() == {"error": TOKEN_UNAVAILABLE}
        assert len(service.startup.calls) == 4, "the startup provider produced the Chatterbox generation"


@pytest.mark.parametrize(("choice", "expected"), [
    pytest.param({"provider": "mock"}, UNSUPPORTED_PROVIDER, id="provider-mock"),
    pytest.param({"provider": "azure"}, UNSUPPORTED_PROVIDER, id="provider-azure"),
    pytest.param({"provider": "Google"}, UNSUPPORTED_PROVIDER, id="provider-letter-case"),
    pytest.param({"provider": " chatterbox"}, UNSUPPORTED_PROVIDER, id="provider-whitespace"),
    pytest.param({"provider": 7}, UNSUPPORTED_PROVIDER, id="provider-not-a-string"),
    pytest.param({"provider": "chatterbox"}, UNSUPPORTED_LANGUAGE, id="language-absent"),
    pytest.param({"provider": "chatterbox", "language": None}, UNSUPPORTED_LANGUAGE, id="language-null"),
    pytest.param({"provider": "chatterbox", "language": ""}, UNSUPPORTED_LANGUAGE, id="language-empty"),
    pytest.param({"provider": "chatterbox", "language": "EN"}, UNSUPPORTED_LANGUAGE, id="language-letter-case"),
    pytest.param({"provider": "chatterbox", "language": " hi"}, UNSUPPORTED_LANGUAGE, id="language-whitespace"),
    pytest.param({"provider": "chatterbox", "language": "fr"}, UNSUPPORTED_LANGUAGE, id="language-other"),
    pytest.param({"provider": "chatterbox", "language": 1}, UNSUPPORTED_LANGUAGE, id="language-not-a-string"),
])
def test_unsupported_provider_or_language_is_rejected_without_generating(harness, choice, expected):
    with harness.inference() as service:
        response = generate(service.client, "rejected", script="Hello", voice_id=harness.voices.uploaded, **choice)
        assert response.status_code == 400, response.text
        assert response.json() == expected
        assert service.startup.calls == []
        assert service.client.get("/inference/generations/rejected").status_code == 404
        missing = generate(service.client, "rejected", voice_id=harness.voices.uploaded, **choice)
        assert missing.status_code == 400 and missing.json() == MISSING_FIELDS


def cause(error: str, *, settings=None, voice="uploaded", language="en", id: str):
    return pytest.param(SimpleNamespace(error=error, settings=settings or {}, voice=voice, language=language), id=id)


PRE_CALL_CAUSES = [
    cause(NOT_CONFIGURED, settings={"CHATTERBOX_URL": None}, id="OAF-1-url-absent"),
    cause(NOT_CONFIGURED, settings={"CHATTERBOX_URL": ""}, language="hi", id="OAF-1-url-empty"),
    cause(NOT_CONFIGURED, settings={"CHATTERBOX_URL": "   "}, id="OAF-1-url-blank"),
    cause(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "0"}, language="hi", id="OAF-2-zero"),
    cause(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "-5"}, id="OAF-2-negative"),
    cause(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "10.5"}, language="hi", id="OAF-2-fraction"),
    cause(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "ten"}, id="OAF-2-word"),
    cause(SAMPLE_UNREADABLE, voice="unknown", language="hi", id="OAF-3-unknown-voice"),
    cause(SAMPLE_UNREADABLE, voice="preloaded", id="OAF-3-voice-without-sample"),
    cause(SAMPLE_UNREADABLE, voice="deleted", language="hi", id="OAF-3-deleted-voice"),
    cause(SAMPLE_UNREADABLE, settings={"VOICE_SERVICE_URL": UNUSABLE_URL}, id="OAF-3-voice-service-unreachable"),
    cause(TOKEN_UNAVAILABLE, language="hi", id="OAF-4-key-setting-absent"),
    cause(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": "  "}, id="OAF-4-key-setting-blank"),
    cause(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": MISSING_KEY}, language="hi",
          id="OAF-4-key-file-missing"),
    cause(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": NOT_JSON_KEY}, id="OAF-4-key-file-not-json"),
    cause(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": AUTHORIZED_USER_KEY}, language="hi",
          id="OAF-4-not-a-service-account-key"),
    cause(TOKEN_UNAVAILABLE, settings={"VOICE_SERVICE_URL": PADDED_VOICE_SERVICE_URL},
          id="OAF-4-voice-service-url-trimmed"),
    cause(TOKEN_UNAVAILABLE, settings={"CHATTERBOX_TIMEOUT_SECONDS": " 7 "}, language="hi",
          id="OAF-4-time-limit-padded-is-valid"),
    cause(TOKEN_UNAVAILABLE, settings={"CHATTERBOX_TIMEOUT_SECONDS": "   "},
          id="OAF-4-time-limit-blank-is-the-default"),
    cause(NOT_CONFIGURED, settings={"CHATTERBOX_URL": None, "CHATTERBOX_TIMEOUT_SECONDS": "ten"}, voice="unknown",
          language="hi", id="order-OAF-1-before-OAF-2-OAF-3-OAF-4"),
    cause(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "ten"}, voice="unknown",
          id="order-OAF-2-before-OAF-3-OAF-4"),
]


@pytest.mark.parametrize("case", PRE_CALL_CAUSES)
def test_each_pre_call_cause_answers_503_with_its_message_and_no_fallback(harness, case):
    harness.settings(**case.settings)
    with harness.inference() as service:
        earlier = generate(service.client, "same-job", script="Earlier narration", voice_id=PRELOADED_VOICE,
                           provider="google")
        assert earlier.status_code == 200, earlier.text
        entry = service.client.get("/inference/generations/same-job").json()
        audio = service.client.get("/inference/jobs/same-job/download").content
        output = service.client.get("/inference/jobs/same-job/output").json()
        files = harness.stored_files()
        assert files, "the earlier generation saved no audio file"
        response = generate(service.client, "same-job", script="Cloned narration",
                            voice_id=harness.voice(case.voice), provider="chatterbox", language=case.language)
        assert response.status_code == 503, response.text
        assert response.json() == {"error": case.error}
        assert case.error.endswith(CLOSING)
        assert len(service.startup.calls) == 1, "another provider produced the failed Chatterbox generation"
        assert service.client.get("/inference/generations/same-job").json() == entry
        assert service.client.get("/inference/jobs/same-job/download").content == audio
        assert service.client.get("/inference/jobs/same-job/output").json() == output
        assert harness.stored_files() == files


def test_provider_list_adds_chatterbox_and_keeps_the_other_providers(harness):
    harness.settings(CHATTERBOX_URL=None)
    with harness.inference() as service:
        response = service.client.get("/inference/backends")
        assert response.status_code == 200, response.text
        backends = response.json()["backends"]
        assert [backend["name"] for backend in backends] == ["azure", "chatterbox", "google", "mock"]
        descriptions = {backend["name"]: backend["description"] for backend in backends}
        assert descriptions == {**BASELINE_DESCRIPTIONS, "chatterbox": CHATTERBOX_DESCRIPTION}
        assert all(isinstance(backend["provider_class"], str) and backend["provider_class"] for backend in backends)


def test_a_generation_request_that_arrives_during_another_waits_then_completes(harness):
    harness.settings(CHATTERBOX_URL=None)
    startup = StartupProvider(delay=2.0)
    with harness.inference(startup) as service, ExitStack() as stack:
        # Clients are created before the first request: creating one took 0.3-0.6 s in planning.
        first_client, second_client, cloned_client = [
            stack.enter_context(httpx.Client(base_url=service.url, trust_env=False, timeout=60)) for _ in range(3)]
        results = {}
        first = post_in_background(first_client, "wait-first", results, script="First", voice_id=PRELOADED_VOICE)
        wait_until(lambda: startup.in_flight == 1, "the first generation did not start")
        second = post_in_background(second_client, "wait-second", results, script="Second",
                                    voice_id=PRELOADED_VOICE, provider="google")
        cloned = post_in_background(cloned_client, "wait-chatterbox", results, script="Cloned",
                                    voice_id=harness.voices.uploaded, provider="chatterbox", language="hi")
        time.sleep(0.3)
        invalid = generate(service.client, "wait-invalid", voice_id=PRELOADED_VOICE)
        invalid_answered = time.monotonic()
        unsupported = generate(service.client, "wait-unsupported", script="Third", voice_id=PRELOADED_VOICE,
                               provider="azure")
        unsupported_answered = time.monotonic()
        for thread in (first, second, cloned):
            thread.join(30)
        assert startup.max_in_flight == 1, "a second generation ran while the first was generating"
        assert len(startup.calls) == 2
        earlier, later = sorted(startup.calls, key=lambda call: call.start)
        assert later.start >= earlier.end
        assert results["wait-first"].response.status_code == 200, results["wait-first"].response.text
        assert results["wait-second"].response.status_code == 200, results["wait-second"].response.text
        assert service.client.get("/inference/generations/wait-second").status_code == 200
        assert results["wait-chatterbox"].response.status_code == 503
        assert results["wait-chatterbox"].response.json() == {"error": NOT_CONFIGURED}
        assert results["wait-chatterbox"].answered >= earlier.end, "the Chatterbox generation did not wait"
        assert invalid.status_code == 400 and invalid.json() == MISSING_FIELDS
        assert invalid_answered < earlier.end, "a request rejected by check 2 waited"
        assert unsupported.status_code == 400 and unsupported.json() == UNSUPPORTED_PROVIDER
        assert unsupported_answered < earlier.end, "a request rejected by check 3 waited"
