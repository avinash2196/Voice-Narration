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
