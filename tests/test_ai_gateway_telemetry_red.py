from fastapi.testclient import TestClient

import voice_narration.inference.application as inference_module
from tests._chatterbox_boundary import isolate_network, running_fake_backend, write_service_account_key
from voice_narration.inference.application import app as inference_app
from voice_narration.simple_voices.application import app as voices_app


def _enable_model(client: TestClient) -> None:
    approval_payload = {
        "model_version": "v3",
        "license_evidence_uri": "https://example.test/license",
        "weights_evidence_uri": "https://example.test/weights",
        "output_use_evidence_uri": "https://example.test/output-use",
        "runtime_class": "self_hosted",
        "languages_supported": ["hi", "en"],
        "approved_by": "pytest",
    }
    approve = client.post("/ai-gateway/v1/models/chatterbox-multilingual-v3/approvals", json=approval_payload)
    assert approve.status_code == 201, approve.text

    enable = client.post("/ai-gateway/v1/models/chatterbox-multilingual-v3/enable", json={"model_version": "v3"})
    assert enable.status_code == 200, enable.text


def _create_profile() -> dict:
    voice_client = TestClient(voices_app)
    response = voice_client.post(
        "/voices",
        data={
            "name": "Telemetry Test",
            "user_id": "telemetry-user",
            "language": "hi-IN",
            "consent": "I consent",
        },
        files={"audio_file": ("sample.wav", b"RIFF....fake-wave", "audio/wav")},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_gateway_execution_returns_non_placeholder_telemetry(monkeypatch, tmp_path):
    guard = isolate_network(monkeypatch)
    with running_fake_backend() as chatterbox:
        key = write_service_account_key(tmp_path / "service-account.json", chatterbox.token_uri)
        monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(key.path))
        monkeypatch.setattr(inference_module, "VOICE_CLONING_API_BASE_URL", chatterbox.base_url)

        infer_client = TestClient(inference_app)
        _enable_model(infer_client)
        profile = _create_profile()

        response = infer_client.post(
            "/ai-gateway/v1/executions",
            json={
                "request_id": "44444444-4444-4444-4444-444444444444",
                "mode": "voice_cloning",
                "text": "Namaste telemetry check",
                "language": "hi",
                "voice_profile_id": profile["id"],
                "model_hint": "chatterbox-multilingual-v3",
                "controls": {"pause_strength": 0.5, "speech_pace": 1.0},
                "idempotency_key": "telemetry-red-1",
                "metadata": {"caller": "telemetry-red"},
                "user_id": profile["user_id"],
                "voice_name": profile["name"],
            },
        )

    assert response.status_code == 202, response.text
    body = response.json()
    usage = body["usage"]

    assert usage["latency_ms"] > 0
    assert usage["compute_ms"] > 0
    assert isinstance(usage["cost_estimate_usd"], str)
    assert usage["cost_estimate_usd"].count(".") == 1
    assert usage["runtime_class"] == "self_hosted"
    assert len(chatterbox.synthesize_calls) == 1
    guard.assert_no_network()
