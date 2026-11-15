"""Tests for provider registry and multi-provider support."""

import pytest
from voice_narration.inference import (
    ProviderRegistry,
    MockInferenceProvider,
    InferenceProvider,
)


class TestProviderRegistry:
    """M022: Provider registry tests for multi-provider support."""

    def test_registry_has_builtin_providers(self):
        """Registry includes mock, google, and azure providers."""
        providers = ProviderRegistry.list_providers()
        assert "mock" in providers
        assert "google" in providers
        assert "azure" in providers

    def test_registry_get_mock_provider(self):
        """Get mock provider from registry."""
        provider = ProviderRegistry.get_provider("mock")
        assert isinstance(provider, MockInferenceProvider)
        assert isinstance(provider, InferenceProvider)

    def test_registry_unknown_provider_raises(self):
        """Registry raises ValueError for unknown provider name."""
        with pytest.raises(ValueError, match="Unknown provider"):
            ProviderRegistry.get_provider("unknown-provider")

    def test_mock_provider_initialization(self):
        """Mock provider initializes without dependencies."""
        provider = MockInferenceProvider()
        assert provider is not None
        assert isinstance(provider, InferenceProvider)

    @pytest.mark.asyncio
    async def test_mock_provider_generate(self):
        """Mock provider can generate audio."""
        provider = MockInferenceProvider()
        output = await provider.generate("Hello world", "test-voice")

        assert "output_seconds" in output
        assert "audio_bytes" in output
        assert "format" in output
        assert output["format"] == "wav"
        assert output["output_seconds"] > 0
        assert len(output["audio_bytes"]) > 0

    @pytest.mark.asyncio
    async def test_mock_provider_estimate_cost(self):
        """Mock provider can estimate cost."""
        provider = MockInferenceProvider()
        cost = await provider.estimate_cost("Hello world", "test-voice")

        assert "cost_usd" in cost
        assert "estimated_seconds" in cost
        assert cost["cost_usd"] == 0.10
        assert cost["estimated_seconds"] > 0

    def test_mock_provider_list_voices(self):
        """Mock provider lists available voices."""
        provider = MockInferenceProvider()
        
        # Get all voices
        all_voices = provider.list_voices()
        assert len(all_voices) > 0
        assert any(v["language"] == "hi" for v in all_voices)
        assert any(v["language"] == "en" for v in all_voices)

        # Filter by language
        hindi_voices = provider.list_voices(language="hi")
        assert all(v["language"] == "hi" for v in hindi_voices)
        assert len(hindi_voices) > 0

        english_voices = provider.list_voices(language="en")
        assert all(v["language"] == "en" for v in english_voices)
        assert len(english_voices) > 0

    @pytest.mark.asyncio
    async def test_mock_provider_reproducibility(self):
        """Mock provider generates reproducible output."""
        provider = MockInferenceProvider()
        script = "Test reproducibility"
        voice_id = "test-voice"

        output1 = await provider.generate(script, voice_id)
        output2 = await provider.generate(script, voice_id)

        # Same input should produce identical output (deterministic)
        assert output1["output_seconds"] == output2["output_seconds"]
        assert output1["audio_bytes"] == output2["audio_bytes"]
        assert output1["format"] == output2["format"]

    def test_provider_interface_contract(self):
        """All providers implement the InferenceProvider interface."""
        providers_to_test = ["mock"]  # Only test mock (google/azure need credentials)

        for name in providers_to_test:
            provider = ProviderRegistry.get_provider(name)

            # Check required methods exist
            assert hasattr(provider, "generate")
            assert callable(provider.generate)
            assert hasattr(provider, "estimate_cost")
            assert callable(provider.estimate_cost)
            assert hasattr(provider, "list_voices")
            assert callable(provider.list_voices)

    def test_google_provider_importable(self):
        """Google provider class can be imported (without credentials needed)."""
        from voice_narration.inference.providers.google_tts import GoogleTextToSpeechProvider
        assert GoogleTextToSpeechProvider is not None

    def test_azure_provider_importable(self):
        """Azure provider class can be imported (without credentials needed)."""
        from voice_narration.inference.providers.azure_speech import AzureSpeechProvider
        assert AzureSpeechProvider is not None

    def test_provider_registry_register_custom(self):
        """Custom provider can be registered."""
        # Create a minimal custom provider for testing
        class CustomProvider(InferenceProvider):
            def __init__(self, config: dict = None):
                self.config = config or {}

            async def generate(self, script: str, voice_id: str, **kwargs) -> dict:
                return {
                    "output_seconds": 1.0,
                    "audio_bytes": b"fake",
                    "format": "wav",
                }

            async def estimate_cost(self, script: str, voice_id: str) -> dict:
                return {"cost_usd": 0.5, "estimated_seconds": 1.0}

            def list_voices(self, language=None):
                return []

        # Register custom provider
        ProviderRegistry.register("custom-test", CustomProvider)
        
        # Retrieve and verify
        provider = ProviderRegistry.get_provider("custom-test")
        assert isinstance(provider, CustomProvider)

        # Cleanup
        ProviderRegistry._providers.pop("custom-test", None)
