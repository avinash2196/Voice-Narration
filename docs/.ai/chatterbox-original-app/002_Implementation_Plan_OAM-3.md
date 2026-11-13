# Implementation Plan

## Milestone

OAM-3 — Voice service GREEN (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-3).

## Milestone Type

GREEN

## Review Summary

- Behavior change: the voice service keeps each sample under a storage root, stores Chrome WebM recordings as PCM WAV and other content byte-identical, answers `400` when a WebM cannot be converted, adds `GET /voices/{voice_id}/sample`, keeps voices, samples and updates across restarts, and removes uploaded voices 120 hours after `uploadedAt`.
- Requirements delivered: COA-2, COA-6 (sample storage format), COA-11, COA-12, COA-15, OAD-1; contract OAC-4 and OAC-10 as written in `API-Contract.md`.
- Files: created `voice_narration/simple_voices/recordings.py`, `voice_narration/simple_voices/store.py`; modified `voice_narration/simple_voices/application.py`, `.gitignore`; deleted none.
- Tests added: none. The 11 OAM-2 tests in `tests/test_voice_sample_persistence_red.py` go from failing to passing, unchanged.
- Verification: `python -m pytest tests/test_voice_sample_persistence_red.py -q` twice, then `python -m pytest -q` once. Expected / Predicted — Not Yet Verified: `11 passed` twice. The full suite fails or errors only on the 25 accepted pre-existing tests listed under Accepted Pre-existing Failures (V3Q-1, answered (a)).
- Needs attention: V3R-9. Most of the full suite has never been run to completion on the baseline. Under V3Q-1 (a), any failure outside the accepted list fails the milestone and stops execution, even if it turns out to be pre-existing. Also V3D-1 (the default storage folder `voice_storage/` plus a new `.gitignore` rule), V3D-6 (store and conversion run synchronously on the event loop), and V3R-1 (carried-over behavior has no tests).
- Revision 2 (2026-11-13): records the user's answer to V3Q-1. It changes only the full-suite criterion, its verification and expected evidence, the Preconditions, the risks, and this summary. The proposed code is unchanged (see Revision Notes).

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13 (`requirements.md:17`) |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13, as written (`Plan.md:5`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` (OAM-1 deliverable, authoritative predecessor) | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 row Complete (`Plan.md:334`) |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | Approved by Avinash Srivastava on 2026-11-13, executed (`001_Implementation_Plan_OAM-2.md:669`) |
| Product-level `docs/requirements.md` | Does not exist (checked `docs/`) |
| Reference contract `feature/voice-cloning@abbe387:docs/.ai/chatterbox-cloud-run/API-Contract.md` | Not read. OAM-3 does not touch the Chatterbox call (`Plan.md:165`) |

## Carried-Forward Decisions

From `001_Implementation_Plan_OAM-2.md` (approved, decisions V2D-1 to V2D-6):

- **V2D-1** (`:99-106`): the seam is `create_app(*, root, clock)`, keyword-only. `root` is a directory, `str` or path-like. `clock` is a zero-argument callable returning a naive `datetime`; `None` means the real clock. `create_app()` with no arguments must keep working (`voice_narration/simple_voices/__main__.py:21`), and its default storage location is OAM-3's decision (V3D-1).
- **V2D-2** (`:107-109`): a restart is a new process stopped with `kill()`. So each upload, update and deletion must be on disk under `root` when the operation answers (V3D-2).
- **V2D-3** (`:110-113`): a sample's bytes are kept unencoded in some file under `root`, and they are removed, not marked deleted (V3D-2).
- **V2D-4, V2D-5** (`:114-123`): the test audio and the unconvertible WebM fixture. OAM-3 must recognise that fixture as WebM and answer it with the conversion-failure `400` (V3D-4, V3D-5).
- **V2D-6** (`:124`): the real-transport tests run uvicorn on a dynamic port. Nothing in OAM-3 changes that.

## Preconditions / Predecessor Evidence

- Plan Status records approval (`Plan.md:5`). OAM-3 is recorded as GREEN (`Plan.md:154`), with predecessor OAM-2 (`Plan.md:155`).
- OAM-2 is `Complete — valid RED established 2026-11-13` (`Plan.md:335`). Its evidence (`Plan.md:343-369`): 11 failed in two runs, every failure from the absent `create_app(*, root, clock)` seam, no other cause, and `audio_storage` unchanged. As V2R-2 records, the behavior-level failures behind the seam were shown by the OAM-2 planning stub.
- OAM-3 Execution Status is `Pending` (`Plan.md:336`). No other Implementation Plan exists for it, approved or stopped. Besides this plan, the folder holds only `requirements.md`, `Plan.md`, `API-Contract.md` and `001_Implementation_Plan_OAM-2.md`. This plan was drafted earlier the same day and stopped on V3Q-1. It has never been approved and has not been executed. This revision records the answer.
- Repository state, inspected 2026-11-13: HEAD `1d35815`, branch `claude/chatterbox-original-app-client-a3ef0e`. When first drafted, `git status --short` printed nothing. At this revision it prints only `?? docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md`, which is this plan. Commit `1d35815` holds the OAM-2 test file and the OAM-2 evidence. The committed `tests/test_voice_sample_persistence_red.py` is identical to the OAM-2 plan's code block (`diff` of `001_Implementation_Plan_OAM-2.md:152-578` against the file printed nothing). No change is unrecorded.

## Current Repository State

- `voice_narration/simple_voices/application.py:10`, `:62-63`: one module-level `VOICES` dict, preloaded with the `DEFAULT_GOOGLE_VOICES` dicts themselves. So PATCH mutates the module constant, and every app in a process shares the same voices.
- `voice_narration/simple_voices/application.py:66`: `def create_app() -> FastAPI:` takes no parameters.
- `voice_narration/simple_voices/application.py:83-103`: the hand-written multipart parser. It yields `voice_name` and `audio_data`, which is `b''` when there is no `file` part.
- `voice_narration/simple_voices/application.py:111-112`: `fileSize` is computed from `audio_data`, and `uploadedAt` from `datetime.now()`. `:116` stores the voice; the audio is discarded.
- `voice_narration/simple_voices/application.py:123-127`: every exception in upload is answered `500 Upload failed: <text>`.
- `voice_narration/simple_voices/application.py:151-195`: Lookup, Update and Deletion read `VOICES`. Update applies `name`, `status` and `approvalScore` in that order (`:172-177`). There is no `/voices/{voice_id}/sample` route.
- `voice_narration/simple_voices/application.py:210-217`: one `@app.middleware("http")` adds the CORS headers.
- `voice_narration/simple_voices/__main__.py:21`: `app = create_app()`. `start-voice-service.bat:18`, `:25` run the service after `cd voice_narration`, so the working directory is not the repository root.
- `.gitignore:1-10`: no rule covers a voice storage folder. `git check-ignore` ignores nothing under `voice_storage/` at HEAD.
- `requirements-dev.txt:10-11`: `numpy==2.5.4` and `av==19.0.2` are pinned. `av` 19.0.2 exposes `av.FFmpegError` (checked: `python -c "import av; print(av.__version__, av.FFmpegError.__mro__)"` printed `19.0.2 (<class 'av.error.FFmpegError'>, ...)`).
- No other module imports `voice_narration.simple_voices.application` or `VOICES` (`grep -rn "DEFAULT_GOOGLE_VOICES\|simple_voices\.application\|\bVOICES\b" --include=*.py .` matched only `application.py`, `__main__.py:13` and the OAM-2 test file).
- Line endings: the index holds LF and the worktree has `core.autocrlf=true` (`git ls-files --eol`). The diffs below are against the LF index content.

## Files in Scope

### Files to Create

- `voice_narration/simple_voices/recordings.py`
- `voice_narration/simple_voices/store.py`

### Files to Modify

- `voice_narration/simple_voices/application.py`
- `.gitignore`

### Files to Delete

None.

## Proposed Changes

1. **Create `voice_narration/simple_voices/recordings.py`** (OAD-1, COA-6; contract Voice Upload, Sample storage and failure 2, `API-Contract.md:125`, `:137`):
   - Constants `EBML_MAGIC` and `WEBM_DOCTYPE` (the DocType element `42 82 84` followed by `webm`).
   - `class ConversionError(Exception)`.
   - `is_webm(data: bytes) -> bool`: true when the bytes start with the EBML magic and the EBML header, whose length is read from its variable-length size field, contains the `webm` DocType element (V3D-4).
   - `webm_to_wav(data: bytes) -> bytes`: decodes the first audio stream with `av`, resamples it to signed 16-bit mono at the decoded sample rate, and writes it with the standard `wave` module. It raises `ConversionError` on `av.FFmpegError`, on `IndexError` (no audio stream), or when no audio was decoded (V3D-5).
2. **Create `voice_narration/simple_voices/store.py`** (COA-2, COA-11; contract Durability, Voice Retention, Voice Deletion, `API-Contract.md:141`, `:231`, `:254-262`):
   - Constants `RETENTION = timedelta(hours=120)`, `INDEX_FILE = "voices.json"` and `SAMPLES_DIRECTORY = "samples"`.
   - `class VoiceStore(root, clock)`. On construction it creates `<root>/samples`, loads `<root>/voices.json`, removes expired voices, and removes sample files that no indexed voice owns (V3D-2).
   - Public methods: `__contains__(voice_id)`, `voices()` (upload order), `get(voice_id)`, `sample(voice_id)` (bytes, or `None` for an unknown voice or one with no sample file), `add(voice, sample)`, `update(voice_id, changes)`, `delete(voice_id)`, and `remove_expired()`.
   - Private helpers: `_remove`, `_remove_unindexed_samples`, `_load`, `_save`. `_save` writes `voices.json.tmp` and then calls `os.replace`.
3. **Modify `voice_narration/simple_voices/application.py`** (complete diff below):
   - Imports: add `Response`, `Path`, `ConversionError`, `is_webm`, `webm_to_wav` and `VoiceStore`.
   - Replace the module-level `VOICES` dict and its initialization loop (`:9-10`, `:61-63`) with `DEFAULT_ROOT = <repository root>/voice_storage` (V3D-1) and the constant `CONVERSION_FAILED`, the contract's exact failure-2 body (`API-Contract.md:137`).
   - `create_app(*, root=None, clock=None)` (V2D-1), with its docstring describing both parameters: `clock` defaults to `datetime.now`. It builds `VoiceStore(DEFAULT_ROOT if root is None else root, clock)` and a per-app `preloaded` dict holding copies of `DEFAULT_GOOGLE_VOICES` (contract `:215`, `:231`, `:261`), and adds two local helpers, `all_voices()` (preloaded first, then uploads oldest first, contract `:157`) and `find_voice(voice_id)`.
   - Upload:
     - `sample = webm_to_wav(audio_data) if is_webm(audio_data) else audio_data`;
     - `uploadedAt` comes from `clock()`;
     - `store.add(voice, sample)` replaces `VOICES[voice_id] = voice`;
     - a new `except ConversionError` clause, placed before the existing `except Exception`, answers `400` `CONVERSION_FAILED` (contract `:135-139` order).
   - List and Approved List iterate `all_voices()`. Their per-voice logic is unchanged.
   - Lookup uses `find_voice`.
   - New route `GET /voices/{voice_id}/sample` (contract Voice Sample, `:233-252`): `404 Voice not found` when `find_voice` finds nothing; `404 Voice sample not found` when `store.sample` gives no bytes; otherwise `Response(content=sample, media_type="application/octet-stream")`.
   - Update builds `changes` from `name`, `status` and `approvalScore`, in that order and with the same membership tests as before. An uploaded voice goes through `store.update`, which persists the change. A preloaded voice is updated in memory.
   - Deletion removes a preloaded voice from `preloaded` (in memory, contract `:231`) and an uploaded voice through `store.delete`. Both answer `{"success": true}`. Any other id answers `404`, as before.
   - New middleware `remove_expired_voices`, which calls `store.remove_expired()` before every request (contract `:260`, V3D-3).
   - Unchanged: the multipart parser, the response fields, the `Invalid content type` and `500` paths, the health route, the OPTIONS route and the CORS middleware (V3D-8).
4. **Modify `.gitignore`**: append `/voice_storage/`, anchored to the repository root, so the default storage folder is never committed (CON-6, `Plan.md:165`).

`voice_narration/simple_voices/__main__.py` is not changed: its `create_app()` call keeps working through the defaults (V2D-1).

### Decisions for Review

- **V3D-1 Default storage root: `<repository root>/voice_storage/`, gitignored.**
  - The location is `Path(__file__).resolve().parents[2] / "voice_storage"`. It is anchored to the module's location, not the working directory, because `start-voice-service.bat:18` changes into `voice_narration/` before starting. A planning-time check from `voice_narration/` resolved it to `<copy>/voice_storage`.
  - The new `.gitignore` rule `/voice_storage/` keeps samples out of version control (CON-6).
  - Alternatives:
    - (a) A folder in the user's home directory. It needs no `.gitignore` change, but the voices would live outside the project the user runs, where they are harder to find and remove.
    - (b) A path relative to the working directory. Rejected: the launcher's `cd` would put it under `voice_narration/`.
    - (c) An environment variable. Rejected: "The voice service gains no setting" (`API-Contract.md:481`, `:65`).
- **V3D-2 On-disk layout and write order.**
  - `<root>/voices.json` is a JSON list of the uploaded voices' stored representations, in upload order. It is replaced atomically: written to `voices.json.tmp`, then moved with `os.replace`. `<root>/samples/<voice id>` holds each sample's raw bytes, so V2D-3's disk scan sees them.
  - Upload writes the sample before the index. Deletion and expiry write the index before removing the sample. At each start, sample files that no indexed voice owns are removed. A process killed between the two writes therefore leaves no recoverable sample after the next start (COA-11, "cannot be recovered").
  - The sample file name is always a service-assigned `voice-<8 hex>` id. `VoiceStore.sample` reads a file only for an id already in the index, so a path segment from a request never reaches the file system.
  - Alternatives:
    - (a) One folder per voice. This needs an extra ordering field to keep upload order after a restart (contract `:157`).
    - (b) The sample inside the JSON. Rejected: base64 breaks V2D-3's unencoded-bytes check.
    - (c) Skip the start-time sweep. It is smaller, but a crash mid-deletion would leave a deleted voice's sample on disk.
- **V3D-3 When expired voices are removed.** At store construction, which happens at service start, and in a middleware before every request, including `/health` and `OPTIONS`. This satisfies "no later than the first voice-service request, or the first voice-service start" (`API-Contract.md:260`). The expiry test is `uploadedAt + 120 h <= now`, which matches the RED boundary checks (1 s before is kept, exactly 120 h is removed). Alternative: a background timer. Rejected: the contract needs only request- and start-time removal, and a timer adds a task to run and stop.
- **V3D-4 Recognising WebM.**
  - The bytes must start with the EBML magic `1A 45 DF A3`, and the EBML header, whose size is read from its variable-length size field, must contain the DocType element `42 82 84 "webm"`.
  - A Matroska file (DocType `matroska`) is "any other content" and is stored byte-identical (`API-Contract.md:126`). A planning probe confirmed `is_webm` is `False` for a PyAV Matroska/Opus file and `True` for the OAM-2 `chrome_recording()` and `unconvertible_webm()` fixtures.
  - Alternative: probe the container with `av`. Rejected: its demuxer name, `matroska,webm`, does not tell the two formats apart.
- **V3D-5 Conversion and what "cannot be converted" means.**
  - The first audio stream is decoded and resampled to signed 16-bit mono at its decoded sample rate (48 kHz for Opus). The sample rate and channel count are not contracted (`API-Contract.md:125`).
  - These count as "cannot be converted", answered `400`: any `av.FFmpegError`, no audio stream (`IndexError`), or no decoded audio (a probe showed the OAM-2 fixture raises `av.error.EOFError`, a subclass of `FFmpegError`, and a video-only WebM raises `IndexError`). Any other exception keeps the carried-over `500 Upload failed: <text>`.
  - Alternative: keep the source's channel count. Rejected because it gives a multi-channel WAV for a stereo recording, and nothing requires that.
- **V3D-6 The store and the conversion run synchronously inside the `async` route functions** (python-fastapi "Do not block the async event loop", Medium, justified).
  - Every read-modify-write of the store then runs to completion on the event loop with no `await` in between, so concurrent requests cannot interleave index writes and no lock is needed.
  - Cost: converting a long recording blocks other voice-service requests while it runs. The service is a single local instance (requirements Operational Characteristics).
  - Alternative: `run_in_threadpool`, as `voice_narration/auth/application.py:33` does, plus a lock around the store. That is more code and new concurrency to verify.
- **V3D-7 No service layer** (python-fastapi Layering, Medium, justified). The route functions call `VoiceStore` and `recordings` directly, as the baseline routes used `VOICES` directly. No service layer exists in this module, so LY1 is not High. The business rules (retention, storage format) live in `store.py` and `recordings.py`, not in the routes.
- **V3D-8 The hand-written multipart parser stays unchanged** (`application.py:83-103`). Replacing it with `python-multipart` could change carried-over behavior that no test covers (V3R-1): `name` handling, and the `500` for a missing boundary. The OAM-2 WAV test already shows the parsed bytes are byte-identical to the upload (Plan OAR-5).

## Proposed Code / Tests

### `voice_narration/simple_voices/recordings.py` (new file, complete content)

```python
"""Chrome recordings stored as PCM WAV (Plan OAD-1).

Chrome's recorder produces WebM audio, which the voice service converts to
WAV when it stores the sample. WebM is recognized from the bytes, never from
the file name or content type the upload carries.
"""

import io
import wave

import av

EBML_MAGIC = b"\x1a\x45\xdf\xa3"
WEBM_DOCTYPE = b"\x42\x82\x84webm"


class ConversionError(Exception):
    """A WebM recording could not be converted to WAV."""


def is_webm(data: bytes) -> bool:
    """True when ``data`` starts with an EBML header whose DocType is ``webm``."""
    if len(data) < 5 or not data.startswith(EBML_MAGIC):
        return False
    marker = data[4]
    width = 1
    while width <= 8 and not marker & (0x80 >> (width - 1)):
        width += 1
    if width > 8:
        return False
    size = marker & (0xFF >> width)
    for byte in data[5:4 + width]:
        size = (size << 8) | byte
    header_start = 4 + width
    return WEBM_DOCTYPE in data[header_start:header_start + size]


def webm_to_wav(data: bytes) -> bytes:
    """Decode the recording's first audio stream to 16-bit PCM mono WAV."""
    resampler = av.AudioResampler(format="s16", layout="mono")
    pcm = bytearray()
    rate = 0
    try:
        with av.open(io.BytesIO(data)) as source:
            for frame in source.decode(audio=0):
                for converted in resampler.resample(frame):
                    rate = converted.sample_rate
                    pcm += converted.to_ndarray().tobytes()
        for converted in resampler.resample(None):
            rate = converted.sample_rate
            pcm += converted.to_ndarray().tobytes()
    except (av.FFmpegError, IndexError) as error:
        raise ConversionError(str(error)) from error
    if not pcm:
        raise ConversionError("the recording holds no audio")
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(bytes(pcm))
    return output.getvalue()
```

### `voice_narration/simple_voices/store.py` (new file, complete content)

```python
"""Durable storage of uploaded voices and their samples, with 5-day retention.

Uploaded voices are kept in upload order in one index file under the storage
root, and each sample is kept unencoded in its own file named by the voice id.
The preloaded Google voices are not stored here.
"""

from datetime import datetime, timedelta
import json
import os
from pathlib import Path

RETENTION = timedelta(hours=120)
INDEX_FILE = "voices.json"
SAMPLES_DIRECTORY = "samples"


class VoiceStore:
    def __init__(self, root, clock):
        self._index = Path(root) / INDEX_FILE
        self._samples = Path(root) / SAMPLES_DIRECTORY
        self._samples.mkdir(parents=True, exist_ok=True)
        self._clock = clock
        self._voices = self._load()
        self.remove_expired()
        self._remove_unindexed_samples()

    def __contains__(self, voice_id):
        return voice_id in self._voices

    def voices(self):
        return list(self._voices.values())

    def get(self, voice_id):
        return self._voices.get(voice_id)

    def sample(self, voice_id):
        """The stored sample's bytes, or None for an unknown voice or one without a sample."""
        if voice_id not in self._voices:
            return None
        path = self._samples / voice_id
        return path.read_bytes() if path.is_file() else None

    def add(self, voice, sample):
        if sample:
            (self._samples / voice["id"]).write_bytes(sample)
        self._voices[voice["id"]] = voice
        self._save()

    def update(self, voice_id, changes):
        self._voices[voice_id].update(changes)
        self._save()
        return self._voices[voice_id]

    def delete(self, voice_id):
        self._remove([voice_id])

    def remove_expired(self):
        now = self._clock()
        expired = [
            voice_id for voice_id, voice in self._voices.items()
            if datetime.fromisoformat(voice["uploadedAt"]) + RETENTION <= now
        ]
        if expired:
            self._remove(expired)

    def _remove(self, voice_ids):
        for voice_id in voice_ids:
            del self._voices[voice_id]
        self._save()
        for voice_id in voice_ids:
            (self._samples / voice_id).unlink(missing_ok=True)

    def _remove_unindexed_samples(self):
        for path in self._samples.iterdir():
            if path.name not in self._voices:
                path.unlink()

    def _load(self):
        if not self._index.is_file():
            return {}
        voices = json.loads(self._index.read_text(encoding="utf-8"))
        return {voice["id"]: voice for voice in voices}

    def _save(self):
        temporary = self._index.with_name(INDEX_FILE + ".tmp")
        temporary.write_text(json.dumps(list(self._voices.values())), encoding="utf-8")
        os.replace(temporary, self._index)
```

### `voice_narration/simple_voices/application.py` (complete unified diff against HEAD `1d35815`)

```diff
diff --git a/voice_narration/simple_voices/application.py b/voice_narration/simple_voices/application.py
--- a/voice_narration/simple_voices/application.py
+++ b/voice_narration/simple_voices/application.py
@@ -1,13 +1,19 @@
 """Voice Application - Production API for voice management"""
 
 from fastapi import FastAPI, Request, UploadFile, File, HTTPException
-from fastapi.responses import JSONResponse
+from fastapi.responses import JSONResponse, Response
 from uuid import uuid4
 from datetime import datetime
 import os
+from pathlib import Path
 
-# In-memory storage (development) - replace with DB in production
-VOICES = {}
+from voice_narration.simple_voices.recordings import ConversionError, is_webm, webm_to_wav
+from voice_narration.simple_voices.store import VoiceStore
+
+# Uploaded voices and samples are kept here unless create_app is given a root;
+# the folder is gitignored (CON-6).
+DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "voice_storage"
+CONVERSION_FAILED = {"error": "Upload failed: the recording could not be converted to WAV."}
 
 # Default Google TTS voices available
 DEFAULT_GOOGLE_VOICES = [
@@ -58,13 +64,26 @@ DEFAULT_GOOGLE_VOICES = [
     },
 ]
 
-# Initialize with default voices
-for voice in DEFAULT_GOOGLE_VOICES:
-    VOICES[voice["id"]] = voice
 
+def create_app(*, root=None, clock=None) -> FastAPI:
+    """Create FastAPI application for voice management service.
+
+    ``root`` is the directory that keeps uploaded voices and samples
+    (``DEFAULT_ROOT`` when omitted); ``clock`` returns the current time
+    (``datetime.now`` when omitted).
+    """
+    clock = clock or datetime.now
+    store = VoiceStore(DEFAULT_ROOT if root is None else root, clock)
+    # Preloaded voices return at every start; changes to them last until a restart.
+    preloaded = {voice["id"]: dict(voice) for voice in DEFAULT_GOOGLE_VOICES}
+
+    def all_voices():
+        return list(preloaded.values()) + store.voices()
+
+    def find_voice(voice_id):
+        voice = preloaded.get(voice_id)
+        return voice if voice is not None else store.get(voice_id)
 
-def create_app() -> FastAPI:
-    """Create FastAPI application for voice management service"""
     app = FastAPI(title="Voice Management Service")
 
     @app.get("/health")
@@ -102,6 +121,7 @@ def create_app() -> FastAPI:
                                     audio_data = b'\r\n'.join(lines[i+3:-1])
                                     break
                 
+                sample = webm_to_wav(audio_data) if is_webm(audio_data) else audio_data
                 voice_id = f"voice-{uuid4().hex[:8]}"
                 voice = {
                     "id": voice_id,
@@ -109,17 +129,19 @@ def create_app() -> FastAPI:
                     "format": "WAV",
                     "duration": 45,
                     "fileSize": len(audio_data) if audio_data else len(body),
-                    "uploadedAt": datetime.now().isoformat(),
+                    "uploadedAt": clock().isoformat(),
                     "status": "approved",
                     "approvalScore": 95,
                 }
-                VOICES[voice_id] = voice
+                store.add(voice, sample)
                 return JSONResponse(content=voice, status_code=201)
             else:
                 return JSONResponse(
                     content={"error": "Invalid content type"},
                     status_code=400
                 )
+        except ConversionError:
+            return JSONResponse(content=CONVERSION_FAILED, status_code=400)
         except Exception as e:
             return JSONResponse(
                 content={"error": f"Upload failed: {str(e)}"},
@@ -130,7 +152,7 @@ def create_app() -> FastAPI:
     async def list_voices():
         """List all voices with approved status"""
         voices_list = []
-        for voice_id, voice in VOICES.items():
+        for voice in all_voices():
             voice_copy = dict(voice)
             voice_copy['status'] = 'approved'
             voice_copy['approvalScore'] = voice_copy.get('approvalScore', 95)
@@ -141,7 +163,7 @@ def create_app() -> FastAPI:
     async def list_approved_voices():
         """List approved voices"""
         approved = []
-        for voice_id, voice in VOICES.items():
+        for voice in all_voices():
             if voice.get('status') == 'approved' or not voice.get('status'):
                 voice_copy = dict(voice)
                 voice_copy['status'] = 'approved'
@@ -151,17 +173,35 @@ def create_app() -> FastAPI:
     @app.get("/voices/{voice_id}")
     async def get_voice(voice_id: str):
         """Get voice details"""
-        if voice_id in VOICES:
-            return JSONResponse(content=VOICES[voice_id])
+        voice = find_voice(voice_id)
+        if voice is not None:
+            return JSONResponse(content=voice)
         return JSONResponse(
             content={"error": "Voice not found"},
             status_code=404
         )
 
+    @app.get("/voices/{voice_id}/sample")
+    async def get_voice_sample(voice_id: str):
+        """Return the voice's stored sample"""
+        if find_voice(voice_id) is None:
+            return JSONResponse(
+                content={"error": "Voice not found"},
+                status_code=404
+            )
+        sample = store.sample(voice_id)
+        if not sample:
+            return JSONResponse(
+                content={"error": "Voice sample not found"},
+                status_code=404
+            )
+        return Response(content=sample, media_type="application/octet-stream")
+
     @app.patch("/voices/{voice_id}")
     async def update_voice(voice_id: str, request: Request):
         """Update voice (rename, etc)"""
-        if voice_id not in VOICES:
+        voice = find_voice(voice_id)
+        if voice is None:
             return JSONResponse(
                 content={"error": "Voice not found"},
                 status_code=404
@@ -169,14 +209,17 @@ def create_app() -> FastAPI:
         
         try:
             data = await request.json()
-            if 'name' in data:
-                VOICES[voice_id]['name'] = data['name']
-            if 'status' in data:
-                VOICES[voice_id]['status'] = data['status']
-            if 'approvalScore' in data:
-                VOICES[voice_id]['approvalScore'] = data['approvalScore']
+            changes = {
+                field: data[field]
+                for field in ("name", "status", "approvalScore")
+                if field in data
+            }
+            if voice_id in store:
+                voice = store.update(voice_id, changes)
+            else:
+                voice.update(changes)
             
-            return JSONResponse(content=VOICES[voice_id])
+            return JSONResponse(content=voice)
         except Exception as e:
             return JSONResponse(
                 content={"error": f"Update failed: {str(e)}"},
@@ -186,8 +229,11 @@ def create_app() -> FastAPI:
     @app.delete("/voices/{voice_id}")
     async def delete_voice(voice_id: str):
         """Delete voice"""
-        if voice_id in VOICES:
-            del VOICES[voice_id]
+        if voice_id in preloaded:
+            del preloaded[voice_id]
+            return JSONResponse(content={"success": True})
+        if voice_id in store:
+            store.delete(voice_id)
             return JSONResponse(content={"success": True})
         return JSONResponse(
             content={"error": "Voice not found"},
@@ -207,6 +253,12 @@ def create_app() -> FastAPI:
             }
         )
 
+    # Remove expired voices before any request is answered (Voice Retention)
+    @app.middleware("http")
+    async def remove_expired_voices(request: Request, call_next):
+        store.remove_expired()
+        return await call_next(request)
+
     # Add CORS headers to all responses
     @app.middleware("http")
     async def add_cors_headers(request: Request, call_next):
```

Notes on the diff:

- The context lines `                ` (line 104 of HEAD) and `        ` / `            ` (lines 169 and 178 of HEAD) are whitespace-only lines, kept exactly as they are.
- `voice.update(changes)` mutates only the per-app `preloaded` copy, never `DEFAULT_GOOGLE_VOICES`.

### `.gitignore` (complete unified diff against HEAD `1d35815`)

```diff
diff --git a/.gitignore b/.gitignore
--- a/.gitignore
+++ b/.gitignore
@@ -8,3 +8,4 @@
 service-account-key.json
 *.key
 *.pem
+/voice_storage/
```

### Contract Rule Coverage (the OAM-2 tests this code makes pass)

| Contract rule (`API-Contract.md`) | Code | OAM-2 test |
| --- | --- | --- |
| WebM recognized from bytes and stored as PCM WAV holding the recording (`:125`); `fileSize` before conversion (`:132`) | `is_webm`, `webm_to_wav`; `fileSize` unchanged | `test_chrome_recording_labelled_wav_is_stored_as_pcm_wav_holding_the_recording` |
| Other content stored byte-identical (`:126`) | `sample = ... else audio_data`; `VoiceStore.add` | `test_wav_upload_sample_is_stored_byte_identical`, `test_mp3_and_ogg_uploads_are_accepted_and_kept_as_received[mp3…]`, `[ogg…]` |
| Approved automatically, sample available straight away (`:134`, `:245`) | carried-over `status`/`approvalScore`; sample written before `201` | `test_new_voice_is_approved_automatically_and_its_sample_is_available_straight_away` |
| Voice Sample `200`/`404` bodies and order (`:244-248`) | `get_voice_sample`, `VoiceStore.sample` | `test_sample_answers_not_found_for_unknown_preloaded_and_sampleless_voices` |
| Upload failure 2, nothing stored (`:137`) | `except ConversionError`; conversion before `store.add` | `test_chrome_recording_that_cannot_be_converted_is_rejected_and_creates_no_voice` |
| Durability, list order, every caller sees every voice (`:141`, `:157-158`, `:215`) | `VoiceStore._load`/`_save`, `all_voices`; no header is read | `test_voices_samples_and_renames_survive_a_restart_and_are_listed_for_every_caller` |
| Retention at exactly 120 h; treated as unknown; removed by the first request; preloaded never expire; update does not extend (`:215`, `:258-261`) | `RETENTION`, `remove_expired`, middleware, `preloaded` | `test_voice_expires_120_hours_after_upload_and_is_removed_unrecoverably` |
| Time while stopped counts; removed at the first start (`:260`, `:262`) | `VoiceStore.__init__` calls `remove_expired` | `test_voice_uploaded_before_a_restart_expires_while_the_service_is_stopped` |
| Deletion removes the sample permanently; second delete `404` (`:230-231`) | `delete_voice`, `VoiceStore._remove` | `test_deleting_a_voice_removes_its_sample_permanently_including_after_a_restart` |

Carried-over rules not covered by any test are kept by leaving their code unchanged (V3D-8, V3R-1): health, CORS, `Invalid content type`, the `500` prefixes, `name` defaulting, the fixed `format`/`duration`, and Update's `400`.

## Execution Steps

1. Confirm this plan's Human Review status records approval, and that `git status --short` prints nothing outside `docs/.ai/chatterbox-original-app/`.
2. Create `voice_narration/simple_voices/recordings.py` and `voice_narration/simple_voices/store.py` with exactly the content above.
3. Apply the `application.py` and `.gitignore` diffs, for example by saving each diff block to a file outside the repository and running `git apply <file>`. Then check the result with `git diff` against the diffs above.
4. Run the commands under Verification in order, writing each log outside the repository.
5. Record the evidence in `Plan.md` Execution Status for OAM-3, and update this plan's Human Review status.

## Acceptance / Completion Criteria

- **V3C-1** The repository changes are exactly: the two new files with the content above, and `application.py` and `.gitignore` changed exactly by the diffs above. No test file changes (`git diff --stat -- tests` is empty), and nothing else changes. This excludes the OAM-3 Execution Status update in `Plan.md` and this plan's Human Review status.
- **V3C-2** `python -m pytest tests/test_voice_sample_persistence_red.py -q` reports `11 passed`, with 0 failed and 0 errors.
- **V3C-3** A second run of the same file, with no cleanup between runs, reports `11 passed` (Repeatable, Isolated Verification).
- **V3C-4** The full backend suite runs once (V3Q-1, answered (a)), and all of the following hold:
  - it collects 173 tests with no collection error;
  - the log ends with pytest's final summary line, so the run completed and was not interrupted;
  - every test reported `FAILED` or `ERROR` is one of the 25 node ids under Accepted Pre-existing Failures. Verification command 4 checks this mechanically: its "unexpected" list must be empty.

  Each accepted test's result is recorded in the evidence. An accepted test that now passes, or fails at a different phase, is recorded and does not fail the milestone. Any other failure or error, including one that may be pre-existing, fails the milestone. Execution then stops and reports it. It does not rerun, skip or repair the test.
- **V3C-5** After every test run, `git status --short -- audio_storage` prints nothing, or is restored by OAV-3 (Verification command 6), with what it printed recorded (OAS-1).
- **V3C-6** No `voice_storage/` folder exists in the repository after the runs, because the tests write only under `tmp_path`. `git check-ignore -v voice_storage/voices.json` names the `.gitignore` rule `/voice_storage/`.
- **V3C-7** `create_app` keeps its no-argument call working: its signature is `(*, root=None, clock=None)`, and `DEFAULT_ROOT` is `<repository root>/voice_storage`.

## Verification

### Commands

Run from the repository root in Git Bash. `$TEMP` is outside the repository.

1. `python -m compileall -q voice_narration/simple_voices && echo compiled`
2. `python -m pytest tests/test_voice_sample_persistence_red.py -q > "$TEMP/oam3-green-run1.log" 2>&1; tail -1 "$TEMP/oam3-green-run1.log"` (OAV-1)
3. `python -m pytest tests/test_voice_sample_persistence_red.py -q > "$TEMP/oam3-green-run2.log" 2>&1; tail -1 "$TEMP/oam3-green-run2.log"` (second run, no cleanup)
4. Full suite and the V3Q-1 check (OAV-2, run in the background with a completion notice):
   - 4a. Write the accepted list to `$TEMP/oam3-accepted.txt`, exactly the content of the block under Accepted Pre-existing Failures, with a heredoc: `cat > "$TEMP/oam3-accepted.txt" <<'EOF'`, then the 25 lines, then `EOF`.
   - 4b. `python -m pytest -q > "$TEMP/oam3-full.log" 2>&1; tail -1 "$TEMP/oam3-full.log"; grep -cE "^!+ (Interrupted|KeyboardInterrupt)" "$TEMP/oam3-full.log"`. A count of `0` means the run was not interrupted. A collection error appears as an `ERROR tests/<file>.py` line, and 4c reports it as unexpected.
   - 4c. `grep -E "^(FAILED|ERROR) " "$TEMP/oam3-full.log" | sed -E 's/^(FAILED|ERROR) //; s/ - .*$//' | LC_ALL=C sort -u > "$TEMP/oam3-failing.txt"; echo "unexpected:"; LC_ALL=C comm -23 "$TEMP/oam3-failing.txt" "$TEMP/oam3-accepted.txt"; echo "accepted, not failing:"; LC_ALL=C comm -13 "$TEMP/oam3-failing.txt" "$TEMP/oam3-accepted.txt"; grep -E "^(FAILED|ERROR) " "$TEMP/oam3-full.log"`
   - 4d. `python -m pytest --collect-only -q -p no:cacheprovider > "$TEMP/oam3-collect.log" 2>&1; tail -1 "$TEMP/oam3-collect.log"`
5. `git status --short -- audio_storage` (OAV-3)
6. Only if command 5 printed anything: record its output, then run `git checkout -- audio_storage` and `git clean -fd -- audio_storage`, then repeat command 5, which must print nothing (OAV-3, `Plan.md:323`)
7. `test ! -e voice_storage && echo absent; git check-ignore -v voice_storage/voices.json`
8. `python -c "import inspect; from voice_narration.simple_voices.application import create_app, DEFAULT_ROOT; print(inspect.signature(create_app)); print(DEFAULT_ROOT)"`
9. `git status --short` and `git diff --stat`

### Affected Tests

- `tests/test_voice_sample_persistence_red.py`, the OAM-2 RED evidence. It is the only test that imports `voice_narration.simple_voices` (`grep -rn simple_voices tests`).
- No other test references the changed package or `.gitignore`. The full suite runs once at execution (command 4) under `prompt-driven-development` Test Scope.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Command 1: `compiled`.
- Commands 2 and 3: `11 passed` each.
- Command 4:
  - 4b's last line is pytest's final summary line, and its grep count is `0`.
  - 4c prints an empty `unexpected:` list. Its `accepted, not failing:` list is predicted empty, but any tests in it are recorded, not treated as a failure.
  - 4c's `FAILED`/`ERROR` lines are recorded as the accepted tests' results: predicted to be 3 `FAILED` and 23 `ERROR` lines, with `[materials1]` appearing in both.
  - 4d prints `173 tests collected`.
  - The run is predicted to take more than 30 minutes, based on the baseline timings below.
  - These predictions rest on a baseline that was not run to completion (V3R-9).
- Commands 5–6: command 5 may print the `audio_storage/` changes written by `tests/test_generation_history_download.py` (Plan OAR-1). After command 6, it prints nothing.
- Command 7: `absent`, and `.gitignore:11:/voice_storage/	voice_storage/voices.json`.
- Command 8: `(*, root=None, clock=None)`, and a path ending in `voice_storage` directly under the repository root.
- Command 9: `?? voice_narration/simple_voices/recordings.py`, `?? voice_narration/simple_voices/store.py`, ` M voice_narration/simple_voices/application.py` and ` M .gitignore`, plus work-item changes under `docs/.ai/chatterbox-original-app/`.

### Baseline Pre-existing Failures

This section is added because `implementation-planning` Pre-existing Failures requires the baseline evidence before approval. It was observed once, on 2026-11-13, in a second disposable copy of HEAD `1d35815` (`scratchpad/baseline`, unmodified). It is not milestone evidence.

| Command (in the unmodified copy) | Result |
| --- | --- |
| `timeout 600 python -m pytest tests/test_real_model_inference.py -q -p no:cacheprovider` | `1 failed, 10 skipped in 1.76s`. The failure is `TestRealModelInferenceRED::test_production_inference_module_missing`: `ImportError: cannot import name 'ProductionInferenceProvider' from 'voice_narration.inference.production'` |
| `timeout 900 python -m pytest tests/test_voice_enrollment.py -q -p no:cacheprovider` | `2 failed, 10 passed, 23 errors in 608.10s` (listed below) |
| `timeout 1200 python -m pytest tests --ignore=tests/test_voice_enrollment.py --ignore=tests/test_real_model_inference.py --ignore=tests/test_voice_sample_persistence_red.py -q -p no:cacheprovider` | Killed by `timeout` after 1200 s (`exit 124`). 28 tests had passed, with no failure or error, before it was stopped. Which tests had not run is unknown, because `-q` prints only dots |

`tests/test_voice_enrollment.py` on the baseline:

- **Failed:**
  - `test_ownership_reference_validation_and_live_consent_fence`
  - `test_all_pass_without_override_and_model_minimal_material_selection[materials1]`
- **Errors:**
  - `test_all_pass_without_override_and_model_minimal_material_selection[materials1]` and `[materials2]`
  - `test_evaluator_execution_failure_cannot_be_overridden`
  - `test_multistream_metadata_playback_and_conditioning`
  - `test_upload_model_parts_closed[missing-model_id]`, `[missing-model_version]`, `[blank-model_id]`, `[blank-model_version]`, `[duplicate-model_id]`, `[duplicate-model_version]`, `[malformed-model_id]` and `[malformed-model_version]`
  - `test_unknown_parts_and_unready_models_discard_streams`
  - `test_selected_model_bounds_guidance_and_independent_reuse`
  - `test_catalog_order_limits_and_authenticated_snapshot`
  - `test_profile_limits_filters_and_stable_snapshot`
  - `test_pagination_configuration_fails_closed[pagination0]` to `[pagination5]`
  - `test_nondefault_pagination_controls_both_handlers`
- **Error lines:** 21 × `psycopg.errors.ConnectionTimeout: connection timeout expired`, one each of `psycopg.errors.AdminShutdown`, `psycopg.OperationalError ... server closed the connection unexpectedly`, `PersistenceError: DEPENDENCY_UNAVAILABLE` and `httpx.ReadTimeout`.
- Hypothesis, not established: the file's PostgreSQL-backed fixtures time out in this environment. That would match the user's description "times out" (`Plan.md:35`). None of these tests imports or calls `voice_narration.simple_voices`.

The two files' results match the user-named pre-existing failures in kind (`Plan.md:35`). The full suite took more than 20 minutes without those two files, so command 4 runs in the background. A process from the enrollment run, a `multiprocessing` child spawned at 10:56 whose parent had exited, was still running afterwards. It was stopped (PID 148544).

### Accepted Pre-existing Failures (V3Q-1, answered (a))

These are exactly the tests that failed or errored in the baseline runs above. Together they make 26 baseline entries under 25 node ids: `[materials1]` both failed and errored. Each id was re-confirmed at this revision with `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_voice_enrollment.py tests/test_real_model_inference.py --collect-only -q -p no:cacheprovider` at HEAD `1d35815` (`45 tests collected`; all 25 ids present). The list is sorted with `LC_ALL=C sort` (checked with `sort -c`), as command 4c's `comm` requires. Command 4a writes it to `$TEMP/oam3-accepted.txt` exactly as shown:

```text
tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing
tests/test_voice_enrollment.py::test_all_pass_without_override_and_model_minimal_material_selection[materials1]
tests/test_voice_enrollment.py::test_all_pass_without_override_and_model_minimal_material_selection[materials2]
tests/test_voice_enrollment.py::test_catalog_order_limits_and_authenticated_snapshot
tests/test_voice_enrollment.py::test_evaluator_execution_failure_cannot_be_overridden
tests/test_voice_enrollment.py::test_multistream_metadata_playback_and_conditioning
tests/test_voice_enrollment.py::test_nondefault_pagination_controls_both_handlers
tests/test_voice_enrollment.py::test_ownership_reference_validation_and_live_consent_fence
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination0]
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination1]
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination2]
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination3]
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination4]
tests/test_voice_enrollment.py::test_pagination_configuration_fails_closed[pagination5]
tests/test_voice_enrollment.py::test_profile_limits_filters_and_stable_snapshot
tests/test_voice_enrollment.py::test_selected_model_bounds_guidance_and_independent_reuse
tests/test_voice_enrollment.py::test_unknown_parts_and_unready_models_discard_streams
tests/test_voice_enrollment.py::test_upload_model_parts_closed[blank-model_id]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[blank-model_version]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[duplicate-model_id]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[duplicate-model_version]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[malformed-model_id]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[malformed-model_version]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[missing-model_id]
tests/test_voice_enrollment.py::test_upload_model_parts_closed[missing-model_version]
```

`test_all_pass_without_override_and_model_minimal_material_selection[materials0]` is not on the list: it passed on the baseline.

The user's answer says "failing tests". The plan's option (a), which the user chose, covers "exactly the failing and erroring tests listed under Baseline Pre-existing Failures". So the 23 erroring tests are included. A reviewer who reads the answer as excluding them should say so before approval.

### Planning-Time Dry Run

This is a planning-time dry run, not milestone evidence. It ran on 2026-11-13 in a disposable copy outside the repository: `C:/Users/avina/AppData/Local/Temp/claude/75d22e5e94aa85f8/7c785373-79e0-4451-8aab-0a1437282b97/scratchpad/oam3`, created with `git -c core.autocrlf=false archive HEAD | tar -x`. The repository was not modified.

| Step | Command (in the copy) | Result |
| --- | --- | --- |
| Apply diffs | `git apply --check ../app.diff ../gi.diff && git apply ../app.diff ../gi.diff` | applied cleanly; the result is identical, apart from line endings, to the intended final files |
| Create files | copy `recordings.py`, `store.py` | done |
| Compile | `python -m compileall -q voice_narration tests` | no error |
| Affected tests | `python -m pytest tests/test_voice_sample_persistence_red.py -q -p no:cacheprovider --durations=3` | `11 passed in 64.80s`. Slowest: the stopped-service expiry test at 26.13 s, the restart test at 15.71 s, and the conversion-failure test at 11.35 s |
| Collect | `python -m pytest --collect-only -q -p no:cacheprovider` | `173 tests collected` |
| Isolation | `ls voice_storage` in the copy root after the run | no such folder |
| `.gitignore` rule | `git init -q .; git check-ignore -v voice_storage/voices.json voice_storage/samples/voice-1234abcd; git check-ignore -v voice_narration/voice_storage/x` (temporary `.git` removed afterwards) | both root paths matched `.gitignore:11:/voice_storage/`; the nested path was not ignored (the rule is anchored) |
| No-argument start from the launcher's directory | from `voice_narration/`: `PYTHONPATH=.. python -c "from fastapi.testclient import TestClient; from voice_narration.simple_voices.application import create_app, DEFAULT_ROOT; print(DEFAULT_ROOT); c = TestClient(create_app()); print(c.get('/health').json(), len(c.get('/voices').json()['data']))"` (run as a multi-line `-c` program with `with TestClient(...)`) | `DEFAULT_ROOT` = `<copy>/voice_storage`; `/health` returned `{'status': 'ok', 'service': 'voice-management'}`; 5 voices listed. The folder it created was deleted |
| Library behavior (V3D-4, V3D-5) | probe script `probe/avprobe.py` | `is_webm` was `True` for `chrome_recording()` and `unconvertible_webm()` and `False` for a Matroska/Opus file. The fixture raised `av.error.EOFError` (an `FFmpegError`), a video-only WebM raised `IndexError`, and `AudioResampler.resample(None)` on a fresh resampler returned `[]` |

Revision 2 checks, run on 2026-11-13 for the V3Q-1 change only. The proposed code is unchanged, so the code checks above were not rerun.

| Step | Command | Result |
| --- | --- | --- |
| Repository unchanged since the draft | `git rev-parse --short HEAD; git status --short` | `1d35815`; only `?? docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` |
| Accepted ids exist | the `--collect-only` command under Accepted Pre-existing Failures | `45 tests collected`; all 25 ids present |
| Accepted list sorted | `LC_ALL=C sort -c` on the list; `wc -l` | sorted; `25` |
| Command 4c logic | 4c's pipeline, run in the scratchpad on two synthetic logs: one with exactly the baseline's 3 `FAILED` and 23 `ERROR` lines, one that adds `FAILED tests/test_inference.py::test_new - …` | first log: `unexpected:` empty, `accepted, not failing:` empty; second log: `unexpected:` lists only `tests/test_inference.py::test_new` |
| Command 4b interrupt check | a scratchpad suite with an import-error test file, then without it | the run with the import error: count `1`, and the line `ERROR tests/test_bad.py`, which 4c would report as unexpected; the run without it: count `0` |

An earlier draft of the code also passed 11 tests (`11 passed in 85.63s`). It differed only in handling `ConversionError` inside the `if` block and in `VoiceStore.sample` not checking the id. The final code above is what the table records.

Created during planning, all under the scratchpad folder: `oam3/` and `baseline/` (copies), `proposed/` (draft files), `lfbase/` (HEAD files with LF line endings), `app.diff`, `gi.diff`, `probe/avprobe.py`, and the logs `oam3-run1.log`, `oam3-final.log`, `baseline-real-model.log`, `baseline-enrollment.log` and `baseline-rest.log`, plus `$TEMP/plan_block.py`, which held the OAM-2 code block for the identity `diff`. All were deleted once the plan was written. `git status --short` then showed only this plan. Pytest temporary directories went under the system pytest temp root. `ref-contract.md` in the scratchpad predates this run and was left untouched.

## Risks

- **V3R-1 Carried-over voice-service behavior has no tests** (V2R-3, `001_Implementation_Plan_OAM-2.md:646`). A change to it would not fail any test. Mitigation within scope: the multipart parser, the error paths, the response fields and CORS are left unchanged in the diff (V3D-8). The reviewer can confirm this from the diff hunks above.
- **V3R-2 A corrupt `voices.json` stops the service from starting.** `VoiceStore._load` raises on invalid JSON, so the service exits at start with a traceback. Only this code writes the file, and it writes atomically (V3D-2), so a process kill cannot leave it half-written. A disk failure or a manual edit could.
- **V3R-3 The event loop blocks during conversion and file writes** (V3D-6). A long Chrome recording delays other voice-service requests while it converts. This is accepted for a single local instance.
- **V3R-4 The full suite writes to tracked `audio_storage/`** (Plan OAR-1). Commands 5–6 detect this and restore it as OAV-3 directs, and the output is recorded.
- **V3R-5 Port race in the real-transport tests** (V2R-1). If another process takes the freed port, the service exits during start. That is an environment failure: execution stops and reports it, with no rerun until it passes.
- **V3R-6 Identity comparisons (security).** None. No voice-service operation authenticates a caller or compares an identity, role or owner (`API-Contract.md:58`). Voice ids are compared exactly, as before. The only identifier that reaches the file system is a service-assigned id already in the index (V3D-2).
- **V3R-7 `av` becomes a runtime import of the voice service.** It is already pinned (`requirements-dev.txt:11`), and no version changes. A Python environment without it would fail when the service starts. The launchers use the same environment as the tests (`start-voice-service.bat:25`).
- **V3R-8 The full suite is long, and it can leave processes behind.** On the baseline, `tests/test_voice_enrollment.py` alone took 608 s, and the rest had not finished after 1200 s. One `multiprocessing` child of the enrollment run outlived its parent. After command 4, execution lists the processes it started and stops any that are left, as `prompt-driven-development` Plan Progress requires.
- **V3R-9 Most of the full suite has an unknown baseline** (V3Q-1 (a)). Outside the two named files, only 28 tests were seen passing before the 1200 s cut-off, and which tests had not yet run is unknown (Baseline Pre-existing Failures). Any other failure or error at command 4, whether OAM-3 caused it or it was already there, fails V3C-4. Execution then stops and reports it for the user. It does not classify it as pre-existing, rerun it, or add it to the accepted list. Separately, the enrollment tests' results may depend on database timeouts in this environment. This is the hypothesis noted above, not established. If one of them now passes, it is recorded, not treated as a failure (V3C-4).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `voice_narration/simple_voices/recordings.py` and `voice_narration/simple_voices/store.py`. Reverse the two diffs with `git apply -R <file>` for each saved diff. If a manual run created a `voice_storage/` folder, it holds voice samples: delete it only at the user's word.

## Explicitly Out of Scope

- Per-user voice separation, consent or manual approval (`Plan.md:165`, COA-12, COA-15).
- Any change to the recorder, the upload form, the inference service or the TTS page (`Plan.md:165`), including the Chatterbox call that uses Voice Sample (OAM-4, OAM-5).
- A voice-service setting for the storage location (`API-Contract.md:65`, `:481`).
- Replacing the multipart parser, adding characterization tests, or changing any test (V3D-8, V3R-1).
- Dependency or version changes. `av` and `numpy` stay as pinned.
- Changes to tracked `audio_storage/` files, and committed samples or keys (CON-6).
- Repair of the pre-existing failures.

## Answered Questions

This section is added because the Plan leaves this decision to each Implementation Plan (`Plan.md:81`).

- **V3Q-1 How do V3C-4 and the full-suite run treat the pre-existing backend failures?** Answered by the user on 2026-11-13 (create-implementation-plan arguments): "(a) Accept exactly the failing tests named in the plan as pre-existing failures; any other failure in the full-suite check fails the milestone." Applied in V3C-4, Verification command 4 and Accepted Pre-existing Failures. The question and its options, as originally put: The Plan Status accepts "the two known backend failures" as named old failures (`Plan.md:5`). On the baseline (Baseline Pre-existing Failures), they are one failing test in `tests/test_real_model_inference.py`, and 2 failures plus 23 errors in `tests/test_voice_enrollment.py`. The other files were not run to completion during planning. Options:
  - (a) Accept, by name, exactly the failing and erroring tests listed under Baseline Pre-existing Failures. The run is accepted only when no other test fails or errors, and each named test's result is recorded. A named test that now passes is recorded, not treated as a failure.
  - (b) Accept any failure or error inside `tests/test_voice_enrollment.py` and `tests/test_real_model_inference.py`, recorded by name. Every test in the other files must pass.
  - (c) Run command 4 with `--ignore=tests/test_voice_enrollment.py --ignore=tests/test_real_model_inference.py`, and require every remaining test to pass. Those two files are then not run at OAM-3.
  - (d) Another rule you state.

## Revision Notes

Revision 2, 2026-11-13. It records V3Q-1's answer (a). Changed:

- the Review Summary;
- Preconditions (this plan's own history, and the current `git status`);
- V3C-4;
- Verification command 4 (now 4a to 4d);
- Command 4's Expected Evidence;
- a new Accepted Pre-existing Failures subsection;
- the revision 2 dry-run table;
- the Open Question section, renamed Answered Questions;
- a new risk, V3R-9.

Unchanged: every Proposed Change, all proposed code and diffs, V3C-1 to V3C-3 and V3C-5 to V3C-7, and decisions V3D-1 to V3D-8.

## Human Review

Status: Approved by Avinash Srivastava on 2026-11-13, as written, including V3Q-1 option (a) with the 25-test accepted list (failing and erroring tests).
