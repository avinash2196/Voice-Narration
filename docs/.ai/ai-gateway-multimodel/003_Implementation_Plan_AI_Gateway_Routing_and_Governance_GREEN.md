# Implementation Plan — AI Gateway Routing & Governance GREEN

## Milestone

AI Gateway Routing & Governance GREEN

## Milestone Type

GREEN

## Authoritative References

| Artifact | Authority |
| --- | --- |
| `docs/.ai/ai-gateway-multimodel/requirements.md` | Approved by avinash2196 on 2026-11-08; AGW-001..AGW-010 ownership is delivered by this GREEN milestone. |
| `docs/.ai/ai-gateway-multimodel/Plan.md` | Approved revised Plan on 2026-11-08; milestone 5 is GREEN, predecessor is milestone 4 (Chatterbox Cloud Run Model API Deployment). |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Approved by avinash2196 on 2026-11-08; defines `/ai-gateway/v1/*` contract behavior and deterministic failure taxonomy. |
| `docs/.ai/ai-gateway-multimodel/002_Implementation_Plan_AI_Gateway_Routing_and_Governance_RED.md` | Executed with RED evidence recorded in Plan.md; failing tests establish missing gateway behavior baseline. |

## Carried-Forward Decisions

- Gateway API is the model-execution boundary and must expose deterministic contract behavior before consumer migration.
- Chatterbox is first model target; enablement is governance-gated and self-hosted runtime constrained.
- RED evidence confirms missing `/ai-gateway/v1/*` routes and behavior; GREEN implements only what RED established.

## Preconditions / Predecessor Evidence

- `Plan.md` execution status records:
  - **AI Gateway Contract: Complete**
  - **Chatterbox Commercial & Feasibility Evidence: Complete**
  - **AI Gateway Routing & Governance RED: Complete** with expected failing checks:
    - `pytest -q tests\test_ai_gateway_red.py` → `5 failed` due to `404 Not Found` on `/ai-gateway/v1/*`.
- Preserved baseline checks pass:
  - `pytest -q tests\test_clone_flow.py` → pass.

## Current Repository State

- Inference service currently executes model generation directly via `GoogleVoiceProvider` in `/inference/jobs`.
- New RED test file `tests/test_ai_gateway_red.py` asserts required gateway endpoints and deterministic failure behavior.
- No gateway endpoints are currently implemented in production code.

## Files in Scope

### Files to Create

- none

### Files to Modify

- `voice_narration/inference/application.py`
- `docs/.ai/ai-gateway-multimodel/Plan.md` (Execution Status and evidence section only, after successful execution)

### Files to Delete

- none

## Proposed Changes

1. Implement AI Gateway model catalog/governance state in `inference/application.py`:
   - in-memory model registry with `chatterbox-multilingual-v3` entry;
   - governance approval and enablement transitions;
   - bilingual language support metadata (`hi`, `en`).
2. Add gateway contract endpoints:
   - `POST /ai-gateway/v1/executions`
   - `GET /ai-gateway/v1/models`
   - `POST /ai-gateway/v1/models/{model_id}/approvals`
   - `POST /ai-gateway/v1/models/{model_id}/enable`
3. Add deterministic error envelope helper for contract codes required by RED tests.
4. Add idempotency bookkeeping for gateway execution requests.
5. Preserve existing `/inference/jobs*` behavior unchanged.

## Proposed Code / Tests

### Modify `voice_narration/inference/application.py` (complete final content)

```python
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from voice_narration.inference.providers import GoogleVoiceProvider

ROOT = Path(__file__).resolve().parents[2]
AUDIO_ROOT = ROOT / "audio_storage"
AUDIO_ROOT.mkdir(exist_ok=True)
DB_PATH = AUDIO_ROOT / "generation_jobs.db"
BASE_URL = os.getenv("INFERENCE_BASE_URL", "http://localhost:8003")

GATEWAY_DEFAULT_MODEL_ID = "chatterbox-multilingual-v3"
GATEWAY_ALLOWED_LANGUAGES = {"hi", "en"}
GATEWAY_ALLOWED_MODES = {"narration", "voice_cloning"}

_gateway_models: dict[str, dict] = {
    GATEWAY_DEFAULT_MODEL_ID: {
        "model_id": GATEWAY_DEFAULT_MODEL_ID,
        "model_version": "v3",
        "license_evidence_uri": None,
        "weights_evidence_uri": None,
        "output_use_evidence_uri": None,
        "runtime_class": "self_hosted",
        "languages_supported": ["hi", "en"],
        "approved_by": None,
        "approved_at": None,
        "state": "draft",
    }
}
_gateway_idempotency: dict[str, dict] = {}


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                voice_profile_id TEXT NOT NULL,
                voice_name TEXT NOT NULL,
                text TEXT NOT NULL,
                status TEXT NOT NULL,
                audio_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


_ensure_db()

app = FastAPI(title="Inference Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _gateway_error(
    status_code: int,
    code: str,
    message: str,
    retryable: bool = False,
    fallback_attempted: bool = False,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "errors": [
                {
                    "code": code,
                    "message": message,
                    "retryable": retryable,
                    "fallback_attempted": fallback_attempted,
                }
            ]
        },
    )


def _profile_lookup(voice_profile_id: str) -> dict:
    voice_db = ROOT / "audio_storage" / "voice_profiles.db"
    if not voice_db.exists():
        raise HTTPException(status_code=404, detail="Voice registry not initialized")
    with sqlite3.connect(voice_db) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM voice_profiles WHERE id = ?",
            (voice_profile_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Voice profile not found")
    return dict(row)


def _execution_fingerprint(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "inference"}


@app.get("/inference/jobs")
def list_jobs() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]


@app.post("/inference/jobs")
def create_job(payload: dict) -> dict:
    text = (payload.get("text") or "").strip()
    voice_profile_id = payload.get("voice_profile_id")
    voice_name = payload.get("voice_name") or "Custom Clone"
    user_id = payload.get("user_id") or "guest"
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    if not voice_profile_id:
        raise HTTPException(status_code=400, detail="voice_profile_id is required")

    profile = _profile_lookup(voice_profile_id)
    if profile.get("status") not in ("approved", "active"):
        raise HTTPException(status_code=403, detail="Voice profile is not available for generation")

    job_id = uuid.uuid4().hex
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_dir = AUDIO_ROOT / "generated"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{job_id}.wav"
    provider = GoogleVoiceProvider()
    provider.generate(text, profile, out_path)

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO jobs (
                id, user_id, voice_profile_id, voice_name, text, status, audio_path,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'completed', ?, ?, ?)
            """,
            (
                job_id,
                user_id,
                voice_profile_id,
                voice_name,
                text,
                str(out_path),
                timestamp,
                timestamp,
            ),
        )
        conn.commit()

    return {
        "id": job_id,
        "status": "completed",
        "audio_url": f"{BASE_URL}/inference/jobs/{job_id}/audio",
        "download_url": f"{BASE_URL}/inference/jobs/{job_id}/audio",
        "voice_profile_id": voice_profile_id,
        "voice_name": voice_name,
    }


@app.get("/inference/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)


@app.get("/inference/jobs/{job_id}/audio")
def job_audio(job_id: str):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    audio_path = Path(row["audio_path"])
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/wav", filename=f"{job_id}.wav")


@app.get("/ai-gateway/v1/models")
def list_gateway_models() -> dict:
    return {"items": [dict(model) for model in _gateway_models.values()]}


@app.post("/ai-gateway/v1/models/{model_id}/approvals")
def approve_gateway_model(model_id: str, payload: dict):
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "Unknown model for approval")

    required_fields = [
        "model_version",
        "license_evidence_uri",
        "weights_evidence_uri",
        "output_use_evidence_uri",
        "runtime_class",
        "languages_supported",
    ]
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return _gateway_error(400, "INVALID_EVIDENCE", f"Missing evidence fields: {', '.join(missing)}")

    if payload.get("runtime_class") not in {"self_hosted", "external_api"}:
        return _gateway_error(400, "INVALID_EVIDENCE", "runtime_class must be self_hosted or external_api")

    langs = payload.get("languages_supported")
    if not isinstance(langs, list) or not langs:
        return _gateway_error(400, "INVALID_EVIDENCE", "languages_supported must be a non-empty list")

    model["model_version"] = payload["model_version"]
    model["license_evidence_uri"] = payload["license_evidence_uri"]
    model["weights_evidence_uri"] = payload["weights_evidence_uri"]
    model["output_use_evidence_uri"] = payload["output_use_evidence_uri"]
    model["runtime_class"] = payload["runtime_class"]
    model["languages_supported"] = langs
    model["approved_by"] = payload.get("approved_by")
    model["approved_at"] = payload.get("approved_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    model["state"] = "approved"

    return JSONResponse(status_code=201, content=dict(model))


@app.post("/ai-gateway/v1/models/{model_id}/enable")
def enable_gateway_model(model_id: str, payload: dict):
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "Unknown model")

    model_version = payload.get("model_version")
    if not model_version or model_version != model.get("model_version"):
        return _gateway_error(409, "MODEL_STATE_CONFLICT", "Model version does not match approved version")

    if model.get("state") != "approved":
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Model is not approved for enablement")

    required_evidence = ["license_evidence_uri", "weights_evidence_uri", "output_use_evidence_uri"]
    if any(not model.get(field) for field in required_evidence):
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Commercial evidence is incomplete")

    if model.get("runtime_class") != "self_hosted":
        return _gateway_error(403, "RUNTIME_POLICY_VIOLATION", "Runtime must be self_hosted for core generation")

    model["state"] = "enabled"
    return dict(model)


@app.post("/ai-gateway/v1/executions")
def create_gateway_execution(payload: dict):
    idempotency_key = (payload.get("idempotency_key") or "").strip()
    if not idempotency_key:
        return _gateway_error(400, "IDEMPOTENCY_KEY_REQUIRED", "idempotency_key is required")

    mode = payload.get("mode")
    if mode not in GATEWAY_ALLOWED_MODES:
        return _gateway_error(400, "INVALID_INPUT", "mode must be narration or voice_cloning")

    text = (payload.get("text") or "").strip()
    if not text:
        return _gateway_error(400, "INVALID_INPUT", "text is required")

    language = payload.get("language")
    if language not in GATEWAY_ALLOWED_LANGUAGES:
        return _gateway_error(400, "UNSUPPORTED_LANGUAGE", "language must be hi or en")

    model_id = payload.get("model_hint") or GATEWAY_DEFAULT_MODEL_ID
    model = _gateway_models.get(model_id)
    if model is None:
        return _gateway_error(422, "ROUTING_NO_MATCH", "No routing candidate for requested model")

    if model.get("state") != "enabled":
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Selected model is not enabled")

    if model.get("runtime_class") != "self_hosted":
        return _gateway_error(403, "RUNTIME_POLICY_VIOLATION", "Selected model runtime is not self-hosted")

    if language not in model.get("languages_supported", []):
        return _gateway_error(400, "UNSUPPORTED_LANGUAGE", "Selected model does not support requested language")

    fingerprint = _execution_fingerprint(payload)
    existing = _gateway_idempotency.get(idempotency_key)
    if existing:
        if existing["fingerprint"] != fingerprint:
            return _gateway_error(409, "IDEMPOTENCY_CONFLICT", "idempotency key used with different request")
        return existing["response"]

    voice_profile_id = payload.get("voice_profile_id")
    if not voice_profile_id:
        return _gateway_error(400, "INVALID_INPUT", "voice_profile_id is required")

    voice_name = payload.get("voice_name") or "Custom Clone"
    user_id = payload.get("user_id") or "guest"

    try:
        job = create_job(
            {
                "text": text,
                "voice_profile_id": voice_profile_id,
                "voice_name": voice_name,
                "user_id": user_id,
            }
        )
    except HTTPException:
        return _gateway_error(503, "MODEL_UNAVAILABLE", "Model execution path unavailable", retryable=True)

    response = {
        "execution_id": job["id"],
        "status": "completed",
        "audio_url": job["audio_url"],
        "routing": {
            "selected_model_id": model["model_id"],
            "selected_model_version": model["model_version"],
            "policy_name": "default-chatterbox-route",
            "policy_revision": "v1",
            "decision_reason": "model_hint_or_default",
            "fallback_applied": False,
            "fallback_from_model_id": None,
        },
        "usage": {
            "latency_ms": 0,
            "queue_ms": None,
            "compute_ms": None,
            "cost_estimate_usd": None,
            "runtime_class": model["runtime_class"],
        },
        "errors": [],
    }
    _gateway_idempotency[idempotency_key] = {"fingerprint": fingerprint, "response": response}
    return JSONResponse(status_code=202, content=response)
```

## Execution Steps

1. Confirm predecessor RED milestone remains complete and evidence unchanged.
2. Apply `inference/application.py` changes exactly as above.
3. Run preserved baseline tests.
4. Run gateway RED test file; verify it now passes.
5. Update `Plan.md` execution row for milestone 4 and append command evidence.
6. Stop; any follow-on optimization or refactor requires separate planning.

## Acceptance / Completion Criteria

- All gateway RED tests pass:
  - `pytest -q tests\test_ai_gateway_red.py`
- Preserved behavior tests pass:
  - `pytest -q tests\test_clone_flow.py`
- Gateway contract behavior required by RED is implemented:
  - `/ai-gateway/v1/models` returns catalog with `chatterbox-multilingual-v3` and `hi/en`;
  - `/ai-gateway/v1/models/{model_id}/enable` returns deterministic `MODEL_NOT_ELIGIBLE` when not approved;
  - `/ai-gateway/v1/executions` enforces `idempotency_key`, language validation, routing-no-match, and deterministic error envelope.
- No unrelated files or dependency manifests are changed.
- `Plan.md` update is limited to Execution Status and evidence notes.

## Verification

### Commands

- `pytest -q tests\test_clone_flow.py`
- `pytest -q tests\test_ai_gateway_red.py`
- `git --no-pager status --short`

### Expected Evidence

- RED tests now pass (failure evidence from predecessor is resolved by GREEN behavior).
- Preserved tests continue passing.
- Diff shows only `voice_narration/inference/application.py` and execution-status updates in `Plan.md`.

### Planning-Time Dry Run

Not performed. Exact proposed code is included above for human review; verification occurs during approved GREEN execution.

## Risks

- In-memory gateway model state/idempotency is non-durable and process-local; acceptable for this milestone but not sufficient for multi-instance production.
- Mapping all execution path exceptions to `MODEL_UNAVAILABLE` may hide granular causes; acceptable for deterministic contract baseline but may need refinement in later milestones.
- Returning `202` for completed execution may differ from future async behavior expectations; contract-compatible for current scope but should be revisited if async execution is introduced.

## Pre-authorized Contingencies

None. Any change to endpoint shapes, error codes, response fields, or additional file scope requires revised plan approval.

## Rollback / Recovery

If GREEN execution must be reverted, restore only `voice_narration/inference/application.py` and milestone-4 execution lines in `Plan.md`; do not revert unrelated repository files.

## Explicitly Out of Scope

- External API integrations for inference.
- Additional model adapters beyond the Chatterbox-first route.
- UI changes for model selection.
- Persistence of gateway governance/idempotency state.

## Human Review

Status: Executed — see Plan.md
