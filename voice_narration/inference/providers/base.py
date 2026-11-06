"""Abstract base class for inference providers (TTS backends)."""

from abc import ABC, abstractmethod
from typing import Optional


class InferenceProvider(ABC):
    """
    Abstract base class for Text-to-Speech inference providers.
    
    All TTS providers (Mock, Google Cloud, Azure Speech, etc.) must implement this interface.
    This allows swapping backends without changing the FastAPI application code.
    """

    @abstractmethod
    async def generate(
        self,
        script: str,
        voice_id: str,
        **kwargs
    ) -> dict:
        """
        Generate audio from script.

        Args:
            script: Text to synthesize
            voice_id: Voice identifier
            **kwargs: Additional parameters (pitch, speed, language, etc.)

        Returns:
            dict with keys:
                - output_seconds (float): Duration of generated audio
                - audio_bytes (bytes): Audio data (WAV format at 16kHz mono)
                - format (str): Audio format (always "wav")
        """
        pass

    @abstractmethod
    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        """
        Estimate cost before generation.

        Args:
            script: Text to estimate
            voice_id: Voice identifier

        Returns:
            dict with keys:
                - cost_usd (float): Estimated cost
                - estimated_seconds (float): Estimated duration
        """
        pass

    @abstractmethod
    def list_voices(self, language: Optional[str] = None) -> list:
        """
        List available voices.

        Args:
            language: Optional language code (e.g., "hi", "en") to filter

        Returns:
            List of voice dicts with keys:
                - voice_id (str): Unique identifier
                - name (str): Human-readable name
                - language (str): Language code
                - gender (str): "male", "female", or "neutral"
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
