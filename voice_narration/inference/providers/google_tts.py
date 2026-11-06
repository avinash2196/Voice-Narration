"""Google Cloud Text-to-Speech provider."""

import os
import struct
from typing import Optional
from .base import InferenceProvider


def _wrap_pcm_as_wav(pcm_bytes: bytes, *, sample_rate: int = 16000, channels: int = 1, bits_per_sample: int = 16) -> bytes:
    """Wrap raw PCM audio payloads in a RIFF/WAV container so browsers can play them."""
    if not pcm_bytes:
        return pcm_bytes

    block_align = channels * bits_per_sample // 8
    byte_rate = sample_rate * block_align
    data_size = len(pcm_bytes)
    header = b"RIFF"
    header += struct.pack("<I", 36 + data_size)
    header += b"WAVE"
    header += b"fmt "
    header += struct.pack("<I", 16)
    header += struct.pack("<HHIIHH", 1, channels, sample_rate, byte_rate, block_align, bits_per_sample)
    header += b"data"
    header += struct.pack("<I", data_size)
    return header + pcm_bytes


class GoogleTextToSpeechProvider(InferenceProvider):
    """
    Google Cloud Text-to-Speech provider.

    Requires: google-cloud-texttospeech SDK and GOOGLE_APPLICATION_CREDENTIALS env var

    Characteristics:
    - Real TTS synthesis (high quality)
    - Languages: Hindi (hi-IN), English (en-IN, en-US, en-GB, etc.)
    - Multiple voices per language
    - Cost: ~$16 per 1M characters
    - Supports: pitch, speaking_rate, volume_gain controls
    - Output: WAV at 16kHz (converted from native format)
    """

    def __init__(self, config: dict = None):
        """
        Initialize Google TTS provider.

        Args:
            config: Configuration dict with optional keys:
                - credentials_path: Path to GCP service account JSON
                - project_id: GCP project ID (optional, from credentials)

        Raises:
            ImportError: If google-cloud-texttospeech not installed
            ValueError: If credentials not configured
        """
        self.config = config or {}

        try:
            from google.cloud import texttospeech
            self.texttospeech = texttospeech
        except ImportError:
            raise ImportError(
                "google-cloud-texttospeech is required. "
                "Install with: pip install google-cloud-texttospeech"
            )

        # Set credentials if path provided
        if "credentials_path" in self.config:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.config["credentials_path"]

        # Verify credentials are available
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
                "Set it to path of GCP service account JSON file."
            )

        # Initialize client
        self.client = texttospeech.TextToSpeechClient()

        # Map of language -> list of voice names
        self._voices_cache = None

    async def generate(
        self,
        script: str,
        voice_id: str,
        pitch: float = 0.0,
        speaking_rate: float = 1.0,
        **kwargs
    ) -> dict:
        """
        Generate audio from script using Google Cloud TTS.

        Args:
            script: Text to synthesize
            voice_id: Voice identifier (e.g., "en-US-Neural2-A")
            pitch: Pitch adjustment (-20.0 to 20.0)
            speaking_rate: Speaking rate (0.25 to 4.0)
            **kwargs: Additional parameters (ignored)

        Returns:
            dict with output_seconds, audio_bytes, format
        """
        # Parse language from voice_id (e.g., "en-US-Neural2-A" -> "en-US")
        language_parts = voice_id.split("-")
        language = "-".join(language_parts[:2]) if len(language_parts) >= 2 else "en-US"

        # Construct synthesis request
        synthesis_input = self.texttospeech.SynthesisInput(text=script)

        voice = self.texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_id,
        )

        audio_config = self.texttospeech.AudioConfig(
            audio_encoding=self.texttospeech.AudioEncoding.LINEAR16,
            pitch=pitch,
            speaking_rate=speaking_rate,
            sample_rate_hertz=16000,
        )

        # Call API
        print(f"[GoogleTTS] Calling API with: script='{script}' voice={voice_id} language={language}")
        
        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
        except Exception as e:
            print(f"[GoogleTTS] ERROR: API call failed with: {str(e)}")
            raise RuntimeError(f"Google TTS API error: {str(e)}")

        audio_bytes = response.audio_content
        wav_bytes = _wrap_pcm_as_wav(audio_bytes, sample_rate=16000, channels=1, bits_per_sample=16)
        print(f"[GoogleTTS] Received {len(audio_bytes)} PCM bytes from API; wrapped as WAV ({len(wav_bytes)} bytes)")

        # Calculate duration (16-bit PCM: 2 bytes per sample at 16kHz)
        num_samples = len(audio_bytes) // 2
        output_seconds = num_samples / 16000.0
        print(f"[GoogleTTS] Duration: {output_seconds:.3f} seconds ({num_samples} samples)")

        return {
            "output_seconds": output_seconds,
            "audio_bytes": wav_bytes,
            "format": "wav",
        }

    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        """
        Estimate cost for script synthesis.

        Google TTS charges ~$16 per 1M characters (Standard voices).
        Neural voices may have different rates.

        Args:
            script: Text to estimate
            voice_id: Voice identifier

        Returns:
            dict with cost_usd, estimated_seconds
        """
        char_count = len(script)
        # Estimate: ~0.1 seconds per word, ~5 chars per word
        estimated_seconds = max(1.0, char_count / 500.0)

        # Cost: $16 / 1M characters = $0.000016 per character
        cost_usd = char_count * 0.000016

        return {
            "cost_usd": cost_usd,
            "estimated_seconds": estimated_seconds,
        }

    def list_voices(self, language: Optional[str] = None) -> list:
        """
        List available Google TTS voices.

        Args:
            language: Optional language code (e.g., "hi", "en") to filter

        Returns:
            List of voice dicts
        """
        if self._voices_cache is None:
            # Fetch available voices from Google
            response = self.client.list_voices()

            voices = []
            for voice in response.voices:
                # voice.name format: "en-US-Neural2-A"
                # voice.language_codes: ["en-US"]
                lang = voice.language_codes[0] if voice.language_codes else "unknown"
                gender_map = {
                    self.texttospeech.SsmlVoiceGender.MALE: "male",
                    self.texttospeech.SsmlVoiceGender.FEMALE: "female",
                    self.texttospeech.SsmlVoiceGender.NEUTRAL: "neutral",
                }
                gender = gender_map.get(voice.ssml_gender, "neutral")

                voices.append({
                    "voice_id": voice.name,
                    "name": voice.name,
                    "language": lang,
                    "gender": gender,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                })

            self._voices_cache = voices

        if language:
            # Filter by language code prefix (e.g., "en" matches "en-US", "en-GB")
            return [
                v for v in self._voices_cache
                if v["language"].lower().startswith(language.lower())
            ]

        return self._voices_cache
