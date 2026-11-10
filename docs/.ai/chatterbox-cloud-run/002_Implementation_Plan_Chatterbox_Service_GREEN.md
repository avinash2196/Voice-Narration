# Implementation Plan — CRM-3 Chatterbox Service GREEN

## Milestone

CRM-3 — Chatterbox Service GREEN, work item `chatterbox-cloud-run` (`docs/.ai/chatterbox-cloud-run/Plan.md`, section "CRM-3 — Chatterbox Service GREEN").

Purpose as recorded in `Plan.md`: Chatterbox accepts the voice sample audio, keeps no voice data, and serves one request at a time. Scope: "Chatterbox's synthesize request takes the voice sample audio as the contract defines in place of the sample path; Chatterbox holds no voice sample or generated audio after responding; cloning requests are served one at a time with later requests waiting; carried-over validation and failure behavior stays as contracted." Owned: CCR-6; CCR-10 (Chatterbox holds no voice data); Consistency and concurrency (one request at a time, others wait).

## Milestone Type

GREEN — as recorded in `Plan.md` ("Milestone type: GREEN") and in its Execution Status row "CRM-3 — Chatterbox Service GREEN (GREEN) | Pending". This plan proposes the smallest production change that makes CRM-2's RED tests pass, and changes one production file only.

## Authoritative References

| Document | Status as read |
| --- | --- |
| `docs/.ai/chatterbox-cloud-run/requirements.md` | Approved by avinash2196 on 2026-11-09 (its Status section) |
| `docs/.ai/chatterbox-cloud-run/Plan.md` | Approved by avinash2196 on 2026-11-09 (its Status section). Execution Status: CRM-1 Complete, CRM-2 Complete (revision 2 evidence), CRM-3 Pending |
| `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved by avinash2196 on 2026-11-09 (accepts CCD-1–CCD-7). Authoritative predecessor delivered by CRM-1; the `Plan.md` CRM-1 row is Complete and points to it |
| `docs/.ai/chatterbox-cloud-run/001_Implementation_Plan_Chatterbox_Service_RED.md` (revision 2) | Human Review: "Revision 2 approved by avinash2196 on 2026-11-09 … Executed on 2026-11-09: RED established". Source of carried-forward decisions |
| `docs/requirements.md` (product level) | Absent — `ls docs/requirements.md` answers "No such file or directory" |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Not re-read for this milestone; referenced by `Plan.md` as an unchanged constraint (approved 2026-11-08). CRM-3 does not touch the inference service or the gateway |
| `docs/developer-setup.md` | Repository documentation, not a PDD artifact; source of the verification command (via `Plan.md` Verification Commands) |
| Plugin skills read: `implementation-planning`, `prompt-driven-development` (with `templates/Implementation-Plan.md`), `python-fastapi`, `testing` | Plugin guidance, not project artifacts |

`security` is not applied: CRM-3 owns and verifies no authentication or authorization requirement. The contract states that "The Chatterbox application performs no identity check of its own and ignores the `Authorization` header" (Chatterbox Caller Identity); CCR-7 is owned by CRM-5 and verified by CRM-4 (`Plan.md` Requirement Traceability). This plan adds no identity, role or ownership comparison.

## Carried-Forward Decisions

From `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2 (approved by avinash2196 on 2026-11-09). These bind CRM-3; none is reopened:

- C2-D-1 — Model boundary convention: the model receives the voice sample as `generate(..., audio_prompt_path=<path to a readable file holding the uploaded bytes>)`. Consequence recorded there: "CRM-3 hands the uploaded bytes to the model through a file it creates and removes." This plan does exactly that (C3-D-4).
- C2-D-2 — Stand-in runtime surface: only the `torch`/`torchaudio` calls the baseline uses (`isinstance(..., torch.Tensor)`, `detach`, `cpu`, `float`, `torch.tensor(..., dtype=torch.float32)`, `ndim`, `unsqueeze(0)`, `torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")`). This plan uses exactly that surface and no other `torch` or `torchaudio` function.
- C2-D-3 — Filesystem retention check through `tempfile.tempdir`: this plan creates the prompt file with `tempfile.mkstemp` in the default temporary directory, so the redirected directory is the one checked.
- C2-D-4 — In-memory retention check over application module globals: this plan adds two module globals, `_generation_lock` (a `threading.Lock`, which has no `__dict__`) and the `_GenerationFailed` class; neither holds sample or audio data.
- C2-D-5 — Concurrency harness on one event loop: it "works whether CRM-3 serializes with a thread lock in a synchronous route or with a lock in an async route". This plan uses a thread lock reached from an async route through the thread pool (C3-D-3).
- C2-D-6, C2-D-7 — real-transport check and server errors observed as answers: test-side only; no effect on this plan's code.

Approved contract decisions this milestone implements: CCD-1, CCD-2, CCD-3, CCD-8 (carried-over text, language and generation-failure rules), CCD-9, CCD-10 and CCD-11 of `API-Contract.md`.

## Preconditions / Predecessor Evidence

- Predecessor CRM-2 (RED): `Plan.md` Execution Status row "CRM-2 — Chatterbox Service RED (RED) | Complete | RED established on 2026-11-09 by `001_Implementation_Plan_Chatterbox_Service_RED.md` revision 2: C2-AC-1–C2-AC-5 met; 13 new tests fail on their own status assertions, 9 existing tests pass, in two consecutive full runs." The evidence section "CRM-2 Execution Evidence (revision 2)" records V1 and V2 `13 failed, 9 passed`, V3 first failing assertion per test, and transport-error count `0`.
- The RED evidence is valid for this GREEN: each of C2-T1–C2-T13 failed on a status assertion caused by the missing multipart request handling, `sample_path` rejection, empty-sample answer, retention and one-at-a-time serving.
- RED test file in the repository is the approved one: `sha256sum tests/test_chatterbox_service_red.py` = `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`, the hash approved in Implementation Plan 001 revision 2 and recorded in `Plan.md`.
- Re-observed on the unmodified baseline in this plan's dry run (disposable copy): `13 failed, 9 passed, 1 warning`, the same 13 `FAILED` lines (see Planning-Time Dry Run, step 1).
- CRM-3 is Pending; no other Implementation Plan exists for CRM-3 in the work-item folder (the folder holds `requirements.md`, `Plan.md`, `API-Contract.md`, `001_Implementation_Plan_Chatterbox_Service_RED.md`).
- Milestone type check: `Plan.md` records CRM-3 as GREEN; this plan is GREEN.
- Pre-existing failures: none. On the unmodified baseline the only failing tests are C2-T1–C2-T13, which are this milestone's subject; the 9 other tests pass.

## Current Repository State

Inspected on 2026-11-09.

- `git rev-parse HEAD`: `ac27993ba7df5326425cfaaf4e94dc7ab4eb5b69` ("Add chatterbox-cloud-run Plan, contract and CRM-2 RED tests", which commits `Plan.md`, `API-Contract.md`, Implementation Plan 001 and `tests/test_chatterbox_service_red.py`). `git status --short` prints nothing: the working tree is clean.
- Line endings: `core.autocrlf` is `true`, there is no `.gitattributes`. `git ls-files --eol` shows `voice_narration/chatterbox_api/application.py` as `i/lf w/crlf` (LF in the repository, CRLF in the working tree) and `tests/test_chatterbox_service_red.py` as `i/lf w/lf`. The committed (LF) `application.py` has SHA-256 `e87ae9cdfc057c8c0c7b1fc70d21cb62e0054b13b48aa7897bcba98037b1357e`; the CRLF working-tree file has `036fe6854e64a1de61a96d4466f38823ada2e823c61b7db57c0c3290c66e0362`.
- `voice_narration/chatterbox_api/application.py` (96 lines) is unchanged since the Plan's Current State:
  - imports `torch`, `torchaudio`, `chatterbox.mtl_tts.ChatterboxMultilingualTTS` at module load (`:7-13`), and `pathlib.Path` (`:5`), used only for the sample path;
  - `SynthesizeRequest` JSON body model with `text`, `language`, optional `sample_path` (`:21-24`);
  - `synthesize` is a synchronous route taking that JSON body: text and language checks (`:55-61`), lazy model load (`:63`), sample-path lookup with `404` (`:64-69`), generation with `503` on error (`:71-74`), WAV encoding into an in-memory buffer (`:76-86`);
  - no lock; generation is not serialized.
  - `health` (`:43-50`) and `metadata` (`:89-96`) — not changed by this milestone.
- `voice_narration/chatterbox_api/__main__.py` runs `uvicorn.run(app, host="0.0.0.0", port=8010)`; `cloudrun/chatterbox-service/Dockerfile:20` runs `uvicorn voice_narration.chatterbox_api.application:app`. Both import `app` by name; this plan keeps that name.
- Installed packages relevant to the change (`pip list` in `.venv`, Python 3.13.17): `fastapi 0.162.0`, `starlette 1.10.0`, `python-multipart 0.0.32`, `anyio 4.16.0`, `pydantic 2.14.3`, `uvicorn 0.54.0`, `httpx 0.28.1`, `pytest 9.1.1`. `requirements-dev.txt` declares `fastapi==0.162.0`, `uvicorn==0.54.0`, `python-multipart==0.0.32`; `starlette` is FastAPI's own dependency (`fastapi-0.162.0.dist-info/METADATA`: `Requires-Dist: starlette>=0.46.0`). The model runtime (`torch`, `torchaudio`, `chatterbox`) is not installed locally (Plan Current State); the RED tests install stand-ins.
- Framework behavior this plan depends on, read from the installed code:
  - FastAPI form parameters treat an empty-string form value as absent: `_get_multidict_value` returns `Undefined` when `isinstance(value, str) and value == ""` (`.venv/Lib/site-packages/fastapi/dependencies/utils.py:828-842`). A required `text: str = Form()` would therefore answer an empty `text` with `422`, while the contract requires `400 text is required`, and an optional `sample_path` form parameter could not tell an empty `sample_path` part from no part, while the contract requires `400` "whatever its value (including empty)".
  - Starlette's `Request.form()` answers an unparseable multipart body by raising `starlette.exceptions.HTTPException(status_code=400, …)` (`starlette/requests.py:295-297`, `:309-311`), and returns an empty `FormData` for any other content type (`:313-314`). File parts are parsed into `starlette.datastructures.UploadFile` objects backed by `SpooledTemporaryFile(max_size=1 MiB)` (`starlette/formparsers.py:135`, `:218`); non-file parts are limited to 1 MiB each (`:172-173`); `FormData.close()` closes every `UploadFile` (`starlette/datastructures.py:510-513`).
  - `RequestValidationError` is answered by FastAPI's handler with `422` and `{"detail": jsonable_encoder(exc.errors())}` (`fastapi/exception_handlers.py:20-26`).
  - `fastapi.concurrency.run_in_threadpool` is Starlette's (`fastapi/concurrency.py:9`).
- Tests (`tests/`): `test_ai_gateway_red.py` (5), `test_ai_gateway_telemetry_red.py` (1), `test_clone_flow.py` (3), `test_chatterbox_service_red.py` (13, CRM-2). No existing test other than the CRM-2 file imports `voice_narration.chatterbox_api` (Plan Current State).
- The preserved test `test_generation_uses_selected_voice_profile` calls Google TTS with the local key (Implementation Plan 001, Current Repository State); the full suite therefore needs network access to Google and the git-ignored local key file.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `voice_narration/chatterbox_api/application.py` — the complete final content and a complete unified diff against the committed file are given under Proposed Code / Tests.

### Files to Delete

None.

## Proposed Changes

All in `voice_narration/chatterbox_api/application.py`:

1. Imports:
   1. remove `from pathlib import Path` (only used for the removed sample path);
   2. add `import tempfile` and `import threading`;
   3. extend `from fastapi import FastAPI, HTTPException` to `from fastapi import FastAPI, HTTPException, Request`;
   4. add `from fastapi.concurrency import run_in_threadpool`, `from fastapi.exceptions import RequestValidationError`, `from starlette.datastructures import UploadFile`, `from starlette.exceptions import HTTPException as StarletteHTTPException`.
2. Remove the `SynthesizeRequest` JSON body model (`text`, `language`, `sample_path`) — CCD-1, CCD-2: the JSON body and the `sample_path` field are removed from the request.
3. Add `class _GenerationFailed(Exception)` — raised inside the worker function when `model.generate` raises, so the route can answer `503` after the worker returns.
4. Add the module global `_generation_lock = threading.Lock()` — CCD-9.
5. Add `_validation_error(loc: tuple[str, ...], message: str) -> dict` — builds one validation-error entry `{"type": "value_error", "loc": loc, "msg": message, "input": None}` for the `422` `detail` list. `input` is always `None`, so no part content (including binary sample bytes) is echoed.
6. Add `_synthesize_wav(text: str, language: str, sample: bytes) -> bytes`, run in the thread pool. Under `_generation_lock` it:
   1. loads the model with the unchanged `_get_model()` (so a model-load failure still propagates as the contract's unspecified `500`, failure 7);
   2. creates the prompt file with `tempfile.mkstemp(suffix=".wav")`, writes the sample bytes to it and closes it (C2-D-1, C3-D-4);
   3. calls `model.generate(text, language_id=language, audio_prompt_path=prompt_path)`; an `Exception` from it is re-raised as `_GenerationFailed(str(exc))`;
   4. deletes the prompt file with `os.unlink` in `finally`, on success and on failure (CCD-10);
   5. converts and encodes the result exactly as the baseline does (`application.py:76-84`), and returns the WAV bytes with `buffer.getvalue()`.
7. Replace the synchronous `synthesize(payload: SynthesizeRequest)` route with `async def synthesize(request: Request)` on the same path `POST /v1/synthesize`, which checks in the contract's order (Chatterbox Synthesize, "Failure status codes, in the order they are checked"):
   1. `await request.form()`; a `StarletteHTTPException` from it (unparseable multipart body) is answered as `RequestValidationError` → `422` (failure 1, Contract-Wide Rules "a body that cannot be parsed … is answered `422`") — C3-D-2;
   2. `text` and `language` must be form fields (`str`) and `sample_audio` a file part (`UploadFile`); each that is not adds one entry, and any entry raises `RequestValidationError` → `422` (failure 1). A non-multipart body (for example the baseline JSON) yields an empty form, so it is answered here;
   3. a part named `sample_path`, whatever its value → `400 sample_path is not supported; send the voice sample as sample_audio` (failure 2);
   4. `text.strip()` empty → `400 text is required` (failure 3, carried over);
   5. `language.strip().lower()` not in `{"hi", "en"}` → `400 language must be hi or en` (failure 4, carried over);
   6. `await sample_audio.read()` empty → `400 sample_audio is required` (failure 5);
   7. the form is closed in `finally` (`await form.close()`), on every path after it was parsed, releasing any spooled upload;
   8. `await run_in_threadpool(_synthesize_wav, text, language, sample)`; `_GenerationFailed` → `503` `{"detail": "chatterbox_synthesis_failed: <error text>"}` (failure 6, carried over); success → `Response(content=wav_bytes, media_type="audio/wav")`.
   Parts other than `text`, `language`, `sample_audio` and `sample_path` are not read (ignored). The part filename and content type of `sample_audio` are not read (not significant, CCD-1).
8. `health`, `metadata`, `_get_model`, `SynthesizeMetadata`, `DEVICE`, `MODEL_VARIANT` and `app` are unchanged (Plan CRM-3 exclusion "no change to the health or metadata operations").

### Implementation decisions for review

- C3-D-1 — Read the form directly instead of declaring FastAPI `Form()`/`File()` parameters. Why: FastAPI maps an empty-string form value to "absent" (`fastapi/dependencies/utils.py:828-842`), so declared parameters would answer an empty `text` or `language` with `422` instead of the contract's `400`, and could not detect an empty `sample_path` part; C2-T2, C2-T6 and C2-T7 test exactly those cases. Alternative: declared parameters plus a custom validation-error handler that re-maps errors. Not chosen: it would change the `422` answer for the whole application and still lose the empty `sample_path` part. Consequence: the route has no declared request model, so FastAPI's generated OpenAPI schema for `/v1/synthesize` no longer describes a body; no approved artifact requires that schema.
- C3-D-2 — Unparseable multipart is answered `422`, not Starlette's default `400`. Why: the contract's Contract-Wide Rules require "a body that cannot be parsed as the operation's declared body type (`multipart/form-data` for Chatterbox Synthesize …) is answered `422`", and Starlette raises a `400` for it (`starlette/requests.py:295-297`). No CRM-2 test sends an unparseable multipart body (Implementation Plan 001 does not list it in its coverage table, nor under "Not tested"); the dry run checked it with a scratch-only script (step 4). Alternative: let Starlette answer `400`. Not chosen, because it contradicts the approved contract.
- C3-D-3 — One-at-a-time serving with a module `threading.Lock` held by the worker function in the thread pool, around model loading, generation and encoding. Why: the route must be `async` to read the form, generation is blocking work that must not block the event loop (`python-fastapi` skill), and a thread lock is independent of which event loop serves the request. Waiting requests wait on the lock and are then served, never rejected (CCD-9); the waiting order is the lock's and is not specified (contract). Including model loading under the lock also stops two first requests from loading the model twice. Alternative: an `asyncio.Lock` in the route, with only generation in the thread pool. Not chosen: it binds to one event loop, while the thread lock works for any; both satisfy C2-D-5.
- C3-D-4 — The sample reaches the model through a temporary file created with `tempfile.mkstemp(suffix=".wav")` in the process temporary directory and removed with `os.unlink` in `finally`. Why: C2-D-1 fixes `audio_prompt_path` as the model boundary, and C2-D-3 checks the process temporary directory. The `.wav` suffix keeps the prompt path in the same form the baseline handed to the model, since the voices service always stores samples under a `.wav` name (`voice_narration/simple_voices/application.py:115`); the contract says the uploaded part's own filename is not significant, and it is not used. Alternative: no suffix. Not chosen, to keep the model input path closest to the baseline.
- C3-D-5 — Starlette's default form limits are kept: at most 1000 fields and 1000 files, and at most 1 MiB per non-file part (`starlette/formparsers.py:172-173`, `starlette/requests.py:273-275`). File parts, including `sample_audio`, have no size limit. A body that exceeds a limit raises inside `request.form()` and is therefore answered `422` by C3-D-2. The contract states "No request-size or sample-size limit is defined", which this plan reads as "no limit is contracted": the sample has no limit, and only a `text` field over 1 MiB or more than 1000 parts is affected. Alternative: pass larger limits to `request.form()`. Not chosen, because it would introduce limit values no approved artifact names. Raised for the reviewer's confirmation in Risks (C3-RSK-4).

No dependency, plugin or configuration setting is introduced. Every import is from the standard library (`io`, `os`, `tempfile`, `threading`), from packages declared in `requirements-dev.txt` (`fastapi`; `python-multipart` is what `request.form()` uses), from `starlette`, FastAPI's own dependency (`Requires-Dist: starlette>=0.46.0`, installed 1.10.0), from `pydantic` (already imported by the baseline), or from the model runtime already imported by the baseline (`torch`, `torchaudio`, `chatterbox`).

## Proposed Code / Tests

### `voice_narration/chatterbox_api/application.py` — unified diff against the committed file

Against `git show HEAD:voice_narration/chatterbox_api/application.py` (LF, SHA-256 `e87ae9cdfc057c8c0c7b1fc70d21cb62e0054b13b48aa7897bcba98037b1357e`). This diff covers every changed line; the complete final content follows and is what execution writes.

```diff
--- a/voice_narration/chatterbox_api/application.py
+++ b/voice_narration/chatterbox_api/application.py
@@ -2,13 +2,18 @@
 
 import io
 import os
-from pathlib import Path
+import tempfile
+import threading
 
 import torch
 import torchaudio
-from fastapi import FastAPI, HTTPException
+from fastapi import FastAPI, HTTPException, Request
+from fastapi.concurrency import run_in_threadpool
+from fastapi.exceptions import RequestValidationError
 from fastapi.responses import JSONResponse, Response
 from pydantic import BaseModel
+from starlette.datastructures import UploadFile
+from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from chatterbox.mtl_tts import ChatterboxMultilingualTTS
 
@@ -18,19 +23,18 @@
 app = FastAPI(title="Chatterbox Model API")
 
 
-class SynthesizeRequest(BaseModel):
-    text: str
-    language: str
-    sample_path: str | None = None
-
-
 class SynthesizeMetadata(BaseModel):
     model_id: str
     model_version: str
     sample_rate_hz: int
 
 
+class _GenerationFailed(Exception):
+    """Model generation raised an error; answered as 503 chatterbox_synthesis_failed."""
+
+
 _model: ChatterboxMultilingualTTS | None = None
+_generation_lock = threading.Lock()
 
 
 def _get_model() -> ChatterboxMultilingualTTS:
@@ -40,6 +44,36 @@
     return _model
 
 
+def _validation_error(loc: tuple[str, ...], message: str) -> dict:
+    return {"type": "value_error", "loc": loc, "msg": message, "input": None}
+
+
+def _synthesize_wav(text: str, language: str, sample: bytes) -> bytes:
+    with _generation_lock:
+        model = _get_model()
+        prompt_fd, prompt_path = tempfile.mkstemp(suffix=".wav")
+        try:
+            with os.fdopen(prompt_fd, "wb") as prompt_file:
+                prompt_file.write(sample)
+            try:
+                wav = model.generate(text, language_id=language, audio_prompt_path=prompt_path)
+            except Exception as exc:
+                raise _GenerationFailed(str(exc)) from exc
+        finally:
+            os.unlink(prompt_path)
+
+        if isinstance(wav, torch.Tensor):
+            tensor = wav.detach().cpu().float()
+        else:
+            tensor = torch.tensor(wav, dtype=torch.float32)
+        if tensor.ndim == 1:
+            tensor = tensor.unsqueeze(0)
+
+        buffer = io.BytesIO()
+        torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")
+        return buffer.getvalue()
+
+
 @app.get("/health")
 def health() -> dict[str, str]:
     return {
@@ -51,39 +85,54 @@
 
 
 @app.post("/v1/synthesize")
-def synthesize(payload: SynthesizeRequest):
-    text = payload.text.strip()
-    if not text:
-        raise HTTPException(status_code=400, detail="text is required")
-
-    language = payload.language.strip().lower()
-    if language not in {"hi", "en"}:
-        raise HTTPException(status_code=400, detail="language must be hi or en")
-
-    model = _get_model()
-    kwargs = {"language_id": language}
-    if payload.sample_path:
-        sample = Path(payload.sample_path)
-        if not sample.exists():
-            raise HTTPException(status_code=404, detail="sample_path does not exist")
-        kwargs["audio_prompt_path"] = str(sample)
+async def synthesize(request: Request):
+    try:
+        form = await request.form()
+    except StarletteHTTPException as exc:
+        raise RequestValidationError(
+            [_validation_error(("body",), f"body is not valid multipart/form-data: {exc.detail}")]
+        ) from exc
 
     try:
-        wav = model.generate(text, **kwargs)
-    except Exception as exc:
-        return JSONResponse(status_code=503, content={"detail": f"chatterbox_synthesis_failed: {exc}"})
+        text_value = form.get("text")
+        language_value = form.get("language")
+        sample_audio = form.get("sample_audio")
+
+        errors = []
+        if not isinstance(text_value, str):
+            errors.append(_validation_error(("body", "text"), "text form field is required"))
+        if not isinstance(language_value, str):
+            errors.append(_validation_error(("body", "language"), "language form field is required"))
+        if not isinstance(sample_audio, UploadFile):
+            errors.append(_validation_error(("body", "sample_audio"), "sample_audio file part is required"))
+        if errors:
+            raise RequestValidationError(errors)
+
+        if "sample_path" in form:
+            raise HTTPException(
+                status_code=400,
+                detail="sample_path is not supported; send the voice sample as sample_audio",
+            )
+
+        text = text_value.strip()
+        if not text:
+            raise HTTPException(status_code=400, detail="text is required")
+
+        language = language_value.strip().lower()
+        if language not in {"hi", "en"}:
+            raise HTTPException(status_code=400, detail="language must be hi or en")
+
+        sample = await sample_audio.read()
+        if not sample:
+            raise HTTPException(status_code=400, detail="sample_audio is required")
+    finally:
+        await form.close()
 
-    if isinstance(wav, torch.Tensor):
-        tensor = wav.detach().cpu().float()
-    else:
-        tensor = torch.tensor(wav, dtype=torch.float32)
-    if tensor.ndim == 1:
-        tensor = tensor.unsqueeze(0)
-
-    buffer = io.BytesIO()
-    torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")
-    buffer.seek(0)
-    return Response(content=buffer.read(), media_type="audio/wav")
+    try:
+        wav_bytes = await run_in_threadpool(_synthesize_wav, text, language, sample)
+    except _GenerationFailed as exc:
+        return JSONResponse(status_code=503, content={"detail": f"chatterbox_synthesis_failed: {exc}"})
+    return Response(content=wav_bytes, media_type="audio/wav")
 
 
 @app.get("/v1/metadata")
```

### `voice_narration/chatterbox_api/application.py` — complete final content (145 lines, LF, SHA-256 `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`)

```python
from __future__ import annotations

import io
import os
import tempfile
import threading

import torch
import torchaudio
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from starlette.datastructures import UploadFile
from starlette.exceptions import HTTPException as StarletteHTTPException

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

DEVICE = os.getenv("CHATTERBOX_DEVICE", "cpu")
MODEL_VARIANT = os.getenv("CHATTERBOX_MODEL_VARIANT", "v3")

app = FastAPI(title="Chatterbox Model API")


class SynthesizeMetadata(BaseModel):
    model_id: str
    model_version: str
    sample_rate_hz: int


class _GenerationFailed(Exception):
    """Model generation raised an error; answered as 503 chatterbox_synthesis_failed."""


_model: ChatterboxMultilingualTTS | None = None
_generation_lock = threading.Lock()


def _get_model() -> ChatterboxMultilingualTTS:
    global _model
    if _model is None:
        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)
    return _model


def _validation_error(loc: tuple[str, ...], message: str) -> dict:
    return {"type": "value_error", "loc": loc, "msg": message, "input": None}


def _synthesize_wav(text: str, language: str, sample: bytes) -> bytes:
    with _generation_lock:
        model = _get_model()
        prompt_fd, prompt_path = tempfile.mkstemp(suffix=".wav")
        try:
            with os.fdopen(prompt_fd, "wb") as prompt_file:
                prompt_file.write(sample)
            try:
                wav = model.generate(text, language_id=language, audio_prompt_path=prompt_path)
            except Exception as exc:
                raise _GenerationFailed(str(exc)) from exc
        finally:
            os.unlink(prompt_path)

        if isinstance(wav, torch.Tensor):
            tensor = wav.detach().cpu().float()
        else:
            tensor = torch.tensor(wav, dtype=torch.float32)
        if tensor.ndim == 1:
            tensor = tensor.unsqueeze(0)

        buffer = io.BytesIO()
        torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")
        return buffer.getvalue()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "chatterbox_api",
        "model_variant": MODEL_VARIANT,
        "device": DEVICE,
    }


@app.post("/v1/synthesize")
async def synthesize(request: Request):
    try:
        form = await request.form()
    except StarletteHTTPException as exc:
        raise RequestValidationError(
            [_validation_error(("body",), f"body is not valid multipart/form-data: {exc.detail}")]
        ) from exc

    try:
        text_value = form.get("text")
        language_value = form.get("language")
        sample_audio = form.get("sample_audio")

        errors = []
        if not isinstance(text_value, str):
            errors.append(_validation_error(("body", "text"), "text form field is required"))
        if not isinstance(language_value, str):
            errors.append(_validation_error(("body", "language"), "language form field is required"))
        if not isinstance(sample_audio, UploadFile):
            errors.append(_validation_error(("body", "sample_audio"), "sample_audio file part is required"))
        if errors:
            raise RequestValidationError(errors)

        if "sample_path" in form:
            raise HTTPException(
                status_code=400,
                detail="sample_path is not supported; send the voice sample as sample_audio",
            )

        text = text_value.strip()
        if not text:
            raise HTTPException(status_code=400, detail="text is required")

        language = language_value.strip().lower()
        if language not in {"hi", "en"}:
            raise HTTPException(status_code=400, detail="language must be hi or en")

        sample = await sample_audio.read()
        if not sample:
            raise HTTPException(status_code=400, detail="sample_audio is required")
    finally:
        await form.close()

    try:
        wav_bytes = await run_in_threadpool(_synthesize_wav, text, language, sample)
    except _GenerationFailed as exc:
        return JSONResponse(status_code=503, content={"detail": f"chatterbox_synthesis_failed: {exc}"})
    return Response(content=wav_bytes, media_type="audio/wav")


@app.get("/v1/metadata")
def metadata() -> SynthesizeMetadata:
    model = _get_model()
    return SynthesizeMetadata(
        model_id="chatterbox-multilingual-v3",
        model_version=MODEL_VARIANT,
        sample_rate_hz=model.sr,
    )
```

### Mapping of RED tests to the change

| RED test (Implementation Plan 001) | Made to pass by |
| --- | --- |
| C2-T1 multipart accepted, sample conditions generation | Changes 6, 7.2, 7.8 |
| C2-T2 `sample_path` part, non-empty or empty → `400` | Changes 7.1, 7.3 (raw form keeps the empty part, C3-D-1) |
| C2-T3 baseline JSON body → `422` | Changes 2, 7.2 (empty form for non-multipart content) |
| C2-T4 missing or non-file parts → `422` | Change 7.2 |
| C2-T5 empty `sample_audio` → `400` | Change 7.6 |
| C2-T6 text and language validation | Changes 7.4, 7.5 |
| C2-T7 check order | Order of changes 7.2 → 7.6 |
| C2-T8 generation error → `503` | Changes 3, 6.3, 7.8 |
| C2-T9, C2-T10 no sample or audio held after success or failure | Changes 6.2, 6.4, 7.7; no module global holds data (C2-D-4) |
| C2-T11 one at a time | Changes 4, 6 (C3-D-3) |
| C2-T12 repeated requests each generate | No caching anywhere in changes 6–7 |
| C2-T13 real transport | Changes 7.2, 7.3, 7.8 (no `500` from echoing binary input, change 5) |

## Execution Steps

1. Confirm this plan's Human Review status records approval.
2. Run `git status --short` and confirm no change to tracked files under `voice_narration/` or `tests/`. Confirm `git diff --quiet HEAD -- voice_narration/chatterbox_api/application.py` exits `0` (the file matches the committed baseline). If either check fails, stop and report.
3. Confirm `sha256sum tests/test_chatterbox_service_red.py` (Linux / Git Bash) or `certutil -hashfile tests\test_chatterbox_service_red.py SHA256` (Windows) prints `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`. If it differs, stop and report.
4. Replace the content of `voice_narration/chatterbox_api/application.py` with exactly the complete final content above, with LF line endings (ASCII). Confirm its SHA-256 is `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`. Confirm `git diff -- voice_narration/chatterbox_api/application.py` shows exactly the hunks of the unified diff above (Git may print a warning that LF will be replaced by CRLF, because `core.autocrlf` is `true`; that warning is expected and changes no content).
5. Run C3-V1, then C3-V2 (repeat, no cleaning), then C3-V3.
6. Run C3-V4 and C3-V5.
7. Record the evidence in `Plan.md` below the Execution Status table and update only the CRM-3 row, as the PDD workflow requires.

## Acceptance / Completion Criteria

- C3-AC-1: `voice_narration/chatterbox_api/application.py` has exactly the complete final content in Proposed Code / Tests (SHA-256 `10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a`). No other file is created, modified or deleted, apart from this milestone's Execution Status update in `Plan.md` and this plan's Human Review status. In particular, `tests/test_chatterbox_service_red.py` still has SHA-256 `2ce5b014e87791b329c2222ef9f1fb923a9524489db18a724129a8d1fff156d4`, and no other test, `requirements-dev.txt`, `pytest.ini`, container, deployment or documentation file changes.
- C3-AC-2: the full suite collects 22 tests with no collection, import or fixture error, and all 22 pass: C2-T1–C2-T13 and the 9 pre-existing tests (`test_voice_enrollment_creates_profile`, `test_generation_uses_selected_voice_profile`, `test_voice_cloning_returns_guidance_when_clone_backend_unavailable`, `test_gateway_execution_returns_non_placeholder_telemetry`, and the five tests in `tests/test_ai_gateway_red.py`).
- C3-AC-3: a second full run without cleaning gives the same result: 22 collected, 22 passed.
- C3-AC-4: the inference service, the voices service, the frontend, `health` and `metadata` are not changed: C3-V5 shows that the diff touches only `voice_narration/chatterbox_api/application.py`, and the `health` and `metadata` functions in it are identical to the baseline.

## Verification

### Commands

Run from the repository root (Windows, the Plan's Verification Commands; on Linux use `.venv/bin/python`):

- C3-V1: `.\.venv\Scripts\python.exe -m pytest tests -ra`
- C3-V2: `.\.venv\Scripts\python.exe -m pytest tests -ra` (second run, no cleaning between runs; required because the CRM-2 tests override `tempfile.tempdir` and `sys.modules`, and this change writes temporary files)
- C3-V3: `.\.venv\Scripts\python.exe -m pytest tests/test_chatterbox_service_red.py -q` (the CRM-2 tests on their own)
- C3-V4: `git status --short`
- C3-V5: `git diff --stat` followed by `git diff -- voice_narration/chatterbox_api/application.py`

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- C3-V1 and C3-V2: exit code `0`; `collected 22 items`; summary `22 passed, 1 warning` (the existing `StarletteDeprecationWarning` from `fastapi/testclient.py`); no `FAILED` or `ERROR` line.
- C3-V3: exit code `0`; `13 passed, 1 warning`.
- C3-V4: exactly ` M voice_narration/chatterbox_api/application.py`, plus ` M docs/.ai/chatterbox-cloud-run/Plan.md` after the status update and `?? docs/.ai/chatterbox-cloud-run/002_Implementation_Plan_Chatterbox_Service_GREEN.md` (or ` M` once committed).
- C3-V5: `git diff --stat` lists `voice_narration/chatterbox_api/application.py` (and `Plan.md` after the status update) only; the `application.py` diff equals the unified diff above, with no hunk inside `health` or `metadata`.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. Run on 2026-11-09 in a disposable copy outside the repository, made with `tar` from the working tree at `ac27993` (excluding `.venv`, `.git`, `Voice-Narration.zip`, `frontend`, `audio_storage`, `__pycache__`, `.pytest_cache`, `.deepeval`) into `C:\Users\avina\AppData\Local\Temp\claude\6b754389e5f1a043\2d723f51-8809-458a-805d-71bf4a41c5a4\scratchpad\crm3\repo`. The copy included the git-ignored `.env` and `service-account-key.json`, which the preserved narration test needs. The repository's `.venv` interpreter was used with the copy as working directory, with `-p no:cacheprovider`.

1. Unmodified baseline in the copy:

   ```
   $ python -m pytest tests -ra -p no:cacheprovider
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
   =================== 13 failed, 9 passed, 1 warning in 4.87s ===================
   ```

2. The complete final content above was written over the copy's `voice_narration/chatterbox_api/application.py`:

   ```
   $ sha256sum voice_narration/chatterbox_api/application.py; wc -l voice_narration/chatterbox_api/application.py
   10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a *voice_narration/chatterbox_api/application.py
   145 voice_narration/chatterbox_api/application.py
   == run 1  (python -m pytest tests -ra -p no:cacheprovider)
   collected 22 items
   ======================== 22 passed, 1 warning in 5.26s ========================
   == run 2  (same command, no cleaning)
   collected 22 items
   ======================== 22 passed, 1 warning in 4.67s ========================
   == new file only  (python -m pytest tests/test_chatterbox_service_red.py -q -p no:cacheprovider)
   13 passed, 1 warning in 2.81s
   ```

3. Diff check: the unified diff above was produced with `diff -u` between `git show HEAD:voice_narration/chatterbox_api/application.py` and the final content, then applied with `patch -p1` to a fresh copy of the committed file:

   ```
   patching file voice_narration/chatterbox_api/application.py
   10cc955bcbb54745878eacb8aa5cfd52ea90250f960f7a3834f234d9d2acc54a *voice_narration/chatterbox_api/application.py
   ```

   The patched file has the same hash as the complete final content.

4. Scratch-only check of contract rules that no CRM-2 test covers (a script outside the copy that installed minimal stand-in runtime modules, imported the copy's application and used `TestClient(raise_server_exceptions=False)`; it never entered the repository):

   ```
   malformed multipart: 422 list
   missing boundary: 422 {'detail': [{'type': 'value_error', 'loc': ['body'], 'msg': 'body is not valid multipart/form-data: Missing boundary in multipart.', 'input': None}]}
   urlencoded body: 422 list
   no body: 422 list
   health: {'status': 'ok', 'service': 'chatterbox_api', 'model_variant': 'v3', 'device': 'cpu'}
   ```

   This shows C3-D-2 (unparseable multipart → `422`, not Starlette's `400`), that a non-multipart form body is answered `422`, and that `health` is unchanged.

5. Created during the dry run, all under `C:\Users\avina\AppData\Local\Temp\claude\6b754389e5f1a043\2d723f51-8809-458a-805d-71bf4a41c5a4\scratchpad\crm3`, and deleted afterwards: `repo\` (the disposable copy), `application.py` (the proposed file), `crm3.diff`, `apply\` (diff-apply check) and `checks\extra_checks.py`. Nothing was written to the repository except this Implementation Plan.

## Risks

- C3-RSK-1 — Real model runtime not exercised. The model runtime is not installed locally (Plan Current State), so the change is verified only against the CRM-2 stand-ins. The calls into the runtime (`from_pretrained`, `generate(..., language_id=..., audio_prompt_path=...)`, the `torch`/`torchaudio` conversion and encoding) are the baseline's own calls, unchanged (C2-D-1, C2-D-2). That the real model reads the prompt file and closes it before `generate` returns, so that `os.unlink` succeeds, is a hypothesis; it is not checked here. Running against the real model belongs to the deployment, which is excluded from this work item.
- C3-RSK-2 — Network-dependent preserved test. `test_generation_uses_selected_voice_profile` calls Google TTS with the local key. If it fails at execution for network or credential reasons, C3-AC-2 is not met; execution stops and reports it. No rerun-until-pass, skip or change is authorized.
- C3-RSK-3 — Waiting requests occupy worker threads. A request waiting for `_generation_lock` waits inside a thread-pool worker (C3-D-3), so many concurrent requests would each hold a worker while waiting. `Plan.md` RSK-2 records that CRM-6 documents instance and per-instance request settings consistent with one-at-a-time serving; this plan adds nothing for it.
- C3-RSK-4 — Starlette's default form limits (C3-D-5). A `text` field over 1 MiB, or more than 1000 parts, is answered `422`. The contract defines no request-size or sample-size limit; this plan reads that as "no limit contracted" and keeps the framework defaults. The reviewer confirms or corrects that reading at review. The sample itself has no limit.
- C3-RSK-5 — Large samples spool to disk during the request. A `sample_audio` part over 1 MiB is held by Starlette in a `SpooledTemporaryFile` that moves to a temporary file (`starlette/formparsers.py:135`, `:218`). The route closes the form in `finally` (`starlette/datastructures.py:510-513`). The CRM-2 retention tests use 52-byte samples, so this path is not exercised by them. That closing the spooled file removes its data from disk relies on Python's `tempfile` behavior for unnamed temporary files, which is not tested here (hypothesis). Code review at Final Review covers it.
- C3-RSK-6 — `metadata` loads the model outside the lock. `GET /v1/metadata` calls `_get_model()` without `_generation_lock` (unchanged, `application.py:89-96`), so a first `metadata` call concurrent with a first synthesize could load the model twice. This is baseline behavior; the Plan excludes changes to the metadata operation.
- C3-RSK-7 — Inference service not yet compatible. Between CRM-3 and CRM-5 the repository's inference service still sends the baseline JSON body and would receive `422` from a running Chatterbox, as the contract's Compatibility Notes state. No existing test calls Chatterbox for real (`test_gateway_execution_returns_non_placeholder_telemetry` replaces the HTTP call; the no-backend test configures no base URL), and the dry run shows all 9 pre-existing tests pass.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Restore only `voice_narration/chatterbox_api/application.py` to its committed content with `git restore -- voice_narration/chatterbox_api/application.py`. No other file is changed by this milestone. Do not use repository-wide reset, clean or checkout operations.

## Explicitly Out of Scope

- Any change to the inference service (`voice_narration/inference/`), voices service, frontend or narration: sample sending, identity token, time limit and failure reasons CFR-1–CFR-9 belong to CRM-4 and CRM-5.
- Any test change, including `tests/test_chatterbox_service_red.py` and the RF-14 and RF-15 tests.
- Container, deployment, `.dockerignore`, `requirements-dev.txt`, `pytest.ini` or documentation changes (CRM-6), and installing the model runtime or acquiring weights.
- Changes to `GET /health` or `GET /v1/metadata`.
- Caller identity checks in the application (the contract assigns the check to Cloud Run).
- Duplicate detection, logging, metrics or alerts.
- Request-size or sample-size limits beyond the framework defaults kept by C3-D-5.

## Human Review

Status: Approved by avinash2196 on 2026-11-09 ("Approve and run"). Executed on 2026-11-09: GREEN verified, C3-AC-1–C3-AC-4 met. Evidence is in `Plan.md`, "CRM-3 Execution Evidence".
