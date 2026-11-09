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
