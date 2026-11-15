"""Azure Cognitive Services Speech provider."""

import os
from typing import Optional
from .base import InferenceProvider


class AzureSpeechProvider(InferenceProvider):
    """
    Azure Cognitive Services Speech provider.

    Requires: azure-cognitiveservices-speech SDK and AZURE_SPEECH_KEY/AZURE_SPEECH_REGION env vars

    Characteristics:
    - Real TTS synthesis (high quality)
    - Languages: Hindi (hi-IN), English (en-IN, en-US, en-GB, etc.)
    - Neural voices (premium quality)
    - Cost: ~$15 per 1M characters (neural voices)
    - Supports: pitch, rate, volume controls
    - Output: WAV at 16kHz (native format)
    """

    def __init__(self, config: dict = None):
        """
        Initialize Azure Speech provider.

        Args:
            config: Configuration dict with optional keys:
                - api_key: Azure Speech API key
                - region: Azure region (e.g., "eastus")

        Raises:
            ImportError: If azure-cognitiveservices-speech not installed
            ValueError: If credentials not configured
        """
        self.config = config or {}

        try:
            import azure.cognitiveservices.speech as speechsdk
            self.speechsdk = speechsdk
        except ImportError:
            raise ImportError(
                "azure-cognitiveservices-speech is required. "
                "Install with: pip install azure-cognitiveservices-speech"
            )

        # Get credentials from config or environment
        api_key = self.config.get("api_key") or os.getenv("AZURE_SPEECH_KEY")
        region = self.config.get("region") or os.getenv("AZURE_SPEECH_REGION")

        if not api_key or not region:
            raise ValueError(
                "Azure Speech API key and region not configured. "
                "Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables "
                "or pass api_key and region in config."
            )

        # Create speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=api_key,
            region=region,
        )

        # Set output format to WAV
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz16BitMonoPcm
        )

        # Map of language -> list of voice names
        self._voices_cache = None

    async def generate(
        self,
        script: str,
        voice_id: str,
        pitch: float = 0.0,
        rate: float = 1.0,
        **kwargs
    ) -> dict:
        """
        Generate audio from script using Azure Speech service.

        Args:
            script: Text to synthesize
            voice_id: Voice identifier (e.g., "hi-IN-MadhurNeural")
            pitch: Pitch adjustment (-50 to +50 in percentage)
            rate: Speaking rate (0.5 to 2.0)
            **kwargs: Additional parameters (ignored)

        Returns:
            dict with output_seconds, audio_bytes, format
        """
        import io

        # Convert rate (1.0 = normal) to Azure format (0 = normal, ±50 = ±50%)
        rate_percent = int((rate - 1.0) * 100)
        rate_str = f"{rate_percent:+d}%" if rate_percent != 0 else "0%"

        # Construct SSML with voice, pitch, and rate
        ssml = f"""
        <speak version="1.0" xml:lang="en-US">
            <voice name="{voice_id}">
                <prosody pitch="{pitch}" rate="{rate_str}">
                    {script}
                </prosody>
            </voice>
        </speak>
        """

        # Synthesize
        synthesizer = self.speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=None,  # Use default (no file output)
        )

        result = synthesizer.speak_ssml_async(ssml).get()

        if result.reason == self.speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_bytes = result.audio_data

            # Calculate duration (16-bit PCM at 16kHz: 2 bytes per sample)
            num_samples = len(audio_bytes) // 2
            output_seconds = num_samples / 16000.0

            return {
                "output_seconds": output_seconds,
                "audio_bytes": audio_bytes,
                "format": "wav",
            }
        else:
            raise RuntimeError(
                f"Azure Speech synthesis failed: {result.error_details}"
            )

    async def estimate_cost(self, script: str, voice_id: str) -> dict:
        """
        Estimate cost for script synthesis.

        Azure TTS charges ~$15 per 1M characters (Neural voices).

        Args:
            script: Text to estimate
            voice_id: Voice identifier

        Returns:
            dict with cost_usd, estimated_seconds
        """
        char_count = len(script)
        # Estimate: ~0.1 seconds per word, ~5 chars per word
        estimated_seconds = max(1.0, char_count / 500.0)

        # Cost: $15 / 1M characters = $0.000015 per character
        cost_usd = char_count * 0.000015

        return {
            "cost_usd": cost_usd,
            "estimated_seconds": estimated_seconds,
        }

    def list_voices(self, language: Optional[str] = None) -> list:
        """
        List available Azure Speech voices.

        Returns cached list of available neural voices.

        Args:
            language: Optional language code (e.g., "hi", "en") to filter

        Returns:
            List of voice dicts
        """
        if self._voices_cache is None:
            # Known Azure neural voices (subset for common languages)
            # Full list: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support
            voices = [
                # Hindi
                {
                    "voice_id": "hi-IN-MadhurNeural",
                    "name": "Madhur (Male)",
                    "language": "hi-IN",
                    "gender": "male",
                },
                {
                    "voice_id": "hi-IN-SwaraNeural",
                    "name": "Swara (Female)",
                    "language": "hi-IN",
                    "gender": "female",
                },
                # English (India)
                {
                    "voice_id": "en-IN-AmolNeural",
                    "name": "Amol (Male)",
                    "language": "en-IN",
                    "gender": "male",
                },
                {
                    "voice_id": "en-IN-NeerjaNeural",
                    "name": "Neerja (Female)",
                    "language": "en-IN",
                    "gender": "female",
                },
                # English (US)
                {
                    "voice_id": "en-US-AriaNeural",
                    "name": "Aria (Female)",
                    "language": "en-US",
                    "gender": "female",
                },
                {
                    "voice_id": "en-US-GuyNeural",
                    "name": "Guy (Male)",
                    "language": "en-US",
                    "gender": "male",
                },
                # English (GB)
                {
                    "voice_id": "en-GB-SoniaNeural",
                    "name": "Sonia (Female)",
                    "language": "en-GB",
                    "gender": "female",
                },
                {
                    "voice_id": "en-GB-RyanNeural",
                    "name": "Ryan (Male)",
                    "language": "en-GB",
                    "gender": "male",
                },
            ]

            self._voices_cache = voices

        if language:
            # Filter by language code prefix (e.g., "hi" matches "hi-IN")
            return [
                v for v in self._voices_cache
                if v["language"].lower().startswith(language.lower())
            ]

        return self._voices_cache
