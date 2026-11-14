# Implementation Plan

## Milestone

OAM-4 — Inference service RED (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-4).

## Milestone Type

RED

## Review Summary

- Behavior change: tests only.
- Requirements covered (verified, not delivered): COA-1 (inference part), COA-4, COA-5, COA-7, COA-8, COA-9, COA-10, COA-13 (waiting), CON-5. Owned: COA-16's automated-test part (the tests use fakes and only `127.0.0.1`). Contract rules are mapped under Contract Rule Coverage.
- Files: created `tests/test_chatterbox_generation_red.py`; modified none; deleted none.
- Tests added: 56 (10 functions, 3 of them parametrized). They prove that a Chatterbox generation sends the whole text, the language and the stored sample, with an identity token for the Chatterbox URL. They also prove the per-generation provider choice, the `400` rejections, all nine failure messages with their order and no fallback, the 1200 s default and the configured limit, history, download, deletion and the 30-day expiry, the provider list, waiting, and completion after the client stops waiting.
- Verification: `python -m pytest tests/test_chatterbox_generation_red.py -q --tb=short`, run twice. Expected / Predicted — Not Yet Verified: `56 failed` each time, in the 7 failure classes listed under V4C-2. Then the 5 preserved files: `29 passed`.
- Needs attention: V4D-2 (the identity token is obtained through the key file's `token_uri`, and the test imports the undeclared `cryptography`), V4D-5 (the database is observed by patching `SessionLocal` and `create_all_tables`), V4D-6 (the time-limit seam `chatterbox_time_limit_seconds`), V4D-9 (the provider-list test), and V4R-2 (timing margins).

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13 (`requirements.md:17`) |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13, as written (`Plan.md:5`). OAM-4 row: `Pending` (`Plan.md:337`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` (OAM-1 deliverable, authoritative predecessor) | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 row Complete (`Plan.md:334`) |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | Approved by Avinash Srivastava on 2026-11-13, executed (`001_Implementation_Plan_OAM-2.md:669`) |
| `docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` | Revision 4 approved by Avinash Srivastava on 2026-11-13, executed (`002_Implementation_Plan_OAM-3.md:801`) |
| Reference contract `feature/voice-cloning@abbe387:docs/.ai/chatterbox-cloud-run/API-Contract.md`, sections Chatterbox Synthesize and Chatterbox Caller Identity only (`Plan.md:73`) | Contract Review Status: Approved 2026-11-09. Read with `git show abbe387:…` |
| Product-level `docs/requirements.md` | Does not exist (checked `docs/`) |

## Carried-Forward Decisions

- **V2D-1** (`001_Implementation_Plan_OAM-2.md:99-106`) and its delivery (`002_Implementation_Plan_OAM-3.md:36`): the voice service is built as `create_app(*, root, clock)`. The tests host the real voice service with `root=<tmp>`, so they never touch the default `voice_storage/` (V3D-1, `002_Implementation_Plan_OAM-3.md:124-130`).
- **V2D-6** (`001_Implementation_Plan_OAM-2.md:124`): new fixed error bodies go over a real uvicorn server on a dynamically allocated port. Every request here goes over real transport (V4D-1).
- **V3Q-3** (`002_Implementation_Plan_OAM-3.md:736-743`): `tests/test_persistence.py`, `tests/test_authentication_consent.py` and `tests/test_voice_enrollment.py` are left out of whole-suite checks. This milestone runs no full suite (`prompt-driven-development` Test Scope: RED runs only the new tests). Its one whole-suite command, the collection check (command 6), applies the same three `--ignore` options. This does not conflict with `Plan.md`: the OAM-4 success criteria (`Plan.md:186`) name only the new tests and the preserved tests, and none of them is in those three files.
- **OAV-3 handling** (`002_Implementation_Plan_OAM-3.md:596-597`): after a test run writes to tracked `audio_storage/`, the output is recorded, then `git checkout -- audio_storage` and `git clean -fd -- audio_storage` restore it.

## Preconditions / Predecessor Evidence

- `Plan.md` Status records approval (`Plan.md:5`). OAM-4 is recorded as RED (`Plan.md:172`), with predecessor OAM-3 (`Plan.md:173`). No FOUNDATION precedes it (`Plan.md:114`, `:182`).
- OAM-3 is `Complete — GREEN verified 2026-11-13` (`Plan.md:336`). Its evidence (`Plan.md:414-434`): the 11 OAM-2 tests passed twice; the reduced full suite failed only on the accepted `test_production_inference_module_missing`; `audio_storage` was restored. It was committed as `0465867`, which is HEAD.
- OAM-4 Execution Status is `Pending` (`Plan.md:337`). No Implementation Plan exists for OAM-4, approved or stopped. The folder holds `requirements.md`, `Plan.md`, `API-Contract.md`, `001_Implementation_Plan_OAM-2.md` and `002_Implementation_Plan_OAM-3.md`, so this plan is `003`.
- Repository state, inspected 2026-11-13: HEAD `0465867`, branch `claude/chatterbox-original-app-client-a3ef0e`. `git status --short` printed nothing. No unrecorded change exists.
- Prerequisites (`Plan.md:182`), checked with `importlib` in the Python on PATH (`finnie-chat\venv`, Python 3.14.3):
  - pinned in `requirements-dev.txt`: fastapi 0.162.0, uvicorn 0.54.0, httpx 0.28.1, python-multipart, pytest 9.1.1;
  - installed but pinned at a different version: SQLAlchemy 2.0.49 (pinned `2.0.41`);
  - installed but undeclared: cryptography 50.0.2, google-auth 2.62.1 and requests 2.33.1. The test file imports only cryptography; the other two are what GREEN is expected to use (V4D-2). `pytest-asyncio` 1.4.0 is not needed, because the new tests are synchronous.
  - No FOUNDATION is needed.

## Current Repository State

- `voice_narration/inference/application.py:392-397`: `create_app(*, provider=None, jobs_app=None, job_repository=None)`. The tests inject the startup provider through `provider` (V4D-7).
- `voice_narration/inference/application.py:461-479`: the generation route reads only `script` and `voice_id`. It calls the startup provider for every request (`:292`), so `provider` and `language` are ignored. `ValueError` gives `400`, and any other exception `500`.
- `grep -rn "Lock\|Semaphore\|CHATTERBOX\|VOICE_SERVICE_URL" voice_narration/inference/` finds nothing. There is no Chatterbox code, no waiting, and no reading of the new settings.
- `voice_narration/inference/application.py:87-89`: `InferenceState.__init__` reads `AUDIO_STORAGE_PATH`, so the tests point storage at `tmp_path`. `storage_root` (`:96-98`) exposes the value in force.
- `voice_narration/inference/application.py:22`, `:107-111`, `:151-179`, `:250-257`: database writes go through the module names `create_all_tables` and `SessionLocal`. `:174` sets `expires_at = created_at + AUDIO_RETENTION_DAYS` (default 30). Exceptions are swallowed (`:178-179`).
- `voice_narration/inference/db.py:14-16` loads `.env` files at import. `:19-28` defaults to a local PostgreSQL URL, and `:31-32` creates the engine at import. A socket check during planning found something listening on `localhost:5432`. No `.env` exists in the worktree (`ls -a`).
- `voice_narration/inference/application.py:623`: `app = create_app()` runs at import. This is pre-existing (V4R-5).
- `voice_narration/inference/application.py:343-373`: the provider list holds the registry's providers with the baseline descriptions (`:356-363`), sorted by name (`registry.py:60`).
- `voice_narration/inference/providers/mock.py:93`: `MockInferenceProvider._generate_silent_wav`, which the startup fake reuses for its audio.
- `voice_narration/simple_voices/application.py:68`: `create_app(*, root=None, clock=None)`. `:184-192`: `GET /voices/{voice_id}/sample` (OAM-3).
- `tests/` has no `conftest.py`. `pytest.ini:2`: `--strict-config --strict-markers`. The new file uses no marker.
- Python's `wave` module cannot read the 32-bit float WAV that Chatterbox returns (CON-5): `wave.open` on the test's `CLONED_WAV` raised `Error unknown format: 3` (planning check). See V4D-8.

## Files in Scope

### Files to Create

- `tests/test_chatterbox_generation_red.py`

### Files to Modify

None.

### Files to Delete

None.

## Proposed Changes

1. Create `tests/test_chatterbox_generation_red.py`. It holds:
   - **Constants:**
     - the contract's exact strings: the nine OAF messages (`timed_out`, `access_denied` and `service_error` fill in `<N>` and `<status>`), `UNSUPPORTED_PROVIDER`, `UNSUPPORTED_LANGUAGE`, `MISSING_FIELDS`, `CHATTERBOX_DESCRIPTION` and `BASELINE_DESCRIPTIONS` (`API-Contract.md:287-290`, `:336-346`, `:449-454`);
     - `HISTORY_FIELDS` (`:298`), `SERVICE_ACCOUNT` (CON-5), `PRELOADED_VOICE` and `UNKNOWN_VOICE`;
     - `LONG_TEXT`: English 6200 characters and Hindi 6600 characters, both with line breaks;
     - `CLONED_FRAMES`/`CLONED_RATE`, and the placeholders `CLOSED_URL`, `MISSING_KEY` and `AUTHORIZED_USER_KEY`.
   - **Audio:**
     - `pcm_wav()`, the uploaded voice sample;
     - `float_wav()`, the 24 kHz float WAV Chatterbox returns (V4D-8);
     - `VOICE_SAMPLE`, `CLONED_WAV` and `STARTUP_WAV`.
   - **Token helpers:** `b64url`, `b64url_decode` and `identity_token()`, a JWT-shaped token with an `exp` claim.
   - **`StartupProvider(MockInferenceProvider)`:** an optional delay. It records calls, the in-flight count and the maximum in-flight count (V4D-7).
   - **`FakeGoogleAndChatterbox`:** one FastAPI app with three routes (V4D-2, V4D-3):
     - `POST /token` verifies the assertion's RS256 signature with the key's public half and records its claims. It answers `{"id_token": …}`, or `token_status`.
     - `POST /v1/synthesize` records the call: authorization, `text`, `language`, the `sample_audio` bytes and whether it is a file part, and start and end times. It then answers as `synth` sets: status, content type, body, a delay, a trickled body, or a redirect. Like Cloud Run, it answers `401` to a `200`-bound call whose bearer token was not issued for exactly its URL.
     - `POST /redirect-target` returns audio, so a followed redirect would show up.
     - Its methods are `reset()`, `respond(**changes)` and `authorized(header)`.
   - **Servers and helpers:**
     - `serve(app)` runs uvicorn in a daemon thread on a socket bound to `127.0.0.1:0` before the server starts, and stops it on exit (V4D-1);
     - `closed_port_url()`, `service_account_key()`, `upload_voice()`, `generate()`, `wait_until()` and `post_in_background()`.
   - **`Harness`:**
     - `resolve` and `settings` set or delete environment variables, using `monkeypatch`;
     - `voice` maps a name to a voice id;
     - `inference(startup)` builds `create_app(provider=startup)`, asserts the storage root in force, and serves it;
     - `stored_files` and `generation_row` read storage and the SQLite database.
   - **Fixtures:**
     - module-scoped `signing_key`, `fake`, and `voices`, which is the real OAM-3 voice service over a temporary root, with one uploaded voice and one deleted voice;
     - per-test `harness`, which writes the key file, patches the database to SQLite (V4D-5) and sets the base environment.
   - **The 10 test functions** listed under Contract Rule Coverage.
2. No production, build, configuration or existing test file changes.

### Decisions for Review (binding OAM-5)

- **V4D-1 Real loopback transport for every party.**
  - The inference app, the real voice service and the fake each run under uvicorn in a thread of the test process. Each uses a socket bound to `127.0.0.1` port 0 before the server starts. So no other process can take the port between choosing and binding it (compare V2R-1). Clients use `httpx.Client(trust_env=False)`.
  - The inference app is created after the test sets its settings in the environment. This binds GREEN to read the OAC-6/OAC-7/OAC-4 settings from the process environment when `create_app` runs (contract `:469`). Reading them on each request would also pass.
  - Alternatives:
    - (a) `TestClient` in process. Rejected for the waiting tests and the client-stops-waiting test, which need concurrent connections and a real disconnect. The testing skill also asks for real transport for fixed error bodies.
    - (b) The inference service as a subprocess, as in V2D-2. Rejected: the startup provider fake and the database patch cannot be injected into it.
- **V4D-2 Identity token through the key file's `token_uri`.**
  - The test writes a service-account key file for `SERVICE_ACCOUNT`, with a fresh RSA key from `cryptography` and `token_uri` set to the fake's `/token`. It sets `GOOGLE_APPLICATION_CREDENTIALS` to that file.
  - The fake checks the assertion's signature, `iss` and `target_audience`. This binds GREEN to obtain the token with the service-account JWT-bearer grant at the key file's `token_uri`. google-auth's `service_account.IDTokenCredentials` does that: the probe passed with it. The dry run also showed that google-auth always sets the assertion's `aud` to `https://oauth2.googleapis.com/token` (`_make_authorization_grant_assertion`) and posts to `token_uri` (`id_token_jwt_grant`). So the tests do not assert `aud`.
  - `cryptography` is installed (50.0.2) but not declared in `requirements-dev.txt` (Plan OAR-4). This RED milestone changes no declaration. GREEN needs a signing library for the same token anyway: google-auth signs with `cryptography` or `rsa`, and only `cryptography` is installed. Whether OAM-5 declares google-auth, requests and cryptography is OAM-5's decision (`Plan.md:441`).
  - Alternatives:
    - (a) A `create_app` parameter that injects a token source. Rejected: it adds a seam the contract does not have, and it leaves the real token request untested.
    - (b) Monkeypatching a google-auth function. Rejected: it binds GREEN to one library entry point.
    - (c) A fixed PEM key embedded in the test, with no signature check. This avoids the `cryptography` import, but it commits private-key text, which secret scanners flag.
- **V4D-3 The fake answers like Cloud Run in front of Chatterbox.** A call that would succeed gets `401` unless its bearer token was issued for exactly the fake's URL. So the success tests prove that the token's audience is the Chatterbox URL in effect (CON-5, reference contract Chatterbox Caller Identity). The fake reads the parts `text`, `language` and `sample_audio` as the reference contract's Chatterbox Synthesize defines them. Alternative: assert only the recorded `Authorization` header. Rejected, because that does not tie the token to the audience.
- **V4D-4 The voice sample comes from the real OAM-3 voice service.** The fixture uploads a PCM WAV, which OAM-3 stores byte-identical, then checks `GET /voices/{id}/sample` returns it before any test runs. For OAF-3 it uses an unknown id, a preloaded voice (no sample), a deleted voice, and a closed port. Alternative: a fake voice service. Rejected: it would not show that the two services work together through OAC-4.
- **V4D-5 The database is observed through SQLite.**
  - Each test patches `voice_narration.inference.application.SessionLocal` and `.create_all_tables` with a SQLite database under `tmp_path`. This lets the 30-day expiry be read without PostgreSQL (Plan OAR-2). It also keeps these tests off the PostgreSQL instance that listens on `localhost:5432`.
  - This binds GREEN to keep writing generation records through those two module-level names (`application.py:22`).
  - Alternatives:
    - (a) The local PostgreSQL. Rejected: it belongs to the user, not the test, and CON-2 rules out a test container.
    - (b) `DATABASE_URL` in a subprocess. Rejected: the engine is created at import (`db.py:31`), and a subprocess cannot take the fakes.
- **V4D-6 Time-limit seam `app.state.inference.chatterbox_time_limit_seconds`.**
  - GREEN must expose the limit in force as an `int`: `1200` when `CHATTERBOX_TIMEOUT_SECONDS` is absent or blank, and the parsed value otherwise. The test asserts it for absent, `"   "` and `" 7 "`. Its value for an invalid setting is not asserted; OAF-2's message covers that case.
  - Reason: the 1200 s default can be seen through OAF-5's `<N>` only after a 1200 s wait. The configured limit is proved through behavior instead, by the OAF-5 cases (`" 2 "` and `"2"`, `<N>` = 2).
  - Alternatives:
    - (a) No seam. The default would then be covered only by a 2.5 s call that is not cut off.
    - (b) Patch the event loop's clock. Rejected as fragile across threads.
- **V4D-7 The startup provider stands in for Google.** The contract makes `"google"`, absent, `null` and `""` all use the startup provider (`API-Contract.md:279-280`). So `create_app(provider=StartupProvider())` serves those generations, and real Google is never called (COA-16).
- **V4D-8 Chatterbox's audio is 32-bit IEEE-float mono WAV at 24 kHz** (CON-5: "WAV (24 kHz float)"). `duration_seconds` must equal `36001 / 24000`, unrounded (`API-Contract.md:329`). This binds GREEN's "readable WAV" check to accept float WAV, which the standard `wave` module rejects (Current Repository State).
- **V4D-9 The provider list is tested here.** The OAM-4 scope bullets (`Plan.md:174-181`) do not name the provider list. But OAC-3 is part of COA-1 (`API-Contract.md:505`), the traceability assigns COA-1's inference part to OAM-4 for verification (`Plan.md:267`), and OAM-5 must deliver it (`Plan.md:195`), which needs RED evidence. If the reviewer reads the scope as excluding it, the test is removed from this plan before approval.
- **V4D-10 Timing values.**
  - OAF-5 uses a limit of 2 s against a 4 s delay, or a body trickled over 4 s. The answer must come in under 3.7 s.
  - The waiting tests use startup delays of 1.5 s and 3 s.
  - The impatient client waits 0.5 s against a 2 s Chatterbox delay.
  - Background requests create their clients before their thread starts. The next request is sent only once the startup provider reports a generation in flight. The first draft did not do this, and the dry run showed its background request could arrive late.

### Contract Rule Coverage

| Contract rule (`API-Contract.md`) | Test |
| --- | --- |
| Chatterbox Call steps 2–4: the sample fetched from `VOICE_SERVICE_URL` (trimmed); token audience = the URL in effect (trimmed, trailing `/` removed), Bearer header; `text` whole and unchanged (> 5000 characters, line breaks), `language`, `sample_audio` as a file part holding the stored bytes (`:320-326`, `:473`, `:476`); success with a media type compared case-insensitively, parameters ignored; body saved unchanged; `duration_seconds` = frames / rate, unrounded (`:329`); output and download carry the audio | `test_chatterbox_generation_sends_whole_text_language_sample_and_identity_token[en]`, `[hi]` |
| `provider` `"chatterbox"` → Chatterbox; `"google"`, absent, `null`, `""` → startup provider; `language` ignored for Google (`:278-283`) | `test_each_generation_uses_the_provider_it_names` |
| Failures 3 and 4 with exact bodies, including letter case, whitespace and non-string values; check 2 before checks 3–4; nothing generated or saved (`:288-290`, `:495`) | `test_unsupported_provider_or_language_is_rejected_without_generating[…]` (12 cases) |
| OAF-1–OAF-9: each answers `503` with its exact message ending with the closing sentence (`:334-346`); the order of causes (`:318-321`, `:507`); no other provider used, no audio file written, the existing history entry, download and output with the same `job_id` unchanged (`:297`, `:300`); redirects not followed (`:327`); the limit covers the whole response, including a slow body (`:328`); invalid limit values (`:474`); blank and absent URL and key settings (`:473`, `:475`) | `test_each_chatterbox_failure_cause_answers_503_with_its_message_and_no_fallback[…]` (35 cases) |
| Absent or blank `CHATTERBOX_TIMEOUT_SECONDS` = 1200; surrounding whitespace is trimmed (`:474`); a slow call within the default completes | `test_time_limit_defaults_to_1200_seconds_and_a_blank_setting_means_the_default` |
| Saving a success: history entry fields exactly as listed, with no field added (`:298`, `:513`); detail; download headers (`:377`); database expiry = `created_at` + 30 days (`:298`); deletion removes the entry, the audio, the in-memory output and the database record (`:438`) | `test_cloned_generation_is_in_history_downloadable_deletable_with_30_day_retention` |
| Provider list: exactly `azure`, `chatterbox`, `google`, `mock` in that order, with baseline descriptions and the Chatterbox description; listed when the settings are absent; `provider_class` is a non-empty string (`:449-454`) | `test_provider_list_adds_chatterbox_and_keeps_the_other_providers` |
| One generation at a time; a request waits and then completes; validation failures are answered without waiting (`:306-308`) | `test_a_generation_request_that_arrives_during_another_waits_then_completes` |
| Waiting covers every provider and does not count toward the time limit (`:306`, `:309`) | `test_waiting_for_another_generation_does_not_count_toward_the_chatterbox_time_limit` |
| A client that stops waiting does not cancel the generation; a success is saved (`:296`, `:48`) | `test_a_generation_whose_client_stops_waiting_still_completes_and_is_saved` |

Not tested, with the reason:

- OAF-3 for an expired voice. The voice service answers an expired voice exactly like an unknown one, `404 Voice not found` (`API-Contract.md:259`; OAM-3 tests). The unknown and deleted cases cover the inference side.
- OAF-3 for a voice-service answer other than `404`, for example `500`. The real voice service has no route that produces one. The two `404` cases and the unreachable case cover "any other answer, or no answer".
- OAF-6 for a TLS failure or a connection lost mid-response. Producing these needs a misbehaving TLS or socket server. The refused-connection and unusable-URL cases cover the transport-failure class.
- That the sample fetch and token request are not bounded by the time limit (`:320-321`). Testing this needs a deliberately slow voice service or token endpoint. It adds no requirement the tests above do not already exercise.
- The order in which waiting requests run, and whether other operations are answered during a generation. The contract leaves both undefined (`:307`, `:310`).
- That the inference service does not check the key's account (`:321`). This is an absence, and Cloud Run enforces it.
- Carried-over behavior that the Plan assigns to no RED scope (`Plan.md:174-181`): failure 1 (`500` for a non-object body), failure 7 (startup-provider errors, including Google rejecting long text), the output, detail and history operations for non-Chatterbox generations, the `.env` loading, `INFERENCE_PROVIDER`, `AUDIO_STORAGE_PATH`, `DATABASE_URL`, CORS. Preserved tests cover them, and they run in command 4.

## Proposed Code / Tests

### `tests/test_chatterbox_generation_red.py` (new file, complete content)

```python
"""OAM-4 RED: the inference service clones speech through the deployed Chatterbox.

Contract: docs/.ai/chatterbox-original-app/API-Contract.md (Inference Generation,
Generation Waiting, Inference Service Chatterbox Call, Chatterbox Failure Causes,
Inference Provider List, Inference Service Settings).

Nothing leaves 127.0.0.1 (COA-16). One local server stands in for Google's token
endpoint, reached through the test key file's ``token_uri``, and for the deployed
Chatterbox (CON-5). The voice service is the real OAM-3 service over a temporary
root. The startup provider is a recording fake, so Google is never called.
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import math
import socket
import struct
import threading
import time
import wave
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
import uvicorn
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from starlette.datastructures import UploadFile

from voice_narration.inference import application as inference_application
from voice_narration.inference.models import Base, Generation
from voice_narration.inference.providers.mock import MockInferenceProvider
from voice_narration.simple_voices.application import create_app as create_voice_app

SERVICE_ACCOUNT = "test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com"
CLOSING = "Please retry, or choose another provider."
NOT_CONFIGURED = f"Chatterbox voice cloning is not configured. {CLOSING}"
INVALID_TIME_LIMIT = (
    "The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; "
    f"it must be a positive whole number of seconds. {CLOSING}"
)
SAMPLE_UNREADABLE = f"The voice sample for the selected voice could not be read. {CLOSING}"
TOKEN_UNAVAILABLE = f"Could not obtain an identity token for Chatterbox. {CLOSING}"
CANNOT_CONNECT = f"Could not connect to Chatterbox. {CLOSING}"
NOT_AUDIO = f"Chatterbox returned a response that is not audio. {CLOSING}"
UNSUPPORTED_PROVIDER = {"error": "Unsupported provider. Choose google or chatterbox."}
UNSUPPORTED_LANGUAGE = {"error": "language must be en or hi for a chatterbox generation."}
MISSING_FIELDS = {"error": "Missing required fields: script, voice_id"}
CHATTERBOX_DESCRIPTION = "Chatterbox voice cloning (deployed Cloud Run service)"
BASELINE_DESCRIPTIONS = {
    "azure": "Azure Cognitive Services Speech (requires AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)",
    "google": "Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS)",
    "mock": "Deterministic mock for testing (no external deps)",
}
HISTORY_FIELDS = {"job_id", "text", "voice_id", "duration_seconds", "file_path", "format", "status", "created_at"}
PRELOADED_VOICE = "en-US-Neural2-A"
UNKNOWN_VOICE = "voice-00000000"
LONG_TEXT = {
    "en": "The quick brown fox jumps over the lazy dog, again and again.\n" * 100,
    "hi": "यह एक लंबा वाक्य है जिसे बिना बाँटे पूरा भेजा जाता है।\n" * 120,
}
CLONED_FRAMES = 36_001
CLONED_RATE = 24_000

# Placeholders in failure cases, replaced by Harness.resolve.
CLOSED_URL = "<closed port>"
MISSING_KEY = "<missing key file>"
AUTHORIZED_USER_KEY = "<authorized-user key file>"


def timed_out(seconds: int) -> str:
    return f"Chatterbox did not respond within {seconds} seconds. {CLOSING}"


def access_denied(status: int) -> str:
    return f"Access to Chatterbox was denied (HTTP {status}). {CLOSING}"


def service_error(status: int) -> str:
    return f"Chatterbox returned an error (HTTP {status}). {CLOSING}"


def pcm_wav(seconds: float = 0.5, rate: int = 16_000) -> bytes:
    """A PCM WAV voice sample, as an upload stores it byte-identical (OAM-3)."""
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


def float_wav(frames: int, rate: int) -> bytes:
    """32-bit float mono WAV, the form the deployed Chatterbox returns (CON-5)."""
    data = struct.pack(
        f"<{frames}f", *(0.25 * math.sin(2 * math.pi * 220 * index / rate) for index in range(frames))
    )
    fmt = struct.pack("<HHIIHH", 3, 1, rate, rate * 4, 4, 32)
    chunks = b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(data)) + data
    return b"RIFF" + struct.pack("<I", 4 + len(chunks)) + b"WAVE" + chunks


VOICE_SAMPLE = pcm_wav()
CLONED_WAV = float_wav(CLONED_FRAMES, CLONED_RATE)
STARTUP_WAV = MockInferenceProvider._generate_silent_wav(1_600)


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def identity_token(audience: str, serial: int) -> str:
    """A JWT-shaped identity token; google-auth reads its expiry without verifying it."""
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claims = {"iss": "https://accounts.google.com", "aud": audience, "email": SERVICE_ACCOUNT,
              "sub": "1", "iat": now, "exp": now + 3600, "serial": serial}
    return ".".join([b64url(json.dumps(header).encode()), b64url(json.dumps(claims).encode()), b64url(b"test")])


class StartupProvider(MockInferenceProvider):
    """The provider the inference service starts with; it serves no provider and "google"."""

    def __init__(self, delay: float = 0.0):
        super().__init__()
        self.delay = delay
        self.calls: list[dict] = []
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
            return {"output_seconds": 0.1, "audio_bytes": STARTUP_WAV, "format": "wav"}
        finally:
            with self._lock:
                self.in_flight -= 1
                self.calls.append({"voice_id": voice_id, "start": started, "end": time.monotonic()})


class FakeGoogleAndChatterbox:
    """Google's token endpoint and the deployed Chatterbox behind Cloud Run, as one local server."""

    def __init__(self, public_key):
        self.public_key = public_key
        self.url = ""
        self.reset()

    def reset(self) -> None:
        self.token_status = 200
        self.assertions: list[dict] = []
        self.issued: dict[str, str] = {}
        self.calls: list[dict] = []
        self.synth = {"status": 200, "content_type": "audio/wav", "body": CLONED_WAV,
                      "delay": 0.0, "trickle": 0.0, "location": None}

    def respond(self, **changes) -> None:
        self.synth.update(changes)

    def authorized(self, header: str | None) -> bool:
        """What Cloud Run accepts: a bearer token issued for exactly this service's URL (CON-5)."""
        if not header or not header.startswith("Bearer "):
            return False
        return self.issued.get(header[len("Bearer "):]) == self.url

    def app(self) -> FastAPI:
        app = FastAPI()

        @app.post("/token")
        async def token(request: Request):
            form = await request.form()
            header, payload, signature = str(form["assertion"]).split(".")
            claims = json.loads(b64url_decode(payload))
            try:
                self.public_key.verify(b64url_decode(signature), f"{header}.{payload}".encode(),
                                       padding.PKCS1v15(), hashes.SHA256())
                claims["signature_valid"] = True
            except InvalidSignature:
                claims["signature_valid"] = False
            self.assertions.append(claims)
            if self.token_status != 200:
                return JSONResponse({"error": "invalid_grant", "error_description": "rejected by the test"},
                                    status_code=self.token_status)
            issued = identity_token(str(claims.get("target_audience")), len(self.issued))
            self.issued[issued] = str(claims.get("target_audience"))
            return JSONResponse({"id_token": issued})

        @app.post("/v1/synthesize")
        async def synthesize(request: Request):
            call = {"start": time.monotonic(), "authorization": request.headers.get("authorization")}
            self.calls.append(call)
            form = await request.form()
            sample = form.get("sample_audio")
            call.update(text=form.get("text"), language=form.get("language"),
                        sample_is_file=isinstance(sample, UploadFile),
                        sample=await sample.read() if isinstance(sample, UploadFile) else sample)
            synth = dict(self.synth)
            if synth["delay"]:
                await asyncio.sleep(synth["delay"])
            call["end"] = time.monotonic()
            if synth["location"]:
                return Response(status_code=synth["status"], headers={"Location": self.url + synth["location"]})
            if synth["status"] == 200 and not self.authorized(call["authorization"]):
                return JSONResponse({"error": "unauthenticated"}, status_code=401)
            if synth["trickle"]:
                body = synth["body"]
                step = max(1, len(body) // 8)

                async def chunks():
                    for start in range(0, len(body), step):
                        await asyncio.sleep(synth["trickle"])
                        yield body[start:start + step]

                return StreamingResponse(chunks(), status_code=200, media_type=synth["content_type"])
            return Response(content=synth["body"], status_code=synth["status"], media_type=synth["content_type"])

        @app.post("/redirect-target")
        async def redirect_target():
            return Response(content=CLONED_WAV, media_type="audio/wav")

        return app


@contextmanager
def serve(app):
    """Run an ASGI app with uvicorn on a socket bound before start, so no other process can take its port."""
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


def closed_port_url() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return f"http://127.0.0.1:{sock.getsockname()[1]}"


def service_account_key(private_key, token_uri: str) -> dict:
    pem = private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                    serialization.NoEncryption()).decode()
    return {"type": "service_account", "project_id": "project-84eb579f-1f7b-4f87-838",
            "private_key_id": "test-key", "private_key": pem, "client_email": SERVICE_ACCOUNT,
            "client_id": "1", "token_uri": token_uri}


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


def post_in_background(url: str, job_id: str, results: dict, **body) -> threading.Thread:
    """Send a generation request from its own thread, with its client created before the thread starts."""
    client = httpx.Client(base_url=url, trust_env=False, timeout=60)

    def post():
        with client:
            results[job_id] = generate(client, job_id, **body)

    thread = threading.Thread(target=post)
    thread.start()
    return thread


class Harness:
    def __init__(self, fake, voices, root: Path, database, monkeypatch):
        self.fake = fake
        self.voices = voices
        self.root = root
        self.database = database
        self.monkeypatch = monkeypatch
        self.closed_url = closed_port_url()

    def resolve(self, value):
        if value == CLOSED_URL:
            return self.closed_url
        if value == MISSING_KEY:
            return str(self.root / "no-such-key.json")
        if value == AUTHORIZED_USER_KEY:
            path = self.root / "authorized-user.json"
            path.write_text(json.dumps({"type": "authorized_user", "client_id": "1",
                                        "client_secret": "s", "refresh_token": "r"}))
            return str(path)
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
            yield SimpleNamespace(app=app, url=url, client=client, startup=startup)

    def stored_files(self) -> list[str]:
        audio = self.root / "audio"
        return sorted(str(path.relative_to(audio)) for path in audio.rglob("*") if path.is_file())

    def generation_row(self, job_id: str):
        with Session(self.database) as session:
            return session.scalars(select(Generation).where(Generation.job_id == job_id)).first()


@pytest.fixture(scope="module")
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="module")
def fake(signing_key):
    fake = FakeGoogleAndChatterbox(signing_key.public_key())
    with serve(fake.app()) as url:
        fake.url = url
        yield fake


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
def harness(fake, voices, signing_key, tmp_path, monkeypatch):
    fake.reset()
    key_file = tmp_path / "service-account-key.json"
    key_file.write_text(json.dumps(service_account_key(signing_key, f"{fake.url}/token")))
    database = create_engine(f"sqlite:///{tmp_path / 'inference.db'}", connect_args={"check_same_thread": False})
    monkeypatch.setattr(inference_application, "SessionLocal",
                        sessionmaker(bind=database, autoflush=False, expire_on_commit=False))
    monkeypatch.setattr(inference_application, "create_all_tables", lambda: Base.metadata.create_all(bind=database))
    for name in ("CHATTERBOX_TIMEOUT_SECONDS", "AUDIO_RETENTION_DAYS", "INFERENCE_PROVIDER"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CHATTERBOX_URL", fake.url)
    monkeypatch.setenv("VOICE_SERVICE_URL", voices.url)
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(key_file))
    monkeypatch.setenv("AUDIO_STORAGE_PATH", str(tmp_path / "audio"))
    yield Harness(fake, voices, tmp_path, database, monkeypatch)
    database.dispose()


@pytest.mark.parametrize("language", ["en", "hi"])
def test_chatterbox_generation_sends_whole_text_language_sample_and_identity_token(harness, language):
    script = LONG_TEXT[language]
    assert len(script) > 5000
    harness.settings(CHATTERBOX_URL=f"  {harness.fake.url}/  ", VOICE_SERVICE_URL=f" {harness.voices.url}/ ")
    harness.fake.respond(content_type="Audio/WAV; rate=24000")
    job_id = f"clone-{language}"
    with harness.inference() as service:
        response = generate(service.client, job_id, script=script, voice_id=harness.voices.uploaded,
                            provider="chatterbox", language=language)
        assert response.status_code == 200, response.text
        assert len(harness.fake.calls) == 1, "Chatterbox received no synthesize request"
        call = harness.fake.calls[0]
        assert call["text"] == script
        assert call["language"] == language
        assert call["sample_is_file"] and call["sample"] == VOICE_SAMPLE
        assert harness.fake.authorized(call["authorization"]), call["authorization"]
        assertion = harness.fake.assertions[-1]
        assert assertion["signature_valid"]
        assert assertion["iss"] == SERVICE_ACCOUNT
        assert assertion["target_audience"] == harness.fake.url
        assert response.json() == {"job_id": job_id, "status": "complete",
                                   "duration_seconds": CLONED_FRAMES / CLONED_RATE}
        assert service.client.get(f"/inference/jobs/{job_id}/download").content == CLONED_WAV
        output = service.client.get(f"/inference/jobs/{job_id}/output").json()
        assert base64.b64decode(output["audio_bytes"]) == CLONED_WAV
        assert service.startup.calls == []


def test_each_generation_uses_the_provider_it_names(harness):
    with harness.inference() as service:
        cloned = generate(service.client, "route-chatterbox", script="Hello there", voice_id=harness.voices.uploaded,
                          provider="chatterbox", language="en")
        assert cloned.status_code == 200, cloned.text
        assert len(harness.fake.calls) == 1, "Chatterbox received no synthesize request"
        assert service.startup.calls == []
        for job_id, choice in [("route-google", {"provider": "google", "language": "fr"}),
                               ("route-absent", {}), ("route-null", {"provider": None}),
                               ("route-empty", {"provider": ""})]:
            response = generate(service.client, job_id, script="Namaste", voice_id=PRELOADED_VOICE, **choice)
            assert response.status_code == 200, response.text
        assert [call["voice_id"] for call in service.startup.calls] == [PRELOADED_VOICE] * 4
        assert len(harness.fake.calls) == 1


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
        assert service.startup.calls == [] and harness.fake.calls == []
        assert service.client.get("/inference/generations/rejected").status_code == 404
        missing = generate(service.client, "rejected", voice_id=harness.voices.uploaded, **choice)
        assert missing.status_code == 400 and missing.json() == MISSING_FIELDS


def failure(error, *, settings=None, voice="uploaded", token_status=200, synth=None,
            reaches_chatterbox=False, max_seconds=None, id):
    return pytest.param(SimpleNamespace(error=error, settings=settings or {}, voice=voice,
                                        token_status=token_status, synth=synth or {},
                                        reaches_chatterbox=reaches_chatterbox, max_seconds=max_seconds), id=id)


FAILURES = [
    failure(NOT_CONFIGURED, settings={"CHATTERBOX_URL": None}, id="OAF-1-url-absent"),
    failure(NOT_CONFIGURED, settings={"CHATTERBOX_URL": "   "}, id="OAF-1-url-blank"),
    failure(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "0"}, id="OAF-2-zero"),
    failure(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "-5"}, id="OAF-2-negative"),
    failure(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "10.5"}, id="OAF-2-fraction"),
    failure(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "ten"}, id="OAF-2-word"),
    failure(SAMPLE_UNREADABLE, voice="unknown", id="OAF-3-unknown-voice"),
    failure(SAMPLE_UNREADABLE, voice="preloaded", id="OAF-3-voice-without-sample"),
    failure(SAMPLE_UNREADABLE, voice="deleted", id="OAF-3-deleted-voice"),
    failure(SAMPLE_UNREADABLE, settings={"VOICE_SERVICE_URL": CLOSED_URL}, id="OAF-3-voice-service-unreachable"),
    failure(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": None}, id="OAF-4-key-setting-absent"),
    failure(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": "  "}, id="OAF-4-key-setting-blank"),
    failure(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": MISSING_KEY}, id="OAF-4-key-file-missing"),
    failure(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": AUTHORIZED_USER_KEY},
            id="OAF-4-not-a-service-account-key"),
    failure(TOKEN_UNAVAILABLE, token_status=400, id="OAF-4-token-request-rejected"),
    failure(timed_out(2), settings={"CHATTERBOX_TIMEOUT_SECONDS": " 2 "}, synth={"delay": 4.0},
            reaches_chatterbox=True, max_seconds=3.7, id="OAF-5-no-answer-within-limit"),
    failure(timed_out(2), settings={"CHATTERBOX_TIMEOUT_SECONDS": "2"}, synth={"trickle": 0.5},
            reaches_chatterbox=True, max_seconds=3.7, id="OAF-5-response-incomplete-within-limit"),
    failure(CANNOT_CONNECT, settings={"CHATTERBOX_URL": CLOSED_URL}, id="OAF-6-connection-refused"),
    failure(CANNOT_CONNECT, settings={"CHATTERBOX_URL": "not-a-url"}, id="OAF-6-unusable-url"),
    failure(access_denied(401), synth={"status": 401}, reaches_chatterbox=True, id="OAF-7-401"),
    failure(access_denied(403), synth={"status": 403}, reaches_chatterbox=True, id="OAF-7-403"),
    *[failure(service_error(status), synth={"status": status, "content_type": "application/json",
                                            "body": b'{"detail": "failed"}'},
              reaches_chatterbox=True, id=f"OAF-8-{status}")
      for status in (400, 422, 429, 500, 503, 504)],
    failure(service_error(307), synth={"status": 307, "location": "/redirect-target"},
            reaches_chatterbox=True, id="OAF-8-redirect-not-followed"),
    failure(NOT_AUDIO, synth={"body": b""}, reaches_chatterbox=True, id="OAF-9-empty-body"),
    failure(NOT_AUDIO, synth={"content_type": "application/json", "body": b'{"audio": "none"}'},
            reaches_chatterbox=True, id="OAF-9-not-audio-wav"),
    failure(NOT_AUDIO, synth={"body": b"this is not a wav file" * 8}, reaches_chatterbox=True,
            id="OAF-9-unreadable-wav"),
    failure(NOT_CONFIGURED, settings={"CHATTERBOX_URL": None, "CHATTERBOX_TIMEOUT_SECONDS": "ten"},
            voice="unknown", id="order-OAF-1-before-OAF-2"),
    failure(INVALID_TIME_LIMIT, settings={"CHATTERBOX_TIMEOUT_SECONDS": "ten"}, voice="unknown",
            id="order-OAF-2-before-OAF-3"),
    failure(SAMPLE_UNREADABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": None}, voice="unknown",
            id="order-OAF-3-before-OAF-4"),
    failure(TOKEN_UNAVAILABLE, settings={"GOOGLE_APPLICATION_CREDENTIALS": None}, synth={"status": 500},
            id="order-OAF-4-before-the-call"),
]


@pytest.mark.parametrize("case", FAILURES)
def test_each_chatterbox_failure_cause_answers_503_with_its_message_and_no_fallback(harness, case):
    harness.settings(**case.settings)
    harness.fake.token_status = case.token_status
    harness.fake.respond(**case.synth)
    with harness.inference() as service:
        earlier = generate(service.client, "same-job", script="Earlier narration", voice_id=PRELOADED_VOICE,
                           provider="google")
        assert earlier.status_code == 200, earlier.text
        entry = service.client.get("/inference/generations/same-job").json()
        audio = service.client.get("/inference/jobs/same-job/download").content
        output = service.client.get("/inference/jobs/same-job/output").json()
        files = harness.stored_files()
        started = time.monotonic()
        response = generate(service.client, "same-job", script="Cloned narration",
                            voice_id=harness.voice(case.voice), provider="chatterbox", language="hi")
        elapsed = time.monotonic() - started
        assert response.status_code == 503, response.text
        assert response.json() == {"error": case.error}
        assert case.error.endswith(CLOSING)
        if case.max_seconds:
            assert elapsed < case.max_seconds, f"answered after {elapsed:.2f} s"
        assert len(service.startup.calls) == 1, "another provider generated the failed generation"
        assert len(harness.fake.calls) == (1 if case.reaches_chatterbox else 0)
        assert service.client.get("/inference/generations/same-job").json() == entry
        assert service.client.get("/inference/jobs/same-job/download").content == audio
        assert service.client.get("/inference/jobs/same-job/output").json() == output
        assert harness.stored_files() == files


def test_time_limit_defaults_to_1200_seconds_and_a_blank_setting_means_the_default(harness):
    for raw, expected in [(None, 1200), ("   ", 1200), (" 7 ", 7)]:
        harness.settings(CHATTERBOX_TIMEOUT_SECONDS=raw)
        app = inference_application.create_app(provider=StartupProvider())
        assert app.state.inference.chatterbox_time_limit_seconds == expected
    harness.settings(CHATTERBOX_TIMEOUT_SECONDS=None)
    harness.fake.respond(delay=2.5)
    with harness.inference() as service:
        response = generate(service.client, "slow-clone", script="A slow cold start",
                            voice_id=harness.voices.uploaded, provider="chatterbox", language="en")
        assert response.status_code == 200, response.text
        assert len(harness.fake.calls) == 1


def test_cloned_generation_is_in_history_downloadable_deletable_with_30_day_retention(harness):
    script = LONG_TEXT["hi"]
    voice_id = harness.voices.uploaded
    with harness.inference() as service:
        response = generate(service.client, "history-clone", script=script, voice_id=voice_id,
                            provider="chatterbox", language="hi")
        assert response.status_code == 200, response.text
        assert len(harness.fake.calls) == 1, "Chatterbox received no synthesize request"
        listing = service.client.get("/inference/generations", params={"voice_id": voice_id}).json()
        assert listing["total"] == 1
        entry = listing["items"][0]
        assert set(entry) == HISTORY_FIELDS
        assert entry["job_id"] == "history-clone" and entry["text"] == script and entry["voice_id"] == voice_id
        assert entry["duration_seconds"] == CLONED_FRAMES / CLONED_RATE
        assert entry["format"] == "wav" and entry["status"] == "complete"
        assert service.client.get("/inference/generations/history-clone").json() == entry
        download = service.client.get("/inference/jobs/history-clone/download")
        assert download.status_code == 200 and download.content == CLONED_WAV
        assert download.headers["content-type"].startswith("audio/wav")
        assert download.headers["content-disposition"] == f'attachment; filename="{voice_id}_history-clone.wav"'
        row = harness.generation_row("history-clone")
        assert row is not None, "the cloned generation was not written to the database"
        assert row.expires_at - row.created_at == timedelta(days=30)
        deleted = service.client.delete("/inference/generations/history-clone")
        assert deleted.status_code == 200 and deleted.json() == {"job_id": "history-clone", "deleted": True}
        assert service.client.get("/inference/generations/history-clone").status_code == 404
        assert service.client.get("/inference/jobs/history-clone/download").status_code == 404
        assert harness.generation_row("history-clone") is None
        assert [name for name in harness.stored_files() if name.endswith(".wav")] == []


def test_provider_list_adds_chatterbox_and_keeps_the_other_providers(harness):
    harness.settings(CHATTERBOX_URL=None, GOOGLE_APPLICATION_CREDENTIALS=None)
    with harness.inference() as service:
        response = service.client.get("/inference/backends")
        assert response.status_code == 200, response.text
        backends = response.json()["backends"]
        assert [backend["name"] for backend in backends] == ["azure", "chatterbox", "google", "mock"]
        descriptions = {backend["name"]: backend["description"] for backend in backends}
        assert descriptions == {**BASELINE_DESCRIPTIONS, "chatterbox": CHATTERBOX_DESCRIPTION}
        assert all(isinstance(backend["provider_class"], str) and backend["provider_class"] for backend in backends)


def test_a_generation_request_that_arrives_during_another_waits_then_completes(harness):
    startup = StartupProvider(delay=1.5)
    with harness.inference(startup) as service:
        results = {}
        first = post_in_background(service.url, "wait-first", results, script="First", voice_id=PRELOADED_VOICE)
        wait_until(lambda: startup.in_flight == 1, "the first generation did not start")
        second = post_in_background(service.url, "wait-second", results, script="Second",
                                    voice_id=PRELOADED_VOICE, provider="google")
        time.sleep(0.3)
        invalid = generate(service.client, "wait-invalid", voice_id=PRELOADED_VOICE)
        invalid_answered = time.monotonic()
        first.join(30)
        second.join(30)
        assert startup.max_in_flight == 1, "a second generation ran while the first was generating"
        assert results["wait-first"].status_code == 200, results["wait-first"].text
        assert results["wait-second"].status_code == 200, results["wait-second"].text
        earlier, later = sorted(startup.calls, key=lambda call: call["start"])
        assert later["start"] >= earlier["end"]
        assert invalid.status_code == 400 and invalid.json() == MISSING_FIELDS
        assert invalid_answered < earlier["end"], "a request rejected by validation waited"


def test_waiting_for_another_generation_does_not_count_toward_the_chatterbox_time_limit(harness):
    harness.settings(CHATTERBOX_TIMEOUT_SECONDS="2")
    startup = StartupProvider(delay=3.0)
    with harness.inference(startup) as service:
        results = {}
        narration = post_in_background(service.url, "narration", results, script="Narration",
                                       voice_id=PRELOADED_VOICE, provider="google")
        wait_until(lambda: startup.in_flight == 1, "the narration did not start")
        cloned = generate(service.client, "clone-after-wait", script="Cloned after a wait",
                          voice_id=harness.voices.uploaded, provider="chatterbox", language="en")
        narration.join(30)
        assert cloned.status_code == 200, cloned.text
        assert len(harness.fake.calls) == 1, "Chatterbox received no synthesize request"
        assert harness.fake.calls[0]["start"] >= startup.calls[0]["end"]
        assert results["narration"].status_code == 200, results["narration"].text


def test_a_generation_whose_client_stops_waiting_still_completes_and_is_saved(harness):
    harness.fake.respond(delay=2.0)
    with harness.inference() as service:
        with httpx.Client(base_url=service.url, trust_env=False, timeout=0.5) as impatient:
            with pytest.raises(httpx.ReadTimeout):
                generate(impatient, "given-up", script="Nobody waits for this", voice_id=harness.voices.uploaded,
                         provider="chatterbox", language="en")
        deadline = time.monotonic() + 15
        while service.client.get("/inference/generations/given-up").status_code != 200:
            assert time.monotonic() < deadline, "the generation was not saved after its client stopped waiting"
            time.sleep(0.2)
        assert service.client.get("/inference/jobs/given-up/download").content == CLONED_WAV
```

## Execution Steps

1. Confirm that this plan's Human Review status records approval, and that `git status --short` prints nothing outside `docs/.ai/chatterbox-original-app/`.
2. Create `tests/test_chatterbox_generation_red.py` with exactly the content above.
3. Run the commands under Verification in order, writing each log outside the repository. Do not start, stop or check the Docker engine, and run no `gcloud` command (CON-2).
4. Record the evidence in `Plan.md` Execution Status for OAM-4, and update this plan's Human Review status.

## Acceptance / Completion Criteria

- **V4C-1** The only repository change is the new file `tests/test_chatterbox_generation_red.py`. Its content is exactly the block above: with CR removed, its SHA-256 is `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948` (command 1). No production, build, configuration or existing test file changes. This excludes the OAM-4 Execution Status update in `Plan.md` and this plan's Human Review status.
- **V4C-2** The first run of the new file reports `56 failed`, with 0 passed and 0 errors. Each failure falls into exactly one of these classes, each caused by the missing approved behavior:
  - 35 failure-cause tests: `assert 200 == 503`. The Chatterbox request was generated by the startup provider.
  - 12 rejection tests: `assert 200 == 400`. `provider` and `language` are not validated.
  - 5 tests: `AssertionError: Chatterbox received no synthesize request`. These are the two `[en]`/`[hi]` call tests, the routing test, the history test and the time-limit-wait test.
  - 1 test: `AssertionError: a second generation ran while the first was generating`. There is no waiting.
  - 1 test: `Failed: DID NOT RAISE` `ReadTimeout`. The generation never reached a slow Chatterbox.
  - 1 test: `AttributeError: 'InferenceState' object has no attribute 'chatterbox_time_limit_seconds'`. This is the absent V4D-6 seam.
  - 1 test: the provider-list assertion `['azure', 'google', 'mock'] == ['azure', 'chatterbox', …]`. Chatterbox is not listed.

  Command 2's class counts must be exactly 35, 12, 5, 1, 1, 1, 1, totalling 56. Any other failure cause, including any import, fixture or server-start failure, is not valid RED evidence and stops execution.
- **V4C-3** A second run of the same file, with no cleanup between runs, gives the same result as V4C-2 (Repeatable, Isolated Verification). The tests keep all state under `tmp_path`, and they assert the storage root in force.
- **V4C-4** After the two runs, `git status --short -- audio_storage` prints nothing, and no `voice_storage/` folder exists. If either fails, stop and report; do not restore and continue.
- **V4C-5** The preserved tests (`Plan.md:184`) still pass: `29 passed`, 0 failed, 0 errors. Then OAV-3 holds, with any `audio_storage/` output written by the preserved tests recorded and restored (Plan OAR-1).
- **V4C-6** Collecting the backend suite with the three V3Q-3 `--ignore` options reports `138 tests collected` with no collection error, 56 of them from the new file.
- **V4C-7** No process or thread started by the runs is left running (`prompt-driven-development` Plan Progress).

## Verification

### Commands

Run from the repository root in Git Bash. `$TEMP` is outside the repository.

1. `tr -d '\r' < tests/test_chatterbox_generation_red.py | sha256sum; python -m compileall -q . -x '(node_modules|\.git|\.venv|frontend)' && echo compiled`
2. `python -m pytest tests/test_chatterbox_generation_red.py -q --tb=short > "$TEMP/oam4-red-run1.log" 2>&1; tail -1 "$TEMP/oam4-red-run1.log"; grep -cE "^(FAILED|ERROR) " "$TEMP/oam4-red-run1.log"; grep -E "^E  " "$TEMP/oam4-red-run1.log" > "$TEMP/oam4-red-run1.e"; for p in "assert 200 == 503" "assert 200 == 400" "AssertionError: Chatterbox received no synthesize request" "AssertionError: a second generation ran while the first was generating" "Failed: DID NOT RAISE" "has no attribute 'chatterbox_time_limit_seconds'" "assert ['azure', 'google', 'mock'] == ['azure', 'ch"; do printf '%s => ' "$p"; grep -cF -- "$p" "$TEMP/oam4-red-run1.e"; done` (OAV-1, with `--tb=short` so that each failure's assertion line is in the log)
3. The same as command 2, with `run2` in place of `run1` in every file name (the second run, with no cleanup).
4. `git status --short -- audio_storage; test ! -e voice_storage && echo absent` (V4C-4)
5. `python -m pytest tests/test_inference.py tests/test_provider_registry.py tests/test_generation_history_download.py tests/test_generation_persistence_red.py tests/test_generation_delete_search_red.py -q > "$TEMP/oam4-preserved.log" 2>&1; tail -1 "$TEMP/oam4-preserved.log"`, then `git status --short -- audio_storage`. Only if it prints anything: record it, run `git checkout -- audio_storage` and `git clean -fd -- audio_storage`, and repeat `git status --short -- audio_storage`, which must print nothing (OAV-3, `Plan.md:323`).
6. `python -m pytest --collect-only -q -p no:cacheprovider --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam4-collect.log" 2>&1; tail -1 "$TEMP/oam4-collect.log"; grep -c "^tests/test_chatterbox_generation_red.py::" "$TEMP/oam4-collect.log"`
7. `git status --short` (it must list only `?? tests/test_chatterbox_generation_red.py`, plus work-item changes under `docs/.ai/chatterbox-original-app/`)
8. Process check: in PowerShell, `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId, CreationDate, CommandLine`. No process from this run may remain. The servers are threads inside each pytest process, which has exited.

### Affected Tests

- The new file only. It changes no shared test file and no production code, so no existing test's result can change.
- The preserved tests named by `Plan.md:184` (`tests/test_inference.py`, `tests/test_provider_registry.py`, `tests/test_generation_history_download.py`, `tests/test_generation_persistence_red.py`, `tests/test_generation_delete_search_red.py`) run once in command 5, because the OAM-4 success criteria require it (`Plan.md:186`). They were found as the tests that import `voice_narration.inference` (`grep -rln "voice_narration.inference" tests --include=*.py`). That search also lists `tests/test_real_model_inference.py`, a named pre-existing failure, and `tests/test_linguistic_chunking_and_controls.py`, which imports `inference.production` and the mock provider (`:39`, `:525`). Neither is in OAM-4's preserved list, and no file either one uses changes, so neither runs.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Command 1: `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948 *-` (Git Bash marks stdin with `*-`; seen in planning), then `compiled`.
- Commands 2 and 3: `56 failed in …` (the dry run took 56–84 s); `56` `FAILED` lines; class counts `35`, `12`, `5`, `1`, `1`, `1`, `1`.
- Command 4: no `git status` output, then `absent`.
- Command 5: `29 passed …`. Then `git status` is predicted to print ` M audio_storage/generation_index.json` and `?? audio_storage/generations/<date>/`, written by `tests/test_generation_history_download.py` (Plan OAR-1; seen in the dry run). After the restore, it prints nothing.
- Command 6: `138 tests collected …` (82 at OAM-3, `Plan.md:426`, plus 56), and `56`.
- Command 7: `?? tests/test_chatterbox_generation_red.py`, plus `docs/.ai/chatterbox-original-app/` changes.
- Command 8: no `python.exe` from this run.
- Preserved-behavior tests (expected to pass at RED): none in the new file. The 29 existing preserved tests in command 5 are expected to pass. They are not RED evidence for any requirement.

### Planning-Time Dry Run

This is a planning-time dry run, not milestone evidence. It ran on 2026-11-13 at HEAD `0465867`. It used two disposable copies created with `git -c core.autocrlf=false archive HEAD | tar -x` under `C:/Users/avina/AppData/Local/Temp/claude/75d22e5e94aa85f8/7c785373-79e0-4451-8aab-0a1437282b97/scratchpad/oam4/`:

- `copy/`, the unmodified code, with a temporary `git init` so `git status` could be read;
- `pcopy/`, with the scratch-only probe.

The exact test file above was placed in each copy's `tests/`. The repository was not modified.

| Step | Command (in the copy) | Result |
| --- | --- | --- |
| Compile | `python -m compileall -q . -x '(node_modules\|\.git\|\.venv\|frontend)'` | `compiled` |
| RED, unmodified (`copy/`) | `python -m pytest tests/test_chatterbox_generation_red.py -q -p no:cacheprovider --tb=short -W ignore::DeprecationWarning` | `56 failed in 56.27s`. `E` lines: `assert 200 == 503` 35, `assert 200 == 400` 12, `Chatterbox received no synthesize request` 5, `a second generation ran while the first was generating` 1, `DID NOT RAISE ReadTimeout` 1, `has no attribute 'chatterbox_time_limit_seconds'` 1, the provider-list assertion 1 |
| Isolation (`copy/`) | `git status --short` after the RED run | no output |
| Probe (`pcopy/`) | same pytest command, with a scratch `chatterbox_probe.py` and a patched `application.py`. The patch adds: `provider`/`language` validation; an `asyncio.Lock` around generation; the settings read in `InferenceState.__init__` with `chatterbox_time_limit_seconds`; the sample fetch with httpx; the token from google-auth `IDTokenCredentials.from_service_account_file(...).refresh(google.auth.transport.requests.Request())`; the call with httpx, `follow_redirects=False`, bounded by `asyncio.wait(..., timeout=limit)`; RIFF chunk parsing; OAF mapping; `chatterbox` added to the provider list | `56 passed in 76.51s`. Slowest: the time-limit-wait test 4.58 s, the default-limit test 3.92 s, the waiting test 3.91 s |
| Preserved tests (`copy/`) | `python -m pytest tests/test_inference.py tests/test_provider_registry.py tests/test_generation_history_download.py tests/test_generation_persistence_red.py tests/test_generation_delete_search_red.py -q -p no:cacheprovider` | `29 passed, 42 warnings in 1.78s`; then `git status --short` printed ` M audio_storage/generation_index.json`, `?? audio_storage/generations/2026-11-13/` |
| Collect with V3Q-3 ignores (`copy/`) | command 6 | `138 tests collected in 2.00s`; `56` |
| Collect all (`copy/`) | `python -m pytest --collect-only -q -p no:cacheprovider` | `229 tests collected` |
| Float WAV and `wave` | `wave.open(io.BytesIO(CLONED_WAV))` | `Error unknown format: 3` |
| Text lengths | `len(LONG_TEXT["en"]), len(LONG_TEXT["hi"])` | `6200 6600` |
| File hash | `sha256sum` of the final file (LF, no CR) | `4a0762e1…f948` |

Corrections from the dry run, all made before this plan was written:

- **The assertion's `aud` claim.** The first draft asserted that `aud` equals the key's `token_uri`. The probe run showed `https://oauth2.googleapis.com/token`, and google-auth's source confirms it: `_make_authorization_grant_assertion` sets that constant, and `id_token_jwt_grant` posts to `token_uri`. The assertion was removed.
- **The cross-provider waiting test.** It failed with the probe: the Chatterbox call started 3.02 s before the narration ended, which equals the narration's delay. So the main-thread request was served before the background one started. Hypothesis, not established: creating the background thread's `httpx.Client` delayed its request. The tests now create each client before its thread starts, and wait until the startup provider reports a generation in flight.
- **The probe's time limit.** It first bounded `client.post` with `asyncio.timeout(limit)`. The trickled-body OAF-5 case then answered after `4.00 s`, not about 2 s, so the cancellation did not take effect until the body had finished arriving. Its cause was not established. The probe passed once it used `asyncio.wait(..., timeout=limit)` and cancelled the task. This is a finding for OAM-5 planning, not a change to the tests (V4R-3).

Created during planning, all under the scratchpad's `oam4/` folder: `copy/`, `pcopy/`, `probe/` (`chatterbox_probe.py`, `apply_probe.py`), `head.md`, `tail.md`, the draft test file, and the logs `red1.log`–`red3.log`, `probe1.log`, `probe2.log`, `preserved.log`, `collect.log` and `collect-all.log`. Also `refc.md`, an extract of the reference contract. All are deleted once this plan is written. Pytest temporary directories went under the system pytest temp root. The scratchpad file `ref-contract.md` predates this run and was left untouched.

## Risks

- **V4R-1 Identity comparisons (security).**
  - The fake compares the token's audience with its own URL exactly (V4D-3). The test compares the assertion's `target_audience` with the URL exactly. Both use the contract's canonical form: surrounding whitespace and trailing `/` removed, one value used both for the call base and as the audience (`API-Contract.md:473`). The success tests send `CHATTERBOX_URL` padded and with a trailing `/` to prove it.
  - `iss` is compared exactly with the key's `client_email`.
  - Voice ids and `job_id` are compared exactly, as the contract states (`:495`).
  - No local service authenticates its callers (`:58`), so there is no role or ownership comparison.
- **V4R-2 Timing assertions.**
  - OAF-5 must answer in under 3.7 s (margin 1.7 s).
  - A rejected request must be answered before the 1.5 s generation ends (margin about 0.9 s).
  - Waiting order is read from `time.monotonic()` across threads of one process.
  - Under heavy load these could fail on unchanged code. Execution then stops and reports it, with no rerun until it passes (testing skill).
- **V4R-3 Deferred cancellation during a body read** (dry run, cause not established). An `asyncio.timeout` around an httpx request did not cut a trickled body at the limit. GREEN must bound the whole call, and the `OAF-5-response-incomplete-within-limit` case will show it if it does not.
- **V4R-4 The closed-port URL.** `closed_port_url()` releases a port it bound. If another process takes the port before the test connects, OAF-3 or OAF-6 sees a different answer. That is an environment failure, not RED evidence: execution stops and reports it.
- **V4R-5 Import-time side effects** (pre-existing). Importing `voice_narration.inference.application` runs `create_app()` (`:623`). That creates empty `audio_storage/` subfolders and tries the PostgreSQL at `localhost:5432` (`db.py:31`, `application.py:107-111`). The new tests' own apps use `tmp_path` and SQLite. Command 4 checks `audio_storage/`.
- **V4R-6 Undeclared libraries (Plan OAR-4).** The test imports `cryptography`, which is installed but undeclared. google-auth and requests, which the probe used, are undeclared too. A fresh environment from `requirements-dev.txt` would fail to import the test, and that would not be RED evidence. Declaring them is OAM-5's decision (`Plan.md:441`), not this milestone's.
- **V4R-7 The tests bind OAM-5** to V4D-1, V4D-2, V4D-5, V4D-6 and V4D-8. A GREEN that obtains the token another way, writes generations through other names, or omits the seam fails these tests, even if the behavior is otherwise correct.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `tests/test_chatterbox_generation_red.py`. Nothing else is changed.

## Explicitly Out of Scope

- Any production change: provider and language handling, the Chatterbox call, the settings, waiting, the provider-list entry and the seam. These belong to OAM-5 (`Plan.md:188-203`).
- Dependency declarations or version changes, including `cryptography`, google-auth and requests (V4R-6).
- Changes to the preserved tests (`Plan.md:184`) or any other existing test, and repair of the pre-existing failures.
- Voice-service and TTS-page tests (`Plan.md:185`).
- Network use beyond `127.0.0.1`, Docker, and `gcloud` (COA-16, CON-2).
- Writing to tracked `audio_storage/` files, `voice_storage/`, or the local PostgreSQL from the new tests. Committed keys or samples (CON-6): the key is generated in memory and written only under `tmp_path`.

## Human Review

Status: Superseded — not executed. The Plan revision approved by Avinash Srivastava on 2026-11-13 (`Plan.md:5`) replaced the COA-16 this plan was written for (requirements Q46–Q48) and records this plan as superseded (`Plan.md:47`, `:358`). OAM-4 is planned in `004_Implementation_Plan_OAM-4.md`. This plan's earlier approval (Avinash Srivastava, 2026-11-13, as written, including decisions V4D-1 to V4D-10) no longer authorizes execution, and none of its decisions is carried forward.
