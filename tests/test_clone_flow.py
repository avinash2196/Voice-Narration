from fastapi.testclient import TestClient

import voice_narration.inference.application as inference_module
from voice_narration.inference.application import app as inference_app
from voice_narration.simple_voices.application import app as voices_app


def test_voice_enrollment_creates_profile():
    client = TestClient(voices_app)
    payload = {
        "name": "Test Clone",
        "user_id": "test-user",
        "language": "en-US",
        "consent": "I consent",
    }
    audio = ("sample.wav", b"RIFF....fake-wave", "audio/wav")
    response = client.post("/voices", data=payload, files={"audio_file": audio})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Test Clone"
    assert body["status"] == "approved"


def test_generation_uses_selected_voice_profile():
    voice_client = TestClient(voices_app)
    voice_response = voice_client.post(
        "/voices",
        data={
            "name": "Generation Test",
            "user_id": "generation-user",
            "language": "en-US",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    voice_id = voice_response.json()["id"]

    infer_client = TestClient(inference_app)
    response = infer_client.post(
        "/inference/jobs",
        json={
            "text": "Hello from the test suite",
            "voice_profile_id": voice_id,
            "voice_name": "Generation Test",
            "user_id": "generation-user",
        },
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "completed"
    assert "audio_url" in body


def test_voice_cloning_returns_guidance_when_clone_backend_unavailable(monkeypatch):
    voice_client = TestClient(voices_app)
    voice_response = voice_client.post(
        "/voices",
        data={
            "name": "Clone Backend Check",
            "user_id": "clone-backend-user",
            "language": "en-US",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    voice_id = voice_response.json()["id"]

    monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", "")

    infer_client = TestClient(inference_app)
    response = infer_client.post(
        "/inference/jobs",
        json={
            "text": "Please clone this voice",
            "voice_profile_id": voice_id,
            "voice_name": "Clone Backend Check",
            "user_id": "clone-backend-user",
            "mode": "voice_cloning",
        },
    )

    assert response.status_code == 503, response.text
    detail = response.json()["detail"]
    assert "Please retry" in detail
    assert "Google voice narration mode" in detail
