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


def test_generation_delete_removes_record_and_file():
    client.post(
        "/inference/jobs/delete-check/infer",
        json={"script": "delete me", "voice_id": "en-US-Neural2-A"},
    )

    delete_response = client.delete("/inference/generations/delete-check")
    assert delete_response.status_code == 200, delete_response.text

    history = client.get("/inference/generations?skip=0&limit=100")
    assert history.status_code == 200, history.text
    payload = history.json()
    assert all(item["job_id"] != "delete-check" for item in payload["items"])


def test_generation_filters_by_voice_and_search():
    client.post(
        "/inference/jobs/filter-one/infer",
        json={"script": "Hindi narration sample", "voice_id": "hi-IN-Neural2-A"},
    )
    client.post(
        "/inference/jobs/filter-two/infer",
        json={"script": "English narration sample", "voice_id": "en-US-Neural2-A"},
    )

    by_voice = client.get("/inference/generations?voice_id=hi-IN-Neural2-A")
    assert by_voice.status_code == 200, by_voice.text
    voice_items = by_voice.json()["items"]
    assert all(item["voice_id"] == "hi-IN-Neural2-A" for item in voice_items)

    by_search = client.get("/inference/generations?search=Hindi")
    assert by_search.status_code == 200, by_search.text
    assert any(item["text"] == "Hindi narration sample" for item in by_search.json()["items"])
