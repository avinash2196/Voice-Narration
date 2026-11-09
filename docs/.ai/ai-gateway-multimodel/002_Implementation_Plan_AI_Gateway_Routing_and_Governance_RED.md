# Implementation Plan — AI Gateway Routing & Governance RED

## Milestone

AI Gateway Routing & Governance RED

## Milestone Type

RED

## Authoritative References

| Artifact | Authority |
| --- | --- |
| `docs/.ai/ai-gateway-multimodel/requirements.md` | Approved by avinash2196 on 2026-11-08; AGW-001..AGW-010 define required gateway behavior to verify. |
| `docs/.ai/ai-gateway-multimodel/Plan.md` | Approved by avinash2196 on 2026-11-08; milestone 3 is RED and tests/checks only. |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Approved by avinash2196 on 2026-11-08; defines gateway endpoints, schemas, and deterministic failure codes. |
| `docs/.ai/ai-gateway-multimodel/001_Implementation_Plan_Chatterbox_Commercial_and_Feasibility_Evidence.md` | Executed; predecessor milestone evidence completed and recorded in Plan.md. |

## Carried-Forward Decisions

- Gateway boundary is mandatory (`POST /ai-gateway/v1/executions`) and replaces direct model execution entry over time; this RED verifies that required surface exists before implementation.  
- Chatterbox remains initial model target, with commercial/runtime feasibility evidence already captured in milestone 2 artifacts.

## Preconditions / Predecessor Evidence

- `Plan.md` execution status records:
  - **AI Gateway Contract: Complete**
  - **Chatterbox Commercial & Feasibility Evidence: Complete**
- Existing preserved regression command passes: `pytest -q tests\test_clone_flow.py` (2 passed).
- Current code still performs direct provider invocation in inference service (`GoogleVoiceProvider`), so RED failure is expected for gateway routes/behavior not yet implemented.

## Current Repository State

- Inference API currently exposes `/inference/jobs*` endpoints and no `/ai-gateway/v1/*` routes.
- Existing tests validate enrollment and generation through legacy flow only (`tests/test_clone_flow.py`).
- Pytest discovery and markers are configured via `pytest.ini`.

## Files in Scope

### Files to Create

- `tests/test_ai_gateway_red.py`

### Files to Modify

- none

### Files to Delete

- none

## Proposed Changes

1. Add a RED-only contract test file asserting required AI Gateway contract behavior:
   - gateway execution endpoint presence and idempotency contract;
   - deterministic failure-code envelope for unsupported language / ineligible model / routing-no-match scenarios;
   - model governance endpoints for listing, approval, and enablement checks;
   - bilingual (`hi`, `en`) support visibility in model metadata.
2. Keep all changes in tests only; no production source/configuration/dependency changes.
3. Preserve existing behavior by re-running clone-flow tests.

## Proposed Code / Tests

### Create `tests/test_ai_gateway_red.py`

```python
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
```

## Execution Steps

1. Confirm predecessor milestones remain complete in `Plan.md`.
2. Add `tests/test_ai_gateway_red.py` exactly as specified.
3. Run preserved checks to confirm pre-existing behavior still passes.
4. Run RED checks and capture expected failures caused only by missing gateway implementation.
5. Record RED evidence in `Plan.md` execution section after verifying failure cause is in-scope.
6. Stop; GREEN requires a separate approved Implementation Plan.

## Acceptance / Completion Criteria

- Only test files are added/changed; no production source, runtime config, or dependency manifest changes.
- `pytest -q tests\test_clone_flow.py` passes.
- `pytest -q tests\test_ai_gateway_red.py` fails for missing approved gateway behavior (route/contract behavior not implemented), not for unrelated environment/setup failures.
- RED evidence captured in `Plan.md` execution status/evidence notes.

## Verification

### Commands

- `pytest -q tests\test_clone_flow.py`
- `pytest -q tests\test_ai_gateway_red.py`
- `git --no-pager status --short`

### Expected Evidence

- Preserved-behavior tests (expected to pass at RED):
  - `tests/test_clone_flow.py` — preserved baseline flow from existing implementation.
- RED behavior checks (expected to fail at RED):
  - `tests/test_ai_gateway_red.py` assertions against `/ai-gateway/v1/*` contract behavior.

### Planning-Time Dry Run

Not performed. This artifact defines proposed RED tests for human review; execution-time RED evidence will be captured after approval.

## Risks

- If failure output is only HTTP 404 without structured error body, tests may need narrowing in a revised RED plan to align with minimal contract-introduction sequencing.
- Existing global app state/database files may introduce incidental noise in test output; mitigation is explicit command isolation and preserved baseline run first.

## Pre-authorized Contingencies

None. Any test-scope expansion, assertion relaxation, or additional file changes requires revised plan approval.

## Rollback / Recovery

If RED execution must be undone before GREEN planning, remove only `tests/test_ai_gateway_red.py` and revert only RED evidence lines in `Plan.md`; preserve unrelated changes.

## Explicitly Out of Scope

- Implementing gateway endpoints, adapter logic, routing policy engine, or governance state machine.
- Modifying inference service production code.
- Adding Chatterbox runtime dependencies or deployment configuration.

## Human Review

Status: Executed — see Plan.md
