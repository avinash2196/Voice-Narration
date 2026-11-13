# Implementation Plan

## Milestone

OAM-2 — Voice service RED (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-2).

## Milestone Type

RED

## Review Summary

- Behavior change: tests only.
- Requirements covered (verified, not delivered): COA-2, COA-6 (storage), COA-11, COA-12, COA-15, OAD-1; contract OAC-4 and OAC-10 rules listed under Contract Rule Coverage.
- Files: created `tests/test_voice_sample_persistence_red.py`; modified none; deleted none.
- Tests added: 11 (10 functions, one with two parameters). They prove that a Chrome WebM recording is stored as PCM WAV, that WAV, MP3 and OGG uploads are kept as received, and that the sample can be fetched straight away. They also prove the conversion-failure `400`, that voices, samples and renames survive a process restart for every caller, the 120-hour expiry with unrecoverable removal, and that deletion removes the sample.
- Verification: `python -m pytest tests/test_voice_sample_persistence_red.py -q`, run twice. Expected / Predicted — Not Yet Verified: `11 failed` each time, and every failure is `TypeError: create_app() got an unexpected keyword argument 'root'`.
- Needs attention: V2D-1, the `create_app(*, root, clock)` test seam that binds OAM-3. V2R-2: at execution, RED shows only the absent-seam `TypeError`; the behavior-level failures were shown by the planning stub. V2R-3: carried-over voice-service behavior has no tests.

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13 (`requirements.md:17`) |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13, as written (`Plan.md:5`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` (OAM-1 deliverable, authoritative predecessor) | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 row Complete (`Plan.md:334`) |
| Earlier Implementation Plans in this work item | None exist (folder holds only `requirements.md`, `Plan.md`, `API-Contract.md`) |
| Product-level `docs/requirements.md` | Does not exist (checked `docs/`) |
| Reference contract `feature/voice-cloning@abbe387:docs/.ai/chatterbox-cloud-run/API-Contract.md` | Not read. OAM-2 does not touch the Chatterbox call, and the Plan names it only for OAM-4/OAM-5 |

## Carried-Forward Decisions

None.

## Preconditions / Predecessor Evidence

- Plan Status records approval (`Plan.md:5`). Milestone type recorded as RED (`Plan.md:134`). Predecessor OAM-1 (`Plan.md:135`) is Complete, pointing to the approved contract (`Plan.md:334`).
- OAM-2 Execution Status is `Pending` (`Plan.md:335`). No Implementation Plan exists for it, approved or stopped.
- No FOUNDATION milestone precedes OAM-2 (`Plan.md:114`, `:145`). The prerequisites were checked in the dry run below. pytest 9.1.1, httpx 0.28.1, fastapi 0.162.0, uvicorn 0.54.0, python-multipart, numpy 2.5.4 and av 19.0.2 are all importable, and they are pinned in `requirements-dev.txt:1-11`. The av build provides the `libopus` and `libmp3lame` encoders and the `webm`, `ogg` and `mp3` containers.
- Repository state: HEAD `8d9c5c8`, branch `claude/chatterbox-original-app-client-a3ef0e`, and `git status --short` printed nothing (inspected 2026-11-13). No change is unrecorded.

## Current Repository State

- `voice_narration/simple_voices/application.py:66` is `def create_app() -> FastAPI:`, which takes no parameters. A call with `root=` or `clock=` raises `TypeError` (observed in the dry run).
- `voice_narration/simple_voices/application.py:10`, `:62-63` hold the voices in a module-level dict. In-process re-creation of the app therefore keeps voices, so restart tests use a fresh process (V2D-2).
- `voice_narration/simple_voices/application.py:102`, `:111` extract the file bytes and keep only their length. There is no `/voices/{voice_id}/sample` route (`:129-195`). A `GET` on that path matches only `@app.options("/{path:path}")` (`:197`), and the answer is `405` (observed with the stub).
- `voice_narration/simple_voices/application.py:112` sets `uploadedAt` from `datetime.now()`, which is not injectable at baseline.
- `voice_narration/simple_voices/application.py:13-58` defines the five preloaded voice ids, in the order `PRELOADED_VOICE_IDS` uses.
- `voice_narration/simple_voices/__main__.py:21` calls `create_app()` with no arguments. GREEN must keep that call working (V2D-1).
- `voice_narration/auth/application.py:11` sets the repository convention for injected dependencies: keyword-only `root` (storage directory) and `clock` (callable). V2D-1 follows it.
- `tests/test_authentication_consent.py:41-58` sets the repository convention for real-transport tests: uvicorn on a dynamically allocated `127.0.0.1` port with `httpx.Client(trust_env=False)`.
- `pytest.ini:2-4`: `--strict-config --strict-markers`, `testpaths = tests`, `pythonpath = .`. The new file uses no marker.
- No existing test imports `voice_narration.simple_voices` (`grep -rn simple_voices tests` found nothing).

## Files in Scope

### Files to Create

- `tests/test_voice_sample_persistence_red.py`

### Files to Modify

None.

### Files to Delete

None.

## Proposed Changes

1. Create `tests/test_voice_sample_persistence_red.py`. It holds:
   - **Constants:** `PRELOADED_VOICE_IDS` (contract Voice List ordering), `UPLOAD_TIME`, `RETENTION = timedelta(hours=120)` (contract Voice Retention), and the three normative error bodies: `VOICE_NOT_FOUND`, `SAMPLE_NOT_FOUND` and `CONVERSION_FAILED` (contract Voice Sample, Voice Upload failure 2).
   - **`SERVER_SCRIPT`:** a `python -c` program that runs `uvicorn.run(create_app(root=..., clock=...))` on `127.0.0.1:<port>`, with an optional fixed clock instant (V2D-1, V2D-2).
   - **Audio builders (V2D-4):**
     - `sine_pcm` and `encoded_audio(container, codec)` build 1 s of a 440 Hz sine, 48 kHz mono, with `av`.
     - `chrome_recording()` gives WebM/Opus.
     - `wav_upload()` gives a PCM WAV whose frames contain `\r\n` and `--` runs (Plan OAR-5).
     - `unconvertible_webm()` gives a real EBML/WebM header followed by undecodable bytes (V2D-5).
     - `multipart_without_file_part(name)` builds a multipart body that has a `name` part and no `file` part.
   - **HTTP helpers:**
     - `upload` sends the `file` and `name` parts as `VoiceRecorder.tsx`/`VoiceUpload.tsx` do.
     - `uploaded_voice_id` asserts `201`.
     - `listed_ids` returns the ids in list order.
     - `fetch_sample` asserts `200`, `application/octet-stream` and a non-empty body.
     - `assert_not_found` asserts `404` and the exact body.
   - **Storage and audio checks:**
     - `storage_holds(root, data)` scans every file under `root` for the bytes (V2D-3).
     - `decoded_pcm_wav` reads the sample with the standard `wave` module, which reads PCM only, and supports 8-, 16-, 24- and 32-bit samples.
     - `dominant_frequency` finds the strongest frequency.
   - **Service runners:**
     - `free_port` and `wait_until_healthy` support `running_voice_service(root, log_path, fixed_time=None)`. That function starts the service as its own process, waits for `GET /health` `200`, yields an `httpx.Client`, and kills the process on exit (V2D-2, V2D-6).
     - `in_process_voice_service(root, clock)` wraps `TestClient(create_app(root=root, clock=clock))`.
   - **Fixture:** `root` gives a fresh `tmp_path / "voice-store"` directory.
   - **The 10 test functions** listed under Contract Rule Coverage.
2. No production, build or configuration file changes. No existing test changes.

### Decisions for Review (binding OAM-3)

- **V2D-1 Test seam `create_app(*, root, clock)`.**
  - Every test builds the voice service as `create_app(root=<directory>, clock=<callable or None>)`, keyword-only. `root` is a `str` or path-like directory under which the service keeps voices and samples. `clock` is a zero-argument callable returning a naive `datetime` on the service's clock. `None` means the real clock.
  - What `create_app()` does with no arguments (`__main__.py:21`), including the default storage location, is OAM-3's decision, bounded by CON-6 and the OAM-3 exclusions (`Plan.md:165`).
  - Reason: this follows `voice_narration/auth/application.py:11`. The contract leaves the storage location uncontracted and adds no voice-service setting (`API-Contract.md:65`, `:481`), so an in-code parameter is the only seam that adds no operator setting.
  - Alternatives:
    - (a) An environment variable for the storage directory. Rejected, because the contract states "The voice service gains no setting" (`API-Contract.md:481`).
    - (b) Monkeypatching module globals and the module-level `datetime`. Rejected: it binds GREEN to module-global state, which `application.py:10` already shows hides restart loss in-process. It would also bind GREEN to calling `datetime.now` by that module name.
    - (c) `chdir` into `tmp_path` and relying on a relative default. Rejected, because it would fix the default location, which is OAM-3's decision.
- **V2D-2 A restart is a new process; stopping is a kill.**
  - The restart tests run the service with `sys.executable -c SERVER_SCRIPT` and stop it with `Popen.kill()`. This binds GREEN to have each upload, rename and deletion durable under `root` by the time the operation answers.
  - Alternative: re-create the app in the same process. Rejected for restart evidence, because the module-level store survives it (`application.py:10`). It is used once, in the expiry test, only for the "removed, not hidden" check, which is backed by the disk scan.
- **V2D-3 Unrecoverability is observed on disk.**
  - `storage_holds` first asserts that the sample bytes are present somewhere under `root`, which is also the isolation check (Repeatable, Isolated Verification). After expiry or deletion it asserts they are absent.
  - This binds GREEN to keep a sample's bytes unencoded in some file under `root`, in any layout, and to remove them rather than mark them deleted.
  - Alternative: observe only through the HTTP operations. Rejected, because a hidden but still stored sample would pass while COA-11 requires that it "cannot be recovered".
- **V2D-4 Test audio is made in the test with the pinned `av` and `numpy`.**
  - WebM/Opus is generated as the Chrome recording. "Holding that recording's audio" (`API-Contract.md:125`) is checked as follows:
    - the duration is within ±0.1 s of 1 s;
    - the dominant frequency is within ±10 Hz of 440 Hz;
    - the RMS is above 0.1.
  - Sample rate, channel count and bit depth are not asserted (contract: "not contracted").
  - The MP3 and OGG uploads are real `libmp3lame` and `libopus`/OGG encodings.
  - Alternative: committed audio fixtures. Rejected, because CON-6 keeps voice samples out of version control and the Plan says the recording is "built inside the test" (`Plan.md:75`).
  - The existing `codec_bytes` helper (`tests/test_enrollment_quality.py:53`) is not reused. Importing that module also imports `webrtcvad` (`:15`), which `requirements-dev.txt` does not declare (code-quality RU1, Medium, justified).
- **V2D-5 What "WebM that cannot be converted" means in the test.** The fixture is the real EBML header of a generated WebM recording, which contains DocType `webm`, followed by 1024 bytes of `\xff\x00`. It is recognizably WebM from its bytes and has no decodable audio. Alternative: a WebM with its clusters removed. Rejected: it might convert to an empty WAV, and the contract does not say whether that counts as "converted".
- **V2D-6 Real transport.** The new fixed error bodies go over a real uvicorn server at least once (testing skill): the conversion-failure `400`, `Voice not found` from Voice Sample after deletion and expiry, and `Voice sample not found`. The port is allocated dynamically.

### Contract Rule Coverage

| Contract rule (`API-Contract.md`) | Test |
| --- | --- |
| Upload: WebM content is stored as PCM WAV holding the recording, whatever the file name and type (`:125`); `fileSize` counts the bytes before conversion (`:132`) | `test_chrome_recording_labelled_wav_is_stored_as_pcm_wav_holding_the_recording` |
| Upload: other content is stored byte-identical (`:126`), WAV | `test_wav_upload_sample_is_stored_byte_identical` |
| Upload: other content is stored byte-identical (`:126`), MP3 and OGG still accepted (COA-6) | `test_mp3_and_ogg_uploads_are_accepted_and_kept_as_received[mp3…]`, `[ogg…]` |
| Upload: `status` `approved`, `approvalScore` 95, can be cloned straight away (`:134`); Voice Sample availability (`:245`); Approved Voice List | `test_new_voice_is_approved_automatically_and_its_sample_is_available_straight_away` |
| Voice Sample: `200` `application/octet-stream`, non-empty (`:244`); `404 Voice not found` for an unknown voice and `404 Voice sample not found` for a preloaded voice, a voice with no `file` part, or an empty one (`:127`, `:247-248`) | `test_sample_answers_not_found_for_unknown_preloaded_and_sampleless_voices` |
| Upload failure 2: `400` with the exact body, no voice created and nothing stored (`:137`) | `test_chrome_recording_that_cannot_be_converted_is_rejected_and_creates_no_voice` (real transport) |
| Durability of voices, samples and renames (`:141`, `:215`); list order after a restart (`:157`); every caller gets every voice, with no per-user filter (`:158`, COA-15); preloaded voice has no sample, over real transport | `test_voices_samples_and_renames_survive_a_restart_and_are_listed_for_every_caller` |
| Retention: expiry at exactly 120 h from `uploadedAt` on the service's clock (`:133`, `:258`); not listed, and `404 Voice not found` from Lookup, Sample, Update and Deletion (`:259`); removed no later than the first request after expiry (`:260`); preloaded voices do not expire (`:261`); an update does not extend retention (`:215`) | `test_voice_expires_120_hours_after_upload_and_is_removed_unrecoverably` |
| Retention: time while the service is stopped counts, and removal happens no later than the first start after expiry (`:260`, `:262`); unrecoverable even with an earlier clock | `test_voice_uploaded_before_a_restart_expires_while_the_service_is_stopped` (real transport) |
| Deletion removes the sample permanently, including across a restart; a second delete answers `404` (`:230-231`) | `test_deleting_a_voice_removes_its_sample_permanently_including_after_a_restart` (real transport) |

Not tested, with the reason:

- Health, CORS (including on Voice Sample), `Invalid content type`, the `Upload failed: <text>` `500`, `name` defaulting and trimming, the fixed `format`/`duration`, ignored form parts and query parameters, Voice Update's `400` and its partial-update semantics, `fileSize` for an empty `file` part, and the preloaded voices returning at every start. These are carried over unchanged (`API-Contract.md:52`). They are not in the OAM-2 scope bullets (`Plan.md:136-144`), and no preserved row assigns them to OAM-2 (`Plan.md:286` assigns preserved rows to OAM-5 and OAM-7 only).
- Persistence of `status`/`approvalScore` updates across a restart. These use the same stored-representation update as the rename, which is tested. A separate `status` change would also remove the voice from Approved Voice List, which would assert carried-over Update semantics outside scope.
- A shared voice list before any restart. It is existing behavior (`application.py:129-149`) and would pass at RED, so it is not RED evidence (`implementation-planning` RED). COA-15 is verified through the restart test, which fails at RED.

## Proposed Code / Tests

### `tests/test_voice_sample_persistence_red.py` (new file, complete content)

```python
"""OAM-2 RED: voice-service sample storage, durability and retention.

Contract: docs/.ai/chatterbox-original-app/API-Contract.md (Voice Upload,
Voice List, Voice Lookup, Voice Update, Voice Deletion, Voice Sample,
Voice Retention). Every test gives the voice service its own storage root
under pytest's tmp_path, so nothing is written to the repository.
"""

from contextlib import contextmanager
from datetime import datetime, timedelta
import io
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import wave

import av
import httpx
import numpy as np
import pytest
from fastapi.testclient import TestClient

from voice_narration.simple_voices.application import create_app

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PRELOADED_VOICE_IDS = [
    "en-US-Neural2-A",
    "en-US-Neural2-C",
    "en-US-Neural2-E",
    "hi-IN-Neural2-A",
    "hi-IN-Neural2-B",
]
UPLOAD_TIME = datetime(2026, 11, 13, 9, 0, 0)
RETENTION = timedelta(hours=120)
RECORDING_RATE = 48000
RECORDING_SECONDS = 1.0
RECORDING_FREQUENCY = 440.0
EBML_MAGIC = b"\x1a\x45\xdf\xa3"
VOICE_NOT_FOUND = {"error": "Voice not found"}
SAMPLE_NOT_FOUND = {"error": "Voice sample not found"}
CONVERSION_FAILED = {"error": "Upload failed: the recording could not be converted to WAV."}

# Runs the voice service in a fresh interpreter, so a restart loses every
# in-memory value and only what the service stored under its root survives.
SERVER_SCRIPT = """
import sys
from datetime import datetime

import uvicorn

from voice_narration.simple_voices.application import create_app

root, port, fixed_time = sys.argv[1], int(sys.argv[2]), sys.argv[3]
clock = None
if fixed_time != "-":
    instant = datetime.fromisoformat(fixed_time)
    clock = lambda: instant
uvicorn.run(create_app(root=root, clock=clock), host="127.0.0.1", port=port, log_level="warning")
"""


def sine_pcm(seconds, frequency, rate=RECORDING_RATE):
    times = np.arange(int(rate * seconds)) / rate
    return np.rint(0.5 * np.sin(2 * np.pi * frequency * times) * 32767).astype(np.int16)


def encoded_audio(container, codec, seconds=RECORDING_SECONDS, frequency=RECORDING_FREQUENCY):
    output = io.BytesIO()
    with av.open(output, "w", format=container) as target:
        stream = target.add_stream(codec, rate=RECORDING_RATE)
        stream.layout = "mono"
        frame = av.AudioFrame.from_ndarray(
            sine_pcm(seconds, frequency).reshape(1, -1), format="s16", layout="mono"
        )
        frame.sample_rate = RECORDING_RATE
        for packet in stream.encode(frame):
            target.mux(packet)
        for packet in stream.encode(None):
            target.mux(packet)
    return output.getvalue()


def chrome_recording():
    """WebM/Opus, the format Chrome's MediaRecorder produces by default."""
    return encoded_audio("webm", "libopus")


def wav_upload():
    """A PCM WAV whose frames contain CRLF and dash runs, which a line-splitting
    multipart parser could alter (Plan OAR-5)."""
    frames = (b"\r\n--\r\n\r\n" + bytes(range(256))) * 40
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(16000)
        target.writeframes(frames)
    return output.getvalue()


def unconvertible_webm():
    """A real WebM EBML header followed by bytes no decoder can read."""
    recording = chrome_recording()
    assert recording[:4] == EBML_MAGIC
    header_size = recording[4]
    assert header_size & 0x80, "EBML header size is expected in one byte"
    header_length = 5 + (header_size & 0x7F)
    assert b"webm" in recording[:header_length]
    return recording[:header_length] + b"\xff\x00" * 512


def multipart_without_file_part(name):
    boundary = "voice-sample-red-boundary"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f"{name}\r\n"
        f"--{boundary}--\r\n"
    ).encode()
    return body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}


def upload(client, name, data, filename, content_type, headers=None):
    return client.post(
        "/voice/upload",
        data={"name": name},
        files={"file": (filename, data, content_type)},
        headers=headers or {},
    )


def uploaded_voice_id(response):
    assert response.status_code == 201, response.text
    return response.json()["id"]


def listed_ids(client, path="/voices", headers=None):
    response = client.get(path, headers=headers or {})
    assert response.status_code == 200, response.text
    return [voice["id"] for voice in response.json()["data"]]


def fetch_sample(client, voice_id):
    response = client.get(f"/voices/{voice_id}/sample")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("application/octet-stream")
    assert response.content
    return response.content


def assert_not_found(response, body):
    assert response.status_code == 404, response.text
    assert response.json() == body


def storage_holds(root, data):
    return any(data in path.read_bytes() for path in root.rglob("*") if path.is_file())


def decoded_pcm_wav(data):
    assert data[:4] == b"RIFF" and data[8:12] == b"WAVE", data[:12]
    with wave.open(io.BytesIO(data), "rb") as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        width = source.getsampwidth()
        frames = source.readframes(source.getnframes())
    if width == 1:
        samples = (np.frombuffer(frames, dtype=np.uint8).astype(np.float64) - 128) / 128
    elif width == 3:
        raw = np.frombuffer(frames, dtype=np.uint8).reshape(-1, 3)
        values = raw[:, 0].astype(np.int32) | (raw[:, 1].astype(np.int32) << 8) | (raw[:, 2].astype(np.int32) << 16)
        samples = np.where(values >= 1 << 23, values - (1 << 24), values) / float(1 << 23)
    else:
        dtype = {2: "<i2", 4: "<i4"}[width]
        samples = np.frombuffer(frames, dtype=dtype).astype(np.float64) / float(1 << (8 * width - 1))
    return rate, samples.reshape(-1, channels).mean(axis=1)


def dominant_frequency(samples, rate):
    spectrum = np.abs(np.fft.rfft(samples * np.hanning(len(samples))))
    return np.fft.rfftfreq(len(samples), 1 / rate)[int(np.argmax(spectrum))]


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def wait_until_healthy(client, process, log_path):
    deadline = time.monotonic() + 60
    while True:
        assert process.poll() is None, (
            "voice service exited during start:\n" + log_path.read_text(errors="replace")
        )
        assert time.monotonic() < deadline, "voice service did not start within 60 s"
        try:
            if client.get("/health").status_code == 200:
                return
        except httpx.TransportError:
            pass
        time.sleep(0.1)


@contextmanager
def running_voice_service(root, log_path, fixed_time=None):
    """Start the voice service as its own process over ``root``; stopping it
    kills the process, as closing the service's console window does."""
    port = free_port()
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(REPOSITORY_ROOT), environment.get("PYTHONPATH", "")]
    )
    with open(log_path, "wb") as log:
        process = subprocess.Popen(
            [sys.executable, "-c", SERVER_SCRIPT, str(root), str(port),
             fixed_time.isoformat() if fixed_time else "-"],
            cwd=log_path.parent,
            env=environment,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=30, trust_env=False) as client:
            wait_until_healthy(client, process, log_path)
            yield client
    finally:
        process.kill()
        process.wait(timeout=30)


@contextmanager
def in_process_voice_service(root, clock=lambda: UPLOAD_TIME):
    with TestClient(create_app(root=root, clock=clock)) as client:
        yield client


@pytest.fixture
def root(tmp_path):
    store = tmp_path / "voice-store"
    store.mkdir()
    return store


def test_chrome_recording_labelled_wav_is_stored_as_pcm_wav_holding_the_recording(root):
    recording = chrome_recording()
    assert recording[:4] == EBML_MAGIC

    with in_process_voice_service(root) as service:
        response = upload(service, "Chrome recording", recording, "recording.wav", "audio/wav")

        voice_id = uploaded_voice_id(response)
        assert response.json()["fileSize"] == len(recording)
        sample = fetch_sample(service, voice_id)
    rate, samples = decoded_pcm_wav(sample)
    assert abs(len(samples) / rate - RECORDING_SECONDS) <= 0.1
    assert abs(dominant_frequency(samples, rate) - RECORDING_FREQUENCY) <= 10
    assert np.sqrt(np.mean(samples ** 2)) > 0.1
    assert storage_holds(root, sample)


def test_wav_upload_sample_is_stored_byte_identical(root):
    wav = wav_upload()

    with in_process_voice_service(root) as service:
        voice_id = uploaded_voice_id(upload(service, "WAV upload", wav, "voice.wav", "audio/wav"))

        assert fetch_sample(service, voice_id) == wav
    assert storage_holds(root, wav)


@pytest.mark.parametrize(
    ("container", "codec", "filename", "content_type", "magic"),
    [
        ("mp3", "libmp3lame", "voice.mp3", "audio/mpeg", b"ID3"),
        ("ogg", "libopus", "voice.ogg", "audio/ogg", b"OggS"),
    ],
)
def test_mp3_and_ogg_uploads_are_accepted_and_kept_as_received(
    root, container, codec, filename, content_type, magic
):
    data = encoded_audio(container, codec)
    assert data.startswith(magic)

    with in_process_voice_service(root) as service:
        response = upload(service, f"{container} upload", data, filename, content_type)

        voice_id = uploaded_voice_id(response)
        assert response.json()["status"] == "approved"
        assert fetch_sample(service, voice_id) == data
    assert storage_holds(root, data)


def test_new_voice_is_approved_automatically_and_its_sample_is_available_straight_away(root):
    wav = wav_upload()

    with in_process_voice_service(root) as service:
        response = upload(service, "Instant voice", wav, "voice.wav", "audio/wav")

        voice_id = uploaded_voice_id(response)
        assert response.json()["status"] == "approved"
        assert response.json()["approvalScore"] == 95
        assert fetch_sample(service, voice_id) == wav
        assert voice_id in listed_ids(service, "/voices/approved")


def test_sample_answers_not_found_for_unknown_preloaded_and_sampleless_voices(root):
    with in_process_voice_service(root) as service:
        with_sample = uploaded_voice_id(upload(service, "Has sample", wav_upload(), "voice.wav", "audio/wav"))
        assert fetch_sample(service, with_sample)
        body, headers = multipart_without_file_part("No file part")
        without_file = uploaded_voice_id(service.post("/voice/upload", content=body, headers=headers))
        empty_file = uploaded_voice_id(upload(service, "Empty file", b"", "empty.wav", "audio/wav"))

        assert_not_found(service.get("/voices/voice-00000000/sample"), VOICE_NOT_FOUND)
        assert_not_found(service.get(f"/voices/{PRELOADED_VOICE_IDS[0]}/sample"), SAMPLE_NOT_FOUND)
        assert_not_found(service.get(f"/voices/{without_file}/sample"), SAMPLE_NOT_FOUND)
        assert_not_found(service.get(f"/voices/{empty_file}/sample"), SAMPLE_NOT_FOUND)


def test_chrome_recording_that_cannot_be_converted_is_rejected_and_creates_no_voice(root, tmp_path):
    broken = unconvertible_webm()

    with running_voice_service(root, tmp_path / "service.log") as service:
        response = upload(service, "Broken recording", broken, "recording.wav", "audio/wav")

        assert response.status_code == 400, response.text
        assert response.json() == CONVERSION_FAILED
        assert listed_ids(service) == PRELOADED_VOICE_IDS
    assert not storage_holds(root, broken)


def test_voices_samples_and_renames_survive_a_restart_and_are_listed_for_every_caller(root, tmp_path):
    wav = wav_upload()
    with running_voice_service(root, tmp_path / "before-restart.log") as service:
        wav_voice = uploaded_voice_id(upload(
            service, "Uploaded voice", wav, "voice.wav", "audio/wav",
            headers={"Authorization": "Bearer user-a"},
        ))
        chrome_voice = uploaded_voice_id(upload(
            service, "Recorded voice", chrome_recording(), "recording.wav", "audio/wav",
            headers={"Authorization": "Bearer user-b"},
        ))
        assert service.patch(f"/voices/{wav_voice}", json={"name": "Renamed voice"}).status_code == 200
        chrome_sample = fetch_sample(service, chrome_voice)

    with running_voice_service(root, tmp_path / "after-restart.log") as service:
        expected = PRELOADED_VOICE_IDS + [wav_voice, chrome_voice]
        for caller in ({}, {"Authorization": "Bearer user-a"}, {"Authorization": "Bearer user-c"}):
            assert listed_ids(service, "/voices", caller) == expected
            assert listed_ids(service, "/voices/approved", caller) == expected
        assert service.get(f"/voices/{wav_voice}").json()["name"] == "Renamed voice"
        assert fetch_sample(service, wav_voice) == wav
        assert fetch_sample(service, chrome_voice) == chrome_sample
        assert_not_found(service.get(f"/voices/{PRELOADED_VOICE_IDS[0]}/sample"), SAMPLE_NOT_FOUND)
    assert storage_holds(root, wav)


def test_voice_expires_120_hours_after_upload_and_is_removed_unrecoverably(root):
    now = [UPLOAD_TIME]
    wav = wav_upload()
    with in_process_voice_service(root, clock=lambda: now[0]) as service:
        response = upload(service, "Expiring voice", wav, "voice.wav", "audio/wav")
        voice_id = uploaded_voice_id(response)
        assert datetime.fromisoformat(response.json()["uploadedAt"]) == UPLOAD_TIME

        now[0] = UPLOAD_TIME + timedelta(hours=1)
        assert service.patch(f"/voices/{voice_id}", json={"name": "Renamed"}).status_code == 200

        now[0] = UPLOAD_TIME + RETENTION - timedelta(seconds=1)
        assert voice_id in listed_ids(service)
        assert fetch_sample(service, voice_id) == wav
        assert storage_holds(root, wav)

        now[0] = UPLOAD_TIME + RETENTION
        assert listed_ids(service) == PRELOADED_VOICE_IDS
        assert not storage_holds(root, wav)
        assert listed_ids(service, "/voices/approved") == PRELOADED_VOICE_IDS
        assert_not_found(service.get(f"/voices/{voice_id}"), VOICE_NOT_FOUND)
        assert_not_found(service.get(f"/voices/{voice_id}/sample"), VOICE_NOT_FOUND)
        assert_not_found(service.patch(f"/voices/{voice_id}", json={"name": "Late"}), VOICE_NOT_FOUND)
        assert_not_found(service.delete(f"/voices/{voice_id}"), VOICE_NOT_FOUND)

    earlier = UPLOAD_TIME + timedelta(hours=1)
    with in_process_voice_service(root, clock=lambda: earlier) as recreated:
        assert listed_ids(recreated) == PRELOADED_VOICE_IDS
        assert_not_found(recreated.get(f"/voices/{voice_id}/sample"), VOICE_NOT_FOUND)


def test_voice_uploaded_before_a_restart_expires_while_the_service_is_stopped(root, tmp_path):
    wav = wav_upload()
    with running_voice_service(root, tmp_path / "upload.log", UPLOAD_TIME) as service:
        voice_id = uploaded_voice_id(upload(service, "Stopped voice", wav, "voice.wav", "audio/wav"))
    assert storage_holds(root, wav)

    with running_voice_service(root, tmp_path / "expired.log", UPLOAD_TIME + RETENTION) as service:
        assert not storage_holds(root, wav)
        assert listed_ids(service) == PRELOADED_VOICE_IDS
        assert_not_found(service.get(f"/voices/{voice_id}/sample"), VOICE_NOT_FOUND)

    earlier = UPLOAD_TIME + timedelta(hours=1)
    with running_voice_service(root, tmp_path / "clock-earlier.log", earlier) as service:
        assert listed_ids(service) == PRELOADED_VOICE_IDS
        assert_not_found(service.get(f"/voices/{voice_id}"), VOICE_NOT_FOUND)


def test_deleting_a_voice_removes_its_sample_permanently_including_after_a_restart(root, tmp_path):
    wav = wav_upload()
    with running_voice_service(root, tmp_path / "delete.log") as service:
        voice_id = uploaded_voice_id(upload(service, "Deleted voice", wav, "voice.wav", "audio/wav"))
        assert fetch_sample(service, voice_id) == wav
        assert storage_holds(root, wav)

        response = service.delete(f"/voices/{voice_id}")
        assert response.status_code == 200
        assert response.json() == {"success": True}
        assert_not_found(service.get(f"/voices/{voice_id}"), VOICE_NOT_FOUND)
        assert_not_found(service.get(f"/voices/{voice_id}/sample"), VOICE_NOT_FOUND)
        assert_not_found(service.delete(f"/voices/{voice_id}"), VOICE_NOT_FOUND)
    assert not storage_holds(root, wav)

    with running_voice_service(root, tmp_path / "after-delete.log") as service:
        assert listed_ids(service) == PRELOADED_VOICE_IDS
        assert_not_found(service.get(f"/voices/{voice_id}/sample"), VOICE_NOT_FOUND)
```

## Execution Steps

1. Confirm that this plan's Human Review status records approval, and that `git status --short` prints nothing outside `docs/.ai/chatterbox-original-app/`.
2. Create `tests/test_voice_sample_persistence_red.py` with exactly the content above.
3. Run the commands under Verification in order, writing each log outside the repository.
4. Record the evidence in `Plan.md` Execution Status for OAM-2, and update this plan's Human Review status.

## Acceptance / Completion Criteria

- **V2C-1** The only repository change is the new file `tests/test_voice_sample_persistence_red.py`, with exactly the content in Proposed Code / Tests. No production, build, configuration or existing test file changes. This excludes the OAM-2 Execution Status update in `Plan.md` and this plan's Human Review status.
- **V2C-2** The first run of the new file reports `11 failed`, with 0 passed and 0 errors. Every failure comes from the absent approved signature `create_app(*, root, clock)`: `TypeError: create_app() got an unexpected keyword argument 'root'`.
  - In seven tests the `TypeError` is raised in the test process.
  - In four tests (conversion failure, restart, stopped-service expiry, deletion) it appears in the started service's log, quoted in the assertion "voice service exited during start".
  - Any other failure cause is not valid RED evidence and stops execution.
- **V2C-3** A second run of the same file, with no cleanup between runs, gives the same result as V2C-2. The tests use per-run `tmp_path` storage (Repeatable, Isolated Verification).
- **V2C-4** `git status --short -- audio_storage` prints nothing after the runs (OAV-3, OAS-1).
- **V2C-5** Collecting the whole backend suite reports no collection error, so the new file does not break collection of existing tests. Existing test files and the production code they exercise are unchanged (V2C-1), so their results cannot change. Under `prompt-driven-development` Test Scope, RED execution runs only the new tests.

## Verification

### Commands

Run from the repository root in Git Bash. `$TEMP` is outside the repository.

1. `python -m pytest tests/test_voice_sample_persistence_red.py -q > "$TEMP/oam2-red-run1.log" 2>&1; tail -1 "$TEMP/oam2-red-run1.log"; grep -c "unexpected keyword argument 'root'" "$TEMP/oam2-red-run1.log"` (OAV-1)
2. `python -m pytest tests/test_voice_sample_persistence_red.py -q > "$TEMP/oam2-red-run2.log" 2>&1; tail -1 "$TEMP/oam2-red-run2.log"; grep -c "unexpected keyword argument 'root'" "$TEMP/oam2-red-run2.log"` (second run, no cleanup)
3. `python -m pytest --collect-only -q > "$TEMP/oam2-collect.log" 2>&1; tail -1 "$TEMP/oam2-collect.log"`
4. `git status --short -- audio_storage` (OAV-3; it must print nothing. If it prints anything, stop and report; do not restore and continue)
5. `git status --short` (it must list only `?? tests/test_voice_sample_persistence_red.py` and work-item changes under `docs/.ai/chatterbox-original-app/`)

### Affected Tests

None. No existing test imports `voice_narration.simple_voices` (`grep -rn simple_voices tests`), no shared test file is changed, and the Plan's preserved tests (`Plan.md:184`) belong to OAM-4.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Command 1: `11 failed`, and the grep count is `11`. These are failing tests, not errors.
- Command 2: the same as command 1.
- Command 3: `173 tests collected` with no error. This is the dry-run count at HEAD `8d9c5c8`: 162 existing plus 11 new.
- Command 4: no output.
- Command 5: only the new test file, plus `docs/.ai/chatterbox-original-app/` changes.
- Preserved-behavior tests (expected to pass at RED): none.

### Planning-Time Dry Run

This is a planning-time dry run, not milestone evidence. It ran on 2026-11-13 in a disposable copy outside the repository: `C:/Users/avina/AppData/Local/Temp/claude/75d22e5e94aa85f8/7c785373-79e0-4451-8aab-0a1437282b97/scratchpad/copy`, created with `git archive HEAD | tar -x`. The exact test file above was placed in its `tests/`. The repository was not modified, and `git status --short` printed nothing afterwards.

| Step | Command (in the copy) | Result |
| --- | --- | --- |
| Compile | `python -m compileall -q tests/test_voice_sample_persistence_red.py` | compiled, no error |
| Collect | `python -m pytest --collect-only -q -p no:cacheprovider` | `173 tests collected` |
| Unmodified production | `python -m pytest tests/test_voice_sample_persistence_red.py -q -p no:cacheprovider` | `11 failed`; `unexpected keyword argument 'root'` found 11 times |
| Scratch stub: `create_app(*, root=None, clock=None)` accepting and ignoring both, with no other change | same | `11 failed`. Eight fail at `fetch_sample`'s `200` assertion with `405` (no sample operation). The conversion test fails with `201 == 400` (no conversion rejection). The expiry test fails because `uploadedAt` is not the injected clock. The stopped-service test fails because nothing is stored under `root` |
| Scratch probe: minimal JSON index plus sample files under `root`, purge at start and per request, WebM converted with `av`, sample route | same | `11 passed` |

The stub and the probe were applied only inside the copy. Both lived in the scratch folder, and the copy's original `application.py` was restored after each run. Neither enters the repository. Created during the dry run, all under the scratch folder: `copy/`, `probe/` (`enc.py`, `stub_application.py`, `probe_application.py`, the test file draft), `orig_application.py`, and the run logs. Pytest temporary directories went under the system pytest temp root. The scratch folder is deleted after this plan is written.

The planning runs used `-p no:cacheprovider` to avoid writing `.pytest_cache` in the copy. The execution commands omit it, as OAV-1 does, and `.pytest_cache/` is gitignored (`.gitignore:2`).

## Risks

- **V2R-1 Port race.** `free_port` releases the port before the service binds it, so another process could take it in between. The service would then exit during start, and the failure would quote its log. That would be an environment failure, not RED evidence. Execution stops and reports it; there is no rerun until it passes.
- **V2R-2 The execution-time RED shows one failure class.** On the unmodified repository, all 11 tests fail at the absent `create_app(*, root, clock)` signature, before reaching their behavior assertions. That they then fail for the missing behavior, and pass with it, was shown only by the planning stub and probe above. It becomes executable evidence at OAM-3.
- **V2R-3 Carried-over voice-service behavior is untested.** No test exercises the running voice service (`Plan.md:30`), and this milestone adds tests only for the OAM-2 scope. OAM-3 could change carried-over behavior (for example the hand-parsed `name`, the `500` prefix, or CORS) without a failing test. No in-scope mitigation exists. Adding characterization tests would be new scope, for the user to decide.
- **V2R-4 Encoder availability.** The tests need the `libopus` and `libmp3lame` encoders of the installed `av` wheel (present in the dry run). If they are missing, the tests fail in audio building. That is not valid RED, and execution stops.
- **V2R-5 Identity comparisons (security).** None. Neither voice-service operation authenticates or compares an identity, role or owner (`API-Contract.md:58`). The restart test sends different `Authorization` headers only to show they do not filter the shared list (COA-15).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Delete `tests/test_voice_sample_persistence_red.py`. Nothing else is changed.

## Explicitly Out of Scope

- Any production change, including the `root`/`clock` parameters, the sample route, persistence, conversion and retention. These belong to OAM-3 (`Plan.md:147`, `:150-166`).
- Build, dependency or configuration changes. The tests use only packages already pinned in `requirements-dev.txt`.
- Inference-service and TTS-page tests (`Plan.md:147`), and any network use beyond `127.0.0.1`.
- Changes to existing tests, and repair of the pre-existing failures named in `Plan.md:35-39`.
- Writing to tracked `audio_storage/` files. All storage is under pytest's `tmp_path`.
- Committed audio fixtures or samples (CON-6).

## Human Review

Status: Approved by Avinash Srivastava on 2026-11-13, as written, including decisions V2D-1 to V2D-6.
