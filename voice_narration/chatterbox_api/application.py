from __future__ import annotations

import io
import os
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
    except Exception as exc:
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
