from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
import httpx
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from voice_narration.inference.providers import GoogleVoiceProvider

ROOT = Path(__file__).resolve().parents[2]
AUDIO_ROOT = ROOT / "audio_storage"
AUDIO_ROOT.mkdir(exist_ok=True)
DB_PATH = AUDIO_ROOT / "generation_jobs.db"
BASE_URL = os.getenv("INFERENCE_BASE_URL", "http://localhost:8003")
CHATTERBOX_API_BASE_URL = os.getenv("CHATTERBOX_API_BASE_URL", "").strip()
VOICE_CLONING_API_BASE_URL = os.getenv("VOICE_CLONING_API_BASE_URL", CHATTERBOX_API_BASE_URL).strip()
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


def _synthesize_via_chatterbox_api(text: str, profile: dict, output_path: Path, mode: str) -> bool:
    if mode != "voice_cloning":
        return False
    if not VOICE_CLONING_API_BASE_URL:
        return False
    payload = {
        "text": text,
        "language": str(profile.get("language") or "en").split("-")[0].lower(),
        "sample_path": profile.get("sample_path"),
    }
    try:
        response = httpx.post(f"{VOICE_CLONING_API_BASE_URL}/v1/synthesize", json=payload, timeout=120.0)
    except Exception:
        return False
    if response.status_code != 200:
        return False
    output_path.write_bytes(response.content)
    return True


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
    mode = payload.get("mode") or "narration"
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
    generated = _synthesize_via_chatterbox_api(text, profile, out_path, str(mode))
    if mode == "voice_cloning" and not generated:
        raise HTTPException(
            status_code=503,
            detail="Voice cloning service is unavailable. Please retry, or use Google voice narration mode.",
        )
    if not generated:
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
        return _gateway_error(400, "INVALID_EVIDENCE", "Missing required approval evidence")

    runtime_class = payload.get("runtime_class")
    if runtime_class not in {"self_hosted", "external_api"}:
        return _gateway_error(400, "INVALID_EVIDENCE", "runtime_class must be self_hosted or external_api")

    languages = payload.get("languages_supported")
    if not isinstance(languages, list) or not languages:
        return _gateway_error(400, "INVALID_EVIDENCE", "languages_supported must be non-empty")

    model["model_version"] = payload["model_version"]
    model["license_evidence_uri"] = payload["license_evidence_uri"]
    model["weights_evidence_uri"] = payload["weights_evidence_uri"]
    model["output_use_evidence_uri"] = payload["output_use_evidence_uri"]
    model["runtime_class"] = runtime_class
    model["languages_supported"] = languages
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
        return _gateway_error(409, "MODEL_STATE_CONFLICT", "Model version mismatch")

    if model.get("state") != "approved":
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Model is not approved for enablement")

    if model.get("runtime_class") != "self_hosted":
        return _gateway_error(403, "RUNTIME_POLICY_VIOLATION", "Runtime must be self_hosted")

    if any(not model.get(field) for field in ("license_evidence_uri", "weights_evidence_uri", "output_use_evidence_uri")):
        return _gateway_error(403, "MODEL_NOT_ELIGIBLE", "Commercial evidence is incomplete")

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
    started = time.perf_counter()

    try:
        job = create_job(
            {
                "text": text,
                "voice_profile_id": voice_profile_id,
                "voice_name": voice_name,
                "user_id": user_id,
                "mode": mode,
            }
        )
    except HTTPException as exc:
        if exc.status_code == 503:
            detail = exc.detail if isinstance(exc.detail, str) else "Model execution path unavailable"
            return _gateway_error(503, "MODEL_UNAVAILABLE", detail, retryable=True)
        return _gateway_error(503, "MODEL_UNAVAILABLE", "Model execution path unavailable", retryable=True)

    elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
    cost_estimate_usd = f"{elapsed_ms * 0.000001:.6f}"

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
            "latency_ms": elapsed_ms,
            "queue_ms": 0,
            "compute_ms": elapsed_ms,
            "cost_estimate_usd": cost_estimate_usd,
            "runtime_class": model["runtime_class"],
        },
        "errors": [],
    }
    _gateway_idempotency[idempotency_key] = {"fingerprint": fingerprint, "response": response}
    return JSONResponse(status_code=202, content=response)
