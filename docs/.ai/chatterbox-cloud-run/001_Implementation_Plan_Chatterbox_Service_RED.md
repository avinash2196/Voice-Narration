# Implementation Plan — CRM-2 Chatterbox Service RED

## Milestone

CRM-2 — Chatterbox Service RED, work item `chatterbox-cloud-run` (`docs/.ai/chatterbox-cloud-run/Plan.md`, section "CRM-2 — Chatterbox Service RED").

Purpose as recorded in `Plan.md`: tests that specify Chatterbox's new synthesize behavior, retention and one-at-a-time serving, run without the model runtime, CUDA or model weights, isolating the model runtime boundary within test code.

## Revision

Revision 2, 2026-11-09. Revision 1 was approved by avinash2196 on 2026-11-09 ("Approve plan 001") and executed; execution stopped at a blocker recorded in `Plan.md` "CRM-2 Execution Evidence (stopped)": C2-T13 ended with `httpx.ReadError` (`WinError 10054` in V1, `WinError 10053` in V2) and not with its own assertion, so C2-AC-3 and C2-AC-5 were not met. The user approved this revision ("Yes, revise C2-T13").

What changed from revision 1:

- C2-T13 `test_synthesize_contract_answers_over_real_transport` only: each of its three requests is sent on its own `httpx.Client`, and so on its own connection, and each response is asserted immediately after its request, before the next request is sent. The set of assertions is unchanged; only their position and the client per request changed. Every other test, helper, fixture and constant is unchanged.
- C2-D-6 (real-transport check) records the one-connection-per-request decision and its alternatives.
- The file is now present in the working tree from the stopped execution, so it moves from Files to Create to Files to Modify, with its complete final content and a unified diff against the current file.
- C2-AC-3 names transport errors (`httpx.TransportError` and its subclasses, such as `httpx.ReadError`) explicitly as invalid RED evidence. This states what the revision-1 criterion already excluded ("not because of … environment errors" in `Plan.md` CRM-2 success criteria); it does not loosen any criterion.
- Execution Steps add a content check of the existing file before it is replaced, and of the result after.
- Preconditions, Current Repository State, Expected Evidence, Planning-Time Dry Run, C2-RSK-5 and Human Review are updated to match.

## Milestone Type

RED — as recorded in `Plan.md` ("Milestone type: RED") and in its Execution Status row "CRM-2 — Chatterbox Service RED (RED) | Pending". `Plan.md` records no FOUNDATION milestone ("No FOUNDATION milestone exists in this Plan") and its Prerequisite coverage states that no dependency, build configuration or test infrastructure is missing for CRM-2. This plan proposes RED directly and changes test files only.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Approved by avinash2196 on 2026-11-09 (its Status section); Execution Status: CRM-1 Complete, CRM-2 Pending with "CRM-2 Execution Evidence (stopped)" ("Plan scope unchanged; Implementation Plan revision and re-approval required") |
| `docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md` revision 1 (this file before revision) | Approved by avinash2196 on 2026-11-09; executed and stopped at the C2-T13 blocker; its approval does not carry over to revision 2 |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (accepts CCD-1–CCD-7). Authoritative predecessor delivered by CRM-1 |
| `docs/requirements.md` (product level) | Absent — `ls docs/requirements.md` answers "No such file or directory" |
| `docs/developer-setup.md` | Repository documentation, not a PDD artifact; read as repository evidence for test conventions and verification commands |
| Plugin skills read: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `testing`, `python-fastapi` | Plugin guidance, not project artifacts |

`security` is not applied: CRM-2 owns and verifies no authentication or authorization requirement. The caller-identity rules of the contract (Chatterbox Caller Identity) trace to CCR-7, which `Plan.md` assigns to CRM-5 (owner) and CRM-4 (verifier).

## Carried-Forward Decisions

No other Implementation Plan exists in the work-item folder `docs/.ai/chatterbox-cloud-run/` (it contains `requirements.md`, `Plan.md`, `API-Contract.md` and this file). Implementation Plans of other work items are not authority for this one (`prompt-driven-development` Work-Item Folders).

From revision 1 of this plan, approved by avinash2196 on 2026-11-09, every decision is kept unchanged — C2-D-1 to C2-D-5 and C2-D-7, the stand-in runtime, the fixture, the helpers and C2-T1–C2-T12 — except C2-D-6, which is changed for C2-T13 with the user's explicit approval ("Yes, revise C2-T13"). Reason: the shared pooled connection made C2-T13's result depend on a race (see Preconditions / Predecessor Evidence).

The approved contract decisions this milestone's tests encode are CCD-1, CCD-2, CCD-3, CCD-8 (carried-over text, language and generation-failure rules), CCD-9, CCD-10 and CCD-11 of `API-Contract.md`.

## Preconditions / Predecessor Evidence

- Predecessor CRM-1 (CONTRACT): `Plan.md` Execution Status row "CRM-1 — Chatterbox Cloud Run Contract (CONTRACT) | Complete | `API-Contract.md` Contract Review Status: Approved by avinash2196 on 2026-11-09 (CCD-1–CCD-7 accepted)." `API-Contract.md` Contract Review Status reads the same. CRM-1 changes no executable artifact, so there is no runtime evidence to check beyond the approved artifact.
- CRM-2 is Pending in `Plan.md` Execution Status. Revision 1 of this plan stopped at a blocker, and no other Implementation Plan exists for CRM-2. `Plan.md` records "Plan scope unchanged; Implementation Plan revision and re-approval required", so this revision plans from the same approved Plan.
- Blocker evidence (from `Plan.md` "CRM-2 Execution Evidence (stopped)"): V1 and V2 each gave `13 failed, 9 passed`; C2-T13 failed with `httpx.ReadError` in V1 (`WinError 10054`) and V2 (`WinError 10053`, at `tests\test_chatterbox_service_red.py:479`, the second request), and with `assert 500 == 200` in V3. The other twelve tests failed on their status assertions as predicted; the 9 existing tests passed.
- Cause, established from the installed library code and from a reproduction in the dry run:
  - Starlette's `ServerErrorMiddleware` sends the `500` answer and then re-raises the exception (`.venv/Lib/site-packages/starlette/middleware/errors.py:181`, `:186`).
  - `uvicorn` uses its h11 protocol here, because `httptools` is not installed (`.venv/Lib/site-packages/uvicorn/protocols/http/auto.py:6-11`; `import httptools` fails with `ModuleNotFoundError`). On an exception after the response has started, it closes the connection (`uvicorn/protocols/http/h11_impl.py:414-420`, `else: self.transport.close()`).
  - The `500` answer does not tell the client the connection will close, so `httpx` keeps it in its pool. `httpcore` treats an idle pooled connection as dropped only if its socket is already readable when the connection is picked for the next request (`.venv/Lib/site-packages/httpcore/_sync/http11.py:274-285`).
  - Revision 1's C2-T13 sent its second request on the same `httpx.Client` right after the first `500`. The dry run below reproduced the result: `ReadError` in 3 of 20 isolated runs of the revision-1 test, `assert 500 == 200` in 17. That the outcome depends on whether the server's close has reached the client socket when the connection is picked is a hypothesis consistent with the code cited above; the exact timing was not measured.
- Milestone type check: `Plan.md` records CRM-2 as RED; this plan is RED.
- Repository state matches the Plan's recorded Current State (commit `360846e`, see below), apart from the test file left in place by the stopped execution; no conflict found.

## Current Repository State

Inspected on 2026-11-09.

- `git rev-parse HEAD`: `360846eceb846936e176570543824d4f041c7abd`. `git status --short` (re-inspected for revision 2): `?? docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md`, `?? docs/.ai/chatterbox-cloud-run/API-Contract.md`, `?? docs/.ai/chatterbox-cloud-run/Plan.md`, `?? tests/test_chatterbox_service_red.py` — no tracked file is modified.
- `tests/test_chatterbox_service_red.py` is present, untracked, left by the stopped execution: 487 lines, ASCII, LF, SHA-256 `7e7b443dca7f7660319723bef2d8a4e1521c23023d59e716fbc53ff1ba193921`. It is byte-identical to revision 1's code block (`diff` of the extracted code block against the file printed nothing; the hashes match).
- Chatterbox model API, `voice_narration/chatterbox_api/application.py` (96 lines):
  - imports `torch`, `torchaudio` and `chatterbox.mtl_tts.ChatterboxMultilingualTTS` at module load (`:7-13`);
  - `SynthesizeRequest` is a JSON body model with `text`, `language`, optional `sample_path` (`:21-24`);
  - `synthesize` is a synchronous route: `text` trimmed, blank → `400 text is required` (`:55-57`); `language` trimmed and lowercased, not `hi`/`en` → `400 language must be hi or en` (`:59-61`); model loaded lazily into the module global `_model` (`:33-40`, `:63`); a `sample_path` is opened on Chatterbox's own filesystem and passed as `audio_prompt_path`, missing file → `404` (`:64-69`); `model.generate(text, language_id=..., audio_prompt_path=...)` error → `503 chatterbox_synthesis_failed: <error>` (`:71-74`); the result is converted with `torch.Tensor`, `.detach().cpu().float()`, `torch.tensor(..., dtype=torch.float32)`, `.ndim`, `.unsqueeze(0)` and encoded with `torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")` into an in-memory buffer returned as `audio/wav` (`:76-86`);
  - generation is not serialized: no lock exists in the module.
- Model runtime: in `.venv` (Python 3.13.17) `import torch`, `import torchaudio` and `import chatterbox` each fail with `ModuleNotFoundError` (observed on 2026-11-09). `requirements-dev.txt:10` declares `chatterbox-tts==0.1.7`.
- Test tooling available in `.venv` (observed with `pip list`): `pytest 9.1.1`, `fastapi 0.162.0` (with `starlette 1.10.0`), `httpx 0.28.1`, `python-multipart 0.0.32`, `uvicorn 0.54.0`, `anyio 4.16.0`, `pydantic 2.14.3` — all declared in `requirements-dev.txt:1-5` except `starlette`, `anyio` and `pydantic`, which are FastAPI's own dependencies. `pytest.ini`: `addopts = --strict-config --strict-markers`, `testpaths = tests`, `pythonpath = .`.
- `docs/developer-setup.md` test conventions used by this plan: "use pytest tmp_path for files … verify … effective paths and runtime configuration, and never share state across cases"; "Tests may use stdlib mocks for boundaries, but mocks must not supply the behavior being proved"; "Use HTTPX for in-process ASGI and real loopback/network contract checks; verify contract error responses through real transport"; "loopback-only dynamically allocated local ports".
- Pre-existing tests (`tests/`): `test_ai_gateway_red.py` (5 tests), `test_ai_gateway_telemetry_red.py` (1 test), `test_clone_flow.py` (3 tests). None imports `voice_narration.chatterbox_api`. Baseline run `.\.venv\Scripts\python.exe -m pytest tests -ra` on 2026-11-09: `9 passed, 1 warning in 3.60s` — no pre-existing failure. Revision 2's dry-run baseline, without the CRM-2 file, gave `9 passed, 1 warning in 3.85s`. The only other file in `tests/` is the CRM-2 file described above.
- Observed fact relevant to verification: the preserved test `test_generation_uses_selected_voice_profile` creates a narration job, which calls the Google TTS provider (`voice_narration/inference/application.py:184-186`), whose `generate` calls `self._client.synthesize_speech` (`voice_narration/inference/providers/google.py:70`) with the local credentials located by `_load_local_env` (`google.py:13-35`). The full-suite verification therefore depends on network access to Google and on the local key file. This milestone does not change that test.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `tests/test_chatterbox_service_red.py` — present, untracked, from the stopped execution of revision 1. Only C2-T13 changes. Both the complete final content and a unified diff against the current file are given under Proposed Code / Tests.

### Files to Delete

None.

## Proposed Changes

1. Replace the content of `tests/test_chatterbox_service_red.py` with the complete final content below. Relative to the current file, the only change is in C2-T13 (item 1.6, and the diff below). The file then contains, in this order:
   1. Module docstring stating how the model runtime is isolated.
   2. Constants `APP_MODULE`, `SYNTHESIZE`, `FAKE_SAMPLE_RATE` (`24000`), `GENERATED_SAMPLES`, `SAMPLE_PATH_DETAIL` (the contract's `400` detail for `sample_path`), `SYNTHESIS_FAILED_PREFIX` (the contract's normative `503` prefix).
   3. Stand-in model runtime (test code only):
      - `_Recorder` — test-owned record of each `generate` call (text, `language_id`, prompt path, whether the prompt file existed, its bytes at call time), the number of generations running at once (`active`, `max_active`), and per-test `delay_seconds` and `error` controls.
      - `_FakeTensor` and `_fake_tensor(data, dtype=None)` — stand-ins for the `torch.Tensor` surface the application uses today (`isinstance`, `detach`, `cpu`, `float`, `ndim`, `unsqueeze(0)`, `torch.tensor`, `torch.float32`).
      - `_fake_torchaudio_save(target, tensor, sample_rate, format=None, **kwargs)` — encodes the stand-in samples as 16-bit mono WAV with the stdlib `wave` module.
      - `_FakeMultilingualTTS` — stand-in for `ChatterboxMultilingualTTS` with `sr = 24000`, `from_pretrained(cls, device, **kwargs)`, and `generate(self, text, language_id, audio_prompt_path=None, **kwargs)` that records the call into the per-test recorder (bound as a class attribute of a per-test subclass), optionally sleeps or raises, and returns four fixed samples.
   4. `_Harness` and the `chatterbox` fixture: redirects `tempfile.tempdir` to `tmp_path / "process-temp"`; installs stand-in modules `torch`, `torchaudio`, `chatterbox`, `chatterbox.mtl_tts` with `monkeypatch.setitem(sys.modules, …)`; removes `voice_narration.chatterbox_api.application` from `sys.modules` and imports it fresh (so `_model` starts as `None` in every test); removes it again at teardown. `_Harness.client()` returns `TestClient(app, raise_server_exceptions=False)` so that a server-side error is observed as a `500` answer.
   5. Helpers `_unique_sample`, `_form`, `_sample_file`, `_wav_rate_and_frames`, `_assert_valid_wav_answer`, `_assert_validation_error`, `_module_state_holding` (lists application module globals that hold the sample bytes, the generated WAV bytes, or a generated stand-in tensor, checking each global and one level of its contents), and `_running_server` (runs the application under `uvicorn.Server` in a daemon thread on a loopback socket bound to port `0`, waits up to 10 seconds for `server.started`, and stops it with `should_exit` and `join(timeout=10)`).
   6. Thirteen tests, C2-T1–C2-T13 (table below). C2-T1–C2-T12 are unchanged from revision 1. C2-T13 is changed as follows; this is the only change to the file:
      - It opens a separate `with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:` block for each of its three requests: success, `sample_path` rejection, JSON body. Each request therefore uses its own connection, closed when its block ends.
      - Each response is asserted right after its block ends, inside the `_running_server` block and before the next request is sent: `_assert_valid_wav_answer(success)` and the `prompt_bytes` check after the first, the `400` status and exact detail after the second, and `_assert_validation_error(json_body)` and the final `len(calls) == 1` after the third.
      - No assertion is added, removed or changed.

| ID | Test | Verifies (contract rule; requirement) |
| --- | --- | --- |
| C2-T1 | `test_synthesize_accepts_sample_audio_and_conditions_generation` | Multipart `text`, `language`, `sample_audio` accepted; `200` `audio/wav` at the model's sample rate; text trimmed; language trimmed and lowercased; extra parts ignored; part filename and content type ignored; the sample's exact bytes reach the model as the voice prompt (CCD-1; CCR-6) |
| C2-T2 | `test_synthesize_rejects_sample_path_part` | A `sample_path` part, non-empty or empty, answers `400` with the exact detail; the model is not called (CCD-2; CCR-6) |
| C2-T3 | `test_synthesize_rejects_baseline_json_body` | A JSON body in the baseline shape, with no path, with a path to an existing local file, or with a missing path, answers `422` with a `detail` list; Chatterbox never reads a sample from its own filesystem (CCD-2, Retention "never reads a voice sample from its own filesystem"; CCR-6) |
| C2-T4 | `test_synthesize_missing_or_non_file_parts_are_validation_errors` | After a valid request succeeds: missing `text`, missing `language`, missing `sample_audio`, or `sample_audio` sent as a non-file field each answers `422` with a `detail` list, and no generation runs (CCD-3; CCR-6) |
| C2-T5 | `test_synthesize_rejects_empty_sample_audio` | Zero-byte `sample_audio` answers `400 sample_audio is required` without generation (CCD-3; CCR-6) |
| C2-T6 | `test_synthesize_keeps_text_and_language_validation` | Empty or whitespace `text` → `400 text is required`; `language` `fr`, empty or whitespace → `400 language must be hi or en`; no generation (CCD-8; RF-3, carried over under the new shape) |
| C2-T7 | `test_synthesize_answers_first_failing_check_in_contract_order` | Check order 1 → 2 → 3 → 4 → 5 of the contract's failure list: a missing part (`422`) before `sample_path`, `sample_path` before `text`, `text` before `language`, `language` before empty sample (Chatterbox Synthesize "in the order they are checked"; CCR-6) |
| C2-T8 | `test_synthesize_generation_error_including_unusable_sample_answers_503` | A model generation error, including one raised for a non-empty sample the model cannot use, answers `503` whose `detail` starts with `chatterbox_synthesis_failed: ` (CCD-3, CCD-8; RF-4, carried over under the new shape) |
| C2-T9 | `test_synthesize_holds_no_sample_or_audio_after_success` | Positive first: the prompt file existed during generation with the sample's bytes. Then, after a `200`: the prompt file no longer exists, the process temporary directory is empty, and no application module global holds the sample, the generated WAV or a generated tensor (CCD-10; CCR-10) |
| C2-T10 | `test_synthesize_holds_no_sample_after_generation_failure` | Same as C2-T9 after a `503` generation failure (CCD-10; CCR-10) |
| C2-T11 | `test_synthesize_serves_concurrent_requests_one_at_a_time` | Three concurrent requests on one event loop through `httpx.ASGITransport`, each generation taking 0.3 s: all three answer `200` (none rejected for being busy), all three generations run, and at most one runs at any moment (CCD-9; Consistency and concurrency) |
| C2-T12 | `test_synthesize_repeated_identical_requests_each_generate` | Two identical requests both answer `200` and each runs its own generation with the same sample — no duplicate detection (CCD-11; Consistency and concurrency, retry produces a new clip) |
| C2-T13 | `test_synthesize_contract_answers_over_real_transport` | Over real loopback HTTP connections to `uvicorn`, one new connection per request and each answer asserted before the next request: success `200` `audio/wav` with the sample reaching the model, `sample_path` → `400` with the exact detail, JSON body → `422` with a `detail` list (contract error answers verified through real transport, `testing` skill and `docs/developer-setup.md`; CCR-6) |

### Contract rule coverage (`API-Contract.md`, Chatterbox Synthesize and Contract-Wide Rules)

| Normative rule | Covered by |
| --- | --- |
| Body is `multipart/form-data` with form fields `text`, `language` and file part `sample_audio` | C2-T1, C2-T13 |
| `sample_audio` filename and content type are not significant | C2-T1 |
| Success `200`, `audio/wav`, at the model's sample rate | C2-T1, C2-T9, C2-T11, C2-T12, C2-T13 |
| Failure 1: `422` for a non-multipart body (including the baseline JSON shape) | C2-T3, C2-T13 |
| Failure 1: `422` for a missing `text`, `language` or `sample_audio` part, or a non-file `sample_audio` | C2-T4 |
| Failure 2: `400 sample_path is not supported; send the voice sample as sample_audio`, whatever its value, including empty | C2-T2, C2-T13 |
| Failure 3: `400 text is required` for empty or whitespace `text` | C2-T6 |
| Failure 4: `400 language must be hi or en` after trim and lowercase | C2-T6 (rejection), C2-T1 (` EN ` accepted as `en`) |
| Failure 5: `400 sample_audio is required` for zero bytes | C2-T5 |
| Failure 6: `503`, normative prefix `chatterbox_synthesis_failed: `, including an unusable non-empty sample | C2-T8, C2-T10 |
| Checks applied in the listed order, first applicable answered | C2-T7 (failures 1–5; failures 6 and 7 cannot coincide with an earlier failure because generation runs only after every check passes) |
| `400`/`503` body `{"detail": "<string>"}`; `422` body has a `detail` list | C2-T2, C2-T5, C2-T6, C2-T7, C2-T8 (string); C2-T3, C2-T4, C2-T13 (list) |
| `text` trimmed and the trimmed text spoken | C2-T1 |
| Other parts ignored | C2-T1 (`voice_name` part) |
| One generation at a time; others wait and are served, never rejected for being busy | C2-T11 |
| Each request, including an identical repeat, runs a new generation | C2-T12 |
| After the response (success or failure) no copy of the sample or generated audio is held, in memory or on the filesystem | C2-T9, C2-T10 (see C2-RSK-2 for the reach of the in-memory check) |
| Chatterbox never reads a voice sample from its own filesystem | C2-T3 (JSON path to an existing local file is refused and the model is not called); C2-T1 (the prompt holds the uploaded bytes) |

Not tested, with reason:

- Failure 7, `500` for other unhandled errors such as a model-load failure: carried-over baseline with an unspecified body; `Plan.md` CRM-2 scope lists only the carried-over text and language validation and generation-failure answer.
- Order in which waiting requests are served: the contract leaves it unspecified ("The order in which waiting requests are served is not specified").
- Waiting time counting toward `VOICE_CLONING_TIMEOUT_SECONDS`: a caller-side rule of the inference service (CCR-9), verified by CRM-4.
- Chatterbox Caller Identity (the application ignores `Authorization`; Cloud Run answers `401`/`403`): CCR-7, verified by CRM-4 and Final Review inspection of CRM-6 per `Plan.md` traceability; not assigned to CRM-2.
- `GET /health`, `GET /v1/metadata`: unchanged by this work item (Plan CRM-3 exclusion "no change to the health or metadata operations"); not in CRM-2 scope.

### Test-design decisions for review

These choices bind the GREEN milestone CRM-3, which may not change these tests.

- C2-D-1 — Model boundary convention. The stand-in model receives the voice sample as `generate(..., audio_prompt_path=<path to a readable file holding the uploaded bytes>)`, the keyword the baseline already uses (`application.py:69`). Consequence: CRM-3 hands the uploaded bytes to the model through a file it creates and removes. Alternative: also accept a file-like object, or the model's own conditioning step. Not chosen, because neither is the boundary the repository uses today and the Plan asks for no model-boundary change.
- C2-D-2 — Stand-in runtime surface. The stand-in `torch`/`torchaudio` provide only what the baseline uses (`application.py:76-86`). Consequence: if CRM-3 used another `torch` or `torchaudio` function, its run would fail with `AttributeError`. That would stop CRM-3 for replanning; it is not fixed in CRM-3. Alternative: a broader stand-in. Not chosen, because a guessed wider surface would be untested speculation.
- C2-D-3 — Filesystem retention check. `tempfile.tempdir` is redirected to a per-test directory (asserted in force with `tempfile.gettempdir()`). After the response, the test asserts that the prompt path the model received no longer exists and that this directory is empty. Alternative: snapshot the whole filesystem. Not chosen, because it is impractical and nondeterministic.
- C2-D-4 — In-memory retention check. After the response, no application module global, nor anything one level inside one, holds the sample bytes, the generated WAV bytes, or a generated tensor. Alternative: a garbage-collector scan. Not chosen, because `bytes` objects are not tracked by `gc`, and the test itself holds equal copies.
- C2-D-5 — Concurrency harness. One `asyncio` event loop runs `httpx.ASGITransport(app, raise_app_exceptions=False)` with `asyncio.gather` over three requests. This works whether CRM-3 serializes with a thread lock in a synchronous route or with a lock in an async route. Alternative: several `TestClient` threads. Not chosen, because each thread runs its own event loop, which would break an async-lock implementation for reasons unrelated to the contract.
- C2-D-6 — Real-transport check (changed in revision 2 with the user's approval). `uvicorn` (declared in `requirements-dev.txt:2`) serves the app in a daemon thread on a loopback socket bound to port `0`. Each request is sent on its own `httpx.Client(trust_env=False)`, opened and closed around that one request, so no request reuses a connection. Each answer is asserted before the next request is sent, so the first answer that differs from the contract ends the test with its own assertion.
  - Why: at RED the baseline's `500` makes `uvicorn` close the connection after answering (see Preconditions / Predecessor Evidence), and in revision 1 a pooled reuse of that connection ended the test with `httpx.ReadError`.
  - Alternative: a subprocess server. Not chosen, because a subprocess cannot see the in-process stand-in runtime.
  - Alternative: keep one client and send `Connection: close` on each request, or set `httpx.Limits(max_keepalive_connections=0)`. Not chosen: both also avoid reuse, but a separate client per request makes the one-connection-per-request rule visible in the test without relying on a pool setting.
  - Alternative: retry a request on `httpx.ReadError`. Not chosen, because retrying would hide a transport failure instead of preventing it.
- C2-D-7 — Server errors observed as answers. `TestClient(raise_server_exceptions=False)` and `ASGITransport(raise_app_exceptions=False)` turn an application exception into a `500` answer that the status assertion reports. Otherwise the exception would propagate out of the client. Alternative: the default (raise). Not chosen, because at RED the baseline raises while building its `422` echo of a binary multipart body. The first dry run showed `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8d` from `fastapi/encoders.py:85`. That would end the test with an exception instead of a contract-status assertion.

No dependency, plugin, marker or configuration setting is introduced. Every import is from the standard library or from packages declared in `requirements-dev.txt` (`fastapi`, `httpx`, `pytest`, `uvicorn`), or is the application module under test.

## Proposed Code / Tests

### `tests/test_chatterbox_service_red.py` — unified diff against the current file

The current file is revision 1's content (SHA-256 `7e7b443dca7f7660319723bef2d8a4e1521c23023d59e716fbc53ff1ba193921`). This diff covers every changed line; the complete final content follows it and is what execution writes.

```diff
--- a/tests/test_chatterbox_service_red.py
+++ b/tests/test_chatterbox_service_red.py
@@ -476,12 +476,15 @@
     with _running_server(chatterbox.app) as base_url:
         with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
             success = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))
+        _assert_valid_wav_answer(success)
+        assert chatterbox.recorder.calls[0]["prompt_bytes"] == sample
+
+        with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
             rejected_path = client.post(SYNTHESIZE, data=_form(sample_path="x"), files=_sample_file(sample))
-            json_body = client.post(SYNTHESIZE, json={"text": "Hello there", "language": "en"})
+        assert rejected_path.status_code == 400, rejected_path.text
+        assert rejected_path.json() == {"detail": SAMPLE_PATH_DETAIL}
 
-    _assert_valid_wav_answer(success)
-    assert chatterbox.recorder.calls[0]["prompt_bytes"] == sample
-    assert rejected_path.status_code == 400, rejected_path.text
-    assert rejected_path.json() == {"detail": SAMPLE_PATH_DETAIL}
-    _assert_validation_error(json_body)
-    assert len(chatterbox.recorder.calls) == 1
+        with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
+            json_body = client.post(SYNTHESIZE, json={"text": "Hello there", "language": "en"})
+        _assert_validation_error(json_body)
+        assert len(chatterbox.recorder.calls) == 1
```

### `tests/test_chatterbox_service_red.py` — complete final content (490 lines, SHA-256 `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`)

```python
"""CRM-2 RED: Chatterbox model API synthesize behavior (chatterbox-cloud-run API-Contract.md).

The model runtime (torch, torchaudio, chatterbox) is not installed locally and is never
loaded here. Each test installs stand-in runtime modules in ``sys.modules`` before it
imports the Chatterbox application, so no CUDA, model weights or network access is needed.
The stand-ins only record what the application hands to the model and encode the samples
the model returns as WAV; every asserted behavior is produced by the application itself.
"""

from __future__ import annotations

import asyncio
import contextlib
import importlib
import io
import os
import socket
import sys
import tempfile
import threading
import time
import types
import wave
from pathlib import Path

import httpx
import pytest
import uvicorn
from fastapi.testclient import TestClient

APP_MODULE = "voice_narration.chatterbox_api.application"
SYNTHESIZE = "/v1/synthesize"
FAKE_SAMPLE_RATE = 24000
GENERATED_SAMPLES = [0.0, 0.25, -0.25, 0.5]
SAMPLE_PATH_DETAIL = "sample_path is not supported; send the voice sample as sample_audio"
SYNTHESIS_FAILED_PREFIX = "chatterbox_synthesis_failed: "


class _Recorder:
    """Test-owned record of every call the application makes to the stand-in model."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.calls: list[dict] = []
        self.active = 0
        self.max_active = 0
        self.delay_seconds = 0.0
        self.error: Exception | None = None


class _FakeTensor:
    """Stand-in for the torch.Tensor surface the application uses."""

    def __init__(self, data) -> None:
        self.data = data

    @property
    def ndim(self) -> int:
        return 2 if self.data and isinstance(self.data[0], list) else 1

    def detach(self) -> "_FakeTensor":
        return self

    def cpu(self) -> "_FakeTensor":
        return self

    def float(self) -> "_FakeTensor":
        return self

    def unsqueeze(self, dim: int) -> "_FakeTensor":
        if dim != 0:
            raise ValueError("stand-in tensor supports unsqueeze(0) only")
        return _FakeTensor([list(self.data)])


def _fake_tensor(data, dtype=None) -> _FakeTensor:
    return _FakeTensor([float(value) for value in data])


def _fake_torchaudio_save(target, tensor, sample_rate, format=None, **kwargs) -> None:
    samples = tensor.data[0] if tensor.ndim == 2 else tensor.data
    frames = bytearray()
    for value in samples:
        clipped = max(-1.0, min(1.0, float(value)))
        frames += int(clipped * 32767).to_bytes(2, "little", signed=True)
    with wave.open(target, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(int(sample_rate))
        writer.writeframes(bytes(frames))


class _FakeMultilingualTTS:
    """Stand-in for chatterbox.mtl_tts.ChatterboxMultilingualTTS.

    ``recorder`` is bound on a per-test subclass, so it is a class attribute and is
    never part of the model instance's own state.
    """

    recorder: _Recorder
    sr = FAKE_SAMPLE_RATE

    @classmethod
    def from_pretrained(cls, device, **kwargs) -> "_FakeMultilingualTTS":
        return cls()

    def generate(self, text, language_id, audio_prompt_path=None, **kwargs) -> _FakeTensor:
        recorder = type(self).recorder
        prompt_path = None
        prompt_existed = False
        prompt_bytes = None
        if audio_prompt_path is not None:
            prompt_path = Path(os.fspath(audio_prompt_path))
            prompt_existed = prompt_path.is_file()
            if prompt_existed:
                prompt_bytes = prompt_path.read_bytes()
        with recorder.lock:
            recorder.active += 1
            recorder.max_active = max(recorder.max_active, recorder.active)
            recorder.calls.append(
                {
                    "text": text,
                    "language_id": language_id,
                    "prompt_path": prompt_path,
                    "prompt_existed": prompt_existed,
                    "prompt_bytes": prompt_bytes,
                }
            )
        try:
            if recorder.delay_seconds:
                time.sleep(recorder.delay_seconds)
            if recorder.error is not None:
                raise recorder.error
            return _FakeTensor([list(GENERATED_SAMPLES)])
        finally:
            with recorder.lock:
                recorder.active -= 1


class _Harness:
    def __init__(self, application: types.ModuleType, recorder: _Recorder, temp_root: Path) -> None:
        self.application = application
        self.app = application.app
        self.recorder = recorder
        self.temp_root = temp_root

    def client(self) -> TestClient:
        return TestClient(self.app, raise_server_exceptions=False)


@pytest.fixture
def chatterbox(monkeypatch, tmp_path):
    recorder = _Recorder()
    temp_root = tmp_path / "process-temp"
    temp_root.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(temp_root))

    model_class = type("ChatterboxMultilingualTTS", (_FakeMultilingualTTS,), {"recorder": recorder})

    torch_module = types.ModuleType("torch")
    torch_module.Tensor = _FakeTensor
    torch_module.float32 = "float32"
    torch_module.tensor = _fake_tensor

    torchaudio_module = types.ModuleType("torchaudio")
    torchaudio_module.save = _fake_torchaudio_save

    chatterbox_package = types.ModuleType("chatterbox")
    chatterbox_package.__path__ = []
    mtl_tts_module = types.ModuleType("chatterbox.mtl_tts")
    mtl_tts_module.ChatterboxMultilingualTTS = model_class
    chatterbox_package.mtl_tts = mtl_tts_module

    monkeypatch.setitem(sys.modules, "torch", torch_module)
    monkeypatch.setitem(sys.modules, "torchaudio", torchaudio_module)
    monkeypatch.setitem(sys.modules, "chatterbox", chatterbox_package)
    monkeypatch.setitem(sys.modules, "chatterbox.mtl_tts", mtl_tts_module)

    sys.modules.pop(APP_MODULE, None)
    application = importlib.import_module(APP_MODULE)
    try:
        yield _Harness(application, recorder, temp_root)
    finally:
        sys.modules.pop(APP_MODULE, None)


def _unique_sample() -> bytes:
    return b"RIFF" + os.urandom(48)


def _form(text: str = "Hello there", language: str = "en", **extra: str) -> dict:
    return {"text": text, "language": language, **extra}


def _sample_file(content: bytes, filename: str = "sample.wav", content_type: str = "audio/wav") -> dict:
    return {"sample_audio": (filename, content, content_type)}


def _wav_rate_and_frames(body: bytes) -> tuple[int, int]:
    with wave.open(io.BytesIO(body), "rb") as reader:
        return reader.getframerate(), reader.getnframes()


def _assert_valid_wav_answer(response: httpx.Response) -> None:
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].split(";")[0].strip().lower() == "audio/wav"
    assert _wav_rate_and_frames(response.content) == (FAKE_SAMPLE_RATE, len(GENERATED_SAMPLES))


def _assert_validation_error(response: httpx.Response) -> None:
    assert response.status_code == 422, response.text
    assert isinstance(response.json()["detail"], list)


def _module_state_holding(application: types.ModuleType, needles: list[bytes]) -> list[str]:
    """Names of application module globals that hold any needle bytes or generated audio."""

    def holds(value) -> bool:
        if isinstance(value, (bytes, bytearray, memoryview)):
            data = bytes(value)
            return any(needle in data for needle in needles)
        if isinstance(value, io.BytesIO):
            data = value.getvalue()
            return any(needle in data for needle in needles)
        return isinstance(value, _FakeTensor)

    found = []
    for name, value in list(vars(application).items()):
        if isinstance(value, (types.ModuleType, type, types.FunctionType)):
            continue
        candidates = [value]
        if isinstance(value, dict):
            candidates += list(value.keys()) + list(value.values())
        elif isinstance(value, (list, tuple, set, frozenset)):
            candidates += list(value)
        elif hasattr(value, "__dict__"):
            candidates += list(vars(value).values())
        if any(holds(candidate) for candidate in candidates):
            found.append(name)
    return found


@contextlib.contextmanager
def _running_server(app):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", lifespan="off"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started:
            if not thread.is_alive() or time.monotonic() > deadline:
                raise RuntimeError("Chatterbox test server did not start")
            time.sleep(0.05)
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()


def test_synthesize_accepts_sample_audio_and_conditions_generation(chatterbox):
    client = chatterbox.client()
    sample = _unique_sample()

    response = client.post(
        SYNTHESIZE,
        data=_form(text="  Hello there  ", language=" EN ", voice_name="ignored extra part"),
        files=_sample_file(sample),
    )

    _assert_valid_wav_answer(response)
    assert len(chatterbox.recorder.calls) == 1
    call = chatterbox.recorder.calls[0]
    assert call["text"] == "Hello there"
    assert call["language_id"] == "en"
    assert call["prompt_existed"] is True
    assert call["prompt_bytes"] == sample

    other_sample = _unique_sample()
    response = client.post(
        SYNTHESIZE,
        data=_form(language="hi"),
        files=_sample_file(other_sample, filename="voice.bin", content_type="application/octet-stream"),
    )

    _assert_valid_wav_answer(response)
    assert len(chatterbox.recorder.calls) == 2
    assert chatterbox.recorder.calls[1]["language_id"] == "hi"
    assert chatterbox.recorder.calls[1]["prompt_bytes"] == other_sample


def test_synthesize_rejects_sample_path_part(chatterbox):
    client = chatterbox.client()

    for value in ("C:/voices/sample.wav", ""):
        response = client.post(
            SYNTHESIZE,
            data=_form(sample_path=value),
            files=_sample_file(_unique_sample()),
        )

        assert response.status_code == 400, response.text
        assert response.json() == {"detail": SAMPLE_PATH_DETAIL}
    assert chatterbox.recorder.calls == []


def test_synthesize_rejects_baseline_json_body(chatterbox, tmp_path):
    client = chatterbox.client()
    existing_sample = tmp_path / "chatterbox-local-sample.wav"
    existing_sample.write_bytes(_unique_sample())

    bodies = [
        {"text": "Hello there", "language": "en"},
        {"text": "Hello there", "language": "en", "sample_path": str(existing_sample)},
        {"text": "Hello there", "language": "en", "sample_path": str(tmp_path / "missing.wav")},
    ]
    for body in bodies:
        _assert_validation_error(client.post(SYNTHESIZE, json=body))
    assert chatterbox.recorder.calls == []


def test_synthesize_missing_or_non_file_parts_are_validation_errors(chatterbox):
    client = chatterbox.client()

    _assert_valid_wav_answer(client.post(SYNTHESIZE, data=_form(), files=_sample_file(_unique_sample())))
    assert len(chatterbox.recorder.calls) == 1

    _assert_validation_error(
        client.post(SYNTHESIZE, data={"language": "en"}, files=_sample_file(_unique_sample()))
    )
    _assert_validation_error(
        client.post(SYNTHESIZE, data={"text": "Hello there"}, files=_sample_file(_unique_sample()))
    )
    _assert_validation_error(client.post(SYNTHESIZE, data=_form(), files={"other": ("x.wav", b"RIFF", "audio/wav")}))
    _assert_validation_error(
        client.post(
            SYNTHESIZE,
            data=_form(sample_audio="not a file part"),
            files={"other": ("x.wav", b"RIFF", "audio/wav")},
        )
    )
    assert len(chatterbox.recorder.calls) == 1


def test_synthesize_rejects_empty_sample_audio(chatterbox):
    client = chatterbox.client()

    response = client.post(SYNTHESIZE, data=_form(), files=_sample_file(b""))

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "sample_audio is required"}
    assert chatterbox.recorder.calls == []


def test_synthesize_keeps_text_and_language_validation(chatterbox):
    client = chatterbox.client()

    for text in ("", "   "):
        response = client.post(SYNTHESIZE, data=_form(text=text), files=_sample_file(_unique_sample()))
        assert response.status_code == 400, response.text
        assert response.json() == {"detail": "text is required"}

    for language in ("fr", "", "  "):
        response = client.post(SYNTHESIZE, data=_form(language=language), files=_sample_file(_unique_sample()))
        assert response.status_code == 400, response.text
        assert response.json() == {"detail": "language must be hi or en"}
    assert chatterbox.recorder.calls == []


def test_synthesize_answers_first_failing_check_in_contract_order(chatterbox):
    client = chatterbox.client()

    _assert_validation_error(
        client.post(SYNTHESIZE, data={"language": "fr", "sample_path": "x"}, files=_sample_file(b""))
    )

    response = client.post(SYNTHESIZE, data=_form(text=" ", language="fr", sample_path="x"), files=_sample_file(b""))
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": SAMPLE_PATH_DETAIL}

    response = client.post(SYNTHESIZE, data=_form(text=" ", language="fr"), files=_sample_file(b""))
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "text is required"}

    response = client.post(SYNTHESIZE, data=_form(language="fr"), files=_sample_file(b""))
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "language must be hi or en"}
    assert chatterbox.recorder.calls == []


def test_synthesize_generation_error_including_unusable_sample_answers_503(chatterbox):
    client = chatterbox.client()
    chatterbox.recorder.error = RuntimeError("sample could not be decoded")

    response = client.post(SYNTHESIZE, data=_form(), files=_sample_file(_unique_sample()))

    assert response.status_code == 503, response.text
    detail = response.json()["detail"]
    assert isinstance(detail, str)
    assert detail.startswith(SYNTHESIS_FAILED_PREFIX)
    assert len(chatterbox.recorder.calls) == 1


def test_synthesize_holds_no_sample_or_audio_after_success(chatterbox):
    assert tempfile.gettempdir() == str(chatterbox.temp_root)
    client = chatterbox.client()
    sample = _unique_sample()

    response = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))

    _assert_valid_wav_answer(response)
    call = chatterbox.recorder.calls[0]
    assert call["prompt_existed"] is True
    assert call["prompt_bytes"] == sample
    assert not call["prompt_path"].exists()
    assert list(chatterbox.temp_root.iterdir()) == []
    assert _module_state_holding(chatterbox.application, [sample, response.content]) == []


def test_synthesize_holds_no_sample_after_generation_failure(chatterbox):
    assert tempfile.gettempdir() == str(chatterbox.temp_root)
    client = chatterbox.client()
    sample = _unique_sample()
    chatterbox.recorder.error = RuntimeError("generation failed")

    response = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))

    assert response.status_code == 503, response.text
    call = chatterbox.recorder.calls[0]
    assert call["prompt_existed"] is True
    assert call["prompt_bytes"] == sample
    assert not call["prompt_path"].exists()
    assert list(chatterbox.temp_root.iterdir()) == []
    assert _module_state_holding(chatterbox.application, [sample]) == []


def test_synthesize_serves_concurrent_requests_one_at_a_time(chatterbox):
    chatterbox.recorder.delay_seconds = 0.3

    async def send_concurrently() -> list[httpx.Response]:
        transport = httpx.ASGITransport(app=chatterbox.app, raise_app_exceptions=False)
        async with httpx.AsyncClient(transport=transport, base_url="http://chatterbox.test", timeout=30) as client:
            return await asyncio.gather(
                *(
                    client.post(SYNTHESIZE, data=_form(text=f"Clip {index}"), files=_sample_file(_unique_sample()))
                    for index in range(3)
                )
            )

    responses = asyncio.run(send_concurrently())

    for response in responses:
        _assert_valid_wav_answer(response)
    assert sorted(call["text"] for call in chatterbox.recorder.calls) == ["Clip 0", "Clip 1", "Clip 2"]
    assert chatterbox.recorder.max_active == 1


def test_synthesize_repeated_identical_requests_each_generate(chatterbox):
    client = chatterbox.client()
    sample = _unique_sample()

    first = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))
    second = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))

    _assert_valid_wav_answer(first)
    _assert_valid_wav_answer(second)
    assert len(chatterbox.recorder.calls) == 2
    assert [call["prompt_bytes"] for call in chatterbox.recorder.calls] == [sample, sample]


def test_synthesize_contract_answers_over_real_transport(chatterbox):
    sample = _unique_sample()
    with _running_server(chatterbox.app) as base_url:
        with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
            success = client.post(SYNTHESIZE, data=_form(), files=_sample_file(sample))
        _assert_valid_wav_answer(success)
        assert chatterbox.recorder.calls[0]["prompt_bytes"] == sample

        with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
            rejected_path = client.post(SYNTHESIZE, data=_form(sample_path="x"), files=_sample_file(sample))
        assert rejected_path.status_code == 400, rejected_path.text
        assert rejected_path.json() == {"detail": SAMPLE_PATH_DETAIL}

        with httpx.Client(base_url=base_url, timeout=30, trust_env=False) as client:
            json_body = client.post(SYNTHESIZE, json={"text": "Hello there", "language": "en"})
        _assert_validation_error(json_body)
        assert len(chatterbox.recorder.calls) == 1
```

## Execution Steps

1. Confirm this plan's Human Review status records approval of revision 2.
2. Confirm `git status --short` shows no change to tracked files under `voice_narration/` or `tests/`, and that `tests/test_chatterbox_service_red.py` is present and untracked.
3. Confirm the current `tests/test_chatterbox_service_red.py` has SHA-256 `7e7b443dca7f7660319723bef2d8a4e1521c23023d59e716fbc53ff1ba193921` (revision 1's content), for example with `certutil -hashfile tests\test_chatterbox_service_red.py SHA256` on Windows or `sha256sum tests/test_chatterbox_service_red.py` on Linux. If it differs, stop and report; do not replace it.
4. Replace the content of `tests/test_chatterbox_service_red.py` with exactly the complete final content above (LF line endings, UTF-8). Confirm the result has SHA-256 `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`.
5. Run verification command V1, then V2 (repeat without cleaning), then V3.
6. Run V4 to confirm the only change is the test file.
7. Record the evidence in `Plan.md` below the Execution Status table and update only the CRM-2 row, as the PDD workflow requires.

## Acceptance / Completion Criteria

- C2-AC-1: `tests/test_chatterbox_service_red.py` exists with exactly the complete final content in Proposed Code / Tests. No other file is created, modified or deleted, apart from this milestone's Execution Status update in `Plan.md`. In particular, no production file, existing test, dependency, `pytest.ini` or other configuration changes.
- C2-AC-2: pytest collects 22 tests without collection, import or fixture-setup errors: the 9 existing tests plus C2-T1–C2-T13.
- C2-AC-3: each of C2-T1–C2-T13 fails with an `AssertionError` raised by its own assertions. The failure class is a response status that differs from the contract's answer, because the multipart request shape, the `sample_path` rejection, the empty-sample answer, the retention behavior and the one-at-a-time serving are missing (the unmodified route still expects a JSON body). Failures from `ImportError`/`ModuleNotFoundError`, fixture errors, server start-up errors (`RuntimeError: Chatterbox test server did not start`), transport errors (`httpx.TransportError` and its subclasses, such as `httpx.ReadError`, `httpx.ConnectError`, `httpx.RemoteProtocolError`) or timeouts are not valid RED evidence.
- C2-AC-4: the 9 pre-existing tests pass.
- C2-AC-5: a second full run without cleaning between runs gives the same result as the first: the same 13 tests fail for the same class of reason, and 9 tests pass.

## Verification

### Commands

Run from the repository root (Windows, the Plan's Verification Commands; on Linux use `.venv/bin/python`):

- V1: `.\.venv\Scripts\python.exe -m pytest tests -ra`
- V2: `.\.venv\Scripts\python.exe -m pytest tests -ra` (second run, no cleaning between runs; required because the tests override `tempfile.tempdir` and `sys.modules`)
- V3: `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -q --tb=short` (shows each new test's first failing assertion for C2-AC-3)
- V4: `git status --short`

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- V1 and V2: exit code 1; `collected 22 items`; summary `13 failed, 9 passed` (plus the existing `StarletteDeprecationWarning` warning); the `FAILED` lines name exactly C2-T1–C2-T13; no `httpx.ReadError` or other transport error appears as any test's failure. C2-T13's captured log may show `uvicorn`'s `Exception in ASGI application` with the baseline's `UnicodeDecodeError`. That is the server-side cause of the `500` answer, not the test's failure.
- V3: every failure is an `AssertionError` on a status comparison, predicted as follows:
  - C2-T1, C2-T4, C2-T9, C2-T11, C2-T12, C2-T13: `assert 500 == 200` (for C2-T13, on its first request; its second and third requests are not sent at RED, because the first assertion ends the test);
  - C2-T2, C2-T6: `assert 500 == 400`;
  - C2-T5, C2-T7: `assert 422 == 400`;
  - C2-T8, C2-T10: `assert 500 == 503`;
  - C2-T3: `assert 200 == 422`.

  The `500` answers come from the unmodified JSON-body route failing while it builds its validation-error echo of a binary multipart body (`UnicodeDecodeError` in `fastapi/encoders.py:85`, observed in the dry run). They are a consequence of the missing multipart request handling, not of the test setup. The exact status per test is a prediction; what C2-AC-3 requires is the failure class.
- V4: the only entries are the untracked artifacts already present (`docs/.ai/chatterbox-cloud-run/API-Contract.md`, `Plan.md`, this Implementation Plan) and `?? tests/test_chatterbox_service_red.py`; no tracked file is modified.
- Preserved-behavior tests (expected to pass at RED): none. `Plan.md` traceability assigns two preserved rows to CRM-2 as verifier: "Carried-over Chatterbox validation and generation-failure behavior (RF-3, RF-4)" and "Consistency and concurrency — a retried request produces a new clip". The contract requires those rules to hold under the new multipart request shape (CCR-6), and the baseline route cannot accept that shape. So C2-T6, C2-T8 and C2-T12 fail at RED because the new request shape is missing, not because of the preserved rules. They are not RED evidence for RF-3, RF-4 or the retry rule. They show that those rules still hold once CRM-3 delivers the shape.

### Planning-Time Dry Run

#### Revision 2 dry run

Planning-time dry run — not milestone evidence. Run on 2026-11-09 in a disposable copy outside the repository. The copy was made with `tar` from the working tree (excluding `.venv`, `.git`, `Voice-Narration.zip`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache`, `.deepeval`) into `C:\Users\avina\AppData\Local\Temp\claude\6b754389e5f1a043\2d723f51-8809-458a-805d-71bf4a41c5a4\scratchpad\rev\repo`. It included the git-ignored `.env` and `service-account-key.json`. The repository's `.venv` interpreter was used with the copy as working directory, with `-p no:cacheprovider`. The revised file was produced from revision 1's extracted code block by replacing only the C2-T13 function. Its diff against the current repository file is exactly the diff above, and its SHA-256 is `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`.

1. Baseline in the copy, with the CRM-2 file moved out:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider
   ======================== 9 passed, 1 warning in 3.85s =========================
   ```

2. Reproduction of the blocker with revision 1's C2-T13: 20 isolated runs of the single test, counting each run's first error line.

   ```
   $ for i in $(seq 1 20); do python -m pytest "tests/test_chatterbox_service_red.py::test_synthesize_contract_answers_over_real_transport" -q --tb=line -p no:cacheprovider | grep -oE "httpx.ReadError: \[WinError [0-9]+\]|assert 500 == 200" | head -1; done | sort | uniq -c
        17 assert 500 == 200
         3 httpx.ReadError: [WinError 10053]
   ```

3. Revised C2-T13, the same 20 isolated runs:

   ```
        20 assert 500 == 200
   ```

   No transport error, server start-up error or other exception occurred in any of the 20 runs.

4. V1 and V2 with the revised file (two consecutive full runs, no cleaning):

   ```
   == V1
   collected 22 items
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_accepts_sample_audio_and_conditions_generation
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_sample_path_part
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_baseline_json_body
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_missing_or_non_file_parts_are_validation_errors
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_empty_sample_audio
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_keeps_text_and_language_validation
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_answers_first_failing_check_in_contract_order
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_generation_error_including_unusable_sample_answers_503
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_or_audio_after_success
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_after_generation_failure
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_serves_concurrent_requests_one_at_a_time
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_repeated_identical_requests_each_generate
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_contract_answers_over_real_transport
   =================== 13 failed, 9 passed, 1 warning in 3.88s ===================
   == V2
   collected 22 items
   (same 13 FAILED lines)
   =================== 13 failed, 9 passed, 1 warning in 3.70s ===================
   ```

   In both runs, filtering the output for `Error` showed no `httpx` transport error. The only non-assertion error text was `uvicorn`'s captured log for C2-T13: `fastapi.exceptions.RequestValidationError: 1 validation error:` / `UnicodeDecodeError: 'utf-8' codec can't decode byte …`. This is the server-side source of the `500`.

5. V3 with the revised file, first failing assertion per test, in file order (C2-T1 to C2-T13):

   ```
   E   assert 500 == 200
   E   assert 500 == 400
   E   assert 200 == 422
   E   assert 500 == 200
   E   assert 422 == 400
   E   assert 500 == 400
   E   assert 422 == 400
   E   assert 500 == 503
   E   assert 500 == 200
   E   assert 500 == 503
   E   assert 500 == 200
   E   assert 500 == 200
   E   assert 500 == 200
   13 failed, 1 warning in 2.93s
   ```

   A second V3 run, counting `ReadError` in its output, printed `0`.

6. Pass proof with a scratch-only probe, which never enters the repository. The copy's `voice_narration/chatterbox_api/application.py` was replaced by a probe of a possible CRM-3 change, rebuilt for this revision because revision 1's probe was deleted. Like revision 1's probe, it uses an async route that reads the form and checks the contract's failures in order. It writes the sample to a `tempfile.mkstemp` file, runs generation in a worker thread under a module `threading.Lock`, deletes the file in `finally`, and encodes with `torchaudio.save`.

   ```
   == probe full suite
   ======================== 22 passed, 1 warning in 4.79s ========================
   == probe C2-T13, 20 isolated runs
        20 1 passed, 1 warning
   == probe without the sample_path rejection, C2-T13 only
   E   assert 200 == 400
   1 failed, 1 warning in 1.34s
   ```

   The last probe shows that C2-T13's second request is still sent and asserted once the first answer is correct. A further probe, with only the probe's explicit non-multipart check removed, still passed C2-T13, because the probe's own missing-part check also answers the JSON body with `422`. It therefore does not isolate the third assertion. That third assertion is unchanged from revision 1 and is also covered by C2-T3. After each probe, the copy's `application.py` was restored and compared with the repository's (`diff` printed nothing; "baseline restored identical").

7. Created during the dry run, all under `C:\Users\avina\AppData\Local\Temp\claude\6b754389e5f1a043\2d723f51-8809-458a-805d-71bf4a41c5a4\scratchpad\rev`, and deleted afterwards: `repo\` (the disposable copy), `plan_code.py` (revision 1's extracted code block), `revised.py` (the revised file), `c2t13.diff`, `old_on_disk.py`, `baseline_application.py`, `probe_application.py`, and for the final artifact check `final_from_plan.py`, `diff_from_plan.diff` and `apply\`. That check confirmed that the plan's code block hashes to `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`, and that the plan's diff applies with `patch -p1` to a copy of the current file and produces that same hash. Nothing was written to the repository except this Implementation Plan.

#### Revision 1 dry run (kept for reference)

In this dry run, C2-T13 gave `assert 500 == 200` in all of its runs. The race in steps 2 and 3 above did not occur there; at the 3-in-20 rate observed above, that is plausible over a few runs.

Planning-time dry run — not milestone evidence. Run on 2026-11-09 in a disposable copy outside the repository, made with `tar` from the working tree (excluding `.venv`, `.git`, `Voice-Narration.zip`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache`) into the session scratchpad at `C:\Users\avina\AppData\Local\Temp\claude\6b754389e5f1a043\2d723f51-8809-458a-805d-71bf4a41c5a4\scratchpad\crm2-dryrun\repo`. The copy included the git-ignored `.env` and `service-account-key.json`, which the preserved narration test needs. The repository's `.venv` interpreter was used with the copy as working directory; `-p no:cacheprovider` kept pytest from writing a cache into the copy.

1. Baseline in the copy, before adding the test:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider
   ======================== 9 passed, 1 warning in 6.19s =========================
   ```

2. RED run with the proposed test file added. The first draft had two defects, both fixed in the code above: a non-file `sample_audio` request without any file part was sent URL-encoded rather than multipart, and default client settings turned the baseline's `UnicodeDecodeError` into a raised exception instead of a `500` answer (C2-D-7). A third change, made after the probe runs in step 3, added the opening missing-part check to C2-T7. That test was then re-run on the baseline (`E   assert 422 == 400`, `1 failed`) and the full suite against the probe (`22 passed, 1 warning in 8.59s`). With the final file, two consecutive full runs without cleaning:

   ```
   == run 1
   collected 22 items
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_accepts_sample_audio_and_conditions_generation
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_sample_path_part
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_baseline_json_body
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_missing_or_non_file_parts_are_validation_errors
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_rejects_empty_sample_audio
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_keeps_text_and_language_validation
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_answers_first_failing_check_in_contract_order
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_generation_error_including_unusable_sample_answers_503
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_or_audio_after_success
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_after_generation_failure
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_serves_concurrent_requests_one_at_a_time
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_repeated_identical_requests_each_generate
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_contract_answers_over_real_transport
   =================== 13 failed, 9 passed, 1 warning in 7.83s ===================
   == run 2
   collected 22 items
   (same 13 FAILED lines)
   =================== 13 failed, 9 passed, 1 warning in 7.08s ===================
   ```

   First failing assertion per test, each run on its own with `--tb=short`:

   ```
   test_synthesize_accepts_sample_audio_and_conditions_generation         assert 500 == 200
   test_synthesize_rejects_sample_path_part                               assert 500 == 400
   test_synthesize_rejects_baseline_json_body                             assert 200 == 422
   test_synthesize_missing_or_non_file_parts_are_validation_errors        assert 500 == 200
   test_synthesize_rejects_empty_sample_audio                             assert 422 == 400
   test_synthesize_keeps_text_and_language_validation                     assert 500 == 400
   test_synthesize_answers_first_failing_check_in_contract_order          assert 422 == 400
   test_synthesize_generation_error_including_unusable_sample_answers_503 assert 500 == 503
   test_synthesize_holds_no_sample_or_audio_after_success                 assert 500 == 200
   test_synthesize_holds_no_sample_after_generation_failure               assert 500 == 503
   test_synthesize_serves_concurrent_requests_one_at_a_time               assert 500 == 200
   test_synthesize_repeated_identical_requests_each_generate              assert 500 == 200
   test_synthesize_contract_answers_over_real_transport                   assert 500 == 200
   ```

   An earlier run with default client settings showed the source of the `500`: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8d in position 424` raised at `fastapi/encoders.py:85` (`bytes: lambda o: o.decode()`), reached from the baseline route's JSON-body validation error.

3. Pass proof with a scratch-only probe, which never enters the repository. The copy's `voice_narration/chatterbox_api/application.py` was replaced by a probe of a possible CRM-3 change. The probe makes the route async, reads the form, checks the contract's failures in order, writes the sample to a `tempfile.mkstemp` file, runs generation in the thread pool under a module `threading.Lock`, deletes the file in `finally`, and encodes with `torchaudio.save` as today.

   ```
   == probe with lock (full suite)
   22 passed, 1 warning in 8.59s
   == probe without lock (new file only)
   E        +  where 3 = <test_chatterbox_service_red._Recorder object at 0x000001CBCFFAC230>.max_active
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_serves_concurrent_requests_one_at_a_time
   1 failed, 12 passed, 1 warning in 5.70s
   == probe keeping the temp file (os.unlink removed)
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_or_audio_after_success
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_after_generation_failure
   2 failed, 11 passed, 1 warning in 15.47s
   == probe caching the sample in a module global
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_or_audio_after_success
   FAILED tests/test_chatterbox_service_red.py::test_synthesize_holds_no_sample_after_generation_failure
   2 failed, 11 passed, 1 warning in 18.08s
   ```

   Then the copy's `application.py` was restored and compared with the repository's (`diff` printed nothing; "baseline restored identical") before the RED runs in step 2 were repeated.

4. Created during the dry run, all under the session scratchpad and deleted afterwards: `crm2-dryrun\repo` (the disposable copy), and `crm2-src\` holding the draft test file, the probe, the baseline copy of `application.py` and the draft of this plan. Nothing was written to the repository except this Implementation Plan.

## Risks

- C2-RSK-1 — Stand-in boundary drift. The tests fix the model and runtime boundary to the baseline's calls (C2-D-1, C2-D-2). If CRM-3 needs a different call, its tests fail for a reason that is not missing behavior. Mitigation inside scope: CRM-3 stops and returns to planning; it does not edit these tests.
- C2-RSK-2 — Limited reach of the retention checks. The filesystem check covers the prompt path handed to the model and the process temporary directory. The in-memory check covers application module globals one level deep (C2-D-3, C2-D-4). A copy kept elsewhere, for example in a closure, a nested object or a file outside the temporary directory, would not be detected. The probes in the dry run show that the checks catch a left-over temporary file and a module-level cached sample. Code review at CRM-3 and Final Review cover the remainder.
- C2-RSK-3 — Timing in the concurrency test. C2-T11 relies on three 0.3-second stand-in generations overlapping when nothing serializes them. The dry-run probe without a lock measured `max_active` 3. If a heavily loaded machine did not overlap the requests, an unserialized implementation could pass C2-T11 by chance (a false pass, never a false failure). This is a hypothesis about scheduling, not an observed failure.
- C2-RSK-4 — Network-dependent preserved test. `test_generation_uses_selected_voice_profile` calls Google TTS with the local key (see Current Repository State). If that call fails at execution for network or credential reasons, C2-AC-4 is not met. Execution then stops and reports it; no rerun-until-pass, skip or change is authorized.
- C2-RSK-5 — Loopback server and connections. C2-T13 binds a dynamically allocated loopback port and stops the server in `finally`. If the server cannot start, the test fails with `RuntimeError: Chatterbox test server did not start`. Revision 2 sends each request on its own client and connection, so no request reuses a connection the server closed after a `500` (C2-D-6); in the dry run, 20 of 20 isolated runs ended with the test's own assertion. If a transport error still occurs at execution, C2-AC-3 excludes it as RED evidence. Execution then stops and reports it; no retry, rerun-until-pass or change is authorized.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `tests/test_chatterbox_service_red.py`; the file exists only because of this milestone (created by the stopped execution of revision 1, replaced by revision 2). No other file is changed by this milestone. Do not use repository-wide reset, clean or checkout operations.

## Explicitly Out of Scope

- Any production change, including `voice_narration/chatterbox_api/application.py` (CRM-3).
- Any change to existing tests (`tests/test_clone_flow.py`, `tests/test_ai_gateway_red.py`, `tests/test_ai_gateway_telemetry_red.py`) — the RF-14 and RF-15 test updates belong to CRM-4.
- Inference-service tests: sample sending, identity token, time limit, failure reasons CFR-1–CFR-9 (CRM-4).
- Dependency, `requirements-dev.txt`, `pytest.ini`, container, deployment or documentation changes; installing the model runtime or acquiring weights.
- Tests of `GET /health`, `GET /v1/metadata`, the Chatterbox Caller Identity rules, or the unspecified `500` answer.
- Duplicate detection, logging, metrics or alerts.

## Human Review

Status: Revision 2 approved by avinash2196 on 2026-11-09. Approval recorded by the main conversation at the user's explicit approval ("Approve and re-run"). Executed on 2026-11-09: RED established, C2-AC-1–C2-AC-5 met; see `Plan.md` "CRM-2 Execution Evidence (revision 2)".

History:

- Revision 1: approved by avinash2196 on 2026-11-09 ("Approve plan 001"). Execution stopped at a blocker — see `Plan.md` "CRM-2 Execution Evidence (stopped)". On 2026-11-09, C2-T13 failed with `httpx.ReadError` in V1 and V2 rather than with an assertion; C2-AC-3 and C2-AC-5 were not met.
- Revision 2: C2-T13 revised at the user's request ("Yes, revise C2-T13"); see Revision. Approved by avinash2196 on 2026-11-09 ("Approve and re-run") and executed — see `Plan.md` "CRM-2 Execution Evidence (revision 2)".
