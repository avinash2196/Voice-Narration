# Implementation Plan — Gateway Telemetry Fidelity RED

## Milestone

Gateway Telemetry Fidelity RED

## Milestone Type

RED

## Authoritative References

| Artifact | Authority |
| --- | --- |
| `docs/.ai/ai-gateway-multimodel/requirements.md` | Approved; AGW-009 requires usage/decision metadata sufficient for governance and troubleshooting. |
| `docs/.ai/ai-gateway-multimodel/Plan.md` | Revised approved plan includes milestones 6/7 for telemetry fidelity follow-up. |
| `docs/.ai/ai-gateway-multimodel/Final-Review.md` | Finding FR-AGW-001 identifies placeholder telemetry values requiring remediation. |

## Preconditions / Predecessor Evidence

- Milestones 1–5 are complete in `Plan.md`.
- Current gateway execution response uses placeholder telemetry (`latency_ms=0`, null compute/cost fields).

## Current Repository State

- `tests/test_ai_gateway_red.py` verifies contract and routing behavior, but not telemetry fidelity.
- Gateway execution success path currently returns static telemetry values.

## Files in Scope

### Files to Create
- `tests/test_ai_gateway_telemetry_red.py`

### Files to Modify
- none

### Files to Delete
- none

## Proposed Changes

Add RED tests that require:
1. successful gateway execution telemetry has measured non-placeholder latency/compute values;
2. cost estimate is present and decimal-formatted;
3. runtime class remains deterministic and self-hosted for approved chatterbox route.

## Proposed Code / Tests

### Create `tests/test_ai_gateway_telemetry_red.py`

```python
from fastapi.testclient import TestClient

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


def test_gateway_execution_returns_non_placeholder_telemetry():
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
```

## Verification

### Commands
- `pytest -q tests\test_clone_flow.py`
- `pytest -q tests\test_ai_gateway_red.py`
- `pytest -q tests\test_ai_gateway_telemetry_red.py`

### Expected Evidence
- Preserved checks pass.
- Telemetry RED test fails only on placeholder telemetry behavior.

## Human Review

Status: Executed — see Plan.md
