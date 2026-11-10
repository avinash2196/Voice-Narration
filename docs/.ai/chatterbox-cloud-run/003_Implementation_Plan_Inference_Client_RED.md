# Implementation Plan — CRM-4 Inference Client RED

## Milestone

CRM-4 — Inference Client RED, work item `chatterbox-cloud-run` (`docs/.ai/chatterbox-cloud-run/Plan.md`, section "CRM-4 — Inference Client RED").

Purpose as recorded in `Plan.md`: tests that specify the inference service's cloning call to the private Chatterbox and its failure reporting. In voice cloning mode the tests verify that the request carries the stored voice sample audio and no sample path (CCR-5), carries a Google identity token for the configured credential's service account and the configured Chatterbox (CCR-7), answers each contract failure reason with its message (CCR-8, Dependency failure), is bounded by the configured time limit with a 10-minute default (CCR-9), saves and serves the generated audio locally (CCR-10 local part, RF-13), and makes no network call. The RF-14 test is updated to the contract's no-backend message, keeping its status assertion. The RF-15 test is updated to keep exercising the voice cloning path under the new request and identity attachment, with all of its telemetry assertions unchanged.

## Milestone Type

RED — as recorded in `Plan.md` ("Milestone type: RED") and in its Execution Status row "CRM-4 — Inference Client RED (RED) | Pending". `Plan.md` records no FOUNDATION milestone ("No FOUNDATION milestone exists in this Plan"). Its Prerequisite coverage for CRM-4 states that the test tooling exists and that "The RED tests isolate the Chatterbox call and the identity-token source within their own test code, making no network call". This plan proposes RED directly and changes test files only.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Approved by avinash2196 on 2026-11-09 (its Status section). Execution Status: CRM-1 Complete, CRM-2 Complete, CRM-3 Complete, CRM-4 Pending, CRM-5 Pending, CRM-6 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (accepts CCD-1–CCD-7). Authoritative predecessor delivered by CRM-1; the `Plan.md` CRM-1 row is Complete and points to it |
| `docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md` (revision 2) | Human Review: "Revision 2 approved by avinash2196 on 2026-11-09 … Executed on 2026-11-09: RED established". Source of carried-forward decisions |
| `docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md` | Human Review: "Approved by avinash2196 on 2026-11-09 ("Approve and run"). Executed on 2026-11-09: GREEN verified". Source of carried-forward decisions |
| `docs/requirements.md` (product level) | Absent — `docs/` holds only `.ai/` and `developer-setup.md` |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Not re-read; referenced by `Plan.md` and `API-Contract.md` as an unchanged constraint (approved 2026-11-08). This milestone does not test the gateway's error shape |
| `docs/developer-setup.md` | Repository documentation, not a PDD artifact; source of the test-isolation conventions and, through `Plan.md` Verification Commands, of the verification command |
| Plugin skills read: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `security`, `testing`, `python-fastapi` | Plugin guidance, not project artifacts |

`security` is applied: CRM-4 verifies CCR-7, the private-access requirement (the inference service attaches the service account's Google identity token). The identity comparisons are listed in Risks (C4-RSK-1).

## Carried-Forward Decisions

From `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2 (approved by avinash2196 on 2026-11-09):

- C2-D-6 — Real-transport check: an app served by `uvicorn` in a daemon thread on a loopback socket bound to port `0`, each request sent on its own `httpx.Client(trust_env=False)`. Reused for the stand-in backend (C4-D-1) and for the real-transport check C4-T20 (C4-D-9).
- C2-D-7 — Server errors observed as answers: the in-process client is created with `raise_server_exceptions=False`, so an application exception is reported as a `500` status assertion and not as an exception out of the client. Reused for every `TestClient` of the inference application.

From `002_Implementation_Plan_Chatterbox_Service_GREEN.md` (approved by avinash2196 on 2026-11-09):

- The executed Chatterbox behavior (CCD-1–CCD-3): a JSON body is answered `422`, a body without the `text` and `language` form fields and the `sample_audio` file part is answered `422`, and a `sample_path` part is answered `400 sample_path is not supported; send the voice sample as sample_audio` (`voice_narration/chatterbox_api/application.py` as executed at commit `467b9f2`). The stand-in Chatterbox answers the same way (C4-D-7), so the tests do not accept a request the real Chatterbox would reject.

Approved contract decisions these tests encode: CCD-1 (inference side: the stored sample bytes sent unmodified as the `sample_audio` file part), CCD-2 (no `sample_path` part), CCD-4, CCD-5, CCD-6, CCD-7 and CCD-8 (carried-over job-creation success body, `text` trimming and the `language` derivation) of `API-Contract.md`.

## Preconditions / Predecessor Evidence

- Predecessor CRM-3 (GREEN): `Plan.md` Execution Status row "CRM-3 — Chatterbox Service GREEN (GREEN) | Complete | GREEN verified on 2026-11-09 by `002_Implementation_Plan_Chatterbox_Service_GREEN.md`: C3-AC-1–C3-AC-4 met; `application.py` matches the planned content (SHA-256 `10cc955b…c54a`); 22 of 22 tests pass in two consecutive full runs". "CRM-3 Execution Evidence" records C3-V1 and C3-V2 `22 passed, 1 warning`.
- Re-observed now: `git log` shows `467b9f2 CRM-3 GREEN: Chatterbox accepts sample upload, keeps no data` as HEAD. `git show HEAD:voice_narration/chatterbox_api/application.py | sha256sum` prints `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`, the hash CRM-3 recorded. The full suite on the unmodified repository: `.\.venv\Scripts\python.exe -m pytest tests -q` → `22 passed, 1 warning in 10.01s`.
- CRM-4 is Pending in `Plan.md` Execution Status. No Implementation Plan for CRM-4 exists: the work-item folder holds `requirements.md`, `Plan.md`, `API-Contract.md`, `001_Implementation_Plan_Chatterbox_Service_RED.md` and `002_Implementation_Plan_Chatterbox_Service_GREEN.md`. This plan is numbered `003`.
- Milestone type check: `Plan.md` records CRM-4 as RED; this plan is RED. No new test passes at RED (see Planning-Time Dry Run), so the Plan's traceability matches the repository (Plan Content Rule 8).
- Pre-existing failures: none. The unmodified suite passes (22 of 22), here and in the dry-run baseline.

## Current Repository State

Inspected on 2026-11-09.

- `git rev-parse HEAD`: `467b9f2a9ef070d0f4cce774e7aab0944622a8fc`. `git status --short` printed nothing: the working tree is clean.
- Line endings: `core.autocrlf` is `true`; there is no `.gitattributes`. `git ls-files --eol` shows `tests/test_clone_flow.py` and `tests/test_ai_gateway_telemetry_red.py` as `i/lf w/crlf`, and `tests/test_chatterbox_service_red.py` as `i/lf w/lf`. Committed (LF) SHA-256: `tests/test_clone_flow.py` `fba164b7783612ad7e7efa2f9b747f5e44ef2dc5dee2ee82d48f2ec698585d64` (86 lines); `tests/test_ai_gateway_telemetry_red.py` `321b739234d579ed22be5d1920f159c744f00bddd635c9346f86fb2672f1d7d9` (78 lines).
- Inference service, `voice_narration/inference/application.py` (unchanged by this work item so far):
  - module-level settings and paths: `ROOT`, `AUDIO_ROOT`, `DB_PATH` (`:18-21`); `CHATTERBOX_API_BASE_URL` and `VOICE_CLONING_API_BASE_URL` read from the environment at import and stripped (`:23-24`); `_ensure_db()` creates the `jobs` table and runs at import (`:52-72`);
  - `_profile_lookup` reads `ROOT / "audio_storage" / "voice_profiles.db"` at call time (`:84-96`);
  - `_synthesize_via_chatterbox_api` (`:99-116`): returns `False` outside `voice_cloning` mode or with no base URL; sends a JSON body `{"text", "language", "sample_path"}` with `httpx.post(..., json=payload, timeout=120.0)`; any exception or non-`200` status returns `False`; otherwise writes `response.content` to the output path. It attaches no `Authorization` header and does not check the response's content type.
  - `create_job` (`:157-216`): trims `text`; in `voice_cloning` mode a `False` result raises `503` "Voice cloning service is unavailable. Please retry, or use Google voice narration mode." (`:178-183`); otherwise narration uses `GoogleVoiceProvider` (`:16`, `:184-186`); the job row is inserted after generation (`:188-207`), so a failure creates no job row.
  - The gateway execution passes a `503` detail through (`:363-366`).
- Google narration provider, `voice_narration/inference/providers/google.py`: `_load_local_env()` sets `GOOGLE_APPLICATION_CREDENTIALS` from the environment, the repository-root `.env`, or `service-account-key.json` at the repository root (`:13-35`). Both git-ignored files exist locally (`.gitignore:5`, `:10`); `.env` defines `GOOGLE_APPLICATION_CREDENTIALS` among other keys.
- Voices service, `voice_narration/simple_voices/application.py`: table `voice_profiles` (`:32-43`; `language TEXT NOT NULL`, `sample_path TEXT` nullable); uploaded samples are stored under `audio_storage/voices/<user_id>/<uuid>_<name>.wav` and the path recorded (`:111-116`, `:134`).
- Tests (`tests/`, no `__init__.py`, no `conftest.py`): `test_ai_gateway_red.py` (5), `test_ai_gateway_telemetry_red.py` (1, RF-15), `test_chatterbox_service_red.py` (13, CRM-2), `test_clone_flow.py` (3, RF-14 is `test_voice_cloning_returns_guidance_when_clone_backend_unavailable` at `:55-86`). RF-15 (`test_ai_gateway_telemetry_red.py:41-78`) replaces `inference_module.httpx.post` with a lambda that accepts any arguments and sets `VOICE_CLONING_API_BASE_URL` to `https://mock-chatterbox`.
- `pytest.ini`: `addopts = --strict-config --strict-markers`, `testpaths = tests`, `pythonpath = .`; no `python_files` setting, so only `test_*.py` and `*_test.py` are collected. The import mode is the default (`prepend`).
- Installed packages relevant to the tests (`pip list` in `.venv`, Python 3.13.17): `pytest 9.1.1`, `fastapi 0.162.0`, `starlette 1.10.0`, `httpx 0.28.1`, `httpcore 1.0.9`, `uvicorn 0.54.0`, `python-multipart 0.0.32`, `cryptography 50.0.2`, `google-auth 2.62.1`, `requests 2.34.2`. `requirements-dev.txt` declares `fastapi`, `uvicorn`, `python-multipart`, `pytest` and `httpx`. `cryptography` is not declared there; it is an unconditional dependency of the installed `google-auth` (`google_auth-2.62.1.dist-info/METADATA`: `Requires-Dist: cryptography>=38.0.3; python_version < "3.14"`), which the narration provider already uses (`Plan.md` RSK-6). No package named `tests` is installed in `.venv/Lib/site-packages`.
- Library behavior the tests depend on, read from the installed code:
  - `google.oauth2.service_account.IDTokenCredentials` signs an assertion whose claims include `iss` (the key's `client_email`) and `target_audience` (`service_account.py:794-818`), and `refresh` posts it to the key file's `token_uri` (`:861-870`; `token_uri` from the key info, `:681`). The grant is a form-encoded `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer` with `assertion` (`_client.py:382-418`, `:184-185`), and the returned `id_token` is decoded without verification to read `exp` (`_client.py:427-430`). A key whose `universe_domain` is not `googleapis.com` uses the IAM endpoint instead (`service_account.py:656-657`), so the test key sets `googleapis.com`.
  - `google.oauth2.id_token.fetch_id_token_credentials` falls back to a metadata-server ping when `GOOGLE_APPLICATION_CREDENTIALS` names a file whose `type` is neither `service_account` nor `impersonated_service_account` (`id_token.py:299-361`).
  - `uvicorn.Config` accepts `timeout_graceful_shutdown` (`uvicorn/config.py:236`).
  - `httpx.HTTPTransport.handle_request` is the default synchronous transport entry point (`httpx/_transports/default.py:230`).
- `docs/developer-setup.md` conventions used: "use pytest tmp_path for files … verify … effective paths and runtime configuration, and never share state across cases"; "Tests may use stdlib mocks for boundaries, but mocks must not supply the behavior being proved"; "Use HTTPX for in-process ASGI and real loopback/network contract checks; verify contract error responses through real transport"; "loopback-only dynamically allocated local ports".
- The preserved test `test_generation_uses_selected_voice_profile` calls Google TTS with the local key (Implementation Plan 001, Current Repository State), so the full suite needs network access to Google and the git-ignored local key file. This milestone does not change that test.

## Files in Scope

### Files to Create

- `tests/_chatterbox_boundary.py` — test-only stand-ins: the stand-in token endpoint and Chatterbox, the test service-account key, the network guard, and loopback server helpers. Not collected by pytest (its name does not match `test_*.py`).
- `tests/test_inference_client_red.py` — the CRM-4 tests C4-T1–C4-T20.

### Files to Modify

- `tests/test_clone_flow.py` — RF-14 test: the two message assertions become one exact comparison with CFR-1; the status assertion is kept.
- `tests/test_ai_gateway_telemetry_red.py` — RF-15 test: the any-argument `httpx.post` replacement is replaced by the stand-in backend, a test key and the network guard; every telemetry assertion is kept.

### Files to Delete

None.

## Proposed Changes

1. Create `tests/_chatterbox_boundary.py` with exactly the content under Proposed Code / Tests. It contains:
   1. Constants `SERVICE_ACCOUNT_EMAIL` (`crm4-test-invoker@crm4-test-project.iam.gserviceaccount.com`, a test identity distinct from the real account, so the tests show the identity comes from the key file), `JWT_BEARER_GRANT`, `SAMPLE_PATH_DETAIL` (the contract's `400` detail), `PROXY_VARIABLES`, `TRICKLE_PIECES` (`12`).
   2. `b64url_encode`, `b64url_decode`, `jwt_parts(token)` — split a compact JWT without verifying it.
   3. `ServiceAccountKey` with `verify(assertion) -> dict` (checks `alg` `RS256` and the RSA PKCS#1 v1.5 SHA-256 signature with the key's public half, returns the claims), and `write_service_account_key(path, token_uri, email=SERVICE_ACCOUNT_EMAIL) -> ServiceAccountKey` (generates a 2048-bit RSA key with `cryptography` and writes a `type: service_account` key file with that `token_uri` and `universe_domain: googleapis.com`).
   4. `NetworkGuard` (`blocked` list, `record`, `assert_no_network`) and `isolate_network(monkeypatch) -> NetworkGuard`: deletes the proxy variables, and replaces `socket.getaddrinfo`, `socket.socket.connect` and `socket.socket.connect_ex` with versions that record and refuse any host that is not loopback (`localhost`, `127.0.0.0/8`, `::1`).
   5. `FakeBackend`: a FastAPI app with `POST /token` (records the form, optional delay, `token_status` other than `200` → `{"error": "invalid_grant", …}`, otherwise issues a new unsigned-for-test JWT whose `aud` is the assertion's `target_audience`, and records `{"fields", "id_token"}` in `token_grants`) and `POST /v1/synthesize` (records `authorization`, `content_type` and every multipart part as `{"name", "is_file", "content"}`, then answers in the order given in C4-D-7). Configurable per test: `status`, `media_type`, `body`, `delay_seconds`, `trickle_seconds`, `token_status`, `token_delay_seconds`. `audio` is a unique WAV-like byte string per instance.
   6. `running_app(app)` (C2-D-6 pattern, `log_level="warning"`, `lifespan="off"`, plus `timeout_graceful_shutdown=5`, C4-D-1), `running_fake_backend()`, `closed_loopback_url()`, and `TruncatingServer` (a raw-socket loopback server that reads the whole request, answers `200 audio/wav` with `Content-Length: 1000` and 12 body bytes, and closes the connection).
2. Create `tests/test_inference_client_red.py` with exactly the content under Proposed Code / Tests. It contains:
   1. Constants: `INFERENCE_MODULE`, `INFERENCE_PACKAGE`, `JOBS` (`/inference/jobs`), `NARRATION_AUDIO` (the stand-in narration audio of C4-T6), `SUFFIX` and `CFR1`–`CFR9` (the contract's `detail` strings, with `{n}` and `{status}` for CFR-5, CFR-7 and CFR-8), `VOICE_PROFILES_SCHEMA` (a scratch copy of the voices table, `voice_narration/simple_voices/application.py:32-43`), and the sentinels `UNSET` (setting not set) and `DEFAULT` (harness default).
   2. `_Harness` with `load(base_url=, chatterbox_base_url=, timeout=, credentials=)` (C4-D-4), `add_profile(language=, sample_path=)`, `create_job(profile_id, text=, mode=)`, `job_count()`, `generated_files()`, `assert_cloning_failed(response, detail)` (`503`, body exactly `{"detail": detail}`, no job row, no generated file), `assert_job_saved(response, audio)` (`200`, completed body, audio served at the job's audio URL equals `audio`, stored file under the test's `audio_storage`), and `token_for(call)` (finds the issued token the call carries).
   3. Fixture `inference(monkeypatch, tmp_path)`: installs the network guard, starts the stand-in backend, writes the test key, yields a `_Harness`. Helpers `_part_names(call)` (sorted part names of a recorded call) and `_part(call, name)` (the one part with that name).
   4. Twenty tests, C4-T1–C4-T20 (table below), 49 test cases in all.
3. Modify `tests/test_clone_flow.py` (RF-14) as in the unified diff: replace `assert "Please retry" in detail` and `assert "Google voice narration mode" in detail` with `assert detail == "Voice cloning failed: no voice cloning service is configured. Please retry, or use Google voice narration mode."`. `assert response.status_code == 503, response.text` is kept. No other line changes.
4. Modify `tests/test_ai_gateway_telemetry_red.py` (RF-15) as in the unified diff:
   1. add `from tests._chatterbox_boundary import isolate_network, running_fake_backend, write_service_account_key`;
   2. the test takes `tmp_path` as well as `monkeypatch`; `_FakeResponse` and the `httpx.post` replacement are removed;
   3. it installs the network guard, runs the stand-in backend, writes a test key, sets `GOOGLE_APPLICATION_CREDENTIALS` to it with `monkeypatch.setenv`, and sets `inference_module.VOICE_CLONING_API_BASE_URL` to the stand-in's base URL (the same module attribute the test set before);
   4. the model enablement, profile creation and gateway request are unchanged, indented into the `with` block;
   5. the five telemetry assertions and the `202` status assertion are unchanged; two assertions are added at the end: `assert len(chatterbox.synthesize_calls) == 1` (the voice cloning path reached Chatterbox) and `guard.assert_no_network()`.

| ID | Test (cases) | Verifies (contract rule; requirement) |
| --- | --- | --- |
| C4-T1 | `test_cloning_request_carries_sample_audio_and_identity_token` (1) | One `POST <base>/v1/synthesize`, `multipart/form-data`, exactly the parts `text` (trimmed), `language` (`hi` from `hi-IN`) and file part `sample_audio` holding the stored sample's exact bytes (binary, including non-UTF-8 bytes), and no `sample_path` part; `Authorization: Bearer <token>` with a token obtained by the ID-token grant (`grant_type` jwt-bearer), whose assertion is signed by the configured key, `iss` = the key's `client_email`, `target_audience` = the base URL in effect; `200` with the carried-over body; the audio is saved under the local `audio_storage`, recorded on one job row and served at `audio_url` (CCD-1, CCD-2, CCD-4, CCD-7, CCD-8; CCR-5, CCR-7, CCR-10 local part, RF-13) |
| C4-T2 | `test_cloning_language_part_follows_profile_language` (3) | `language` part is the profile language before the first `-`, lowercased; `en` when the profile has no language (Inference Service Voice Cloning Call, carried over under the new request; CCR-5) |
| C4-T3 | `test_base_url_in_effect_is_call_target_and_token_audience` (1) | `CHATTERBOX_API_BASE_URL` is used when `VOICE_CLONING_API_BASE_URL` is not set; `VOICE_CLONING_API_BASE_URL` wins when set; surrounding whitespace is removed and the result is both the call target and the token audience (Settings rows 1–2, CCD-4, CCD-7; CCR-7) |
| C4-T4 | `test_no_configured_base_url_answers_cfr1` (3) | Neither setting, `VOICE_CLONING_API_BASE_URL` empty with `CHATTERBOX_API_BASE_URL` set (no fallback), or whitespace only → `503` CFR-1; no Chatterbox call (CFR-1, Settings rows 1–2; CCR-8) |
| C4-T5 | `test_invalid_time_limit_answers_cfr2` (7) | `0`, `00`, `-5`, `+5`, `10.5`, `ten`, `1 0` → `503` CFR-2; no Chatterbox call (CFR-2, Settings row 3; CCR-9) |
| C4-T6 | `test_invalid_time_limit_leaves_narration_unaffected` (1) | Positive first: with `ten`, cloning answers CFR-2; then narration (no `mode`) still completes and is saved, using a stand-in Google provider (Settings row 3 "Narration is unaffected"; CCR-9, CCR-2) |
| C4-T7 | `test_unreadable_voice_sample_answers_cfr3` (3) | Profile with no `sample_path`, a missing file, or a directory → `503` CFR-3; no Chatterbox call (CFR-3; CCR-8) |
| C4-T8 | `test_identity_token_unavailable_answers_cfr4` (4) | Key file missing, not JSON, not a service-account key, or the token request refused (`400`) → `503` CFR-4; no Chatterbox call (CFR-4; CCR-7, CCR-8) |
| C4-T9 | `test_time_limit_bounds_wait_for_chatterbox_response` (1) | Limit `1`, Chatterbox answers after 2.5 s → `503` CFR-5 with `1`, in under 2.2 s (CFR-5, CCD-6 "including any wait at Chatterbox"; CCR-9) |
| C4-T10 | `test_time_limit_bounds_complete_response_not_each_read` (1) | Limit `1`, Chatterbox sends its body in 12 pieces over 3 s (each read well under the limit) → `503` CFR-5, in under 2.5 s (CCD-6 "until the complete response"; CCR-9) |
| C4-T11 | `test_identity_token_time_is_not_counted_toward_time_limit` (1) | Limit `1`, token endpoint answers after 1.5 s, Chatterbox at once → `200`, saved (Voice Cloning Call "Obtaining the identity token … is not counted"; CCR-9) |
| C4-T12 | `test_time_limit_in_effect_is_reported_when_reached` (5) | Not set, empty, whitespace → limit `600`; `  7  `, `007` → `7`: when the transport times out, `503` CFR-5 names that limit (Settings row 3 default and form, CFR-5 `<N>`; CCR-9 10-minute default) |
| C4-T13 | `test_time_limit_setting_is_read_at_service_start` (1) | Started with `ten`, then the variable is changed to `5` without a restart → still CFR-2 (Settings "read once, when the service starts"; CCD-6) |
| C4-T14 | `test_unreachable_chatterbox_answers_cfr6` (2) | Connection refused; connection lost before the full response (request received, body truncated) → `503` CFR-6 (CFR-6; CCR-8 "cannot connect") |
| C4-T15 | `test_access_denied_answers_cfr7` (2) | `401`, `403` → `503` CFR-7 with the status (CFR-7; CCR-8 "access denied") |
| C4-T16 | `test_chatterbox_error_status_answers_cfr8` (6) | `400`, `422`, `429`, `500`, `503`, `504` → `503` CFR-8 with the status (CFR-8; CCR-8 "Chatterbox error") |
| C4-T17 | `test_success_status_without_audio_answers_cfr9` (4) | `200` with an empty `audio/wav` body, a JSON body, no `Content-Type`, or `text/plain` → `503` CFR-9 (CFR-9, Voice Cloning Call success rule; CCR-8 "bad response") |
| C4-T18 | `test_audio_wav_media_type_is_matched_case_insensitively_ignoring_parameters` (1) | `Audio/WAV; rate=24000` is a success and is saved (Contract-Wide Rules, matching semantics) |
| C4-T19 | `test_failure_reasons_are_checked_in_contract_order` (1) | With several causes present, the first in order wins: CFR-1 before CFR-2, CFR-2 before CFR-3, CFR-3 before CFR-4, CFR-4 before a connection attempt (CFR-6); no Chatterbox call ("checked in this order"; CCD-5) |
| C4-T20 | `test_cloning_failure_answer_over_real_transport` (1) | Over a real loopback HTTP connection to the inference service under `uvicorn`: `503` CFR-7 (`403`), no job row (contract error answer through real transport, `testing` skill, `docs/developer-setup.md`; CCR-8) |
| RF-14 | `tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable` (updated) | `503` kept; `detail` is exactly CFR-1 (CFR-1 replaces RF-14's baseline message, CCD-5) |
| RF-15 | `tests/test_ai_gateway_telemetry_red.py::test_gateway_execution_returns_non_placeholder_telemetry` (updated) | The gateway's voice cloning execution reaches the stand-in Chatterbox once, with the new request and identity token, and keeps all of its telemetry assertions (RF-15 preserved row) |

Every test in `tests/test_inference_client_red.py`, and the updated RF-15 test, ends with `assert_no_network()` (Plan CRM-4 scope "every test makes no network call"). Every failure test also asserts that no job row and no audio file were created ("A cloning failure creates no job record and no audio file"), after its positive `detail` assertion.

### Contract rule coverage (`API-Contract.md`: Inference Service Voice Cloning Call, Inference Job Creation, Inference Service Settings, Contract-Wide Rules)

| Normative rule | Covered by |
| --- | --- |
| Call target `<base URL>/v1/synthesize`, base URL with surrounding whitespace removed and otherwise unchanged | C4-T1, C4-T3, C4-T12 (URL asserted) |
| `text` part: the job's text, trimmed | C4-T1 |
| `language` part: profile language before the first `-`, lowercased; `en` when none | C4-T1, C4-T2 |
| `sample_audio`: the complete, unmodified bytes of the file at the stored `sample_path`, as a file part | C4-T1, C4-T2 |
| No `sample_path` part | C4-T1 (exact part list) |
| `Authorization: Bearer <token>`: identity token for the service account of the key named by `GOOGLE_APPLICATION_CREDENTIALS`, audience = base URL in effect | C4-T1, C4-T3 |
| Time limit spans sending the request to receiving the complete response, including waiting at Chatterbox | C4-T9, C4-T10 |
| Obtaining the identity token is not counted | C4-T11 |
| Success: `200`, media type `audio/wav` case-insensitive with parameters ignored, non-empty body; body saved as the job's audio | C4-T1, C4-T18 (positive), C4-T17 (negative) |
| CFR-1–CFR-9 conditions and full `detail` strings, `<N>` and `<status>` filled in | C4-T4–C4-T17, C4-T20, RF-14 |
| Failure reasons checked in order | C4-T19 (CFR-1 → CFR-4 and CFR-4 before connecting); CFR-5–CFR-9 are mutually exclusive outcomes of one call |
| A cloning failure creates no job record and no audio file | every failure test, through `assert_cloning_failed` |
| Failure body `{"detail": "<string>"}` | every failure test (whole-body equality) |
| Success body (carried over): `id`, `status` `completed`, `audio_url`, `download_url`, `voice_profile_id`, `voice_name`; audio served at `audio_url` | C4-T1 (all fields), `assert_job_saved` (status, `audio_url`, served audio) |
| `VOICE_CLONING_API_BASE_URL` precedence over `CHATTERBOX_API_BASE_URL`; set-but-blank gives an empty base URL (no fallback) | C4-T3, C4-T4 |
| `VOICE_CLONING_TIMEOUT_SECONDS`: digits only, whitespace removed, at least `1`; not set, empty or whitespace → `600`; any other value → CFR-2; narration unaffected | C4-T5, C4-T6, C4-T12 |
| Settings read once at service start | C4-T13 (time limit); the base URL settings are read at import in the baseline (`application.py:23-24`) and every test sets them before importing |
| Error answer verified through real transport | C4-T20 |

Not tested, with reason:

- `GOOGLE_APPLICATION_CREDENTIALS` located from the repository-root `.env` or `service-account-key.json` when the variable is not set: testing it would need repository-root files to be created, changed or removed, and the developer's real `.env` and key exist there. The location rule is the narration provider's existing one (`google.py:13-35`), carried over by CCD-7. Every test sets the variable explicitly.
- CFR-6 by name resolution or TLS failure: the contract lists them as examples of "any transport failure". Name resolution would need DNS, which the network guard blocks, and TLS would need a certificate fixture that no approved artifact names. Connection refused and connection lost (C4-T14) cover the class.
- Cloud Run's own `401`/`403` enforcement and the real Google-signed token: a property of the deployment, verified at Final Review of CRM-6's document (`Plan.md` Final Acceptance Criteria, AC-CCR-4). The tests verify the token request and the header the inference service sends.
- "No setting disables" the identity token: no such setting exists, and C4-T1, C4-T3, C4-T11, C4-T18 and RF-15 show the token on every successful call.
- The gateway's `503 MODEL_UNAVAILABLE` pass-through of the new messages: an unchanged constraint (`voice_narration/inference/application.py:363-366`) that `Plan.md` does not assign to CRM-4.
- Carried-over job-creation validations (`422`, `400`, `404`, `403`) and narration-mode behavior beyond C4-T6: unchanged, not in CRM-4 scope; the narration test is preserved by CRM-5's full run.
- No upper bound on `VOICE_CLONING_TIMEOUT_SECONDS`: the contract defines none, so there is nothing to test.

### Test-design decisions for review

These choices bind the GREEN milestone CRM-5, which may not change these tests.

- C4-D-1 — Boundaries isolated by loopback stand-ins over real HTTP. Chatterbox and the token endpoint are a FastAPI app under `uvicorn` on a dynamically allocated loopback port (C2-D-6). Why: the tests then observe the request the inference service actually sends — its parts, headers and timing — whatever HTTP client code CRM-5 writes. Alternative: replace `httpx.post`, as RF-15 did. Not chosen: it would fix CRM-5's call signature and cannot observe multipart parts or time limits. Alternative: `httpx.MockTransport`. Not chosen: it requires the client to be built with a transport the test hands over. The server is started with `timeout_graceful_shutdown=5` (`uvicorn/config.py:236`): after C4-T9's client stops waiting, the stand-in's delayed answer is still running, and `uvicorn` waits for running tasks when it shuts down. Five seconds bounds that wait; the dry run measured 1.60 s for C4-T9's teardown.
- C4-D-2 — Identity token obtained through the key file's token endpoint. Each test writes a service-account key with a new RSA key and `token_uri` on the stand-in. The test verifies the ID-token grant (`grant_type` jwt-bearer), the RS256 signature by that key, `iss` = the key's `client_email`, `target_audience` = the base URL in effect, and that the `Authorization` header carries exactly the token the endpoint issued. Consequence: CRM-5 obtains the token with the service-account ID-token grant at the key file's `token_uri`, as `google.oauth2.service_account.IDTokenCredentials` does (Current Repository State). It cannot use the IAM `generateIdToken` endpoint or the metadata server, because neither is reachable without the network. Alternative: replace a token function in the inference module. Not chosen: no such function exists, and the replacement would supply the token value being proved (`testing` skill).
- C4-D-3 — Network guard fails the test on any non-loopback access. Consequence: a CRM-5 that, for a key file that is not a service-account key, falls back to the metadata server would fail C4-T8 `not-a-service-account-key`. `google.oauth2.id_token.fetch_id_token` does that fallback (`id_token.py:299-361`). That it would fail this case is read from that code, not run. The contract names the key file as the token source (CCD-7) and not the metadata server. Alternative: block without failing. Not chosen: the Plan's CRM-4 scope requires "every test makes no network call", and a blocked attempt would otherwise be silent.
- C4-D-4 — A fresh import of the inference application per configuration. `load()` sets the four settings with `monkeypatch`, asserts they are in effect, removes `voice_narration.inference.application` from `sys.modules` and imports it again, as at service start. It then points the module's `ROOT`, `AUDIO_ROOT` and `DB_PATH` at the test's `tmp_path`, reruns `_ensure_db()`, and asserts the effective `DB_PATH`. `monkeypatch` restores `sys.modules` and the package attribute at teardown, so other test files keep the original module. Consequence: CRM-5 keeps the existing names `ROOT`, `AUDIO_ROOT`, `DB_PATH`, `_ensure_db`, `GoogleVoiceProvider` (C4-T6) and `VOICE_CLONING_API_BASE_URL` (RF-14, RF-15) (`application.py:16`, `:18-21`, `:24`, `:52`). Alternative: `importlib.reload`. Not chosen: it changes the module object the other test files share. Alternative: set a time-limit attribute directly. Not chosen: it would fix a name the contract does not define.
- C4-D-5 — Time-limit checks. Real time with limit `1`: delayed headers (C4-T9), a trickled body (C4-T10) and a delayed token (C4-T11). The default `600` and the setting's accepted forms are checked through CFR-5's `<N>` (C4-T12): the test replaces `httpx.HTTPTransport.handle_request` so that the call to `/v1/synthesize` raises `httpx.ReadTimeout`; any other request goes through. Consequence: CRM-5 sends the call through httpx's default synchronous transport, as the baseline's `httpx.post` does, and answers an httpx timeout as CFR-5 with the limit in effect. Alternative: wait 600 s. Not chosen: impractical. Alternative: assert `request.extensions["timeout"]`. Not chosen: it would fix httpx's per-request timeout as the mechanism, which C4-T10 shows is not enough on its own.
- C4-D-6 — "Read at service start" checked for the new setting only (C4-T13). The base URL settings are already read at import (`application.py:23-24`, carried over), and the tests set every setting before the import.
- C4-D-7 — Stand-in Chatterbox answers in this order: a forced `401`/`403` (as Cloud Run); `401` unless `Authorization` carries an issued token (as Cloud Run); any other forced status; `422` unless the body has the `text` and `language` form fields and the `sample_audio` file part; `400` for a `sample_path` part (both as CRM-3's Chatterbox); otherwise the configured delay, then the configured body. Consequence at RED: the baseline's JSON request without a token gets `401`, so each test fails on the inference service's answer, not on the stand-in. Alternative: a stand-in that accepts any request. Not chosen: C4-T1 would then not show that the request is one the contracted Chatterbox and Cloud Run accept.
- C4-D-8 — Shared test helper module `tests/_chatterbox_boundary.py`, imported as `tests._chatterbox_boundary`. The import resolves through `pythonpath = .` in `pytest.ini`, because `tests/` has no `__init__.py` and no other `tests` package is installed; the dry run confirms it. The file is not collected. This plan reads the Plan's exclusion "no dependency, build or test-infrastructure change" as covering dependencies, pytest configuration, plugins and `conftest.py`, not test code shared by two test files, which `Plan.md` Prerequisite coverage describes as "their own test code". The reviewer confirms or corrects that reading. Alternative: copy the stand-ins into the RF-15 test file. Not chosen: about 150 duplicated lines. Alternative: import them from `test_inference_client_red.py`. Not chosen: that imports one test module from another.
- C4-D-9 — Real-transport check of one contract error answer (C4-T20). It serves the inference application under `uvicorn` on a loopback port and sends one request on its own `httpx.Client(trust_env=False)` (C2-D-6). One error answer is checked, as the `testing` skill requires "at least once".
- C4-D-10 — Timing thresholds: C4-T9 `elapsed < 2.2` s for a 1 s limit against a 2.5 s delay; C4-T10 `elapsed < 2.5` s against a 3 s trickle in 0.25 s pieces; C4-T11 `elapsed >= 1.5` s. They separate "stopped at the limit" from "waited for the full answer" with at least 0.3 s margin either side. The dry-run probe measured 1.17 s and 1.35 s for C4-T9 and C4-T10.
- C4-D-11 — Updated existing tests. RF-14: only the message assertions change, to the exact CFR-1 string; the status assertion stays. Exact equality is stricter than the two `in` checks it replaces. RF-15: the telemetry and `202` assertions are unchanged. Two assertions are added: one Chatterbox call (proves the voice cloning path, not narration, produced the answer) and no network access. No assertion is weakened or removed (`Plan.md` CRM-4 exclusions).

No dependency, plugin, marker or configuration setting is introduced. Every import is from the standard library, from packages declared in `requirements-dev.txt` (`fastapi`, `httpx`, `pytest`, `uvicorn`; `python-multipart` is what `request.form()` uses), from `starlette` (FastAPI's dependency), from `cryptography` (installed as an unconditional dependency of `google-auth`, not declared in `requirements-dev.txt`; `Plan.md` RSK-6 asks that this be stated), or from the application packages under test. The tests do not import `google-auth`.

## Proposed Code / Tests

### `tests/_chatterbox_boundary.py` — complete content (397 lines, LF, ASCII, SHA-256 `7ef1a7bd05e3a273faf76eebca9973984000ff1ad5f408e550784865ca710608`)

```python
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
```

### `tests/test_inference_client_red.py` — complete content (580 lines, LF, ASCII, SHA-256 `fff78d051a09ec355ab465e8c2751b7c53d627d2b7d0139a8273c4691798314e`)

```python
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
```

### `tests/test_clone_flow.py` — unified diff against the committed file

Against `git show HEAD:tests/test_clone_flow.py` (LF, SHA-256 `fba164b7783612ad7e7efa2f9b747f5e44ef2dc5dee2ee82d48f2ec698585d64`). Result: 88 lines, LF, SHA-256 `84416efa942f57fd1675d4955f8e7546e6ff3c782978ee15d248d6c85870edb8`.

```diff
--- a/tests/test_clone_flow.py
+++ b/tests/test_clone_flow.py
@@ -82,5 +82,7 @@
 
     assert response.status_code == 503, response.text
     detail = response.json()["detail"]
-    assert "Please retry" in detail
-    assert "Google voice narration mode" in detail
+    assert detail == (
+        "Voice cloning failed: no voice cloning service is configured. "
+        "Please retry, or use Google voice narration mode."
+    )
```

### `tests/test_clone_flow.py` — complete final content

```python
from fastapi.testclient import TestClient

import voice_narration.inference.application as inference_module
from voice_narration.inference.application import app as inference_app
from voice_narration.simple_voices.application import app as voices_app


def test_voice_enrollment_creates_profile():
    client = TestClient(voices_app)
    payload = {
        "name": "Test Clone",
        "user_id": "test-user",
        "language": "en-US",
        "consent": "I consent",
    }
    audio = ("sample.wav", b"RIFF....fake-wave", "audio/wav")
    response = client.post("/voices", data=payload, files={"audio_file": audio})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Test Clone"
    assert body["status"] == "approved"


def test_generation_uses_selected_voice_profile():
    voice_client = TestClient(voices_app)
    voice_response = voice_client.post(
        "/voices",
        data={
            "name": "Generation Test",
            "user_id": "generation-user",
            "language": "en-US",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    voice_id = voice_response.json()["id"]

    infer_client = TestClient(inference_app)
    response = infer_client.post(
        "/inference/jobs",
        json={
            "text": "Hello from the test suite",
            "voice_profile_id": voice_id,
            "voice_name": "Generation Test",
            "user_id": "generation-user",
        },
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "completed"
    assert "audio_url" in body


def test_voice_cloning_returns_guidance_when_clone_backend_unavailable(monkeypatch):
    voice_client = TestClient(voices_app)
    voice_response = voice_client.post(
        "/voices",
        data={
            "name": "Clone Backend Check",
            "user_id": "clone-backend-user",
            "language": "en-US",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    voice_id = voice_response.json()["id"]

    monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", "")

    infer_client = TestClient(inference_app)
    response = infer_client.post(
        "/inference/jobs",
        json={
            "text": "Please clone this voice",
            "voice_profile_id": voice_id,
            "voice_name": "Clone Backend Check",
            "user_id": "clone-backend-user",
            "mode": "voice_cloning",
        },
    )

    assert response.status_code == 503, response.text
    detail = response.json()["detail"]
    assert detail == (
        "Voice cloning failed: no voice cloning service is configured. "
        "Please retry, or use Google voice narration mode."
    )
```

### `tests/test_ai_gateway_telemetry_red.py` — unified diff against the committed file

Against `git show HEAD:tests/test_ai_gateway_telemetry_red.py` (LF, SHA-256 `321b739234d579ed22be5d1920f159c744f00bddd635c9346f86fb2672f1d7d9`). Result: 80 lines, LF, SHA-256 `ab285fd7f808bfa2358ef80c4ca6ba6e68afbbfc154d07c005f9d20455032f88`.

```diff
--- a/tests/test_ai_gateway_telemetry_red.py
+++ b/tests/test_ai_gateway_telemetry_red.py
@@ -1,6 +1,7 @@
 from fastapi.testclient import TestClient
 
 import voice_narration.inference.application as inference_module
+from tests._chatterbox_boundary import isolate_network, running_fake_backend, write_service_account_key
 from voice_narration.inference.application import app as inference_app
 from voice_narration.simple_voices.application import app as voices_app
 
@@ -38,34 +39,33 @@
     return response.json()
 
 
-def test_gateway_execution_returns_non_placeholder_telemetry(monkeypatch):
-    class _FakeResponse:
-        status_code = 200
-        content = b"RIFF....fake-wave-from-chatterbox"
-
-    monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", "https://mock-chatterbox")
-    monkeypatch.setattr(inference_module.httpx, "post", lambda *args, **kwargs: _FakeResponse())
-
-    infer_client = TestClient(inference_app)
-    _enable_model(infer_client)
-    profile = _create_profile()
-
-    response = infer_client.post(
-        "/ai-gateway/v1/executions",
-        json={
-            "request_id": "44444444-4444-4444-4444-444444444444",
-            "mode": "voice_cloning",
-            "text": "Namaste telemetry check",
-            "language": "hi",
-            "voice_profile_id": profile["id"],
-            "model_hint": "chatterbox-multilingual-v3",
-            "controls": {"pause_strength": 0.5, "speech_pace": 1.0},
-            "idempotency_key": "telemetry-red-1",
-            "metadata": {"caller": "telemetry-red"},
-            "user_id": profile["user_id"],
-            "voice_name": profile["name"],
-        },
-    )
+def test_gateway_execution_returns_non_placeholder_telemetry(monkeypatch, tmp_path):
+    guard = isolate_network(monkeypatch)
+    with running_fake_backend() as chatterbox:
+        key = write_service_account_key(tmp_path / "service-account.json", chatterbox.token_uri)
+        monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(key.path))
+        monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", chatterbox.base_url)
+
+        infer_client = TestClient(inference_app)
+        _enable_model(infer_client)
+        profile = _create_profile()
+
+        response = infer_client.post(
+            "/ai-gateway/v1/executions",
+            json={
+                "request_id": "44444444-4444-4444-4444-444444444444",
+                "mode": "voice_cloning",
+                "text": "Namaste telemetry check",
+                "language": "hi",
+                "voice_profile_id": profile["id"],
+                "model_hint": "chatterbox-multilingual-v3",
+                "controls": {"pause_strength": 0.5, "speech_pace": 1.0},
+                "idempotency_key": "telemetry-red-1",
+                "metadata": {"caller": "telemetry-red"},
+                "user_id": profile["user_id"],
+                "voice_name": profile["name"],
+            },
+        )
 
     assert response.status_code == 202, response.text
     body = response.json()
@@ -76,3 +76,5 @@
     assert isinstance(usage["cost_estimate_usd"], str)
     assert usage["cost_estimate_usd"].count(".") == 1
     assert usage["runtime_class"] == "self_hosted"
+    assert len(chatterbox.synthesize_calls) == 1
+    guard.assert_no_network()
```

### `tests/test_ai_gateway_telemetry_red.py` — complete final content

```python
from fastapi.testclient import TestClient

import voice_narration.inference.application as inference_module
from tests._chatterbox_boundary import isolate_network, running_fake_backend, write_service_account_key
from voice_narration.inference.application import app as inference_app
from voice_narration.simple_voices.application import app as voices_app


def _enable_model(client: TestClient) -> None:
    approval_payload = {
        "model_version": "v3",
        "license_evidence_uri": "https://example.test/license",
        "weights_evidence_uri": "https://example.test/weights",
        "output_use_evidence_uri": "https://example.test/output-use",
        "runtime_class": "self_hosted",
        "languages_supported": ["hi", "en"],
        "approved_by": "pytest",
    }
    approve = client.post("/ai-gateway/v1/models/chatterbox-multilingual-v3/approvals", json=approval_payload)
    assert approve.status_code == 201, approve.text

    enable = client.post("/ai-gateway/v1/models/chatterbox-multilingual-v3/enable", json={"model_version": "v3"})
    assert enable.status_code == 200, enable.text


def _create_profile() -> dict:
    voice_client = TestClient(voices_app)
    response = voice_client.post(
        "/voices",
        data={
            "name": "Telemetry Test",
            "user_id": "telemetry-user",
            "language": "hi-IN",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_gateway_execution_returns_non_placeholder_telemetry(monkeypatch, tmp_path):
    guard = isolate_network(monkeypatch)
    with running_fake_backend() as chatterbox:
        key = write_service_account_key(tmp_path / "service-account.json", chatterbox.token_uri)
        monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(key.path))
        monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", chatterbox.base_url)

        infer_client = TestClient(inference_app)
        _enable_model(infer_client)
        profile = _create_profile()

        response = infer_client.post(
            "/ai-gateway/v1/executions",
            json={
                "request_id": "44444444-4444-4444-4444-444444444444",
                "mode": "voice_cloning",
                "text": "Namaste telemetry check",
                "language": "hi",
                "voice_profile_id": profile["id"],
                "model_hint": "chatterbox-multilingual-v3",
                "controls": {"pause_strength": 0.5, "speech_pace": 1.0},
                "idempotency_key": "telemetry-red-1",
                "metadata": {"caller": "telemetry-red"},
                "user_id": profile["user_id"],
                "voice_name": profile["name"],
            },
        )

    assert response.status_code == 202, response.text
    body = response.json()
    usage = body["usage"]

    assert usage["latency_ms"] > 0
    assert usage["compute_ms"] > 0
    assert isinstance(usage["cost_estimate_usd"], str)
    assert usage["cost_estimate_usd"].count(".") == 1
    assert usage["runtime_class"] == "self_hosted"
    assert len(chatterbox.synthesize_calls) == 1
    guard.assert_no_network()
```

## Execution Steps

1. Confirm this plan's Human Review status records approval.
2. Run `git status --short` and confirm no change to tracked files under `voice_narration/` or `tests/`. Confirm `git diff --quiet HEAD -- tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py voice_narration/` exits `0`, and that `tests/_chatterbox_boundary.py` and `tests/test_inference_client_red.py` do not exist. If any check fails, stop and report.
3. Create `tests/_chatterbox_boundary.py` and `tests/test_inference_client_red.py`, and replace the content of `tests/test_clone_flow.py` and `tests/test_ai_gateway_telemetry_red.py`, each with exactly its complete content above, with LF line endings (ASCII).
4. Run C4-V5 and confirm each SHA-256 matches. Run `git diff -- tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py` and confirm it shows exactly the changed lines of the two unified diffs above. Git may print a warning that LF will be replaced by CRLF, because `core.autocrlf` is `true`; that warning is expected and changes no content. If a hash differs, stop and report.
5. Run C4-V1, then C4-V2 (repeat, no cleaning), then C4-V3.
6. Run C4-V4.
7. Record the evidence in `Plan.md` below the Execution Status table and update only the CRM-4 row, as the PDD workflow requires.

## Acceptance / Completion Criteria

- C4-AC-1: the four files in scope have exactly the content in Proposed Code / Tests (SHA-256: `tests/_chatterbox_boundary.py` `7ef1a7bd05e3a273faf76eebca9973984000ff1ad5f408e550784865ca710608`, `tests/test_inference_client_red.py` `fff78d051a09ec355ab465e8c2751b7c53d627d2b7d0139a8273c4691798314e`, `tests/test_clone_flow.py` `84416efa942f57fd1675d4955f8e7546e6ff3c782978ee15d248d6c85870edb8`, `tests/test_ai_gateway_telemetry_red.py` `ab285fd7f808bfa2358ef80c4ca6ba6e68afbbfc154d07c005f9d20455032f88`). No other file is created, modified or deleted, apart from this milestone's Execution Status update in `Plan.md` and this plan's Human Review status. In particular, no production file, `tests/test_chatterbox_service_red.py`, `tests/test_ai_gateway_red.py`, `requirements-dev.txt`, `pytest.ini`, `conftest.py` or other configuration changes.
- C4-AC-2: pytest collects 71 tests with no collection, import or fixture-setup error: the 22 existing tests plus the 49 cases of C4-T1–C4-T20.
- C4-AC-3: each of the 49 new cases and the 2 updated tests (RF-14, RF-15) fails with an `AssertionError` raised by its own assertions or by the `_Harness` assertions it calls. The failure class: the inference service's answer differs from the contract's, because the multipart request with the voice sample, the identity token, the time limit and the per-reason failure messages are missing (the unmodified service sends a JSON body without a token and answers every cloning failure with its single generic message). Not valid RED evidence: `ImportError`/`ModuleNotFoundError`, fixture errors, `RuntimeError: CRM-4 test server did not start`, an httpx transport error raised in test code, the network guard's `non-loopback network access was attempted`, or a pytest timeout.
- C4-AC-4: the 20 other tests pass: the 13 tests of `tests/test_chatterbox_service_red.py`, the 5 tests of `tests/test_ai_gateway_red.py`, `test_voice_enrollment_creates_profile` and `test_generation_uses_selected_voice_profile`.
- C4-AC-5: a second full run without cleaning gives the same result as the first: the same 51 tests fail for the same class of reason, and the same 20 pass.

## Verification

### Commands

Run from the repository root (Windows, the Plan's Verification Commands; on Linux use `.venv/bin/python`):

- C4-V1: `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C4-V2: `.\.venv\Scripts\python.exe -m pytest tests -ra` (second run, no cleaning between runs; required because the tests write files and databases, override environment variables and `sys.modules`, and patch `socket` and `httpx`)
- C4-V3: `.\.venv\Scripts\python.exe -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable tests/test_ai_gateway_telemetry_red.py -q --tb=line` (each failing test's first failing assertion, for C4-AC-3)
- C4-V4: `git status --short`
- C4-V5: `sha256sum tests/_chatterbox_boundary.py tests/test_inference_client_red.py tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py` (Git Bash or Linux), or `certutil -hashfile <file> SHA256` for each file (Windows)

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- C4-V1 and C4-V2: exit code `1`; `collected 71 items`; summary `51 failed, 20 passed, 1 warning` (the existing `StarletteDeprecationWarning` from `fastapi/testclient.py`). The `FAILED` lines name the 49 cases of `tests/test_inference_client_red.py`, `tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable` and `tests/test_ai_gateway_telemetry_red.py::test_gateway_execution_returns_non_placeholder_telemetry`. No `ERROR` line, and the output does not contain `did not start`, `network access was attempted`, `ModuleNotFoundError` or an httpx transport error name. The `FAILED` lines of the two runs are identical.
- C4-V3: exit code `1`; `51 failed, 1 warning`; first failing assertion per test, predicted:
  - 42 cases at `tests/test_inference_client_red.py:156` (`assert response.json() == {"detail": detail}` in `assert_cloning_failed`): the service answers `503` with "Voice cloning service is unavailable. Please retry, or use Google voice narration mode." instead of the contract's reason message. These are C4-T4–C4-T10, C4-T12–C4-T17, C4-T19 and C4-T20.
  - 7 cases at `tests/test_inference_client_red.py:161` (`assert response.status_code == 200` in `assert_job_saved`): `503` instead of `200`, because the stand-in answers the baseline's tokenless JSON request with `401`. These are C4-T1, the three C4-T2 cases, C4-T3, C4-T11 and C4-T18.
  - `tests/test_clone_flow.py:85`: the exact CFR-1 comparison.
  - `tests/test_ai_gateway_telemetry_red.py:70`: `503` (`MODEL_UNAVAILABLE` with the generic message) instead of `202`.

  The exact line per test is a prediction; what C4-AC-3 requires is the failure class.
- C4-V4: exactly `?? tests/_chatterbox_boundary.py`, `?? tests/test_inference_client_red.py`, ` M tests/test_ai_gateway_telemetry_red.py`, ` M tests/test_clone_flow.py`, plus this Implementation Plan (`??` until committed) and ` M docs/.ai/chatterbox-cloud-run/Plan.md` after the status update.
- C4-V5: the four hashes in C4-AC-1.
- Preserved-behavior tests (expected to pass at RED): none. `Plan.md` traceability assigns two preserved rows to CRM-4 as verifier: "CCR-10 local part (generated audio saved by the local app, RF-13)" and "Gateway telemetry on the voice cloning path (RF-15)". The contract requires both under the new request with the identity token (CCR-5, CCR-7), which the unmodified service cannot send. So C4-T1 (local save) and the updated RF-15 test fail at RED because the new request is missing, not because local saving or telemetry is missing. They are not RED evidence for those preserved rows. They show the rows still hold once CRM-5 delivers the request.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. Run on 2026-11-09 in a disposable copy outside the repository. The copy was made with `tar` from the working tree at `467b9f2` (excluding `.venv`, `.git`, `Voice-Narration.zip`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache`, `.deepeval`) into `C:\Users\avina\AppData\Local\Temp\claude\dd431ff1ad187051\a64835d9-b6b8-4c46-a2ab-81eb4d20b4b6\scratchpad\crm4\repo`. It included the git-ignored `.env` and `service-account-key.json`, which the preserved narration test needs. The repository's `.venv` interpreter was used with the copy as working directory, with `-p no:cacheprovider`. The files written into the copy are the ones whose content and hashes appear above.

1. Unmodified baseline in the copy:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider
   ======================= 22 passed, 1 warning in 10.16s ========================
   ```

2. The four files applied (both new files created, both existing files replaced with their complete final content). RED run 1 (C4-V1):

   ```
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 1)
   collected 71 items
   FAILED tests/test_ai_gateway_telemetry_red.py::test_gateway_execution_returns_non_placeholder_telemetry
   FAILED tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable
   FAILED tests/test_inference_client_red.py::test_cloning_request_carries_sample_audio_and_identity_token
   FAILED tests/test_inference_client_red.py::test_cloning_language_part_follows_profile_language[hi-IN]
   FAILED tests/test_inference_client_red.py::test_cloning_language_part_follows_profile_language[EN-GB]
   FAILED tests/test_inference_client_red.py::test_cloning_language_part_follows_profile_language[no-language]
   FAILED tests/test_inference_client_red.py::test_base_url_in_effect_is_call_target_and_token_audience
   FAILED tests/test_inference_client_red.py::test_no_configured_base_url_answers_cfr1[neither-set]
   FAILED tests/test_inference_client_red.py::test_no_configured_base_url_answers_cfr1[empty-no-fallback]
   FAILED tests/test_inference_client_red.py::test_no_configured_base_url_answers_cfr1[whitespace]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[0]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[00]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[-5]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[+5]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[10.5]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[ten]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_answers_cfr2[1 0]
   FAILED tests/test_inference_client_red.py::test_invalid_time_limit_leaves_narration_unaffected
   FAILED tests/test_inference_client_red.py::test_unreadable_voice_sample_answers_cfr3[no-sample-path]
   FAILED tests/test_inference_client_red.py::test_unreadable_voice_sample_answers_cfr3[missing-file]
   FAILED tests/test_inference_client_red.py::test_unreadable_voice_sample_answers_cfr3[directory]
   FAILED tests/test_inference_client_red.py::test_identity_token_unavailable_answers_cfr4[missing-key-file]
   FAILED tests/test_inference_client_red.py::test_identity_token_unavailable_answers_cfr4[not-json]
   FAILED tests/test_inference_client_red.py::test_identity_token_unavailable_answers_cfr4[not-a-service-account-key]
   FAILED tests/test_inference_client_red.py::test_identity_token_unavailable_answers_cfr4[token-request-refused]
   FAILED tests/test_inference_client_red.py::test_time_limit_bounds_wait_for_chatterbox_response
   FAILED tests/test_inference_client_red.py::test_time_limit_bounds_complete_response_not_each_read
   FAILED tests/test_inference_client_red.py::test_identity_token_time_is_not_counted_toward_time_limit
   FAILED tests/test_inference_client_red.py::test_time_limit_in_effect_is_reported_when_reached[not-set]
   FAILED tests/test_inference_client_red.py::test_time_limit_in_effect_is_reported_when_reached[empty]
   FAILED tests/test_inference_client_red.py::test_time_limit_in_effect_is_reported_when_reached[whitespace]
   FAILED tests/test_inference_client_red.py::test_time_limit_in_effect_is_reported_when_reached[padded-7]
   FAILED tests/test_inference_client_red.py::test_time_limit_in_effect_is_reported_when_reached[leading-zeros-7]
   FAILED tests/test_inference_client_red.py::test_time_limit_setting_is_read_at_service_start
   FAILED tests/test_inference_client_red.py::test_unreachable_chatterbox_answers_cfr6[connection-refused]
   FAILED tests/test_inference_client_red.py::test_unreachable_chatterbox_answers_cfr6[connection-lost-before-full-response]
   FAILED tests/test_inference_client_red.py::test_access_denied_answers_cfr7[401]
   FAILED tests/test_inference_client_red.py::test_access_denied_answers_cfr7[403]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[400]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[422]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[429]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[500]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[503]
   FAILED tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[504]
   FAILED tests/test_inference_client_red.py::test_success_status_without_audio_answers_cfr9[empty-body]
   FAILED tests/test_inference_client_red.py::test_success_status_without_audio_answers_cfr9[json-body]
   FAILED tests/test_inference_client_red.py::test_success_status_without_audio_answers_cfr9[no-content-type]
   FAILED tests/test_inference_client_red.py::test_success_status_without_audio_answers_cfr9[text-plain]
   FAILED tests/test_inference_client_red.py::test_audio_wav_media_type_is_matched_case_insensitively_ignoring_parameters
   FAILED tests/test_inference_client_red.py::test_failure_reasons_are_checked_in_contract_order
   FAILED tests/test_inference_client_red.py::test_cloning_failure_answer_over_real_transport
   ================== 51 failed, 20 passed, 1 warning in 29.28s ==================
   ```

   Searching the output (case-insensitive) for `Traceback`, `TransportError`, `ReadError`, `ConnectError`, `ImportError`, `ModuleNotFoundError`, `fixture … not found` and `did not start` counted `0`.

3. Pass proof with a scratch-only probe, which never enters the repository. The copy's `voice_narration/inference/application.py` was replaced by a probe of a possible CRM-5 change. The probe reads `VOICE_CLONING_TIMEOUT_SECONDS` at import. It checks CFR-1 → CFR-4 in order, and reads the sample bytes. It obtains the token with `service_account.IDTokenCredentials.from_service_account_file(..., target_audience=<base URL>)` and `refresh(google.auth.transport.requests.Request())`, after `_load_local_env()`. It then streams `POST /v1/synthesize` (multipart `text`, `language`, `sample_audio`, `Authorization: Bearer`) with `httpx.Client(timeout=<limit>)`, checking a monotonic deadline between body chunks. Finally it maps timeouts, transport errors, `401`/`403`, other statuses and non-audio answers to CFR-5–CFR-9, and `create_job` answers `503` with the reason message.

   ```
   == probe, full suite                                     (exit 0)
   ======================= 71 passed, 1 warning in 40.40s ========================
   == probe, full suite again, no cleaning, --durations=8   (exit 0)
   2.20s call     tests/test_inference_client_red.py::test_unreachable_chatterbox_answers_cfr6[connection-refused]
   1.80s call     tests/test_inference_client_red.py::test_identity_token_time_is_not_counted_toward_time_limit
   1.60s teardown tests/test_inference_client_red.py::test_time_limit_bounds_wait_for_chatterbox_response
   1.35s call     tests/test_inference_client_red.py::test_time_limit_bounds_complete_response_not_each_read
   1.17s call     tests/test_inference_client_red.py::test_time_limit_bounds_wait_for_chatterbox_response
   1.11s call     tests/test_clone_flow.py::test_generation_uses_selected_voice_profile
   0.98s call     tests/test_chatterbox_service_red.py::test_synthesize_serves_concurrent_requests_one_at_a_time
   0.68s call     tests/test_ai_gateway_telemetry_red.py::test_gateway_execution_returns_non_placeholder_telemetry
   ======================= 71 passed, 1 warning in 34.96s ========================
   ```

   The copy's `application.py` was then restored and compared with the repository's (`diff -q` printed nothing; "baseline restored identical").

4. RED run 2 (C4-V2) on the restored copy, without cleaning:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 1)
   collected 71 items
   ================== 51 failed, 20 passed, 1 warning in 30.71s ==================
   FAILED lines identical          (diff of the FAILED lines of runs 1 and 2 printed nothing)
   0                               (count of transport, import, start-up and network-guard error text)
   ```

5. C4-V3, exactly as planned:

   ```
   $ python -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable tests/test_ai_gateway_telemetry_red.py -q --tb=line -p no:cacheprovider        (exit 1)
   51 failed, 1 warning in 49.47s
   first failing location per test, counted:
        42 test_inference_client_red.py:156: AssertionError
         7 test_inference_client_red.py:161: AssertionError
         1 test_clone_flow.py:85: AssertionError
         1 test_ai_gateway_telemetry_red.py:70: AssertionError
   ```

6. Diff check: the two unified diffs above were produced with `diff -u` between `git show HEAD:<file>` and the final content, then applied with `patch -p1` to fresh copies of the committed files:

   ```
   patching file tests/test_clone_flow.py
   patching file tests/test_ai_gateway_telemetry_red.py
   ab285fd7f808bfa2358ef80c4ca6ba6e68afbbfc154d07c005f9d20455032f88 *tests/test_ai_gateway_telemetry_red.py
   84416efa942f57fd1675d4955f8e7546e6ff3c782978ee15d248d6c85870edb8 *tests/test_clone_flow.py
   ```

   The patched files have the same hashes as the complete final contents.

7. Created during the dry run, all under `C:\Users\avina\AppData\Local\Temp\claude\dd431ff1ad187051\a64835d9-b6b8-4c46-a2ab-81eb4d20b4b6\scratchpad\crm4`, and deleted afterwards: `repo\` (the disposable copy), `src\` (the four proposed files, the committed versions of the two modified files, and the two diffs), `probe\` (the probe and the baseline copies of `application.py`), `apply\` and `apply2\` (diff-apply checks, the second applying the diffs extracted from this plan), the run logs `red1.log`, `red2.log`, `red3.log`, `v3.log`, `probe1.log`, `probe2.log`, and `plan_template.md` with `build_plan.py` (used to embed the exact file contents into this plan). Nothing was written to the repository except this Implementation Plan.

## Risks

- C4-RSK-1 — Identity comparisons (`security`). The inference service makes no authorization decision; the comparisons in this milestone are:
  - Token audience against the Chatterbox URL. The contract fixes one canonical form: the configured base URL with surrounding whitespace removed and nothing else changed, used both for the call URL and as the audience (Settings row 1, CCD-4). C4-T1 and C4-T3 compare the assertion's `target_audience` with exactly that string, including the fallback setting and a value padded with spaces and a tab. No case folding or trailing-slash normalization is applied, on either side. Cloud Run compares the token's audience with its own service URL, so a configured URL that differs from the service URL (for example by a trailing `/`) is rejected there and answered as CFR-7. That is deployment behavior, documented by CRM-6 and not testable here.
  - Service-account identity. The assertion's `iss` is compared exactly with the key file's `client_email`, both read from the same file (C4-T1). The real account's IAM invoker check is Cloud Run's, at deployment.
  - The `Authorization` header. The stand-in accepts only `Bearer ` followed by a token it issued, compared as an exact string (C4-D-7). C4-T1 asserts the same exact form, as the contract writes it (`Authorization: Bearer <token>`).
  - No user identity, role or ownership comparison exists: login and authentication of application users are excluded (requirements Explicit Exclusions).
- C4-RSK-2 — Secrets. The tests generate their own RSA key per test in `tmp_path` and never read the real `service-account-key.json`: every new test and the updated RF-15 test set `GOOGLE_APPLICATION_CREDENTIALS` to the test key, and the network guard blocks Google's endpoints. The preserved narration test and the RF-14 test still use the developer's environment, as before; RF-14 fails at CFR-1 before any credential is read.
- C4-RSK-3 — Bindings on CRM-5 (C4-D-2, C4-D-3, C4-D-4, C4-D-5). If CRM-5 needs a different token source, transport or module name, its run fails for a reason that is not missing behavior. Mitigation inside scope: CRM-5 stops and returns to planning; it does not edit these tests.
- C4-RSK-4 — Timing. C4-T9, C4-T10 and C4-T11 depend on wall-clock margins (C4-D-10). On a heavily loaded machine a correct implementation could exceed `elapsed < 2.2` s or `< 2.5` s; that is a hypothesis, not observed. Under the probe, C4-T9 took 1.17 s and C4-T10 1.35 s. If it happens at CRM-5, it is a finding to report; no rerun-until-pass or threshold change is authorized.
- C4-RSK-5 — Connection refused on Windows takes about 2 s. The probe measured 2.20 s for C4-T14 `connection-refused` (Windows retries the loopback SYN before refusing; this explanation is a hypothesis, not measured further). The default limit (600 s) applies there, so the timing cannot turn CFR-6 into CFR-5.
- C4-RSK-6 — Shared state outside `tmp_path`. A fresh import runs the module's own import-time code against the repository's `audio_storage` (`AUDIO_ROOT.mkdir`, `_ensure_db()`; `application.py:20`, `:72`) before `load()` redirects it. This is the same import-time effect every existing test has, and creates nothing new once `audio_storage/generation_jobs.db` exists. The RF-14 and RF-15 tests keep using the repository's `audio_storage` through the voices service, as before. Every assertion of the new tests reads only `tmp_path`.
- C4-RSK-7 — Network-dependent preserved test. `test_generation_uses_selected_voice_profile` calls Google TTS with the local key. If it fails at execution for network or credential reasons, C4-AC-4 is not met; execution stops and reports it. No rerun-until-pass, skip or change is authorized.
- C4-RSK-8 — Helper-module reading (C4-D-8). If the reviewer reads `tests/_chatterbox_boundary.py` as a test-infrastructure change that the Plan excludes, the plan returns for revision (copy the stand-ins into the test files) before approval.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `tests/_chatterbox_boundary.py` and `tests/test_inference_client_red.py`; restore `tests/test_clone_flow.py` and `tests/test_ai_gateway_telemetry_red.py` with `git restore -- tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py`. No other file is changed by this milestone. Do not use repository-wide reset, clean or checkout operations.

## Explicitly Out of Scope

- Any production change, including `voice_narration/inference/application.py` and `voice_narration/inference/providers/google.py` (CRM-5).
- Chatterbox tests and `tests/test_chatterbox_service_red.py` (CRM-2, executed).
- Any change to `tests/test_ai_gateway_red.py`, to `test_voice_enrollment_creates_profile` or to `test_generation_uses_selected_voice_profile`.
- Dependency, `requirements-dev.txt`, `pytest.ini`, `conftest.py`, container, deployment or documentation changes (CRM-6 for the deployment document).
- Tests of user login or authentication, of the gateway's error shape, or of Cloud Run's own enforcement.
- Logging, metrics, alerts, duplicate detection.

## Human Review

Status: Approved by avinash2196 on 2026-11-09 ("Approve plan"). Executed on 2026-11-09: RED established (C4-AC-1–C4-AC-5 met) — see `Plan.md` "CRM-4 Execution Evidence".
