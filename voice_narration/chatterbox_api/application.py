from __future__ import annotations

import io
import os
import tempfile
import threading

import torch
import torchaudio
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from starlette.datastructures import UploadFile
from starlette.exceptions import HTTPException as StarletteHTTPException

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

DEVICE = os.getenv("CHATTERBOX_DEVICE", "cpu")
MODEL_VARIANT = os.getenv("CHATTERBOX_MODEL_VARIANT", "v3")

app = FastAPI(title="Chatterbox Model API")


class SynthesizeMetadata(BaseModel):
    model_id: str
    model_version: str
    sample_rate_hz: int


class _GenerationFailed(Exception):
    """Model generation raised an error; answered as 503 chatterbox_synthesis_failed."""


_model: ChatterboxMultilingualTTS | None = None
_generation_lock = threading.Lock()


def _get_model() -> ChatterboxMultilingualTTS:
    global _model
    if _model is None:
        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
    return _model


def _validation_error(loc: tuple[str, ...], message: str) -> dict:
    return {"type": "value_error", "loc": loc, "msg": message, "input": None}


def _synthesize_wav(text: str, language: str, sample: bytes) -> bytes:
    with _generation_lock:
        model = _get_model()
        prompt_fd, prompt_path = tempfile.mkstemp(suffix=".wav")
        try:
            with os.fdopen(prompt_fd, "wb") as prompt_file:
                prompt_file.write(sample)
            try:
                wav = model.generate(text, language_id=language, audio_prompt_path=prompt_path)
            except Exception as exc:
                raise _GenerationFailed(str(exc)) from exc
        finally:
            os.unlink(prompt_path)

        if isinstance(wav, torch.Tensor):
            tensor = wav.detach().cpu().float()
        else:
            tensor = torch.tensor(wav, dtype=torch.float32)
        if tensor.ndim == 1:
            tensor = tensor.unsqueeze(0)

        buffer = io.BytesIO()
        torchaudio.save(buffer, tensor, sample_rate=model.sr, format="wav")
        return buffer.getvalue()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "chatterbox_api",
        "model_variant": MODEL_VARIANT,
        "device": DEVICE,
    }


@app.post("/v1/synthesize")
async def synthesize(request: Request):
    try:
        form = await request.form()
    except StarletteHTTPException as exc:
        raise RequestValidationError(
            [_validation_error(("body",), f"body is not valid multipart/form-data: {exc.detail}")]
        ) from exc

    try:
        text_value = form.get("text")
        language_value = form.get("language")
        sample_audio = form.get("sample_audio")

        errors = []
        if not isinstance(text_value, str):
            errors.append(_validation_error(("body", "text"), "text form field is required"))
        if not isinstance(language_value, str):
            errors.append(_validation_error(("body", "language"), "language form field is required"))
        if not isinstance(sample_audio, UploadFile):
            errors.append(_validation_error(("body", "sample_audio"), "sample_audio file part is required"))
        if errors:
            raise RequestValidationError(errors)

        if "sample_path" in form:
            raise HTTPException(
                status_code=400,
                detail="sample_path is not supported; send the voice sample as sample_audio",
            )

        text = text_value.strip()
        if not text:
            raise HTTPException(status_code=400, detail="text is required")

        language = language_value.strip().lower()
        if language not in {"hi", "en"}:
            raise HTTPException(status_code=400, detail="language must be hi or en")

        sample = await sample_audio.read()
        if not sample:
            raise HTTPException(status_code=400, detail="sample_audio is required")
    finally:
        await form.close()

    try:
        wav_bytes = await run_in_threadpool(_synthesize_wav, text, language, sample)
    except _GenerationFailed as exc:
        return JSONResponse(status_code=503, content={"detail": f"chatterbox_synthesis_failed: {exc}"})
    return Response(content=wav_bytes, media_type="audio/wav")


@app.get("/v1/metadata")
def metadata() -> SynthesizeMetadata:
    model = _get_model()
    return SynthesizeMetadata(
        model_id="chatterbox-multilingual-v3",
        model_version=MODEL_VARIANT,
        sample_rate_hz=model.sr,
    )
