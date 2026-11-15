import base64

from fastapi.testclient import TestClient

from voice_narration.inference.application import create_app
from voice_narration.inference.providers.mock import MockInferenceProvider


class DummyProvider(MockInferenceProvider):
    async def generate(self, script: str, voice_id: str, **kwargs):
        return {
            "audio_bytes": b"RIFF....WAVE",
            "format": "wav",
            "output_seconds": 2.5,
        }


client = TestClient(create_app(provider=DummyProvider()))


def test_generation_download_returns_wav_bytes():
    response = client.post(
        "/inference/jobs/job-123/infer",
        json={"script": "hello world", "voice_id": "en-US-Neural2-A"},
    )
    assert response.status_code == 200, response.text

    download = client.get("/inference/jobs/job-123/download")
    assert download.status_code == 200, download.text
    assert download.headers["content-type"].startswith("audio/wav")
    assert len(download.content) > 0


def test_generation_list_returns_persisted_history():
    client.post(
        "/inference/jobs/job-456/infer",
        json={"script": "second generation", "voice_id": "hi-IN-Neural2-A"},
    )

    response = client.get("/inference/generations?skip=0&limit=20")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["total"] >= 2
    assert any(item["job_id"] == "job-123" for item in payload["items"])


def test_generation_detail_returns_metadata():
    response = client.get("/inference/generations/job-456")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["text"] == "second generation"
    assert payload["voice_id"] == "hi-IN-Neural2-A"
