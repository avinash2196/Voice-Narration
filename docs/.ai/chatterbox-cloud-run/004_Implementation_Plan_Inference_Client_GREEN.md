# Implementation Plan — CRM-5 Inference Client GREEN

## Milestone

CRM-5 — Inference Client GREEN, work item `chatterbox-cloud-run` (`docs/.ai/chatterbox-cloud-run/Plan.md`, section "CRM-5 — Inference Client GREEN").

Purpose as recorded in `Plan.md`: "The inference service sends the sample audio with the service account's identity, within the configurable time limit, and reports why a cloning call failed." Scope: "cloning requests carry the locally stored voice sample audio and the service account's Google identity token as the contract defines; each cloning request is bounded by the configurable limit defaulting to 10 minutes; each cloning failure is answered with the reason the contract defines; narration mode, local saving of generated audio, and the gateway's pass-through stay as they are." Owned: CCR-5; CCR-7 (the inference service attaches the service account's identity token); CCR-8; CCR-9; Dependency failure characteristic.

## Milestone Type

GREEN — as recorded in `Plan.md` ("Milestone type: GREEN") and in its Execution Status row "CRM-5 — Inference Client GREEN (GREEN) | Pending". This plan proposes the smallest production change that makes CRM-4's RED tests pass. It changes one production file, `voice_narration/inference/application.py`, and no test.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Approved by avinash2196 on 2026-11-09 (its Status section). Execution Status: CRM-1 Complete, CRM-2 Complete, CRM-3 Complete, CRM-4 Complete, CRM-5 Pending, CRM-6 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (accepts CCD-1–CCD-7). Authoritative predecessor delivered by CRM-1; the `Plan.md` CRM-1 row is Complete and points to it |
| `docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md` (revision 2) | Human Review: revision 2 approved by avinash2196 on 2026-11-09; executed, RED established. Source of carried-forward decisions |
| `docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md` | Human Review: approved by avinash2196 on 2026-11-09 ("Approve and run"); executed, GREEN verified. Source of carried-forward decisions |
| `docs/.ai/chatterbox-cloud-run/003_Implementation_Plan_Inference_Client_RED.md` | Human Review: "Approved by avinash2196 on 2026-11-09 ("Approve plan"). Executed on 2026-11-09: RED established (C4-AC-1–C4-AC-5 met)". Direct predecessor; source of the test-design decisions that bind this milestone |
| `docs/requirements.md` (product level) | Absent — `docs/` holds only `.ai/` and `developer-setup.md` |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Not re-read; referenced by `Plan.md` and `API-Contract.md` as an unchanged constraint (approved 2026-11-08). This plan does not change the gateway code path (`application.py:363-366` is unchanged) |
| `docs/developer-setup.md` | Repository documentation, not a PDD artifact; source of the verification command through `Plan.md` Verification Commands |
| Plugin skills read: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `security` | Plugin guidance, not project artifacts |

`security` is applied: CRM-5 owns CCR-7, the private-access requirement (the inference service attaches the service account's Google identity token). The identity comparisons are listed in Risks (C5-RSK-1).

## Carried-Forward Decisions

From `003_Implementation_Plan_Inference_Client_RED.md` (approved by avinash2196 on 2026-11-09). Its "Test-design decisions for review" state "These choices bind the GREEN milestone CRM-5, which may not change these tests." None is reopened:

- C4-D-1 — Chatterbox and the token endpoint are loopback stand-ins over real HTTP. This plan's code therefore sends a real HTTP request; no test hook is added.
- C4-D-2 — The identity token is obtained with the service-account ID-token grant (`grant_type` jwt-bearer) at the key file's `token_uri`, with an RS256 assertion signed by the key, `iss` = the key's `client_email` and `target_audience` = the base URL in effect. This plan uses `google.oauth2.service_account.IDTokenCredentials`, which does exactly that (C5-D-1), and not the IAM endpoint or the metadata server.
- C4-D-3 — Any non-loopback network access fails the test. This plan does not use `google.oauth2.id_token.fetch_id_token`, whose metadata-server fallback C4-D-3 names; a key file that is not a service-account key is rejected before any request (C5-D-1).
- C4-D-4 — Fresh import per configuration. This plan keeps the names `ROOT`, `AUDIO_ROOT`, `DB_PATH`, `_ensure_db`, `GoogleVoiceProvider` and `VOICE_CLONING_API_BASE_URL` unchanged, and reads `VOICE_CLONING_API_BASE_URL` as a module global at call time (the RF-14 and RF-15 tests set that attribute).
- C4-D-5 — The call goes through httpx's default synchronous transport (`httpx.HTTPTransport.handle_request`), and an httpx timeout is answered as CFR-5 with the limit in effect. This plan uses `httpx.Client` with its default transport and maps `httpx.TimeoutException` to CFR-5 (C5-D-3, C5-D-4).
- C4-D-6 — The time-limit setting is read once at service start (module import). This plan parses it at import into `VOICE_CLONING_TIMEOUT_SECONDS` (C5-D-7).
- C4-D-7 — The stand-in Chatterbox answers as the executed CRM-3 Chatterbox and Cloud Run do. This plan sends the contract's multipart request with the token, so the stand-in reaches its success branch.
- C4-D-8 — `tests/_chatterbox_boundary.py` is shared test code. No effect on production code.
- C4-D-10 — Timing thresholds (C4-T9 `< 2.2` s, C4-T10 `< 2.5` s, C4-T11 `>= 1.5` s). This plan's time-limit mechanism is measured against them in the dry run.

From `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2 and `002_Implementation_Plan_Chatterbox_Service_GREEN.md` (both approved by avinash2196 on 2026-11-09): the executed Chatterbox takes `multipart/form-data` with the form fields `text` and `language` and the file part `sample_audio`, and answers a JSON body `422` and a `sample_path` part `400` (CCD-1–CCD-3). This plan's request matches that shape. C2-D-6 and C2-D-7 are test-side only.

Approved contract decisions this milestone implements (`API-Contract.md`): CCD-1 (inference side: the stored sample bytes sent unmodified as the `sample_audio` file part), CCD-2 (no `sample_path` part), CCD-4 (identity token in `Authorization: Bearer`, audience = base URL in effect), CCD-5 (CFR-1–CFR-9 in order, worded as tabled), CCD-6 (`VOICE_CLONING_TIMEOUT_SECONDS`), CCD-7 (base URL settings carried over and used as the audience; the key file named by `GOOGLE_APPLICATION_CREDENTIALS`, located as the narration provider locates it; no opt-out), and CCD-8 (carried-over job-creation inputs, validations, success body and pass-through).

## Preconditions / Predecessor Evidence

- Predecessor CRM-4 (RED): `Plan.md` Execution Status row "CRM-4 — Inference Client RED (RED) | Complete | RED established on 2026-11-09 by `003_Implementation_Plan_Inference_Client_RED.md`: C4-AC-1–C4-AC-5 met; 4 files match the planned SHA-256; 71 collected, 51 fail on their own assertions (49 new cases, RF-14, RF-15), 20 pass, in two consecutive full runs." Its evidence section "CRM-4 Execution Evidence" records C4-V1 and C4-V2 `51 failed, 20 passed`, error-text count `0`, and C4-V3's first failing locations (42 at `test_inference_client_red.py:156`, 7 at `:161`, `test_clone_flow.py:85`, `test_ai_gateway_telemetry_red.py:70`).
- The RED evidence is valid for this GREEN: every one of the 51 tests failed with an `AssertionError` because the unmodified inference service sends a tokenless JSON body and answers every cloning failure with its single generic message (CRM-4 Execution Evidence, Result).
- RED test files in the repository are the approved ones. `sha256sum` now prints:
  - `tests/_chatterbox_boundary.py` `7ef1a7bd05e3a273faf76eebca9973984000ff1ad5f408e550784865ca710608`
  - `tests/test_inference_client_red.py` `fff78d051a09ec355ab465e8c2751b7c53d627d2b7d0139a8273c4691798314e`
  - `tests/test_clone_flow.py` `84416efa942f57fd1675d4955f8e7546e6ff3c782978ee15d248d6c85870edb8`
  - `tests/test_ai_gateway_telemetry_red.py` `ab285fd7f808bfa2358ef80c4ca6ba6e68afbbfc154d07c005f9d20455032f88`
  - `tests/test_chatterbox_service_red.py` `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`

  The first four are the hashes CRM-4 recorded; the fifth is the hash CRM-2 and CRM-3 recorded.
- Re-observed on the unmodified baseline in this plan's dry run (disposable copy): `51 failed, 20 passed, 1 warning` (Planning-Time Dry Run, step 1), the same counts CRM-4 recorded.
- CRM-5 is Pending in `Plan.md` Execution Status. No Implementation Plan for CRM-5 exists: the work-item folder holds `requirements.md`, `Plan.md`, `API-Contract.md` and Implementation Plans `001`, `002`, `003`. This plan is numbered `004`.
- Milestone type check: `Plan.md` records CRM-5 as GREEN; this plan is GREEN.
- Pre-existing failures: none. On the unmodified baseline the only failing tests are the 51 CRM-4 tests, which are this milestone's subject; the 20 other tests pass.

## Current Repository State

Inspected on 2026-11-10.

- `git rev-parse HEAD`: `575e85ec1b51a0c81d417d97ff199f3992eeba47` ("CRM-4 RED: inference client tests for sample upload, identity token and failure reasons"). `git status --short` printed nothing: the working tree is clean.
- Line endings: `git ls-files --eol voice_narration/inference/application.py` shows `i/lf w/crlf` (LF in the repository, CRLF in the working tree; `core.autocrlf` is `true` and there is no `.gitattributes`, as Implementation Plan 003 recorded). The committed (LF) file: `git show HEAD:voice_narration/inference/application.py | sha256sum` = `9d55caf9b6ff2111418e7e824608bd7bd286b1179fae806f9ac98b5373ea1caf`, 395 lines.
- `voice_narration/inference/application.py` is unchanged by this work item so far:
  - settings read at import: `CHATTERBOX_API_BASE_URL` and `VOICE_CLONING_API_BASE_URL` (`:23-24`); no time-limit setting;
  - `_synthesize_via_chatterbox_api` (`:99-116`): returns `False` outside `voice_cloning` mode or with no base URL; sends `httpx.post(..., json={"text", "language", "sample_path"}, timeout=120.0)` with no `Authorization` header; any exception or non-`200` status returns `False`; otherwise writes `response.content` to the output path without checking its content type;
  - `create_job` (`:157-216`): a `False` result in `voice_cloning` mode raises `503` "Voice cloning service is unavailable. Please retry, or use Google voice narration mode." (`:179-183`); otherwise narration uses `GoogleVoiceProvider` (`:184-186`); the job row is inserted only after generation (`:188-207`);
  - the gateway execution passes a `503` detail through as `MODEL_UNAVAILABLE` (`:363-366`).
- `git grep` for `_synthesize_via_chatterbox_api` finds only its definition (`:99`) and its one caller (`:178`); the generic message appears only at `:182`.
- `voice_narration/inference/providers/google.py`: `_load_local_env()` (`:13-35`) leaves `GOOGLE_APPLICATION_CREDENTIALS` as set in the process environment; otherwise it takes it from the repository-root `.env` (`os.environ.setdefault` for every `.env` key, `:23-30`), and otherwise sets it to `service-account-key.json` at the repository root (`:17-20`, `:32-35`). `GoogleVoiceProvider.__init__` calls it on every narration job (`:39-41`). This is the location rule the contract names for the key file (Inference Service Settings, `GOOGLE_APPLICATION_CREDENTIALS` row). The local `.env` defines `GOOGLE_APPLICATION_CREDENTIALS` and no `VOICE_CLONING_*` or `CHATTERBOX_*` key (key names read; values not read).
- RED tests (CRM-4) relied on by this plan, read from the repository files:
  - `tests/test_inference_client_red.py` `_Harness.load` sets `VOICE_CLONING_API_BASE_URL`, `CHATTERBOX_API_BASE_URL`, `VOICE_CLONING_TIMEOUT_SECONDS` and `GOOGLE_APPLICATION_CREDENTIALS` and then imports a fresh copy of the module (`:90-118`). C4-T13 changes `VOICE_CLONING_TIMEOUT_SECONDS` after import and expects CFR-2 still (`:456-464`).
  - `tests/test_clone_flow.py` (RF-14) sets the module attribute `VOICE_CLONING_API_BASE_URL` to `""` on the module imported at collection and expects exactly CFR-1 (`:69`, `:83-88`).
  - `tests/test_ai_gateway_telemetry_red.py` (RF-15) uses the module imported at collection, sets `GOOGLE_APPLICATION_CREDENTIALS` with `monkeypatch.setenv` after that import, and sets the module attribute `VOICE_CLONING_API_BASE_URL` (`:46-47`). The key file must therefore be located when the call is made, not at import.
  - C4-T12 replaces `httpx.HTTPTransport.handle_request` so the `/v1/synthesize` call raises `httpx.ReadTimeout` (`:437-445`).
- Installed packages this plan's code imports (`pip list` in `.venv`, Python 3.13.17): `httpx 0.28.1`, `fastapi 0.162.0`, `google-auth 2.62.1`, `requests 2.34.2`. `requirements-dev.txt` declares `httpx==0.28.1` and `fastapi==0.162.0`; it declares neither `google-auth` nor `requests` (`Plan.md` RSK-6). Both are installed as requirements of the Google TTS client the narration provider already imports (`voice_narration/inference/providers/google.py:8`): `google_cloud_texttospeech-2.38.0.dist-info/METADATA` has `Requires-Dist: google-api-core[grpc]<3.0.0,>=2.28.0` and `Requires-Dist: google-auth!=2.24.0,!=2.25.0,<3.0.0,>=2.14.1`, and `google_api_core-2.44.0.dist-info/METADATA` has `Requires-Dist: requests<3.0.0,>=2.33.0`.
- Library behavior this plan depends on, read from the installed code:
  - `IDTokenCredentials.from_service_account_info(info, target_audience=...)` requires `client_email` and `token_uri` in the key info (`google/oauth2/service_account.py:687-705`), takes `token_uri` and `universe_domain` from it (`:680-684`), and uses the IAM endpoint only when `universe_domain` is not `googleapis.com` (`:656-657`). `refresh(request)` otherwise posts the signed assertion to `token_uri` with `_client.id_token_jwt_grant` and stores the returned ID token in `token` (`:861-870`).
  - `google.auth.transport.requests.Request()` creates a `requests.Session` when none is given (`google/auth/transport/requests.py:146-150`), closes it in `__del__` (`:166-174`), and uses a 120-second default timeout per request (`:49`, `:235`).
  - The token grant retries only for retryable status codes or the error codes `internal_failure`, `server_error`, `temporarily_unavailable` (`google/oauth2/_client.py`, `_can_retry`).
- The preserved test `test_generation_uses_selected_voice_profile` calls Google TTS with the developer's local key (Implementation Plan 003, Current Repository State), so the full suite needs network access to Google and the git-ignored local key file. This milestone does not change that test or the narration path.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `voice_narration/inference/application.py` — a complete unified diff against the committed file and the complete final content are given under Proposed Code / Tests.

### Files to Delete

None.

## Proposed Changes

All in `voice_narration/inference/application.py`:

1. Imports:
   1. add `from concurrent.futures import ThreadPoolExecutor` and `from concurrent.futures import TimeoutError as FutureTimeoutError` (C5-D-3);
   2. add `import google.auth.transport.requests` and `from google.oauth2 import service_account` (C5-D-1);
   3. add `from voice_narration.inference.providers.google import _load_local_env` (C5-D-2).
2. Time-limit setting (CCR-9, CCD-6, Settings row `VOICE_CLONING_TIMEOUT_SECONDS`), after `GATEWAY_ALLOWED_MODES`:
   1. add `VOICE_CLONING_TIMEOUT_DEFAULT_SECONDS = 600`;
   2. add `_parse_voice_cloning_timeout(raw: str | None) -> int | None`: surrounding whitespace removed; empty (or not set) → `600`; otherwise ASCII decimal digits only with value at least `1` → that integer; anything else → `None` (invalid, answered as CFR-2) (C5-D-7);
   3. add the module global `VOICE_CLONING_TIMEOUT_SECONDS = _parse_voice_cloning_timeout(os.getenv("VOICE_CLONING_TIMEOUT_SECONDS"))`, read once at import (service start).
3. Add `_voice_cloning_failure(reason: str) -> HTTPException`: returns `HTTPException(status_code=503, detail=f"Voice cloning failed: {reason}. Please retry, or use Google voice narration mode.")` — the contract's message form for CFR-1–CFR-9 (CCD-5).
4. Add `_voice_cloning_identity_token(audience: str) -> str` (CCR-7, CCD-4, CCD-7): calls `_load_local_env()`; reads `GOOGLE_APPLICATION_CREDENTIALS` from the process environment; raises `ValueError` when it is empty; reads and parses the key file as JSON; raises `ValueError` unless it is a JSON object with `type` equal to `service_account`; builds `service_account.IDTokenCredentials.from_service_account_info(info, target_audience=audience)`, calls `refresh(google.auth.transport.requests.Request())`, and returns `credentials.token` (C5-D-1).
5. Add `_post_voice_cloning_request(url, token, text, language, sample, limit, deadline) -> tuple[int, str, bytes]` (CCR-5, CCD-1, CCD-2, CCD-4, CCD-6): with `httpx.Client(timeout=limit)` it streams `POST url` with header `Authorization: Bearer <token>`, form fields `text` and `language`, and the file part `sample_audio` = `("sample.wav", sample, "audio/wav")` (C5-D-5), and no `sample_path` part. It reads the body chunk by chunk and raises `httpx.ReadTimeout` when a chunk arrives at or after `deadline`. It returns the status code, the `Content-Type` header (`""` when absent) and the body.
6. Replace the body of `_synthesize_via_chatterbox_api` (signature unchanged). Outside `voice_cloning` mode it still returns `False`. In `voice_cloning` mode it checks in the contract's order and raises `_voice_cloning_failure(...)` for the first reason that applies (CCD-5, C5-D-6):
   1. CFR-1: the module global `VOICE_CLONING_API_BASE_URL` is empty;
   2. CFR-2: `VOICE_CLONING_TIMEOUT_SECONDS` is `None`;
   3. CFR-3: the profile's `sample_path` is empty or absent, or `Path(sample_path).read_bytes()` raises `OSError`;
   4. CFR-4: `_voice_cloning_identity_token(base_url)` raises any `Exception`;
   5. the call: `language` is derived as before (`str(profile.get("language") or "en").split("-")[0].lower()`); `deadline = time.monotonic() + limit`; `_post_voice_cloning_request` runs on a one-worker `ThreadPoolExecutor`, which is shut down with `wait=False` at once; the result is awaited with `call.result(timeout=max(0.0, deadline - time.monotonic()))` (C5-D-3);
   6. CFR-5: the wait times out (`FutureTimeoutError`) or the call raises `httpx.TimeoutException`; the message names `limit`;
   7. CFR-6: the call raises any other `Exception` (C5-D-4);
   8. CFR-7: status `401` or `403`, the message naming the status;
   9. CFR-8: any other status that is not `200`, the message naming the status;
   10. CFR-9: status `200` whose `Content-Type` media type (before `;`, trimmed, lowercased) is not `audio/wav`, or whose body is empty;
   11. success: writes the body to `output_path` and returns `True` (RF-13, CCR-10 local part).
7. In `create_job`, remove the block that answered every voice cloning failure with "Voice cloning service is unavailable. Please retry, or use Google voice narration mode." (`:179-183`). `_synthesize_via_chatterbox_api` now raises the reason's `503` itself, so a `False` result means narration mode, which keeps using `GoogleVoiceProvider` unchanged.
8. Unchanged: every other function and route, including `_profile_lookup`, the job row insert, the success body, `job_audio`, the gateway routes and the gateway's `503` pass-through (`create_gateway_execution`, `:363-366`), and the names `ROOT`, `AUDIO_ROOT`, `DB_PATH`, `BASE_URL`, `CHATTERBOX_API_BASE_URL`, `VOICE_CLONING_API_BASE_URL`, `_ensure_db`, `GoogleVoiceProvider`, `app`.

### Implementation decisions for review

- C5-D-1 — Identity token through `google.oauth2.service_account.IDTokenCredentials` from the parsed key file, refreshed with `google.auth.transport.requests.Request()`, one new token per cloning call. Why: it performs the service-account ID-token grant at the key file's `token_uri` with an RS256 assertion carrying `iss` and `target_audience` (Current Repository State), which is what CCD-4, CCD-7 and C4-D-2 require. The explicit `type == "service_account"` check makes a key file that is not a service-account key a CFR-4 before any request (contract CFR-4: "is not a service-account key"). `from_service_account_info` alone would accept any JSON with `client_email`, `token_uri` and `private_key`. Alternatives: `google.oauth2.id_token.fetch_id_token` — not chosen: it falls back to the metadata server (C4-D-3). Signing the assertion with `cryptography` directly — not chosen: more code that duplicates the library. Caching the token until it expires — not chosen: no approved artifact asks for it, and it adds state; the cost is one token request to Google per cloning call, which the contract does not count toward the time limit.
- C5-D-2 — The key file is located by calling the narration provider's existing `_load_local_env()`. Why: the contract says it is "Located as the existing narration provider locates it" (Settings, `GOOGLE_APPLICATION_CREDENTIALS` row), and reusing the function keeps both paths identical. It is called at call time, because RF-15 sets `GOOGLE_APPLICATION_CREDENTIALS` after the module is imported (Current Repository State). Consequence: as on every narration job today (`google.py:39-41`), a cloning call copies the `.env` keys missing from the process environment into it (`os.environ.setdefault`, `google.py:30`). Alternative: copy the location rule into `application.py` without that side effect. Not chosen: two copies of one rule, and the side effect already happens on every narration job. The import uses a name with a leading underscore from a sibling module of the same package.
- C5-D-3 — The time limit is enforced by waiting for a worker thread with a timeout, plus a deadline the worker checks itself. `call.result(timeout=...)` returns or times out within `limit` seconds of the request starting, whatever the server does: delayed headers (C4-T9), a trickled body (C4-T10), or a slow connect. The worker's `httpx.Client(timeout=limit)` bounds each network wait, and its deadline check between body chunks makes it stop reading soon after the deadline. So an abandoned worker ends on its own. The deadline is set after the token is obtained, so obtaining the token is not counted (C4-T11, contract). Alternative A: stream in the request thread with `httpx.Client(timeout=limit)` and check the deadline between chunks (the CRM-4 dry-run probe). Not chosen: httpx timeouts apply to each connect, write and read separately, so a call that has used most of its limit can still wait up to one more `limit` in a single read. The answer could then come up to about twice the limit, not within it. Alternative B: `httpx.post(..., timeout=limit)` alone. Not chosen: a body trickled in pieces each shorter than the limit is never stopped (C4-T10, C4-D-5). Consequence: a timed-out call leaves the worker thread connected to Chatterbox until its next chunk, its own per-operation timeout, or the response, whichever comes first. Chatterbox's own generation is not cancelled in any case (C5-RSK-4).
- C5-D-4 — Exception mapping for the call. `httpx.TimeoutException` (which includes the worker's own deadline `ReadTimeout`) and the wait timeout → CFR-5. Any other `Exception` raised by the call → CFR-6 "could not connect". This includes every `httpx.TransportError`, such as connection refused, a connection lost before the full response (`httpx.RemoteProtocolError`), name resolution, TLS and unsupported URL scheme, and any other error raised while sending. Why: the contract defines CFR-6 as "Any transport failure other than CFR-5", and the baseline treated any exception from the call as a cloning failure (`application.py:111-112`). Alternative: map only `httpx.TransportError` to CFR-6 and let other exceptions become a `500`. Not chosen: it changes a baseline `503` answer into a `500`. Likewise, any `Exception` from obtaining the token → CFR-4 (contract CFR-4 lists the missing or unreadable file, the wrong key type and a failed token request), and any `OSError` from reading the sample → CFR-3.
- C5-D-5 — The `sample_audio` file part is sent with the fixed filename `sample.wav` and content type `audio/wav`, not the stored file's name. Why: the contract says "The part's filename and content type are not significant and are ignored" (CCD-1), and Starlette treats a part as a file only when it has a filename. The stored name is `<uuid>_<voice name>.wav` (`voice_narration/simple_voices/application.py:115`), so sending it would pass the profile's voice name to the cloud service for no purpose. Alternative: send `Path(sample_path).name`. Not chosen, for that reason.
- C5-D-6 — Failure reasons are raised as `HTTPException(503)` from `_synthesize_via_chatterbox_api`, and the generic block in `create_job` is removed. Why: the function's existing signature and caller stay, the gateway's existing `except HTTPException` pass-through (`:363-366`) receives each reason's detail unchanged, and no voice cloning failure can reach the generic message any more (it would be dead code). The job row and the audio file are written only after a success (`:188-207`, and the body is written only on success), so a failure creates neither, as the contract requires.
- C5-D-7 — Parsing `VOICE_CLONING_TIMEOUT_SECONDS` accepts only ASCII decimal digits (`value.isascii() and value.isdigit()`) after `strip()`. Why: the contract's form is "decimal digits only, surrounding whitespace removed, value at least `1`". Python's `int()` alone would also accept `+5`, `-5`, `1_0` and non-ASCII digits, and `str.isdigit()` alone accepts non-ASCII digits such as superscripts. Leading zeros are accepted (`007` → `7`, C4-T12). No upper bound is applied (the contract defines none).
- C5-D-8 — `httpx.Client` keeps httpx's default `trust_env=True`, as the baseline `httpx.post` did, so proxy environment settings apply to the call as before. No setting is added.

No dependency, plugin or configuration setting is introduced into any manifest or configuration file. The only operator-set setting the code introduces is `VOICE_CLONING_TIMEOUT_SECONDS`, defined by the approved contract (CCD-6). The code newly imports `google-auth` (`google.oauth2.service_account`, `google.auth.transport.requests`) and, through `google.auth.transport.requests`, `requests`. Neither is declared in `requirements-dev.txt`. Both are installed as requirements of the Google TTS client the narration provider already imports (Current Repository State), and `Plan.md` RSK-6 asks that this be stated: "This Plan does not change dependency declarations; the CRM-4 and CRM-5 Implementation Plans state which installed packages their code relies on." No version is chosen or changed. For reference, PyPI (`https://pypi.org/project/google-auth/`, read 2026-11-10) lists 2.62.1 as released 2026-11-03 and 2.62.2 (2026-11-10) as the latest 2.x release. Every other import is from the standard library (`concurrent.futures`), from `httpx` and `fastapi` (declared), or from the application package.

## Proposed Code / Tests

### `voice_narration/inference/application.py` — unified diff against the committed file

Produced with `diff -u` from `git show HEAD:voice_narration/inference/application.py` (LF) to the complete final content below; applied with `patch -p1` to the committed file in the dry run, it gives the same SHA-256 as the complete final content.

```diff
--- a/voice_narration/inference/application.py
+++ b/voice_narration/inference/application.py
@@ -4,16 +4,21 @@
 import os
 import sqlite3
 import uuid
+from concurrent.futures import ThreadPoolExecutor
+from concurrent.futures import TimeoutError as FutureTimeoutError
 from datetime import datetime, timezone
 from pathlib import Path
 import httpx
 import time
 
+import google.auth.transport.requests
 from fastapi import FastAPI, HTTPException
 from fastapi.middleware.cors import CORSMiddleware
 from fastapi.responses import FileResponse, JSONResponse
+from google.oauth2 import service_account
 
 from voice_narration.inference.providers import GoogleVoiceProvider
+from voice_narration.inference.providers.google import _load_local_env
 
 ROOT = Path(__file__).resolve().parents[2]
 AUDIO_ROOT = ROOT / "audio_storage"
@@ -25,6 +30,20 @@
 GATEWAY_DEFAULT_MODEL_ID = "chatterbox-multilingual-v3"
 GATEWAY_ALLOWED_LANGUAGES = {"hi", "en"}
 GATEWAY_ALLOWED_MODES = {"narration", "voice_cloning"}
+VOICE_CLONING_TIMEOUT_DEFAULT_SECONDS = 600
+
+
+def _parse_voice_cloning_timeout(raw: str | None) -> int | None:
+    value = (raw or "").strip()
+    if not value:
+        return VOICE_CLONING_TIMEOUT_DEFAULT_SECONDS
+    if not (value.isascii() and value.isdigit()):
+        return None
+    seconds = int(value)
+    return seconds if seconds >= 1 else None
+
+
+VOICE_CLONING_TIMEOUT_SECONDS = _parse_voice_cloning_timeout(os.getenv("VOICE_CLONING_TIMEOUT_SECONDS"))
 
 _gateway_models: dict[str, dict] = {
     GATEWAY_DEFAULT_MODEL_ID: {
@@ -96,23 +115,87 @@
     return dict(row)
 
 
+def _voice_cloning_failure(reason: str) -> HTTPException:
+    return HTTPException(
+        status_code=503,
+        detail=f"Voice cloning failed: {reason}. Please retry, or use Google voice narration mode.",
+    )
+
+
+def _voice_cloning_identity_token(audience: str) -> str:
+    _load_local_env()
+    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
+    if not key_path:
+        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")
+    info = json.loads(Path(key_path).read_text(encoding="utf-8"))
+    if not isinstance(info, dict) or info.get("type") != "service_account":
+        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS does not name a service-account key")
+    credentials = service_account.IDTokenCredentials.from_service_account_info(info, target_audience=audience)
+    credentials.refresh(google.auth.transport.requests.Request())
+    return credentials.token
+
+
+def _post_voice_cloning_request(
+    url: str, token: str, text: str, language: str, sample: bytes, limit: int, deadline: float
+) -> tuple[int, str, bytes]:
+    with httpx.Client(timeout=limit) as client:
+        with client.stream(
+            "POST",
+            url,
+            headers={"Authorization": f"Bearer {token}"},
+            data={"text": text, "language": language},
+            files={"sample_audio": ("sample.wav", sample, "audio/wav")},
+        ) as response:
+            chunks: list[bytes] = []
+            for chunk in response.iter_bytes():
+                if time.monotonic() >= deadline:
+                    raise httpx.ReadTimeout("voice cloning time limit reached", request=response.request)
+                chunks.append(chunk)
+            return response.status_code, response.headers.get("content-type", ""), b"".join(chunks)
+
+
 def _synthesize_via_chatterbox_api(text: str, profile: dict, output_path: Path, mode: str) -> bool:
     if mode != "voice_cloning":
         return False
-    if not VOICE_CLONING_API_BASE_URL:
-        return False
-    payload = {
-        "text": text,
-        "language": str(profile.get("language") or "en").split("-")[0].lower(),
-        "sample_path": profile.get("sample_path"),
-    }
+    base_url = VOICE_CLONING_API_BASE_URL
+    if not base_url:
+        raise _voice_cloning_failure("no voice cloning service is configured")
+    limit = VOICE_CLONING_TIMEOUT_SECONDS
+    if limit is None:
+        raise _voice_cloning_failure("VOICE_CLONING_TIMEOUT_SECONDS must be a positive whole number of seconds")
+    sample_path = profile.get("sample_path")
+    try:
+        if not sample_path:
+            raise FileNotFoundError("the voice profile has no stored sample_path")
+        sample = Path(sample_path).read_bytes()
+    except OSError:
+        raise _voice_cloning_failure("the voice sample for this profile could not be read") from None
     try:
-        response = httpx.post(f"{VOICE_CLONING_API_BASE_URL}/v1/synthesize", json=payload, timeout=120.0)
+        token = _voice_cloning_identity_token(base_url)
     except Exception:
-        return False
-    if response.status_code != 200:
-        return False
-    output_path.write_bytes(response.content)
+        raise _voice_cloning_failure("could not obtain an identity token for the voice cloning service") from None
+    language = str(profile.get("language") or "en").split("-")[0].lower()
+
+    deadline = time.monotonic() + limit
+    executor = ThreadPoolExecutor(max_workers=1)
+    call = executor.submit(
+        _post_voice_cloning_request, f"{base_url}/v1/synthesize", token, text, language, sample, limit, deadline
+    )
+    executor.shutdown(wait=False)
+    try:
+        status_code, content_type, body = call.result(timeout=max(0.0, deadline - time.monotonic()))
+    except (FutureTimeoutError, httpx.TimeoutException):
+        raise _voice_cloning_failure(f"the voice cloning service did not respond within {limit} seconds") from None
+    except Exception:
+        raise _voice_cloning_failure("could not connect to the voice cloning service") from None
+
+    if status_code in (401, 403):
+        raise _voice_cloning_failure(f"access to the voice cloning service was denied (HTTP {status_code})")
+    if status_code != 200:
+        raise _voice_cloning_failure(f"the voice cloning service returned an error (HTTP {status_code})")
+    if content_type.split(";", 1)[0].strip().lower() != "audio/wav" or not body:
+        raise _voice_cloning_failure("the voice cloning service returned a response that is not audio")
+    output_path.write_bytes(body)
     return True
 
 
@@ -176,11 +259,6 @@
     out_dir.mkdir(exist_ok=True)
     out_path = out_dir / f"{job_id}.wav"
     generated = _synthesize_via_chatterbox_api(text, profile, out_path, str(mode))
-    if mode == "voice_cloning" and not generated:
-        raise HTTPException(
-            status_code=503,
-            detail="Voice cloning service is unavailable. Please retry, or use Google voice narration mode.",
-        )
     if not generated:
         provider = GoogleVoiceProvider()
         provider.generate(text, profile, out_path)
```

### `voice_narration/inference/application.py` — complete final content (473 lines, LF, ASCII, SHA-256 `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`)

```python
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from datetime import datetime, timezone
from pathlib import Path
import httpx
import time

import google.auth.transport.requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from google.oauth2 import service_account

from voice_narration.inference.providers import GoogleVoiceProvider
from voice_narration.inference.providers.google import _load_local_env

ROOT = Path(__file__).resolve().parents[2]
AUDIO_ROOT = ROOT / "audio_storage"
AUDIO_ROOT.mkdir(exist_ok=True)
DB_PATH = AUDIO_ROOT / "generation_jobs.db"
BASE_URL = os.getenv("INFERENCE_BASE_URL", "http://localhost:8003")
CHATTERBOX_API_BASE_URL = os.getenv("CHATTERBOX_API_BASE_URL", "").strip()
VOICE_CLONING_API_BASE_URL = os.getenv("VOICE_CLONING_API_BASE_URL", CHATTERBOX_API_BASE_URL).strip()
GATEWAY_DEFAULT_MODEL_ID = "chatterbox-multilingual-v3"
GATEWAY_ALLOWED_LANGUAGES = {"hi", "en"}
GATEWAY_ALLOWED_MODES = {"narration", "voice_cloning"}
VOICE_CLONING_TIMEOUT_DEFAULT_SECONDS = 600


def _parse_voice_cloning_timeout(raw: str | None) -> int | None:
    value = (raw or "").strip()
    if not value:
        return VOICE_CLONING_TIMEOUT_DEFAULT_SECONDS
    if not (value.isascii() and value.isdigit()):
        return None
    seconds = int(value)
    return seconds if seconds >= 1 else None


VOICE_CLONING_TIMEOUT_SECONDS = _parse_voice_cloning_timeout(os.getenv("VOICE_CLONING_TIMEOUT_SECONDS"))

_gateway_models: dict[str, dict] = {
    GATEWAY_DEFAULT_MODEL_ID: {
        "model_id": GATEWAY_DEFAULT_MODEL_ID,
        "model_version": "v3",
        "license_evidence_uri": None,
        "weights_evidence_uri": None,
        "output_use_evidence_uri": None,
        "runtime_class": "self_hosted",
        "languages_supported": ["hi", "en"],
        "approved_by": None,
        "approved_at": None,
        "state": "draft",
    }
}
_gateway_idempotency: dict[str, dict] = {}


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                voice_profile_id TEXT NOT NULL,
                voice_name TEXT NOT NULL,
                text TEXT NOT NULL,
                status TEXT NOT NULL,
                audio_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


_ensure_db()

app = FastAPI(title="Inference Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _profile_lookup(voice_profile_id: str) -> dict:
    voice_db = ROOT / "audio_storage" / "voice_profiles.db"
    if not voice_db.exists():
        raise HTTPException(status_code=404, detail="Voice registry not initialized")
    with sqlite3.connect(voice_db) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM voice_profiles WHERE id = ?",
            (voice_profile_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Voice profile not found")
    return dict(row)


def _voice_cloning_failure(reason: str) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=f"Voice cloning failed: {reason}. Please retry, or use Google voice narration mode.",
    )


def _voice_cloning_identity_token(audience: str) -> str:
    _load_local_env()
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not key_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")
    info = json.loads(Path(key_path).read_text(encoding="utf-8"))
    if not isinstance(info, dict) or info.get("type") != "service_account":
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS does not name a service-account key")
    credentials = service_account.IDTokenCredentials.from_service_account_info(info, target_audience=audience)
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


def _post_voice_cloning_request(
    url: str, token: str, text: str, language: str, sample: bytes, limit: int, deadline: float
) -> tuple[int, str, bytes]:
    with httpx.Client(timeout=limit) as client:
        with client.stream(
            "POST",
            url,
            headers={"Authorization": f"Bearer {token}"},
            data={"text": text, "language": language},
            files={"sample_audio": ("sample.wav", sample, "audio/wav")},
        ) as response:
            chunks: list[bytes] = []
            for chunk in response.iter_bytes():
                if time.monotonic() >= deadline:
                    raise httpx.ReadTimeout("voice cloning time limit reached", request=response.request)
                chunks.append(chunk)
            return response.status_code, response.headers.get("content-type", ""), b"".join(chunks)


def _synthesize_via_chatterbox_api(text: str, profile: dict, output_path: Path, mode: str) -> bool:
    if mode != "voice_cloning":
        return False
    base_url = VOICE_CLONING_API_BASE_URL
    if not base_url:
        raise _voice_cloning_failure("no voice cloning service is configured")
    limit = VOICE_CLONING_TIMEOUT_SECONDS
    if limit is None:
        raise _voice_cloning_failure("VOICE_CLONING_TIMEOUT_SECONDS must be a positive whole number of seconds")
    sample_path = profile.get("sample_path")
    try:
        if not sample_path:
            raise FileNotFoundError("the voice profile has no stored sample_path")
        sample = Path(sample_path).read_bytes()
    except OSError:
        raise _voice_cloning_failure("the voice sample for this profile could not be read") from None
    try:
        token = _voice_cloning_identity_token(base_url)
    except Exception:
        raise _voice_cloning_failure("could not obtain an identity token for the voice cloning service") from None
    language = str(profile.get("language") or "en").split("-")[0].lower()

    deadline = time.monotonic() + limit
    executor = ThreadPoolExecutor(max_workers=1)
    call = executor.submit(
        _post_voice_cloning_request, f"{base_url}/v1/synthesize", token, text, language, sample, limit, deadline
    )
    executor.shutdown(wait=False)
    try:
        status_code, content_type, body = call.result(timeout=max(0.0, deadline - time.monotonic()))
    except (FutureTimeoutError, httpx.TimeoutException):
        raise _voice_cloning_failure(f"the voice cloning service did not respond within {limit} seconds") from None
    except Exception:
        raise _voice_cloning_failure("could not connect to the voice cloning service") from None

    if status_code in (401, 403):
        raise _voice_cloning_failure(f"access to the voice cloning service was denied (HTTP {status_code})")
    if status_code != 200:
        raise _voice_cloning_failure(f"the voice cloning service returned an error (HTTP {status_code})")
    if content_type.split(";", 1)[0].strip().lower() != "audio/wav" or not body:
        raise _voice_cloning_failure("the voice cloning service returned a response that is not audio")
    output_path.write_bytes(body)
    return True


def _gateway_error(
    status_code: int,
    code: str,
    message: str,
    retryable: bool = False,
    fallback_attempted: bool = False,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "errors": [
                {
                    "code": code,
                    "message": message,
                    "retryable": retryable,
                    "fallback_attempted": fallback_attempted,
                }
            ]
        },
    )


def _execution_fingerprint(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "inference"}


@app.get("/inference/jobs")
def list_jobs() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]


@app.post("/inference/jobs")
def create_job(payload: dict) -> dict:
    text = (payload.get("text") or "").strip()
    voice_profile_id = payload.get("voice_profile_id")
    voice_name = payload.get("voice_name") or "Custom Clone"
    user_id = payload.get("user_id") or "guest"
    mode = payload.get("mode") or "narration"
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    if not voice_profile_id:
        raise HTTPException(status_code=400, detail="voice_profile_id is required")

    profile = _profile_lookup(voice_profile_id)
    if profile.get("status") not in ("approved", "active"):
        raise HTTPException(status_code=403, detail="Voice profile is not available for generation")

    job_id = uuid.uuid4().hex
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_dir = AUDIO_ROOT / "generated"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{job_id}.wav"
    generated = _synthesize_via_chatterbox_api(text, profile, out_path, str(mode))
    if not generated:
        provider = GoogleVoiceProvider()
        provider.generate(text, profile, out_path)

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO jobs (
                id, user_id, voice_profile_id, voice_name, text, status, audio_path,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'completed', ?, ?, ?)
            """,
            (
                job_id,
                user_id,
                voice_profile_id,
                voice_name,
                text,
                str(out_path),
                timestamp,
                timestamp,
            ),
        )
        conn.commit()

    return {
        "id": job_id,
        "status": "completed",
        "audio_url": f"{BASE_URL}/inference/jobs/{job_id}/audio",
        "download_url": f"{BASE_URL}/inference/jobs/{job_id}/audio",
        "voice_profile_id": voice_profile_id,
        "voice_name": voice_name,
    }


@app.get("/inference/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)


@app.get("/inference/jobs/{job_id}/audio")
def job_audio(job_id: str):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    audio_path = Path(row["audio_path"])
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/wav", filename=f"{job_id}.wav")


@app.get("/ai-gateway/v1/models")
def list_gateway_models() -> dict:
    return {"items": [dict(model) for model in _gateway_models.values()]}


@app.post("/ai-gateway/v1/models/{model_id}/approvals")
def approve_gateway_model(model_id: str, payload: dict):
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "Unknown model for approval")

    required_fields = [
        "model_version",
        "license_evidence_uri",
        "weights_evidence_uri",
        "output_use_evidence_uri",
        "runtime_class",
        "languages_supported",
    ]
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return _gateway_error(400, "INVALID_EVIDENCE", "Missing required approval evidence")

    runtime_class = payload.get("runtime_class")
    if runtime_class not in {"self_hosted", "external_api"}:
        return _gateway_error(400, "INVALID_EVIDENCE", "runtime_class must be self_hosted or external_api")

    languages = payload.get("languages_supported")
    if not isinstance(languages, list) or not languages:
        return _gateway_error(400, "INVALID_EVIDENCE", "languages_supported must be non-empty")

    model["model_version"] = payload["model_version"]
    model["license_evidence_uri"] = payload["license_evidence_uri"]
    model["weights_evidence_uri"] = payload["weights_evidence_uri"]
    model["output_use_evidence_uri"] = payload["output_use_evidence_uri"]
    model["runtime_class"] = runtime_class
    model["languages_supported"] = languages
    model["approved_by"] = payload.get("approved_by")
    model["approved_at"] = payload.get("approved_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    model["state"] = "approved"
    return JSONResponse(status_code=201, content=dict(model))


@app.post("/ai-gateway/v1/models/{model_id}/enable")
def enable_gateway_model(model_id: str, payload: dict):
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "Unknown model")

    model_version = payload.get("model_version")
    if not model_version or model_version != model.get("model_version"):
        return _gateway_error(409, "MODEL_STATE_CONFLICT", "Model version mismatch")

    if model.get("state") != "approved":
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Model is not approved for enablement")

    if model.get("runtime_class") != "self_hosted":
        return _gateway_error(403, "RUNTIME_POLICY_VIOLATION", "Runtime must be self_hosted")

    if any(not model.get(field) for field in ("license_evidence_uri", "weights_evidence_uri", "output_use_evidence_uri")):
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Commercial evidence is incomplete")

    model["state"] = "enabled"
    return dict(model)


@app.post("/ai-gateway/v1/executions")
def create_gateway_execution(payload: dict):
    idempotency_key = (payload.get("idempotency_key") or "").strip()
    if not idempotency_key:
        return _gateway_error(400, "IDEMPOTENCY_KEY_REQUIRED", "idempotency_key is required")

    mode = payload.get("mode")
    if mode not in GATEWAY_ALLOWED_MODES:
        return _gateway_error(400, "INVALID_INPUT", "mode must be narration or voice_cloning")

    text = (payload.get("text") or "").strip()
    if not text:
        return _gateway_error(400, "INVALID_INPUT", "text is required")

    language = payload.get("language")
    if language not in GATEWAY_ALLOWED_LANGUAGES:
        return _gateway_error(400, "UNSUPPORTED_LANGUAGE", "language must be hi or en")

    model_id = payload.get("model_hint") or GATEWAY_DEFAULT_MODEL_ID
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "No routing candidate for requested model")

    if model.get("state") != "enabled":
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Selected model is not enabled")

    if model.get("runtime_class") != "self_hosted":
        return _gateway_error(403, "RUNTIME_POLICY_VIOLATION", "Selected model runtime is not self-hosted")

    if language not in model.get("languages_supported", []):
        return _gateway_error(400, "UNSUPPORTED_LANGUAGE", "Selected model does not support requested language")

    fingerprint = _execution_fingerprint(payload)
    existing = _gateway_idempotency.get(idempotency_key)
    if existing:
        if existing["fingerprint"] != fingerprint:
            return _gateway_error(409, "IDEMPOTENCY_CONFLICT", "idempotency key used with different request")
        return existing["response"]

    voice_profile_id = payload.get("voice_profile_id")
    if not voice_profile_id:
        return _gateway_error(400, "INVALID_INPUT", "voice_profile_id is required")

    voice_name = payload.get("voice_name") or "Custom Clone"
    user_id = payload.get("user_id") or "guest"
    started = time.perf_counter()

    try:
        job = create_job(
            {
                "text": text,
                "voice_profile_id": voice_profile_id,
                "voice_name": voice_name,
                "user_id": user_id,
                "mode": mode,
            }
        )
    except HTTPException as exc:
        if exc.status_code == 503:
            detail = exc.detail if isinstance(exc.detail, str) else "Model execution path unavailable"
            return _gateway_error(503, "MODEL_UNAVAILABLE", detail, retryable=True)
        return _gateway_error(503, "MODEL_UNAVAILABLE", "Model execution path unavailable", retryable=True)

    elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
    cost_estimate_usd = f"{elapsed_ms * 0.000001:.6f}"

    response = {
        "execution_id": job["id"],
        "status": "completed",
        "audio_url": job["audio_url"],
        "routing": {
            "selected_model_id": model["model_id"],
            "selected_model_version": model["model_version"],
            "policy_name": "default-chatterbox-route",
            "policy_revision": "v1",
            "decision_reason": "model_hint_or_default",
            "fallback_applied": False,
            "fallback_from_model_id": None,
        },
        "usage": {
            "latency_ms": elapsed_ms,
            "queue_ms": 0,
            "compute_ms": elapsed_ms,
            "cost_estimate_usd": cost_estimate_usd,
            "runtime_class": model["runtime_class"],
        },
        "errors": [],
    }
    _gateway_idempotency[idempotency_key] = {"fingerprint": fingerprint, "response": response}
    return JSONResponse(status_code=202, content=response)
```

### Mapping of RED tests to the change

| RED tests (CRM-4) | Satisfied by |
| --- | --- |
| C4-T1, C4-T2, C4-T3 (multipart parts, sample bytes, no `sample_path`, token grant and audience, base URL in effect, local save) | Changes 4, 5, 6.5, 6.11 |
| C4-T4, RF-14 (CFR-1) | Change 6.1 |
| C4-T5, C4-T6, C4-T13 (CFR-2; narration unaffected; read at start) | Changes 2, 6.2; narration path unchanged (change 7) |
| C4-T7 (CFR-3) | Change 6.3 |
| C4-T8 (CFR-4) | Changes 4, 6.4 |
| C4-T9, C4-T10, C4-T11, C4-T12 (CFR-5, time limit span, default `600`, accepted forms) | Changes 2, 5, 6.5, 6.6 |
| C4-T14 (CFR-6) | Change 6.7 |
| C4-T15, C4-T20 (CFR-7, also over real transport) | Change 6.8 |
| C4-T16 (CFR-8) | Change 6.9 |
| C4-T17, C4-T18 (CFR-9; media type matching) | Changes 6.10, 6.11 |
| C4-T19 (order CFR-1 → CFR-4, before any connection) | Change 6 order |
| RF-15 (gateway telemetry on the voice cloning path) | Changes 4, 5, 6; gateway unchanged (change 8) |

## Execution Steps

1. Confirm this plan's Human Review status records approval.
2. Run `git status --short` and confirm no tracked file under `voice_narration/` or `tests/` is modified. Confirm `git diff --quiet HEAD -- voice_narration/ tests/` exits `0`. Confirm `git show HEAD:voice_narration/inference/application.py | sha256sum` prints `9d55caf9b6ff2111418e7e824608bd7bd286b1179fae806f9ac98b5373ea1caf`. If any check fails, stop and report.
3. Run C5-V1 (before the change) and confirm the five test-file hashes listed under Preconditions / Predecessor Evidence. If a hash differs, stop and report.
4. Replace the content of `voice_narration/inference/application.py` with exactly its complete final content above, with LF line endings (ASCII). Confirm `sha256sum voice_narration/inference/application.py` prints `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`. Confirm that `diff -u` from `git show HEAD:voice_narration/inference/application.py` to the new file matches the plan's unified diff. Git may print a warning that LF will be replaced by CRLF, because `core.autocrlf` is `true`; that warning is expected and changes no content. If the hash differs, stop and report.
5. Run C5-V2, then C5-V3 (repeat, no cleaning), then C5-V4.
6. Run C5-V1 again (after the change), then C5-V5, C5-V6 and C5-V7.
7. Record the evidence in `Plan.md` below the Execution Status table and update only the CRM-5 row, as the PDD workflow requires.

## Acceptance / Completion Criteria

- C5-AC-1: `voice_narration/inference/application.py` has exactly the complete final content above (SHA-256 `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`). No other file is created, modified or deleted, apart from this milestone's Execution Status update in `Plan.md` and this plan's Human Review status. In particular, the five test files keep the hashes listed under Preconditions / Predecessor Evidence, and `voice_narration/inference/providers/google.py`, `voice_narration/chatterbox_api/`, `voice_narration/simple_voices/`, `frontend/`, `requirements-dev.txt`, `pytest.ini`, `cloudrun/` and `docs/developer-setup.md` do not change.
- C5-AC-2: the full suite collects 71 tests and all 71 pass. These are the 51 tests that failed at CRM-4 (the 49 cases of `tests/test_inference_client_red.py`, RF-14 and RF-15) and the 20 that passed there: the 13 CRM-2 tests, the 5 gateway tests, `test_voice_enrollment_creates_profile` and the preserved narration test `test_generation_uses_selected_voice_profile` (`Plan.md` CRM-5 success criteria, CCR-2 preserved row). There is no `FAILED` or `ERROR` line.
- C5-AC-3: a second full run without cleaning gives the same result: 71 collected, 71 passed.
- C5-AC-4: the generic message "Voice cloning service is unavailable" no longer occurs anywhere under `voice_narration/` (CCR-8 "replacing today's single generic message").

## Verification

### Commands

Run from the repository root (Windows, the Plan's Verification Commands; on Linux use `.venv/bin/python`):

- C5-V1: `sha256sum tests/_chatterbox_boundary.py tests/test_inference_client_red.py tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py tests/test_chatterbox_service_red.py voice_narration/inference/application.py` (Git Bash or Linux), or `certutil -hashfile <file> SHA256` for each file (Windows). Before the change, `application.py` is the CRLF working-tree file and its hash is not compared; the committed hash is checked in step 2.
- C5-V2: `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C5-V3: `.\.venv\Scripts\python.exe -m pytest tests -ra` (second run, no cleaning between runs; required because the tests write files and databases, override environment variables and `sys.modules`, and patch `socket` and `httpx`)
- C5-V4: `.\.venv\Scripts\python.exe -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py::test_voice_cloning_returns_guidance_when_clone_backend_unavailable tests/test_ai_gateway_telemetry_red.py -q` (the 51 CRM-4 RED tests on their own)
- C5-V5: `git status --short`
- C5-V6: `git diff --stat`
- C5-V7: `git grep -n "Voice cloning service is unavailable" -- voice_narration` (C5-AC-4; expected to print nothing and exit `1`)

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- C5-V1 after the change: the five test-file hashes unchanged, and `application.py` `4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088`.
- C5-V2 and C5-V3: exit code `0`; `collected 71 items`; summary `71 passed, 1 warning` (the existing `StarletteDeprecationWarning` from `fastapi/testclient.py`); no `FAILED` or `ERROR` line.
- C5-V4: exit code `0`; `51 passed, 1 warning`.
- C5-V5: exactly ` M voice_narration/inference/application.py`, plus this Implementation Plan (`??` until committed) and ` M docs/.ai/chatterbox-cloud-run/Plan.md` after the status update.
- C5-V6: `voice_narration/inference/application.py` is the only file listed before the status update: `1 file changed, 95 insertions(+), 17 deletions(-)` (the counts of `+` and `-` lines in the plan's unified diff). Git may count differently if it aligns lines differently. C5-AC-1 is judged by the hash.
- C5-V7: no output, exit code `1`.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. Run on 2026-11-10 in a disposable copy outside the repository. The copy was made with `tar` from the working tree at `575e85e` into `C:\Users\avina\AppData\Local\Temp\claude\dd431ff1ad187051\a64835d9-b6b8-4c46-a2ab-81eb4d20b4b6\scratchpad\crm5\repo`. It excluded `.venv`, `.git`, `Voice-Narration.zip`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache` and `.deepeval`, and included the git-ignored `.env` and `service-account-key.json`, which the preserved narration test needs. The repository's `.venv` interpreter was used with the copy as working directory and `-p no:cacheprovider`. The file written into the copy is the one whose content and hash appear above. It was produced by a scratch script that applied exactly the four replacements of changes 1–7 to `git show HEAD:voice_narration/inference/application.py`. The diff and the complete content in this plan were embedded from that output.

1. Unmodified baseline in the copy (the CRM-4 RED state):

   ```
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 1)
   E         {'detail': 'Voice cloning service is unavailable. Please retry, or use Google voice narration mode.'} != {'detail': 'Voice cloning failed: access to the voice cloning service was denied (HTTP 403). Please retry, or use Google voice narration mode.'}
   ================== 51 failed, 20 passed, 1 warning in 29.42s ==================
   51                                                       (count of FAILED lines)
   ```

2. Proposed `application.py` applied. GREEN run 1 (C5-V2):

   ```
   $ python -m pytest tests -ra -p no:cacheprovider        (exit 0)
   collected 71 items
   tests\test_ai_gateway_red.py .....                                       [  7%]
   tests\test_ai_gateway_telemetry_red.py .                                 [  8%]
   tests\test_chatterbox_service_red.py .............                       [ 26%]
   tests\test_clone_flow.py ...                                             [ 30%]
   tests\test_inference_client_red.py ..................................... [ 83%]
   ======================= 71 passed, 1 warning in 40.19s ========================
   ```

3. GREEN run 2 (C5-V3), without cleaning, with `--durations=8` added to read the timing margins of C4-D-10:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider --durations=8        (exit 0)
   collected 71 items
   2.36s call     tests/test_inference_client_red.py::test_unreachable_chatterbox_answers_cfr6[connection-refused]
   1.87s call     tests/test_inference_client_red.py::test_identity_token_time_is_not_counted_toward_time_limit
   1.55s teardown tests/test_inference_client_red.py::test_time_limit_bounds_wait_for_chatterbox_response
   1.25s call     tests/test_inference_client_red.py::test_time_limit_bounds_wait_for_chatterbox_response
   1.18s call     tests/test_inference_client_red.py::test_time_limit_bounds_complete_response_not_each_read
   1.08s call     tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[503]
   1.03s call     tests/test_inference_client_red.py::test_chatterbox_error_status_answers_cfr8[500]
   1.00s call     tests/test_chatterbox_service_red.py::test_synthesize_serves_concurrent_requests_one_at_a_time
   ======================= 71 passed, 1 warning in 43.97s ========================
   ```

   The one warning is `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated` from `fastapi/testclient.py:1`, as at CRM-3 and CRM-4. C4-T9's call took 1.25 s (threshold `< 2.2` s), C4-T10's 1.18 s (`< 2.5` s), C4-T11's 1.87 s (`>= 1.5` s). Why the CFR-8 `500` and `503` cases take about 1 s was not investigated; no threshold applies to them.

4. C5-V4, the CRM-4 RED tests on their own, plus the rest of `tests/test_clone_flow.py`:

   ```
   $ python -m pytest tests/test_inference_client_red.py tests/test_clone_flow.py tests/test_ai_gateway_telemetry_red.py -q -p no:cacheprovider        (exit 0)
   53 passed, 1 warning in 40.56s
   ```

   This ran all of `tests/test_clone_flow.py` (3 tests) rather than the single RF-14 test of C5-V4, so it shows 53 and not 51. C5-V4 itself selects only RF-14 from that file.

5. Diff check: the unified diff above was applied with `patch -p1` to a fresh copy of the committed file:

   ```
   patching file voice_narration/inference/application.py
   4a98dafc04c18efce33225ce04d475da63fe43acf4c6e7f664e18f96b52c1088 *voice_narration/inference/application.py
   ```

   The patched file has the same hash as the complete final content. A search of the new file for non-ASCII bytes found none.

6. Repository search for completeness (read-only, in the repository): `_synthesize_via_chatterbox_api` is defined at `application.py:99` and called only at `:178`; "Voice cloning service is unavailable" occurs only at `application.py:182`, which this change removes; `VOICE_CLONING_TIMEOUT` occurs only in `tests/test_inference_client_red.py`. Nothing outside `application.py` needs to change.

7. Not run in the dry run: C5-V5, C5-V6 and C5-V7 depend on the repository's Git state after execution and were not run against the copy, which has no `.git`.

8. Created during the dry run, all under `C:\Users\avina\AppData\Local\Temp\claude\dd431ff1ad187051\a64835d9-b6b8-4c46-a2ab-81eb4d20b4b6\scratchpad\crm5`, and deleted afterwards: `repo\` (the disposable copy), `src\` (the committed `application.py`, the scratch build script, the proposed file, the diff, the template and scripts used to embed them into this plan and extract them again), `apply\` and `apply2\` (diff-apply checks, the second applying the diff extracted from this plan), `ex\` (the code blocks extracted from this plan, byte-identical to the proposed file and diff), and the run logs `baseline.log`, `green1.log`, `green2.log`. Nothing was written to the repository except this Implementation Plan.

## Risks

- C5-RSK-1 — Identity comparisons (`security`). The inference service makes no authorization decision of its own; it presents an identity that Cloud Run checks. The comparisons involved:
  - Token audience against the Chatterbox URL. The audience is the module global `VOICE_CLONING_API_BASE_URL`, the base URL in effect (configured value with surrounding whitespace removed, `application.py:23-24`, unchanged). The call URL is built from the same string (`f"{base_url}/v1/synthesize"`), so both use one canonical form, as the contract fixes it (Settings row 1, CCD-4). No case folding or trailing-slash normalization is applied to either. Cloud Run compares the token's audience with its own service URL. A configured URL that differs from it, for example by a trailing `/`, is rejected there and answered as CFR-7. That is deployment behavior, documented by CRM-6.
  - Service-account identity. The assertion's `iss` is the key file's `client_email`, set by `google-auth` from the same file the key is read from. The key type check compares `type` exactly with `service_account`, the value Google key files carry. The real account's IAM invoker check is Cloud Run's.
  - The `Authorization` header is sent exactly as `Bearer <token>`, as the contract writes it.
  - No user identity, role or ownership comparison exists: login and authentication of application users are excluded (requirements Explicit Exclusions).
- C5-RSK-2 — Secrets. The identity token and the key file's contents are not logged and not placed in any answer. Every CFR message is a fixed string, apart from the time limit and the status code. Exception text is never included (each failure is raised `from None` with a fixed reason). The token is sent to whatever scheme the base URL names. The contract does not restrict the scheme, so an `http://` base URL would send the token unencrypted. The documented Cloud Run service URL is `https://` (CRM-6 scope). This plan adds no scheme check, because no approved artifact defines one.
- C5-RSK-3 — `.env` side effect (C5-D-2). A cloning call copies missing `.env` keys into the process environment, as a narration job already does. The `.env` defines `INFERENCE_BASE_URL` among other keys. `BASE_URL` is read only at import (`application.py:22`), so a running service is unaffected. In the test session, later fresh imports may read it; the tests check only the end of `audio_url` (`tests/test_inference_client_red.py:165`). The dry run passed twice with the local `.env` present.
- C5-RSK-4 — Abandoned worker after a timeout (C5-D-3). After CFR-5 the worker thread can stay connected until the next body chunk, a single network wait of up to `limit` seconds, or the response. It writes nothing: the body is written to disk only by the request thread, after a success. Chatterbox's generation of the abandoned request is not cancelled in any design, because CRM-3's Chatterbox runs it in its thread pool under a lock (Implementation Plan 002, C3-D-3). A retried request therefore waits behind it, within its own time limit (contract Concurrency: "Waiting time counts toward the caller's time limit").
- C5-RSK-5 — Timing (carried from C4-RSK-4). C4-T9, C4-T10 and C4-T11 depend on wall-clock margins. The dry run measured 1.25 s, 1.18 s and 1.87 s against `< 2.2`, `< 2.5` and `>= 1.5` s. On a heavily loaded machine a correct implementation could exceed a threshold; that is a hypothesis, not observed. If it happens at execution, it is a finding to report. No rerun until it passes and no threshold change is authorized.
- C5-RSK-6 — Network-dependent preserved test (carried from C4-RSK-7). `test_generation_uses_selected_voice_profile` calls Google TTS with the local key. If it fails at execution for network or credential reasons, C5-AC-2 is not met; execution stops and reports it. No rerun until it passes, no skip and no change is authorized.
- C5-RSK-7 — Undeclared packages (`Plan.md` RSK-6). `google-auth` and `requests` are now imported directly but stay undeclared in `requirements-dev.txt`. They are installed only because of `google-cloud-texttospeech`, which is itself undeclared. An environment built from `requirements-dev.txt` alone would fail to import the inference application, and it already fails today at `providers/google.py:8`. `Plan.md` keeps dependency declarations out of scope.
- C5-RSK-8 — Windows connection-refused timing (carried from C4-RSK-5). C4-T14 `connection-refused` took 2.36 s. The default limit `600` applies there, so it cannot become CFR-5.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Restore the one changed file with `git restore -- voice_narration/inference/application.py`. No other file is changed by this milestone. Do not use repository-wide reset, clean or checkout operations.

## Explicitly Out of Scope

- Any test change, including the five test files listed under Preconditions / Predecessor Evidence (CRM-4 tests bind this milestone).
- Chatterbox (`voice_narration/chatterbox_api/`), the voices service, the frontend, the narration provider (`voice_narration/inference/providers/`) and the narration path (`Plan.md` CRM-5 exclusions).
- Any AI Gateway contract or gateway code change (the `503` pass-through at `application.py:363-366` is unchanged).
- User login or authentication.
- Logging, metrics or alerts; duplicate detection; token caching; a request-size limit; a URL-scheme check.
- Dependency declarations, `requirements-dev.txt`, `pytest.ini`, container, deployment and documentation changes (CRM-6 for the deployment document).

## Human Review

Status: Approved by avinash2196 on 2026-11-10 ("Approve plan"). Executed on 2026-11-10: GREEN verified (C5-AC-1–C5-AC-4 met; see `Plan.md` "CRM-5 Execution Evidence").
