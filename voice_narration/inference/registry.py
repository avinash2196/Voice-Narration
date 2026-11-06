"""Provider registry for TTS inference backends."""

from typing import Dict, Type
from .providers.base import InferenceProvider


class ProviderRegistry:
    """
    Factory for creating and managing TTS inference providers.

    Allows swapping between different TTS backends (mock, Google, Azure)
    without changing application code.
    """

    _providers: Dict[str, Type[InferenceProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: Type[InferenceProvider]):
        """
        Register a new provider.

        Args:
            name: Provider name (e.g., "mock", "google", "azure")
            provider_class: Provider class implementing InferenceProvider
        """
        cls._providers[name] = provider_class

    @classmethod
    def get_provider(cls, name: str, config: dict = None) -> InferenceProvider:
        """
        Get provider instance by name.

        Args:
            name: Provider name ("mock", "google", "azure")
            config: Provider-specific configuration dict

        Returns:
            Initialized InferenceProvider instance

        Raises:
            ValueError: If provider name not found
        """
        if name not in cls._providers:
            available = ", ".join(cls.list_providers())
            raise ValueError(
                f"Unknown provider: {name}. Available: {available}"
            )

        provider_class = cls._providers[name]
        return provider_class(config or {})

    @classmethod
    def list_providers(cls) -> list:
        """
        List all registered provider names.

        Returns:
            List of provider name strings
        """
        return sorted(cls._providers.keys())

    @classmethod
    def reset(cls):
        """Clear all registered providers (for testing)."""
        cls._providers.clear()


# Auto-register built-in providers
def _register_builtin_providers():
    """Register built-in TTS providers."""
    from .providers.mock import MockInferenceProvider
    from .providers.google_tts import GoogleTextToSpeechProvider
    from .providers.azure_speech import AzureSpeechProvider

    ProviderRegistry.register("mock", MockInferenceProvider)
    ProviderRegistry.register("google", GoogleTextToSpeechProvider)
    ProviderRegistry.register("azure", AzureSpeechProvider)


# Register providers when module is imported
_register_builtin_providers()
