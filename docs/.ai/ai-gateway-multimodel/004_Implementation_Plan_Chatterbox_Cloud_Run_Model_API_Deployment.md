# Implementation Plan — Chatterbox Cloud Run Model API Deployment

## Milestone

Chatterbox Cloud Run Model API Deployment

## Milestone Type

OTHER

## Authoritative References

| Artifact | Authority |
| --- | --- |
| `docs/.ai/ai-gateway-multimodel/requirements.md` | Approved by avinash2196 on 2026-11-08; AGW-011 requires separate Cloud Run-hosted Chatterbox API behind gateway. |
| `docs/.ai/ai-gateway-multimodel/Plan.md` | Approved revised Plan on 2026-11-08; milestone 4 is OTHER with AGW-011 ownership. |
| `docs/.ai/ai-gateway-multimodel/contract/API-Contract.md` | Approved on 2026-11-08; gateway contract behavior remains authoritative and unchanged by this milestone. |
| `docs/.ai/ai-gateway-multimodel/002_Implementation_Plan_AI_Gateway_Routing_and_Governance_RED.md` | Executed RED evidence exists; milestone 4 must not invalidate RED history. |

## Carried-Forward Decisions

- Chatterbox is the initial model target for gateway-backed routing.
- Commercial-use and self-hosted runtime gates are already evidenced in milestone 2 artifacts.
- RED evidence is established and must remain preserved; this milestone changes topology/deployment integration, not approved contract decisions.

## Preconditions / Predecessor Evidence

- `Plan.md` records milestone 1 (CONTRACT), milestone 2 (OTHER evidence), and milestone 3 (RED) as complete.
- Existing preserved checks:
  - `pytest -q tests\test_clone_flow.py` passes.
  - `pytest -q tests\test_ai_gateway_red.py` currently fails by expected RED reasons (missing `/ai-gateway/v1/*` behavior).

## Current Repository State

- No dedicated Chatterbox model API service exists in repository runtime paths.
- Inference service currently runs in-process synthesis only, with no separate backend API target.
- No Cloud Run deployment artifact exists for a standalone model service.

## Files in Scope

### Files to Create

- `voice_narration/chatterbox_api/__init__.py`
- `voice_narration/chatterbox_api/application.py`
- `voice_narration/chatterbox_api/__main__.py`
- `cloudrun/chatterbox-service/Dockerfile`
- `cloudrun/chatterbox-service/README.md`

### Files to Modify

- `voice_narration/inference/application.py`
- `requirements-dev.txt`
- `docs/.ai/ai-gateway-multimodel/Plan.md` (execution/status evidence only after successful execution)

### Files to Delete

- none

## Proposed Changes

1. Add a dedicated Chatterbox API service package exposing HTTP synthesis endpoint for Cloud Run hosting.
2. Add Cloud Run container artifact and deployment instructions for the model API service.
3. Add inference-service backend integration seam (environment-driven) so runtime can call separate Chatterbox API without changing current behavior when disabled.
4. Add required Python dependency for Chatterbox runtime.
5. Preserve all existing behavior checks; this milestone is complete only when preserved checks still pass and topology artifacts are in place.

## Proposed Code / Tests

### Create `voice_narration/chatterbox_api/__init__.py`

```python
"""Chatterbox model API service."""
```

### Create `voice_narration/chatterbox_api/application.py`

```python
from __future__ import annotations

import io
import os
import tempfile
import wave
from pathlib import Path

import torch
import torchaudio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

DEVICE = os.getenv("CHATTERBOX_DEVICE", "cpu")
MODEL_VARIANT = os.getenv("CHATTERBOX_MODEL_VARIANT", "v3")

app = FastAPI(title="Chatterbox Model API")


class SynthesizeRequest(BaseModel):
    text: str
    language: str
    sample_path: str | None = None


class SynthesizeMetadata(BaseModel):
    model_id: str
    model_version: str
    sample_rate_hz: int


_model: ChatterboxMultilingualTTS | None = None


def _get_model() -> ChatterboxMultilingualTTS:
    global _model
    if _model is None:
        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE, t3_model=MODEL_VARIANT)
    return _model


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "chatterbox_api",
        "model_variant": MODEL_VARIANT,
        "device": DEVICE,
    }


@app.post("/v1/synthesize")
def synthesize(payload: SynthesizeRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    language = payload.language.strip().lower()
    if language not in {"hi", "en"}:
        raise HTTPException(status_code=400, detail="language must be hi or en")

    model = _get_model()
    kwargs = {"language_id": language}
    if payload.sample_path:
        sample = Path(payload.sample_path)
        if not sample.exists():
            raise HTTPException(status_code=404, detail="sample_path does not exist")
        kwargs["audio_prompt_path"] = str(sample)

    try:
        wav = model.generate(text, **kwargs)
    except Exception as exc:  # explicit API error surfacing
        return JSONResponse(status_code=503, content={"detail": f"chatterbox_synthesis_failed: {exc}"})

    if isinstance(wav, torch.Tensor):
        tensor = wav.detach().cpu().float()
    else:
        tensor = torch.tensor(wav, dtype=torch.float32)
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)

    buffer = io.BytesIO()
    torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="audio/wav")


@app.get("/v1/metadata")
def metadata() -> SynthesizeMetadata:
    model = _get_model()
    return SynthesizeMetadata(
        model_id="chatterbox-multilingual-v3",
        model_version=MODEL_VARIANT,
        sample_rate_hz=model.sr,
    )
```

### Create `voice_narration/chatterbox_api/__main__.py`

```python
import uvicorn

from .application import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
```

### Create `cloudrun/chatterbox-service/Dockerfile`

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --upgrade pip && pip install -r /app/requirements-dev.txt

COPY voice_narration /app/voice_narration

ENV CHATTERBOX_DEVICE=cpu
ENV CHATTERBOX_MODEL_VARIANT=v3
ENV PORT=8080

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "voice_narration.chatterbox_api.application:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Create `cloudrun/chatterbox-service/README.md`

```md
# Chatterbox Cloud Run Model Service

## Build and deploy

```powershell
gcloud builds submit --tag gcr.io/<PROJECT_ID>/chatterbox-model-api -f cloudrun/chatterbox-service/Dockerfile .
gcloud run deploy chatterbox-model-api `
  --image gcr.io/<PROJECT_ID>/chatterbox-model-api `
  --platform managed `
  --region <REGION> `
  --allow-unauthenticated `
  --port 8080 `
  --set-env-vars CHATTERBOX_DEVICE=cpu,CHATTERBOX_MODEL_VARIANT=v3
```

## Runtime endpoints

- `GET /health`
- `GET /v1/metadata`
- `POST /v1/synthesize`
```

### Modify `requirements-dev.txt` (complete unified diff)

```diff
--- a/requirements-dev.txt
+++ b/requirements-dev.txt
@@
 fastapi==0.162.0
 uvicorn==0.54.0
 python-multipart==0.0.32
 pytest==9.1.1
 httpx==0.28.1
 psycopg[binary]==3.3.6
 numpy==2.5.4
 av==19.0.2
 playwright==1.64.1
+chatterbox-tts==0.1.7
```

### Modify `voice_narration/inference/application.py` (complete unified diff)

```diff
--- a/voice_narration/inference/application.py
+++ b/voice_narration/inference/application.py
@@
 import json
 import os
 import sqlite3
 import uuid
 from datetime import datetime, timezone
 from pathlib import Path
+import httpx
@@
 BASE_URL = os.getenv("INFERENCE_BASE_URL", "http://localhost:8003")
+CHATTERBOX_API_BASE_URL = os.getenv("CHATTERBOX_API_BASE_URL", "").strip()
@@
 def _profile_lookup(voice_profile_id: str) -> dict:
@@
     return dict(row)
+
+
+def _synthesize_via_chatterbox_api(text: str, profile: dict, output_path: Path) -> bool:
+    if not CHATTERBOX_API_BASE_URL:
+        return False
+    payload = {
+        "text": text,
+        "language": str(profile.get("language") or "en").split("-")[0].lower(),
+        "sample_path": profile.get("sample_path"),
+    }
+    try:
+        response = httpx.post(f"{CHATTERBOX_API_BASE_URL}/v1/synthesize", json=payload, timeout=120.0)
+    except Exception:
+        return False
+    if response.status_code != 200:
+        return False
+    output_path.write_bytes(response.content)
+    return True
@@
 def create_job(payload: dict) -> dict:
@@
     out_dir = AUDIO_ROOT / "generated"
     out_dir.mkdir(exist_ok=True)
     out_path = out_dir / f"{job_id}.wav"
-    provider = GoogleVoiceProvider()
-    provider.generate(text, profile, out_path)
+    generated = _synthesize_via_chatterbox_api(text, profile, out_path)
+    if not generated:
+        provider = GoogleVoiceProvider()
+        provider.generate(text, profile, out_path)
```

### Modify `docs/.ai/ai-gateway-multimodel/Plan.md`

Execution-time update only:
- Mark milestone `Chatterbox Cloud Run Model API Deployment` as `Complete`.
- Add execution evidence commands/output under execution evidence section.

## Execution Steps

1. Confirm revised Plan remains approved and predecessors remain complete.
2. Create Chatterbox API service files and Cloud Run deployment artifacts.
3. Apply integration seam in inference service behind `CHATTERBOX_API_BASE_URL`.
4. Install/restore dependencies as required by modified manifest.
5. Run preserved checks and targeted verification.
6. Update only `Plan.md` execution status/evidence for milestone 4.
7. Stop; milestone 5 GREEN requires its own approved Implementation Plan.

## Acceptance / Completion Criteria

- Separate Chatterbox API service exists in repository with health/metadata/synthesize endpoints.
- Cloud Run container/deployment artifacts exist for the separate model API.
- Inference service includes backend seam to target separate model API when configured, while preserving existing fallback behavior.
- Preserved tests pass and no unrelated behavior regressions are introduced.
- Only scoped files change, plus `Plan.md` execution-status evidence updates.

## Verification

### Commands

- `pytest -q tests\test_clone_flow.py`
- `pytest -q tests\test_ai_gateway_red.py`
- `python -m compileall voice_narration\chatterbox_api voice_narration\inference\application.py`
- `git --no-pager status --short`

### Expected Evidence

- Preserved-behavior tests:
  - `tests/test_clone_flow.py` passes.
- RED suite continues to encode contract baseline until milestone 5 implementation updates gateway behavior (failure in RED suite remains acceptable at this milestone because milestone 5 owns AGW-001..AGW-010 behavior delivery).
- New service modules compile without syntax errors.

### Planning-Time Dry Run

Not performed. This is a planning artifact; execution-time results and exact command output will be recorded in `Plan.md` evidence.

## Risks

- Chatterbox dependency footprint (torch/audio/model weights) may increase build time and Cloud Run cold starts.
- Runtime resource limits on Cloud Run may require CPU/memory tuning beyond this milestone.
- External service call latency/availability may require retry/circuit-breaker policy in later milestone work.

## Pre-authorized Contingencies

None. Any change to endpoint shape, additional deployment platform, or expanded routing behavior requires revised plan approval.

## Rollback / Recovery

If execution must be rolled back, remove created Chatterbox service/deployment artifacts and revert inference seam changes only; preserve unrelated repository changes and prior milestone evidence.

## Explicitly Out of Scope

- Implementing milestone 5 gateway GREEN behavior changes.
- Adding non-Chatterbox model backends.
- UI changes for model selection or deployment management.

## Human Review

Status: Executed — see Plan.md
