from __future__ import annotations

import os
import wave
from pathlib import Path
from typing import Any

from google.cloud import texttospeech

from .base import BaseProvider


def _load_local_env() -> None:
    root = Path(__file__).resolve().parents[3]
    env_file = root / ".env"
    if not env_file.exists():
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            default_path = root / "service-account-key.json"
            if default_path.exists():
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(default_path)
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        if not key or key.startswith("#"):
            continue
        os.environ.setdefault(key, value.strip('"'))

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        default_path = root / "service-account-key.json"
        if default_path.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(default_path)


class GoogleVoiceProvider(BaseProvider):
    def __init__(self) -> None:
        _load_local_env()
        self._client = texttospeech.TextToSpeechClient()

    def _resolve_voice_name(self, language: str | None, voice_name: str | None) -> str:
        preferred = (voice_name or "").strip()
        if preferred and preferred.startswith(("en-", "hi-", "fr-", "es-", "ja-", "ko-")):
            return preferred

        normalized = (language or "").strip().lower()
        if normalized.startswith("hi"):
            return "hi-IN-Chirp3-HD-Achernar"
        return "en-US-Chirp-HD-F"

    def generate(self, text: str, voice_profile: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        language = str(voice_profile.get("language") or os.getenv("TTS_LANGUAGE", "en-US"))
        voice_name = self._resolve_voice_name(language, str(voice_profile.get("voice_name") or ""))

        request = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=22050,
        )

        response = self._client.synthesize_speech(
            request={
                "input": request,
                "voice": voice,
                "audio_config": audio_config,
            }
        )

        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            wav_file.writeframes(response.audio_content)

        return output_path
