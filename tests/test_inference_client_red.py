"""CRM-4 RED: the inference service's voice cloning call to the private Chatterbox.

Work item chatterbox-cloud-run, API-Contract.md: Inference Service Voice Cloning Call, Inference
Job Creation (voice cloning failure reasons CFR-1 to CFR-9) and Inference Service Settings.

Each test imports a fresh copy of the inference application after setting its environment, so
the settings are read as at service start. Files and databases live under the test's tmp_path.
Chatterbox and the OAuth 2.0 token endpoint named by a test-generated service-account key are
stand-ins served on loopback ports (tests/_chatterbox_boundary.py); every non-loopback connection
or DNS lookup is blocked and fails the test. Every asserted answer is produced by the inference
service itself.
"""

from __future__ import annotations

import importlib
import os
import sqlite3
import sys
import time
import uuid
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from tests._chatterbox_boundary import (
    JWT_BEARER_GRANT,
    TruncatingServer,
    closed_loopback_url,
    isolate_network,
    running_app,
    running_fake_backend,
    write_service_account_key,
)

INFERENCE_MODULE = "voice_narration.inference.application"
INFERENCE_PACKAGE = "voice_narration.inference"
JOBS = "/inference/jobs"
NARRATION_AUDIO = b"RIFF" + b"crm4-stub-narration-audio"

SUFFIX = " Please retry, or use Google voice narration mode."
CFR1 = "Voice cloning failed: no voice cloning service is configured." + SUFFIX
CFR2 = "Voice cloning failed: VOICE_CLONING_TIMEOUT_SECONDS must be a positive whole number of seconds." + SUFFIX
CFR3 = "Voice cloning failed: the voice sample for this profile could not be read." + SUFFIX
CFR4 = "Voice cloning failed: could not obtain an identity token for the voice cloning service." + SUFFIX
CFR5 = "Voice cloning failed: the voice cloning service did not respond within {n} seconds." + SUFFIX
CFR6 = "Voice cloning failed: could not connect to the voice cloning service." + SUFFIX
CFR7 = "Voice cloning failed: access to the voice cloning service was denied (HTTP {status})." + SUFFIX
CFR8 = "Voice cloning failed: the voice cloning service returned an error (HTTP {status})." + SUFFIX
CFR9 = "Voice cloning failed: the voice cloning service returned a response that is not audio." + SUFFIX

# Scratch copy of the voices service's table (voice_narration/simple_voices/application.py:32-43).
VOICE_PROFILES_SCHEMA = """
CREATE TABLE IF NOT EXISTS voice_profiles (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    language TEXT NOT NULL,
    consent TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'approved',
    sample_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    model TEXT NOT NULL DEFAULT 'google-tts'
)
"""

UNSET = object()
DEFAULT = object()


class _Harness:
    def __init__(self, monkeypatch, tmp_path: Path, backend, guard, key) -> None:
        self.monkeypatch = monkeypatch
        self.tmp_path = tmp_path
        self.backend = backend
        self.guard = guard
        self.key = key
        self.audio_root = tmp_path / "audio_storage"
        self.audio_root.mkdir()
        self.voices_db = self.audio_root / "voice_profiles.db"
        with sqlite3.connect(self.voices_db) as conn:
            conn.execute(VOICE_PROFILES_SCHEMA)
            conn.commit()
        self.module = None
        self.client: TestClient | None = None

    def load(self, *, base_url=DEFAULT, chatterbox_base_url=UNSET, timeout=UNSET, credentials=DEFAULT):
        """Set the inference service's settings, then import a fresh copy of it, as at service start."""
        settings = {
            "VOICE_CLONING_API_BASE_URL": self.backend.base_url if base_url is DEFAULT else base_url,
            "CHATTERBOX_API_BASE_URL": chatterbox_base_url,
            "VOICE_CLONING_TIMEOUT_SECONDS": timeout,
            "GOOGLE_APPLICATION_CREDENTIALS": str(self.key.path) if credentials is DEFAULT else credentials,
        }
        for name, value in settings.items():
            if value is UNSET:
                self.monkeypatch.delenv(name, raising=False)
            else:
                self.monkeypatch.setenv(name, value)
        for name, value in settings.items():
            assert os.environ.get(name) == (None if value is UNSET else value), name

        package = importlib.import_module(INFERENCE_PACKAGE)
        self.monkeypatch.setattr(package, "application", getattr(package, "application", None), raising=False)
        self.monkeypatch.delitem(sys.modules, INFERENCE_MODULE, raising=False)
        module = importlib.import_module(INFERENCE_MODULE)
        self.monkeypatch.setattr(module, "ROOT", self.tmp_path)
        self.monkeypatch.setattr(module, "AUDIO_ROOT", self.audio_root)
        self.monkeypatch.setattr(module, "DB_PATH", self.audio_root / "generation_jobs.db")
        module._ensure_db()
        assert module.DB_PATH == self.audio_root / "generation_jobs.db"
        assert module.DB_PATH.exists()
        self.module = module
        self.client = TestClient(module.app, raise_server_exceptions=False)
        return module

    def add_profile(self, *, language: str = "hi-IN", sample_path=DEFAULT) -> tuple[str, bytes | None]:
        profile_id = uuid.uuid4().hex
        sample: bytes | None = None
        if sample_path is DEFAULT:
            sample = b"RIFF" + os.urandom(48) + b"\x00\xff\x8d WAVEfmt crm4-sample"
            voice_dir = self.audio_root / "voices" / "crm4-user"
            voice_dir.mkdir(parents=True, exist_ok=True)
            path = voice_dir / f"{uuid.uuid4().hex}_CRM-4_Clone.wav"
            path.write_bytes(sample)
            sample_path = str(path)
        now = "2026-11-09T00:00:00Z"
        with sqlite3.connect(self.voices_db) as conn:
            conn.execute(
                "INSERT INTO voice_profiles (id, name, user_id, language, consent, status, sample_path,"
                " created_at, updated_at, model) VALUES (?, ?, ?, ?, ?, 'approved', ?, ?, ?, 'google-tts')",
                (profile_id, "CRM-4 Clone", "crm4-user", language, "I consent", sample_path, now, now),
            )
            conn.commit()
        return profile_id, sample

    def create_job(self, profile_id: str, *, text: str = "  Namaste duniya  ", mode: str | None = "voice_cloning"):
        payload = {"text": text, "voice_profile_id": profile_id, "voice_name": "CRM-4 Clone", "user_id": "crm4-user"}
        if mode is not None:
            payload["mode"] = mode
        return self.client.post(JOBS, json=payload)

    def job_count(self) -> int:
        with sqlite3.connect(self.audio_root / "generation_jobs.db") as conn:
            return conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    def generated_files(self) -> list[Path]:
        generated = self.audio_root / "generated"
        return sorted(generated.iterdir()) if generated.exists() else []

    def assert_cloning_failed(self, response, detail: str) -> None:
        assert response.status_code == 503, response.text
        assert response.json() == {"detail": detail}
        assert self.job_count() == 0
        assert self.generated_files() == []

    def assert_job_saved(self, response, audio: bytes) -> str:
        assert response.status_code == 200, response.text
        body = response.json()
        job_id = body["id"]
        assert body["status"] == "completed"
        assert body["audio_url"].endswith(f"/inference/jobs/{job_id}/audio")
        served = self.client.get(f"{JOBS}/{job_id}/audio")
        assert served.status_code == 200, served.text
        assert served.content == audio
        stored = self.client.get(f"{JOBS}/{job_id}").json()
        stored_path = Path(stored["audio_path"])
        assert stored_path.resolve().is_relative_to(self.audio_root.resolve())
        assert stored_path.read_bytes() == audio
        return job_id

    def token_for(self, call: dict) -> dict:
        authorization = call["authorization"]
        assert authorization is not None and authorization.startswith("Bearer "), authorization
        token = authorization[len("Bearer ") :]
        grants = [grant for grant in self.backend.token_grants if grant["id_token"] == token]
        assert len(grants) == 1, "the Authorization header does not carry a token the token endpoint issued"
        return grants[0]


@pytest.fixture
def inference(monkeypatch, tmp_path):
    guard = isolate_network(monkeypatch)
    with running_fake_backend() as backend:
        key = write_service_account_key(tmp_path / "service-account.json", backend.token_uri)
        yield _Harness(monkeypatch, tmp_path, backend, guard, key)


def _part_names(call: dict) -> list[str]:
    return sorted(part["name"] for part in call["parts"])


def _part(call: dict, name: str) -> dict:
    matches = [part for part in call["parts"] if part["name"] == name]
    assert len(matches) == 1, call["parts"]
    return matches[0]


# C4-T1
def test_cloning_request_carries_sample_audio_and_identity_token(inference):
    inference.load()
    profile_id, sample = inference.add_profile(language="hi-IN")

    response = inference.create_job(profile_id, text="  Namaste duniya  ")

    job_id = inference.assert_job_saved(response, inference.backend.audio)
    body = response.json()
    assert body["voice_profile_id"] == profile_id
    assert body["voice_name"] == "CRM-4 Clone"
    assert body["download_url"] == body["audio_url"]
    assert inference.job_count() == 1
    assert [path.name for path in inference.generated_files()] == [f"{job_id}.wav"]

    assert len(inference.backend.synthesize_calls) == 1
    call = inference.backend.synthesize_calls[0]
    assert call["content_type"].lower().startswith("multipart/form-data")
    assert _part_names(call) == ["language", "sample_audio", "text"]
    assert _part(call, "text") == {"name": "text", "is_file": False, "content": "Namaste duniya"}
    assert _part(call, "language") == {"name": "language", "is_file": False, "content": "hi"}
    assert _part(call, "sample_audio")["is_file"] is True
    assert _part(call, "sample_audio")["content"] == sample

    grant = inference.token_for(call)
    assert grant["fields"]["grant_type"] == JWT_BEARER_GRANT
    claims = inference.key.verify(grant["fields"]["assertion"])
    assert claims["iss"] == inference.key.email
    assert claims["target_audience"] == inference.backend.base_url
    inference.guard.assert_no_network()


# C4-T2
@pytest.mark.parametrize(
    ("profile_language", "expected"),
    [("hi-IN", "hi"), ("EN-GB", "en"), ("", "en")],
    ids=["hi-IN", "EN-GB", "no-language"],
)
def test_cloning_language_part_follows_profile_language(inference, profile_language, expected):
    inference.load()
    profile_id, sample = inference.add_profile(language=profile_language)

    response = inference.create_job(profile_id)

    inference.assert_job_saved(response, inference.backend.audio)
    call = inference.backend.synthesize_calls[0]
    assert _part(call, "language")["content"] == expected
    assert _part(call, "sample_audio")["content"] == sample
    inference.guard.assert_no_network()


# C4-T3
def test_base_url_in_effect_is_call_target_and_token_audience(inference):
    base_url = inference.backend.base_url

    inference.load(base_url=UNSET, chatterbox_base_url=f"  {base_url}  ")
    profile_id, _ = inference.add_profile()
    inference.assert_job_saved(inference.create_job(profile_id), inference.backend.audio)

    inference.load(base_url=f" {base_url}\t", chatterbox_base_url="http://127.0.0.1:9/unused")
    profile_id, _ = inference.add_profile()
    inference.assert_job_saved(inference.create_job(profile_id), inference.backend.audio)

    assert len(inference.backend.synthesize_calls) == 2
    for call in inference.backend.synthesize_calls:
        claims = inference.key.verify(inference.token_for(call)["fields"]["assertion"])
        assert claims["target_audience"] == base_url
    inference.guard.assert_no_network()


# C4-T4
@pytest.mark.parametrize(
    ("voice_cloning_base_url", "chatterbox_base_url"),
    [(UNSET, UNSET), ("", DEFAULT), ("   ", UNSET)],
    ids=["neither-set", "empty-no-fallback", "whitespace"],
)
def test_no_configured_base_url_answers_cfr1(inference, voice_cloning_base_url, chatterbox_base_url):
    if chatterbox_base_url is DEFAULT:
        chatterbox_base_url = inference.backend.base_url
    inference.load(base_url=voice_cloning_base_url, chatterbox_base_url=chatterbox_base_url)
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR1)
    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T5
@pytest.mark.parametrize("value", ["0", "00", "-5", "+5", "10.5", "ten", "1 0"])
def test_invalid_time_limit_answers_cfr2(inference, value):
    inference.load(timeout=value)
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR2)
    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T6
def test_invalid_time_limit_leaves_narration_unaffected(inference):
    inference.load(timeout="ten")
    narration_calls: list[str] = []

    class _StubGoogleProvider:
        def generate(self, text, voice_profile, output_path):
            narration_calls.append(text)
            output_path.write_bytes(NARRATION_AUDIO)
            return output_path

    inference.monkeypatch.setattr(inference.module, "GoogleVoiceProvider", _StubGoogleProvider)
    profile_id, _ = inference.add_profile()

    cloning = inference.create_job(profile_id)
    inference.assert_cloning_failed(cloning, CFR2)

    narration = inference.create_job(profile_id, text="Narrate this", mode=None)
    inference.assert_job_saved(narration, NARRATION_AUDIO)
    assert narration_calls == ["Narrate this"]
    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T7
@pytest.mark.parametrize("case", ["no-sample-path", "missing-file", "directory"])
def test_unreadable_voice_sample_answers_cfr3(inference, case):
    inference.load()
    if case == "no-sample-path":
        sample_path = None
    elif case == "missing-file":
        sample_path = str(inference.audio_root / "voices" / "absent.wav")
    else:
        directory = inference.audio_root / "voices" / "a-directory.wav"
        directory.mkdir(parents=True)
        sample_path = str(directory)
    profile_id, _ = inference.add_profile(sample_path=sample_path)

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR3)
    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T8
@pytest.mark.parametrize("case", ["missing-key-file", "not-json", "not-a-service-account-key", "token-request-refused"])
def test_identity_token_unavailable_answers_cfr4(inference, case):
    credentials = DEFAULT
    if case == "missing-key-file":
        credentials = str(inference.tmp_path / "absent-key.json")
    elif case == "not-json":
        path = inference.tmp_path / "not-json-key.json"
        path.write_text("this is not a key file", encoding="utf-8")
        credentials = str(path)
    elif case == "not-a-service-account-key":
        path = inference.tmp_path / "authorized-user.json"
        path.write_text(
            '{"type": "authorized_user", "client_id": "crm4", "client_secret": "crm4", "refresh_token": "crm4"}',
            encoding="utf-8",
        )
        credentials = str(path)
    else:
        inference.backend.token_status = 400
    inference.load(credentials=credentials)
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR4)
    if case == "token-request-refused":
        assert len(inference.backend.token_requests) >= 1
    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T9
def test_time_limit_bounds_wait_for_chatterbox_response(inference):
    inference.load(timeout="1")
    inference.backend.delay_seconds = 2.5
    profile_id, _ = inference.add_profile()

    started = time.monotonic()
    response = inference.create_job(profile_id)
    elapsed = time.monotonic() - started

    inference.assert_cloning_failed(response, CFR5.format(n=1))
    assert len(inference.backend.synthesize_calls) == 1
    assert elapsed < 2.2, elapsed
    inference.guard.assert_no_network()


# C4-T10
def test_time_limit_bounds_complete_response_not_each_read(inference):
    inference.load(timeout="1")
    inference.backend.trickle_seconds = 3.0
    profile_id, _ = inference.add_profile()

    started = time.monotonic()
    response = inference.create_job(profile_id)
    elapsed = time.monotonic() - started

    inference.assert_cloning_failed(response, CFR5.format(n=1))
    assert len(inference.backend.synthesize_calls) == 1
    assert elapsed < 2.5, elapsed
    inference.guard.assert_no_network()


# C4-T11
def test_identity_token_time_is_not_counted_toward_time_limit(inference):
    inference.load(timeout="1")
    inference.backend.token_delay_seconds = 1.5
    profile_id, _ = inference.add_profile()

    started = time.monotonic()
    response = inference.create_job(profile_id)
    elapsed = time.monotonic() - started

    inference.assert_job_saved(response, inference.backend.audio)
    assert elapsed >= 1.5, elapsed
    assert len(inference.backend.synthesize_calls) == 1
    inference.guard.assert_no_network()


# C4-T12
@pytest.mark.parametrize(
    ("value", "limit"),
    [(UNSET, 600), ("", 600), ("   ", 600), ("  7  ", 7), ("007", 7)],
    ids=["not-set", "empty", "whitespace", "padded-7", "leading-zeros-7"],
)
def test_time_limit_in_effect_is_reported_when_reached(inference, value, limit):
    inference.load(timeout=value)
    timed_out: list[str] = []
    real_handle_request = httpx.HTTPTransport.handle_request

    def handle_request(self, request):
        if request.url.path == "/v1/synthesize":
            timed_out.append(str(request.url))
            raise httpx.ReadTimeout("simulated: time limit reached", request=request)
        return real_handle_request(self, request)

    inference.monkeypatch.setattr(httpx.HTTPTransport, "handle_request", handle_request)
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR5.format(n=limit))
    assert timed_out == [f"{inference.backend.base_url}/v1/synthesize"]
    inference.guard.assert_no_network()


# C4-T13
def test_time_limit_setting_is_read_at_service_start(inference):
    inference.load(timeout="ten")
    inference.monkeypatch.setenv("VOICE_CLONING_TIMEOUT_SECONDS", "5")
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR2)
    inference.guard.assert_no_network()


# C4-T14
@pytest.mark.parametrize("case", ["connection-refused", "connection-lost-before-full-response"])
def test_unreachable_chatterbox_answers_cfr6(inference, case):
    profile_id, _ = inference.add_profile()
    if case == "connection-refused":
        inference.load(base_url=closed_loopback_url())
        response = inference.create_job(profile_id)
    else:
        with TruncatingServer() as server:
            inference.load(base_url=server.base_url)
            response = inference.create_job(profile_id)
        assert server.requests == ["POST /v1/synthesize HTTP/1.1"]

    inference.assert_cloning_failed(response, CFR6)
    inference.guard.assert_no_network()


# C4-T15
@pytest.mark.parametrize("status", [401, 403])
def test_access_denied_answers_cfr7(inference, status):
    inference.load()
    inference.backend.status = status
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR7.format(status=status))
    assert len(inference.backend.synthesize_calls) == 1
    inference.guard.assert_no_network()


# C4-T16
@pytest.mark.parametrize("status", [400, 422, 429, 500, 503, 504])
def test_chatterbox_error_status_answers_cfr8(inference, status):
    inference.load()
    inference.backend.status = status
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR8.format(status=status))
    assert len(inference.backend.synthesize_calls) == 1
    inference.guard.assert_no_network()


# C4-T17
@pytest.mark.parametrize(
    ("body", "media_type"),
    [(b"", "audio/wav"), (b'{"ok": true}', "application/json"), (b"RIFFcrm4", None), (b"RIFFcrm4", "text/plain")],
    ids=["empty-body", "json-body", "no-content-type", "text-plain"],
)
def test_success_status_without_audio_answers_cfr9(inference, body, media_type):
    inference.load()
    inference.backend.body = body
    inference.backend.media_type = media_type
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_cloning_failed(response, CFR9)
    assert len(inference.backend.synthesize_calls) == 1
    inference.guard.assert_no_network()


# C4-T18
def test_audio_wav_media_type_is_matched_case_insensitively_ignoring_parameters(inference):
    inference.load()
    inference.backend.media_type = "Audio/WAV; rate=24000"
    profile_id, _ = inference.add_profile()

    response = inference.create_job(profile_id)

    inference.assert_job_saved(response, inference.backend.audio)
    inference.guard.assert_no_network()


# C4-T19
def test_failure_reasons_are_checked_in_contract_order(inference):
    no_sample_id, _ = inference.add_profile(sample_path=None)
    readable_id, _ = inference.add_profile()
    absent_key = str(inference.tmp_path / "absent-key.json")

    inference.load(base_url="", timeout="ten", credentials=absent_key)
    inference.assert_cloning_failed(inference.create_job(no_sample_id), CFR1)

    inference.load(timeout="ten", credentials=absent_key)
    inference.assert_cloning_failed(inference.create_job(no_sample_id), CFR2)

    inference.load(credentials=absent_key)
    inference.assert_cloning_failed(inference.create_job(no_sample_id), CFR3)

    inference.load(base_url=closed_loopback_url(), credentials=absent_key)
    inference.assert_cloning_failed(inference.create_job(readable_id), CFR4)

    assert inference.backend.synthesize_calls == []
    inference.guard.assert_no_network()


# C4-T20
def test_cloning_failure_answer_over_real_transport(inference):
    module = inference.load()
    inference.backend.status = 403
    profile_id, _ = inference.add_profile()

    with running_app(module.app) as inference_url:
        with httpx.Client(base_url=inference_url, timeout=30, trust_env=False) as client:
            response = client.post(
                JOBS,
                json={"text": "Over the wire", "voice_profile_id": profile_id, "mode": "voice_cloning"},
            )

    inference.assert_cloning_failed(response, CFR7.format(status=403))
    assert len(inference.backend.synthesize_calls) == 1
    inference.guard.assert_no_network()
