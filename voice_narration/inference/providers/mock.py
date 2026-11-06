"""Mock inference provider for testing and development."""

import struct
from typing import Optional
from .base import InferenceProvider


class MockInferenceProvider(InferenceProvider):
    """
    Deterministic mock provider for testing and local development.

    Characteristics:
    - Output duration: 1 second per 100 characters (synthetic timing)
    - Audio format: Silent WAV bytes (16 kHz, mono, 16-bit PCM)
    - Latency: Zero (synchronous mock, no external calls)
    - Cost: Fixed $0.10 per generation
    - Deterministic: Same input produces identical output every time
    - No dependencies: No external APIs or libraries required
    """

    MOCK_VOICES = [
        {
            "voice_id": "mock-hindi-female",
            "name": "Mock Hindi Female",
            "language": "hi",
            "gender": "female",
        },
        {
            "voice_id": "mock-hindi-male",
            "name": "Mock Hindi Male",
            "language": "hi",
            "gender": "male",
        },
        {
            "voice_id": "mock-english-female",
            "name": "Mock English Female",
            "language": "en",
            "gender": "female",
        },
        {
            "voice_id": "mock-english-male",
            "name": "Mock English Male",
            "language": "en",
            "gender": "male",
        },
    ]

    def __init__(self, config: dict = None):
        """
        Initialize mock provider.

        Args:
            config: Unused (for compatibility with other providers)
        """
        self.config = config or {}

    async def generate(
        self,
        script: str,
        voice_id: str,
        **kwargs
    ) -> dict:
        """Generate audio from script using mock provider."""
        # Calculate output duration: 1 second per 100 characters
        output_seconds = max(1.0, len(script) / 100.0)

        # Generate silent WAV bytes
        sample_rate = 16000
        num_samples = int(sample_rate * output_seconds)
        audio_bytes = self._generate_silent_wav(num_samples, sample_rate)

        return {
            "output_seconds": output_seconds,
            "audio_bytes": audio_bytes,
            "format": "wav",
        }

    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        """Estimate cost for script synthesis."""
        output_seconds = max(1.0, len(script) / 100.0)
        return {
            "cost_usd": 0.10,
            "estimated_seconds": output_seconds,
        }

    def list_voices(self, language: Optional[str] = None) -> list:
        """List available mock voices."""
        if language:
            return [v for v in self.MOCK_VOICES if v["language"] == language]
        return self.MOCK_VOICES

    @staticmethod
    def _generate_silent_wav(
        num_samples: int,
        sample_rate: int = 16000,
    ) -> bytes:
        """
        Generate minimal valid WAV file with silent audio.

        Creates a proper WAV file structure with silent PCM data.
        Format: 16 kHz, mono, 16-bit PCM.

        Args:
            num_samples: Number of audio samples to generate
            sample_rate: Sample rate in Hz

        Returns:
            WAV file bytes
        """
        channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        subchunk2_size = num_samples * block_align

        # Build WAV header
        wav = b"RIFF"
        wav += struct.pack("<I", 36 + subchunk2_size)  # file size - 8
        wav += b"WAVE"

        # fmt subchunk
        wav += b"fmt "
        wav += struct.pack("<I", 16)  # subchunk1 size
        wav += struct.pack(
            "<HHIIHH",
            1,  # audio format (1 = PCM)
            channels,
            sample_rate,
            byte_rate,
            block_align,
            bits_per_sample,
        )

        # data subchunk
        wav += b"data"
        wav += struct.pack("<I", subchunk2_size)
        wav += b"\x00" * subchunk2_size  # silent PCM data

        return wav
