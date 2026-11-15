# Implementation Plan

## Milestone

OAM-4 — Inference service RED (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-4, `Plan.md:177-195`), under the Plan revision approved on 2026-11-13. This plan replaces `003_Implementation_Plan_OAM-4.md`, which the Plan revision superseded (`Plan.md:47`, `:358`).

## Milestone Type

RED

## Review Summary

- Behavior change: tests only.
- Requirements verified (not delivered): COA-1 (inference part, including the provider list), COA-5 (language choice taken), COA-7 and COA-8 on the four pre-call causes, COA-13 (waiting). Contract rules are mapped under Contract Rule Coverage.
- Files: created `tests/test_inference_provider_choice_red.py`; modified none; deleted the untracked `tests/test_chatterbox_generation_red.py` (the 003 fake-Chatterbox file), after a hash check.
- Tests added: 36 (5 functions, 2 of them parametrized). They prove the per-generation provider choice and its `400` answers, the four pre-call messages in contract order with no fallback and nothing saved, Chatterbox in the provider list, and that a second request waits. None fakes or calls Chatterbox.
- Verification: `python -m pytest tests/test_inference_provider_choice_red.py -q --tb=short`, twice. Expected / Predicted — Not Yet Verified: `36 failed` each time, in 4 classes (22, 12, 1, 1). Then the 5 preserved files: `29 passed`.
- Needs attention: N4D-2 (the network guard), N4D-5 (the database refused through `SessionLocal` and `create_all_tables`), N4D-6 (deleting the 003 file), and 003's Human Review status, now marked superseded.

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13, revision recording Q46–Q48 (`requirements.md:17`) |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13, as written, folding in Q46–Q48 and V3Q-3 (`Plan.md:5`). OAM-4 row: `Pending`, "`003_Implementation_Plan_OAM-4.md` is superseded and not executed; a new Implementation Plan is required" (`Plan.md:358`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` (OAM-1 deliverable, authoritative predecessor) | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 row Complete (`Plan.md:355`) |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | Approved by Avinash Srivastava on 2026-11-13, executed (`001_Implementation_Plan_OAM-2.md:669`) |
| `docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` | Revision 4 approved by Avinash Srivastava on 2026-11-13, executed (`002_Implementation_Plan_OAM-3.md:801`) |
| `docs/.ai/chatterbox-original-app/003_Implementation_Plan_OAM-4.md` | Its Human Review read "Approved by Avinash Srivastava on 2026-11-13, as written, including decisions V4D-1 to V4D-10" (`:979`), but the approved Plan revision records it as superseded and not executed (`Plan.md:47`, `:358`). This planning run changed that status line to `Superseded — not executed`, pointing to this plan. Read for its harness code and its dry-run finding on client timing; none of its decisions is carried forward |
| Reference contract `feature/voice-cloning@abbe387:docs/.ai/chatterbox-cloud-run/API-Contract.md` | Not read. No OAM-4 test reaches the Chatterbox Synthesize or Caller Identity interfaces (COA-16, `Plan.md:194`) |
| Product-level `docs/requirements.md` | Does not exist (checked `docs/`) |

## Carried-Forward Decisions

- **V2D-1** (`001_Implementation_Plan_OAM-2.md:99-106`), delivered by OAM-3 (`voice_narration/simple_voices/application.py:68`): the voice service is built as `create_app(*, root, clock)`. The tests host the real OAM-3 voice service with `root=<tmp>`, so they never touch the default `voice_storage/` (**V3D-1**, `002_Implementation_Plan_OAM-3.md:124-130`).
- **V2D-6** (`001_Implementation_Plan_OAM-2.md:124`): new fixed error bodies go over a real uvicorn server on a dynamically allocated port. Every request in this milestone goes over real loopback transport (N4D-3).
- **V3Q-3** (`002_Implementation_Plan_OAM-3.md:736`): `tests/test_persistence.py`, `tests/test_authentication_consent.py` and `tests/test_voice_enrollment.py` are left out of every whole-suite check (OAV-2, `Plan.md:343`). RED runs no full suite (`prompt-driven-development` Test Scope); the one whole-suite command here, the collection check (command 6), uses the same three `--ignore` options.
- **OAV-3 handling** (`002_Implementation_Plan_OAM-3.md:596-597`): after a test run writes to tracked `audio_storage/`, the output is recorded, then `git checkout -- audio_storage` and `git clean -fd -- audio_storage` restore it.

003's decisions V4D-1 to V4D-10 are not carried forward: the Plan revision supersedes that plan (`Plan.md:47`). Where this plan reuses a mechanism 003 also used (loopback uvicorn threads, a recording startup provider), it is listed again below as this plan's own decision for review.

## Preconditions / Predecessor Evidence

- `Plan.md` Status records approval (`Plan.md:5`). OAM-4 is recorded as RED (`Plan.md:181`), with predecessor OAM-3 (`Plan.md:182`). No FOUNDATION precedes it (`Plan.md:123`, `:191`).
- OAM-3 is `Complete — GREEN verified 2026-11-13` (`Plan.md:357`). Its evidence (`Plan.md:435-455`): the 11 OAM-2 tests passed twice; the OAV-2 suite collected 82 tests and failed only on the accepted `test_production_inference_module_missing`; `audio_storage` was restored. It is committed as `0465867`.
- OAM-4 Execution Status is `Pending` (`Plan.md:358`). The only other OAM-4 Implementation Plan is the superseded 003, never executed (no OAM-4 evidence in `Plan.md`). The folder holds `requirements.md`, `Plan.md`, `API-Contract.md` and `001`–`003`, so this plan is `004`.
- Repository state, inspected 2026-11-13: HEAD `059102c`, branch `claude/chatterbox-original-app-client-a3ef0e`. `git status --short` printed exactly `?? tests/test_chatterbox_generation_red.py`. That file is the one the Plan names (`Plan.md:47`): `tr -d '\r' < tests/test_chatterbox_generation_red.py | sha256sum` printed `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948`, which is also the hash of 003's code block (`003_Implementation_Plan_OAM-4.md:182-850`, CR removed). No other unrecorded change exists.
- No `.env`, `.env.local` or `.env.production` exists in the worktree (`ls -a`: only `.env.example`).
- Prerequisites (`Plan.md:191`), checked in the Python on PATH (`finnie-chat\venv`, Python 3.14.3): pytest 9.1.1, httpx 0.28.1, uvicorn 0.54.0 and fastapi 0.162.0, all pinned in `requirements-dev.txt:1-5`. The new tests are synchronous and import nothing else outside the standard library and the repository, so neither the undeclared `pytest-asyncio` nor google-auth is needed (Plan OAR-4). No FOUNDATION is needed.

## Current Repository State

- `voice_narration/inference/application.py:392-414`: `create_app(*, provider=None, …)`; the tests inject the startup provider through `provider` (N4D-4).
- `voice_narration/inference/application.py:461-479`: the generation route reads only `script` and `voice_id` (`:462-463`) and calls the startup provider for every request (`:471`, `:292`). `provider` and `language` are ignored, so a Chatterbox request is generated by the mock and answered `200` (seen in the dry run).
- No waiting exists: the route awaits the provider with no lock (`:471`, `:292`); `grep -rn "Lock\|Semaphore\|CHATTERBOX\|VOICE_SERVICE_URL" voice_narration/inference/` finds nothing.
- `voice_narration/inference/application.py:87-93`: `InferenceState` reads `AUDIO_STORAGE_PATH`, and `storage_root` (`:96-98`) exposes the value in force. The tests point it at `tmp_path` and assert it.
- `voice_narration/inference/application.py:22`, `:107-111`, `:151-179`: database use goes through the module names `create_all_tables` and `SessionLocal`, and every exception is swallowed (`:110-111`, `:178-179`). `voice_narration/inference/db.py:19-28` defaults to a local PostgreSQL URL (N4D-5).
- `voice_narration/inference/db.py:14-16`: `.env`, `.env.local` and `.env.production` are loaded once, at import, without overriding values already set (python-dotenv default). This is the path Plan OAR-8 names (`Plan.md:466`).
- `voice_narration/inference/application.py:343-373`: the provider list holds the registry's providers with the baseline descriptions (`:356-363`), sorted by name (`voice_narration/inference/registry.py:60`).
- `voice_narration/inference/providers/mock.py:57-76`: `MockInferenceProvider.generate` returns a silent WAV; `StartupProvider` extends it (N4D-4).
- `voice_narration/simple_voices/application.py:68`, `:184-185`: `create_app(*, root=None, clock=None)` and `GET /voices/{voice_id}/sample` (OAM-3).
- `voice_narration/inference/application.py:623`: `app = create_app()` runs at import. This is pre-existing (N4R-5).
- `tests/` has no `conftest.py`. `pytest.ini:2`: `--strict-config --strict-markers`. The new file uses no marker.

## Files in Scope

### Files to Create

- `tests/test_inference_provider_choice_red.py`

### Files to Modify

None.

### Files to Delete

- `tests/test_chatterbox_generation_red.py` (untracked; never committed). Deleted only when its hash, CR removed, is `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948` (Execution Step 2, N4D-6).

## Proposed Changes

1. **Delete `tests/test_chatterbox_generation_red.py`** (N4D-6). It holds 003's 56 tests, which run a local stand-in for Google's token endpoint and for the deployed Chatterbox (`003_Implementation_Plan_OAM-4.md:349-429`). Requirements COA-16 (`requirements.md:72`) forbids faking Chatterbox, and the Plan states the file is not evidence for any milestone (`Plan.md:47`). Left in place, it would be collected by every later backend run, including OAV-2 at OAM-5 and OAM-7.
2. **Create `tests/test_inference_provider_choice_red.py`.** It holds:
   - **Constants:** the contract's exact strings `NOT_CONFIGURED`, `INVALID_TIME_LIMIT`, `SAMPLE_UNREADABLE`, `TOKEN_UNAVAILABLE` (OAF-1–OAF-4, `API-Contract.md:338-341`), `UNSUPPORTED_PROVIDER`, `UNSUPPORTED_LANGUAGE`, `MISSING_FIELDS` (`:288-290`), `CHATTERBOX_DESCRIPTION` and `BASELINE_DESCRIPTIONS` (`:450-451`, `application.py:356-361`), `CLOSING`; `PRELOADED_VOICE`, `UNKNOWN_VOICE`, `UNUSABLE_URL = "http://127.0.0.1:0"` (N4D-1), `SETTINGS_REMOVED`; and the placeholders `MISSING_KEY`, `NOT_JSON_KEY`, `AUTHORIZED_USER_KEY`, `PADDED_VOICE_SERVICE_URL`.
   - **Audio:** `pcm_wav()` and `VOICE_SAMPLE`, the uploaded voice sample.
   - **Guard helpers:** `host_name(host)` and `is_on_this_machine(name)` (N4D-2).
   - **`StartupProvider(MockInferenceProvider)`:** an optional delay; it records each call's voice and start and end times, the in-flight count and the maximum in-flight count, and returns the real mock's audio (N4D-4).
   - **`RefusingDatabase`:** `refuse()` counts each use and raises (N4D-5).
   - **Servers and helpers:** `serve(app)` runs uvicorn in a daemon thread on a socket bound to `127.0.0.1:0` before the server starts, and stops it on exit (N4D-3); `upload_voice()`, `generate()`, `wait_until()` and `post_in_background(client, …)`, which records each answer and when it arrived (N4D-7).
   - **`Harness`:** `resolve` turns the placeholders into files under `tmp_path` or the padded voice-service URL; `settings` sets or removes environment variables through `monkeypatch`; `voice` maps a name to a voice id; `inference(startup)` builds `create_app(provider=startup)`, asserts the storage root in force, and serves it; `stored_files` lists the audio files under `tmp_path / "audio"`.
   - **Fixtures:** the autouse `stay_on_this_machine` guard (N4D-2); module-scoped `voices`, the real OAM-3 voice service over a temporary root, with one uploaded voice and one deleted voice, whose sample is fetched once to show it is readable; per-test `harness`, which refuses the database and sets or removes every setting the tests depend on (N4D-1, N4D-5).
   - **The 5 test functions** listed under Contract Rule Coverage.
3. No production, build, configuration or existing test file changes.

### Decisions for Review (binding OAM-5)

- **N4D-1 No Chatterbox stand-in, and settings that leave no path to a call (COA-16, Plan OAR-8).**
  - No test runs anything that answers as Chatterbox or as Google. The only servers are the inference app and the real OAM-3 voice service.
  - `GOOGLE_APPLICATION_CREDENTIALS` is, in every test, removed, blank, a missing file, a file that is not JSON, or an authorized-user key file. None names a service-account key, so contract step 3 (the identity token, `API-Contract.md:321`) cannot succeed, and step 4 (the call, `:322-327`) cannot be reached.
  - `CHATTERBOX_URL` is removed, `""`, `"   "` or `http://127.0.0.1:0`. It is never the deployed URL. Port 0 cannot be connected to: in the dry run the same value as `VOICE_SERVICE_URL` gave OAF-3 under the probe, so a request to it failed on this machine.
  - The per-test settings are listed under Risks, N4R-3.
  - Alternatives:
    - (a) A closed loopback port, as 003 did (`closed_port_url`). Rejected: another process can take the port between choosing and using it (003 V4R-4).
    - (b) A host under `.invalid`. Rejected: reaching it needs a name lookup, so the safety would rest on the guard alone, not on the settings.
- **N4D-2 Network guard: every name lookup of a host outside this machine is blocked, recorded and fails the test.**
  - The autouse fixture replaces `socket.getaddrinfo` for the test's duration. `localhost` and loopback addresses pass. Any other host raises `socket.gaierror("blocked by the OAM-4 tests: …")`, is recorded, and fails the test at teardown.
  - Reason: Plan OAR-8. The harness removes or sets each setting after `db.py:14-16` has loaded any `.env` file. If an OAM-5 change loaded `.env` again, a removed `CHATTERBOX_URL` or `GOOGLE_APPLICATION_CREDENTIALS` could come back with the user's real values. The guard then stops the lookup of the deployed host name (CON-5) or Google's token host before any packet leaves the machine.
  - Dry-run evidence: a scratch check showed the guard blocks `socket.getaddrinfo`, a synchronous `httpx.Client` and an asynchronous `httpx.AsyncClient` lookup, and lets `127.0.0.1` and `localhost` through. With a scratch `.env` naming the deployed URL, the tests passed under the probe with no lookup recorded.
  - What it does not check: an asynchronous connection to a numeric non-loopback address. Whether such a connection passes through `socket.getaddrinfo` was not established. No setting in these tests names one, and the deployed service and Google's endpoints are host names (N4R-2).
  - It binds OAM-5 to make no lookup outside the machine while answering the four pre-call causes. One example: google-auth's `fetch_id_token_credentials` falls back to the metadata server when `GOOGLE_APPLICATION_CREDENTIALS` is absent or not a service-account key (installed google-auth 2.62.1, `google/oauth2/id_token.py:297-349`). That fallback would be blocked and fail these tests. This matches the contract, which gets the token only from the key file that `GOOGLE_APPLICATION_CREDENTIALS` names (`API-Contract.md:321`, `:341`, `:475`).
  - Alternatives:
    - (a) No guard; rely on the settings. Rejected for the `.env` re-load path above.
    - (b) Fail whenever a `.env` file exists at the repository root. Rejected: once the user creates the OAM-8 settings, every backend run would fail on the user's machine.
    - (c) A socket-blocking pytest plugin. Rejected: it is a new dependency that no approved artifact names.
- **N4D-3 Real loopback transport.**
  - The inference app and the voice service each run under uvicorn in a thread of the test process, on a socket bound to `127.0.0.1` port 0 before the server starts. Clients use `httpx.Client(trust_env=False)`.
  - The inference app is created after the test sets its settings. This binds OAM-5 to read the settings from the process environment when `create_app` runs, as the contract states (`API-Contract.md:469`); reading them on each request would also pass.
  - Alternatives:
    - (a) `TestClient` for the inference app. Rejected: the waiting test needs concurrent connections, and the testing skill asks for real transport for fixed error bodies. The voice service has to be reachable over HTTP anyway (`:320`).
    - (b) Subprocesses. Rejected: the startup provider and the database refusal cannot be injected into them.
- **N4D-4 Startup provider: the real mock, recorded.** `create_app(provider=StartupProvider())` uses the existing injection point (`application.py:392-414`). `StartupProvider` returns `MockInferenceProvider`'s own audio and adds a call record and an optional delay. It is not a stand-in for Google: the contract makes `"google"`, absent, `null` and `""` use the startup provider, which is the mock when the service started with it (`API-Contract.md:279-280`). So real Google is never called. Alternative: plain `MockInferenceProvider`, comparing saved audio. Rejected: it cannot show that one generation waited for another without a delay and an in-flight count.
- **N4D-5 The database is refused.**
  - Each test replaces `voice_narration.inference.application.SessionLocal` and `.create_all_tables` with `RefusingDatabase.refuse`, which counts each use and raises. The contract says a database failure does not fail a generation (`API-Contract.md:298`).
  - This keeps the tests off the local PostgreSQL that `db.py:19-28` defaults to, and off any `DATABASE_URL` a `.env` names. The routing test asserts the refusal was used, which shows the isolation is in force.
  - It binds OAM-5 to keep reaching the database through those two module-level names (`application.py:22`).
  - Alternatives:
    - (a) SQLite under `tmp_path`, as 003 did. Rejected: no OAM-4 test reads the database, because cloned-generation retention needs a Chatterbox call (`Plan.md:194`).
    - (b) Leave the database as is. Rejected: startup-provider generations would write rows to the user's local database.
- **N4D-6 The untracked 003 file is deleted, and the new file has a new name.**
  - Execution deletes `tests/test_chatterbox_generation_red.py` only after its hash matches (Execution Step 2). It creates `tests/test_inference_provider_choice_red.py`.
  - Alternatives:
    - (a) Write the new content at the old path. Rejected: the old name belongs to the superseded plan, and reusing it would make the two files hard to tell apart in history and review.
    - (b) Leave the old file. Rejected: its 56 fake-based tests would run in every later backend run, against COA-16.
- **N4D-7 Timing values.**
  - The first generation in the waiting test takes 2.0 s. The rejected requests are sent 0.3 s after the two waiting requests, and must be answered before the first generation ends.
  - Every client is created before the first request. In the dry run, creating an `httpx.Client` took 0.3–0.6 s (measured: `0.64`, `0.323`, `0.345` s). A first draft that created two clients inside a 1.5 s window sent the rejected request 3 s after the first generation started, so the test failed under the probe.
  - Under parallel load in the final dry run, the tests still passed (N4R-1).
- **N4D-8 The provider list is checked exactly:** names in the order `azure`, `chatterbox`, `google`, `mock`, the baseline descriptions plus the Chatterbox description, and a non-empty `provider_class` string. Chatterbox is listed with no Chatterbox settings (`API-Contract.md:449-454`).

### Contract Rule Coverage

| Contract rule (`API-Contract.md`) | Test |
| --- | --- |
| `provider` `"google"`, absent, `null` and `""` use the startup provider (`:279-280`); `language` is ignored for providers other than Chatterbox (`:283`); `"chatterbox"` is a Chatterbox generation (`:281`), shown by its OAF-4 answer and the startup provider not being called | `test_each_generation_uses_the_provider_it_names` |
| Failure 3 for `mock`, `azure`, a different letter case, whitespace and a non-string value; failure 4 for absent, `null`, `""`, a different letter case, whitespace, another language and a non-string value (`:282`, `:289-290`, `:488`, `:495`); check 2 comes before checks 3–4 (`:286-288`); a failed call changes nothing (`:300`) | `test_unsupported_provider_or_language_is_rejected_without_generating[…]` (12 cases) |
| OAF-1–OAF-4: `503` with each exact message ending with the closing sentence (`:334`, `:338-341`). The order (`:318-321`, `:334`): OAF-1 before OAF-2, OAF-3 and OAF-4; OAF-2 before OAF-3 and OAF-4; every OAF-3 case runs with no key, so OAF-3 comes before OAF-4. No other provider, no audio file written, and the existing entry, download and output for the same `job_id` unchanged (`:297`, `:300`). Language `en` and `hi` both accepted (`:283`, `:290`). Settings: `CHATTERBOX_URL` absent, empty or blank (`:473`); `CHATTERBOX_TIMEOUT_SECONDS` invalid (`0`, `-5`, `10.5`, `ten`), while padded (`" 7 "`) and blank are not invalid (`:474`); `GOOGLE_APPLICATION_CREDENTIALS` absent or blank, a missing or unreadable key file, or one that is not a service-account key (`:341`, `:475`); `VOICE_SERVICE_URL` trimmed of spaces and a trailing `/` (`:476`). The sample: unknown, deleted and sample-less voices, and an unreachable voice service (`:320`, `:340`) | `test_each_pre_call_cause_answers_503_with_its_message_and_no_fallback[…]` (21 cases) |
| Provider list: exactly `azure`, `chatterbox`, `google`, `mock` in that order, with the baseline descriptions and the Chatterbox description; listed when the Chatterbox settings are absent; `provider_class` a non-empty string (`:449-454`) | `test_provider_list_adds_chatterbox_and_keeps_the_other_providers` |
| One generation at a time, for every provider; a request that passes checks 1–4 waits and then runs, a Chatterbox generation included; requests answered by checks 2 and 3 are answered without waiting (`:291`, `:306-308`) | `test_a_generation_request_that_arrives_during_another_waits_then_completes` |

Not tested, with the reason:

- Everything that needs a Chatterbox call, per COA-16 and the OAM-4 exclusions (`Plan.md:194`):
  - the call itself (step 4) and its time limit, including the 1200 s default;
  - OAF-5–OAF-9;
  - the token's account and audience, and `CHATTERBOX_URL` trimming (seen only in the call URL and the audience);
  - the whole text sent;
  - waiting not counting toward the limit (`:309`);
  - a cloned generation's history and retention;
  - that the sample fetch and the token request are not bounded by the limit (`:320-321`).
- OAF-4 when the token request to Google fails (`:341`). This needs a request to Google, or a stand-in for its token endpoint, which the Plan rules out (`Plan.md:191`).
- `VOICE_SERVICE_URL` absent or blank, which defaults to `http://localhost:8002` (`:476`). The answer would depend on whatever runs on that port on the user's machine.
- OAF-3 for an expired voice, and for a voice-service answer other than `404` or no answer. The voice service answers an expired voice exactly like an unknown one (`:259`; OAM-2 tests). The real voice service has no route that answers otherwise, and a stand-in voice service would not show that the two services work together.
- Result delivery when the client stops waiting (OAC-9, `:296`). The Plan puts it in OAM-5's call-dependent scope (`Plan.md:213`), not in OAM-4's (`Plan.md:183-190`).
- The order in which waiting requests run, and whether other operations are answered during a generation. The contract leaves both undefined (`:307`, `:310`).
- Carried-over behavior that OAM-4's scope does not name: failure 1, failure 7, output and history for startup generations, `INFERENCE_PROVIDER`, `AUDIO_RETENTION_DAYS`, CORS. The preserved tests cover it, and they run in command 5.

## Proposed Code / Tests

### `tests/test_chatterbox_generation_red.py` (deleted)

Removed with `rm` after the hash check in Execution Step 2. No replacement content is written at this path.

### `tests/test_inference_provider_choice_red.py` (new file, complete content)

```python
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
```

## Execution Steps

1. Confirm that this plan's Human Review status records approval, and that `git status --short` prints only `?? tests/test_chatterbox_generation_red.py`, plus changes under `docs/.ai/chatterbox-original-app/`.
2. Run `tr -d '\r' < tests/test_chatterbox_generation_red.py | sha256sum`. If it prints `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948`, run `rm tests/test_chatterbox_generation_red.py`. If it prints anything else, or the file is missing, stop and report; do not delete or create anything.
3. Create `tests/test_inference_provider_choice_red.py` with exactly the content above, with LF line endings.
4. Run the commands under Verification in order, writing each log outside the repository. Do not start, stop or check the Docker engine, run no `gcloud` command (CON-2), and create no `.env` file.
5. Record the evidence in `Plan.md` Execution Status for OAM-4, and update this plan's Human Review status.

## Acceptance / Completion Criteria

- **N4C-1** `tests/test_chatterbox_generation_red.py`, confirmed by its hash, is deleted. `tests/test_inference_provider_choice_red.py` is created with exactly the content above: with CR removed, its SHA-256 is `f0f8ab986f603c79bd52a81f4826d3fac6e4da77d9a75ab7eeff32fe7c892365` (command 1). No other repository file changes. This excludes the OAM-4 Execution Status update in `Plan.md` and this plan's Human Review status.
- **N4C-2** The first run of the new file reports `36 failed`, with 0 passed and 0 errors. Each failure falls into exactly one of these classes, each caused by the missing approved behavior:
  - 22 tests: `assert 200 == 503`. A Chatterbox generation was produced by the startup provider. These are the 21 pre-call cause tests and the routing test.
  - 12 rejection tests: `assert 200 == 400`. `provider` and `language` are not validated.
  - 1 test: `AssertionError: a second generation ran while the first was generating`. There is no waiting.
  - 1 test: the provider-list assertion `['azure', 'google', 'mock'] == ['azure', 'chatterbox', …]`. Chatterbox is not listed.

  The class counts must be exactly 22, 12, 1 and 1. Any other failure cause stops execution and is not valid RED evidence. That includes an import, fixture or server-start failure, and an `ERROR` at teardown from the guard.
- **N4C-3** A second run of the same file, with no cleanup between runs, gives the same result as N4C-2 (Repeatable, Isolated Verification). The tests keep all state under `tmp_path`, and they assert the storage root and the database refusal in force.
- **N4C-4** After the two runs, `git status --short -- audio_storage` prints nothing, and no `voice_storage/` folder exists. If either fails, stop and report; do not restore and continue.
- **N4C-5** The preserved tests (`Plan.md:193`) still pass: `29 passed`, 0 failed, 0 errors. Then OAV-3 holds: any `audio_storage/` output the preserved tests wrote is recorded and restored (Plan OAR-1).
- **N4C-6** Collecting the backend suite with the three V3Q-3 `--ignore` options reports `118 tests collected`, with no collection error. 36 of them are from the new file and none from `tests/test_chatterbox_generation_red.py`.
- **N4C-7** No new test fakes or calls Chatterbox (COA-16, `Plan.md:195`):
  - the static check (command 7) finds no web app, no `/v1/synthesize` route, no `sample_audio` part, no `token_uri`, no `id_token` and no `run.app` host in the new file;
  - the guard recorded no lookup outside the machine in either run, so no teardown `ERROR`.
- **N4C-8** No process or thread started by the runs is left running (`prompt-driven-development` Plan Progress).

## Verification

### Commands

Run from the repository root in Git Bash. `$TEMP` is outside the repository.

1. `test ! -e tests/test_chatterbox_generation_red.py && echo deleted; tr -d '\r' < tests/test_inference_provider_choice_red.py | sha256sum; python -m compileall -q . -x '(node_modules|\.git|\.venv|frontend)' && echo compiled`
2. `python -m pytest tests/test_inference_provider_choice_red.py -q --tb=short > "$TEMP/oam4n-red-run1.log" 2>&1; tail -1 "$TEMP/oam4n-red-run1.log"; grep -cE "^(FAILED|ERROR) " "$TEMP/oam4n-red-run1.log"; grep -c "^ERROR " "$TEMP/oam4n-red-run1.log"; grep -E "^E  " "$TEMP/oam4n-red-run1.log" > "$TEMP/oam4n-red-run1.e"; for p in "assert 200 == 503" "assert 200 == 400" "AssertionError: a second generation ran while the first was generating" "assert ['azure', 'google', 'mock'] == ['azure', 'ch"; do printf '%s => ' "$p"; grep -cF -- "$p" "$TEMP/oam4n-red-run1.e"; done` (OAV-1, with `--tb=short` so each failure's assertion line is in the log)
3. The same as command 2, with `run2` in place of `run1` in every file name (the second run, with no cleanup).
4. `git status --short -- audio_storage; test ! -e voice_storage && echo absent` (N4C-4)
5. `python -m pytest tests/test_inference.py tests/test_provider_registry.py tests/test_generation_history_download.py tests/test_generation_persistence_red.py tests/test_generation_delete_search_red.py -q > "$TEMP/oam4n-preserved.log" 2>&1; tail -1 "$TEMP/oam4n-preserved.log"`, then `git status --short -- audio_storage`. Only if it prints anything: record it, run `git checkout -- audio_storage` and `git clean -fd -- audio_storage`, and repeat `git status --short -- audio_storage`, which must print nothing (OAV-3, `Plan.md:344`).
6. `python -m pytest --collect-only -q -p no:cacheprovider --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam4n-collect.log" 2>&1; tail -1 "$TEMP/oam4n-collect.log"; grep -c "^tests/test_inference_provider_choice_red.py::" "$TEMP/oam4n-collect.log"; grep -c "^tests/test_chatterbox_generation_red.py::" "$TEMP/oam4n-collect.log"`
7. `grep -nE "FastAPI\(|/v1/synthesize|sample_audio|token_uri|run\.app|id_token" tests/test_inference_provider_choice_red.py; echo "matches: $?"` (N4C-7; exit status `1` means no match)
8. `git status --short` (it must list only `?? tests/test_inference_provider_choice_red.py`, plus work-item changes under `docs/.ai/chatterbox-original-app/`)
9. Process check: in PowerShell, `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId, CreationDate, CommandLine`. No process from this run may remain. The servers are threads inside each pytest process, which has exited.

### Affected Tests

- The new file only. It changes no shared test file and no production code, so no existing test's result can change.
- The deleted `tests/test_chatterbox_generation_red.py` was never committed and is not evidence (`Plan.md:47`); deleting it removes 56 tests from collection, which command 6 checks.
- The preserved tests that `Plan.md:193` names run once in command 5, because the OAM-4 success criteria require it (`Plan.md:195`). They were found as the tests that import `voice_narration.inference` (`grep -rln "voice_narration.inference" tests --include=*.py`). That search also lists three other files:
  - `tests/test_real_model_inference.py`, a named pre-existing failure;
  - `tests/test_linguistic_chunking_and_controls.py`;
  - the file this plan deletes.

  The first two are not in OAM-4's preserved list, and no file either uses changes, so neither runs.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Command 1: `deleted`, `f0f8ab986f603c79bd52a81f4826d3fac6e4da77d9a75ab7eeff32fe7c892365 *-` (Git Bash marks stdin with `*-`), `compiled`.
- Commands 2 and 3: `36 failed, … in …` (the dry run took 44–82 s); `36` `FAILED` lines; `0` `ERROR` lines; class counts `22`, `12`, `1`, `1`.
- Command 4: no `git status` output, then `absent`.
- Command 5: `29 passed …`. Then `git status` is predicted to print ` M audio_storage/generation_index.json` and `?? audio_storage/generations/<UTC date>/`, written by `tests/test_generation_history_download.py` (Plan OAR-1; seen in the dry run). After the restore it prints nothing.
- Command 6: `118 tests collected …` (82 at OAM-3, `Plan.md:447`, plus 36), then `36`, then `0`.
- Command 7: no match lines, then `matches: 1`.
- Command 8: `?? tests/test_inference_provider_choice_red.py`, plus `docs/.ai/chatterbox-original-app/` changes.
- Command 9: no `python.exe` from this run.
- Preserved-behavior tests (expected to pass at RED): none in the new file. The routing test also checks preserved routing (`"google"`, absent, `null`, `""`), but it fails at RED on its Chatterbox request, so it is RED evidence for COA-1. The 29 existing preserved tests in command 5 are expected to pass; they are not RED evidence for any requirement.

### Planning-Time Dry Run

This is a planning-time dry run, not milestone evidence. It ran on 2026-11-13 at HEAD `059102c`, in two disposable copies under `C:/Users/avina/AppData/Local/Temp/claude/75d22e5e94aa85f8/7c785373-79e0-4451-8aab-0a1437282b97/scratchpad/oam4n/`. Both were made with `git -c core.autocrlf=false archive HEAD | tar -x`, so neither holds the untracked 003 file, which matches the state after Execution Step 2:

- `copy/`: unmodified code, with a temporary `git init` so `git status` could be read;
- `pcopy/`: a scratch-only probe and a scratch `.env`.

The exact test file above was placed in each copy's `tests/`. The repository was not modified.

| Step | Command (in the copy) | Result |
| --- | --- | --- |
| Compile (`copy/`) | `python -m compileall -q . -x '(node_modules\|\.git\|\.venv\|frontend)'` | `compiled` |
| RED, unmodified (`copy/`) | `python -m pytest tests/test_inference_provider_choice_red.py -q -p no:cacheprovider --tb=short`, then the class counts from command 2 | Final file: `36 failed, 200 warnings in 82.22s`; `assert 200 == 503` 22, `assert 200 == 400` 12, `a second generation ran while the first was generating` 1, the provider-list assertion 1. 0 `ERROR` lines. The 200 warnings are pre-existing deprecations (`on_event`, `datetime.utcnow` in `storage.py:22`, `:26`). An earlier run of the same file before two lines were re-wrapped gave `36 failed … in 55.14s` with the same counts |
| Isolation (`copy/`) | `git status --short` after the RED run, before the preserved run | Only the test file itself (the copy's commit held an earlier draft); no `audio_storage` change |
| Probe (`pcopy/`) | Same pytest command plus `tests/test_guard_probe.py`. The scratch `apply_probe.py` patches `application.py` with: `provider` and `language` validation; an `asyncio.Lock` around generation; the settings read in `InferenceState.__init__`; the OAF-1 and OAF-2 checks; the sample fetch with `httpx.AsyncClient(trust_env=False)`; the token through google-auth `IDTokenCredentials.from_service_account_file(...)`; `chatterbox` added to the provider list. It has no Chatterbox call. The scratch `.env` sets `CHATTERBOX_URL` to the CON-5 URL, `GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json`, `CHATTERBOX_TIMEOUT_SECONDS=1200`, `VOICE_SERVICE_URL=http://localhost:8002`, `INFERENCE_PROVIDER=google` and `AUDIO_STORAGE_PATH=./audio_storage` | Final file: `37 passed, 128 warnings in 107.43s`. This ran in parallel with the RED run, so both were under load. With the `.env` in place, all 36 tests passed and the guard recorded no lookup |
| Guard check (`pcopy/`) | scratch `tests/test_guard_probe.py`: `socket.getaddrinfo("example.invalid", 443)`, a sync and an async httpx `GET http://example.invalid/` under the guard fixture | All three raised with `blocked by the OAM-4 tests`. Recorded: `example.invalid` three times. `127.0.0.1` and `localhost` resolved. The async lookup passes the host as bytes; the first draft recorded it as `b'example.invalid'`, so `host_name()` was added |
| Preserved tests (`copy/`) | `python -m pytest tests/test_inference.py tests/test_provider_registry.py tests/test_generation_history_download.py tests/test_generation_persistence_red.py tests/test_generation_delete_search_red.py -q -p no:cacheprovider` | `29 passed, 42 warnings in 2.86s`; then `git status --short` printed ` M audio_storage/generation_index.json`, `?? audio_storage/generations/2026-11-14/` (UTC date, `storage.py:26`) |
| Collect with V3Q-3 ignores (`copy/`) | command 6 | `118 tests collected in 7.00s`; `36`; `0` |
| Static check | command 7 on the final file | no match, exit `1` |
| Client cost | `python -c` timing `httpx.Client(trust_env=False)` three times | `0.64`, `0.323`, `0.345` s (N4D-7) |
| google-auth fallback | `grep -n` in the installed `google/oauth2/id_token.py` | `:297-349`: `GOOGLE_APPLICATION_CREDENTIALS` is used only for `service_account` or `impersonated_service_account` types; otherwise the metadata server is pinged |
| Old file | `sed -n 182,850p 003_Implementation_Plan_OAM-4.md \| tr -d '\r' \| sha256sum` | `4a0762e1…f948`, the same as the untracked file |
| File hash | `tr -d '\r' < <final file> \| sha256sum` | `f0f8ab986f603c79bd52a81f4826d3fac6e4da77d9a75ab7eeff32fe7c892365`; the file has no CR |

Corrections from the dry run, all made before this plan was written:

- **The waiting test's client timing.** The first draft created each background `httpx.Client` after the first generation was seen in flight. Under the probe the test failed with `a request rejected by check 2 waited`. Instrumenting it showed the rejected request was sent 2.6–3.1 s after the first generation started, against a 1.5 s generation. Timing the client constructor (0.3–0.6 s each) established the cause. Now every client is created first, and the generation takes 2.0 s (N4D-7).
- **The guard's record of asynchronous lookups** (bytes host names), as above.
- **Two long lines** were re-wrapped, the `RefusingDatabase` docstring and one parameter case. The RED and probe runs were repeated on the final file.

Created during planning, all under the scratchpad's `oam4n/` folder: `copy/`, `pcopy/` (with its `.env` and `tests/test_guard_probe.py`), `probe/apply_probe.py`, the draft test file, `plan_skeleton.md`, and the logs `compile.log`, `dbg_patch.log`, `red1.log`–`red4.log` with their `.e` extracts, `probe1.log`–`probe4.log`, `preserved.log` and `collect.log`. All are deleted once this plan is written. Pytest temporary directories went under the system pytest temp root. The scratchpad files `oam45.md`, `oam8.md`, `ref-contract.md` and `trace.md` predate this run and were left untouched.

## Risks

- **N4R-1 Timing assertions.**
  - In the waiting test, the requests rejected by checks 2 and 3 must be answered before a 2.0 s generation ends. They are sent about 0.3 s after it starts, so the margin is about 1.5 s.
  - The waiting order is read from `time.monotonic()` across threads of one process.
  - The final dry run passed with the RED and probe runs in parallel. Under heavier load the test could still fail on unchanged code. Execution then stops and reports, with no rerun until it passes (testing skill).
- **N4R-2 The guard's reach** (N4D-2). It intercepts name lookups through `socket.getaddrinfo`. This was shown for direct, synchronous httpx and asynchronous httpx lookups. Whether an asynchronous connection to a numeric non-loopback address passes through it was not established. No setting in these tests names one.
- **N4R-3 Settings in force, per test (Plan OAR-8).** The `harness` fixture, which runs after `db.py:14-16` has loaded any `.env`, removes `CHATTERBOX_TIMEOUT_SECONDS`, `GOOGLE_APPLICATION_CREDENTIALS`, `INFERENCE_PROVIDER` and `AUDIO_RETENTION_DAYS`. It sets `CHATTERBOX_URL=http://127.0.0.1:0`, `VOICE_SERVICE_URL` to the test's voice service, and `AUDIO_STORAGE_PATH` to `tmp_path / "audio"`. Each test then changes only what this table shows.

  | Test | `CHATTERBOX_URL` | `GOOGLE_APPLICATION_CREDENTIALS` | Why no Chatterbox call is possible |
  | --- | --- | --- | --- |
  | routing | `http://127.0.0.1:0` | removed | No key, so no token (step 3); the URL is loopback port 0 |
  | rejection (12) | `http://127.0.0.1:0` | removed | Answered at check 3 or 4, before any call step; and no key |
  | OAF-1 (3) and order OAF-1 | removed, `""` or `"   "` | removed | No URL and no key |
  | OAF-2 (4) and order OAF-2 | `http://127.0.0.1:0` | removed | No key; the URL is loopback port 0 |
  | OAF-3 (4) | `http://127.0.0.1:0` | removed | No key; the URL is loopback port 0 |
  | OAF-4 (8) | `http://127.0.0.1:0` | removed, `"  "`, a missing file, a file that is not JSON, or an authorized-user key | None names a service-account key, so no token |
  | provider list | removed | removed | No generation is sent |
  | waiting | removed | removed | No URL and no key |

  If an OAM-5 change read a `.env` again, the guard still stops any lookup of the deployed or Google host names. The dry run with a `.env` naming the deployed URL passed under the probe. The probe reads only the process environment, so this does not show what a re-reading GREEN would do.
- **N4R-4 Binding OAM-5.** The tests bind OAM-5 to N4D-2 (no lookup outside the machine during the pre-call causes), N4D-3 (settings read from the environment no earlier than `create_app`) and N4D-5 (`SessionLocal` and `create_all_tables`). They also bind it to the four exact messages and the `400` bodies. An OAM-5 that took the token through google-auth's `fetch_id_token` would fail the OAF-4 absent-key and authorized-user cases, because that function pings the metadata server (dry run, google-auth fallback). That matches the contract, which gets the token only from the key file (`API-Contract.md:321`).
- **N4R-5 Import-time side effects** (pre-existing). Importing `voice_narration.inference.application` runs `create_app()` (`:623`). That creates empty `audio_storage/` subfolders (`storage.py:16-19`), which `git status` does not show, and tries the default database (`application.py:107-111`). The new tests' own apps use `tmp_path` and the refused database. Command 4 checks `audio_storage/`.
- **N4R-6 Authentication and authorization.** OAM-4 owns and verifies no authentication or authorization requirement. Neither local service authenticates callers (`API-Contract.md:58`), and the identity token is not obtained in any test. These tests make no identity, role or ownership comparison. Voice ids and `job_id` are compared exactly, as the contract states (`:495`).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `tests/test_inference_provider_choice_red.py`. If the deleted untracked file is wanted back, recreate it from `003_Implementation_Plan_OAM-4.md:182-850`; its hash, CR removed, is `4a0762e1443a2552f5173b76aacd655127b23e8771a0ced1ee0b38fdd620f948`. Nothing else is changed.

## Explicitly Out of Scope

- Any production change: provider and language handling, the pre-call checks, the settings, waiting, the provider-list entry, and the Chatterbox call. These belong to OAM-5 (`Plan.md:197-216`).
- Any test that fakes, stands in for or calls Chatterbox or Google's token endpoint, and any behavior that needs a Chatterbox call (COA-16, `Plan.md:194`). That behavior is checked only at OAM-8.
- Dependency declarations or version changes, including google-auth (Plan OAR-4).
- Changes to the preserved tests (`Plan.md:193`) or any other existing test, and repair of the pre-existing failures.
- Voice-service and TTS-page tests (`Plan.md:194`).
- Network use outside the machine, Docker, `gcloud` (CON-2), and creating a `.env` or key file in the repository (CON-6).
- Writing to tracked `audio_storage/` files, `voice_storage/` or the local PostgreSQL from the new tests.

## Human Review

Status: Executed — RED verified 2026-11-13; see `Plan.md` Execution Status, OAM-4 RED evidence. (Approved by Avinash Srivastava on 2026-11-13, as written, including decisions N4D-1 to N4D-6.)
