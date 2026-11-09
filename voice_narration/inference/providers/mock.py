from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

import numpy as np
import wave

from .base import BaseProvider


class MockVoiceCloneProvider(BaseProvider):
    def generate(self, text: str, voice_profile: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        sample_rate = 22050
        duration = max(1.2, min(6.0, 0.12 * len(text)))
        samples = int(sample_rate * duration)
        time = np.linspace(0, duration, num=samples, endpoint=False)

        seed = int(hashlib.sha1((voice_profile.get("id", "default") + text).encode("utf-8")).hexdigest()[:8], 16)
        base_freq = 110 + (seed % 80)
        formant_a = 2.0 * np.sin(2 * np.pi * (base_freq * 0.75) * time)
        formant_b = 1.5 * np.sin(2 * np.pi * (base_freq * 1.5) * time + 0.7)
        formant_c = 0.9 * np.sin(2 * np.pi * (base_freq * 2.2) * time + 1.3)
        carrier = formant_a + formant_b + formant_c

        envelope = np.sin(np.linspace(0, np.pi, num=samples))
        envelope *= 0.8 + 0.2 * np.sin(2 * np.pi * 2.25 * time + 0.5)
        envelope = np.clip(envelope, 0.12, 1.0)

        waveform = 0.75 * carrier * envelope
        waveform = np.tanh(waveform)

        pcm = np.int16(np.clip(waveform, -1, 1) * 32767)
        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm.tobytes())
        return output_path
