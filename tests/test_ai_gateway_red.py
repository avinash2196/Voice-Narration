from fastapi.testclient import TestClient

from voice_narration.inference.application import app as inference_app


client = TestClient(inference_app)


def _base_execution_request() -> dict:
    return {
        "request_id": "11111111-1111-1111-1111-111111111111",
        "mode": "voice_cloning",
        "text": "Namaste from AI Gateway",
        "language": "hi",
        "voice_profile_id": "22222222-2222-2222-2222-222222222222",
        "model_hint": "chatterbox-multilingual-v3",
        "controls": {"pause_strength": 0.5, "speech_pace": 1.0},
        "idempotency_key": "red-test-key-1",
        "metadata": {"caller": "pytest-red"},
    }


def test_gateway_execution_requires_idempotency_key():
    payload = _base_execution_request()
    payload.pop("idempotency_key")

    response = client.post("/ai-gateway/v1/executions", json=payload)

    assert response.status_code == 400, response.text
    body = response.json()
    assert body["errors"][0]["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_gateway_rejects_unsupported_language_with_deterministic_error():
    payload = _base_execution_request()
    payload["language"] = "xx"
    payload["idempotency_key"] = "red-test-key-2"

    response = client.post("/ai-gateway/v1/executions", json=payload)

    assert response.status_code == 400, response.text
    body = response.json()
    assert body["errors"][0]["code"] == "UNSUPPORTED_LANGUAGE"
    assert body["errors"][0]["retryable"] is False


def test_gateway_rejects_ineligible_model_enablement():
    response = client.post(
        "/ai-gateway/v1/models/chatterbox-multilingual-v3/enable",
        json={"model_version": "v3"},
    )

    assert response.status_code == 403, response.text
    body = response.json()
    assert body["errors"][0]["code"] == "MODEL_NOT_ELIGIBLE"


def test_gateway_model_catalog_exposes_bilingual_support():
    response = client.get("/ai-gateway/v1/models")

    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body["items"], list)
    chatterbox = next(item for item in body["items"] if item["model_id"] == "chatterbox-multilingual-v3")
    assert "hi" in chatterbox["languages_supported"]
    assert "en" in chatterbox["languages_supported"]


def test_gateway_returns_routing_no_match_when_model_hint_is_unknown():
    payload = _base_execution_request()
    payload["model_hint"] = "unknown-model-id"
    payload["idempotency_key"] = "red-test-key-3"

    response = client.post("/ai-gateway/v1/executions", json=payload)

    assert response.status_code == 422, response.text
    body = response.json()
    assert body["errors"][0]["code"] == "ROUTING_NO_MATCH"
    assert body["errors"][0]["fallback_attempted"] in (True, False)
