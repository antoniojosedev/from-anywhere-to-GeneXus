"""Factory for creating AI provider instances."""

import os
from typing import Optional
from dotenv import load_dotenv

from ai_providers_core.base import BaseProvider


class ProviderFactory:
    """Factory class for creating AI provider instances."""

    _providers = {}

    @classmethod
    def register(cls, name: str, provider_class: type) -> None:
        """Register a provider class.
        
        Args:
            name: Provider name (e.g., 'gxeai', 'openai', 'copilot')
            provider_class: Provider class that extends BaseProvider
        """
        cls._providers[name.lower()] = provider_class

    @classmethod
    def create(cls, provider_name: Optional[str] = None) -> BaseProvider:
        """
        Create a provider instance.
        
        Args:
            provider_name: Name of provider ('gxeai', 'openai', 'copilot').
                          If None, uses AI_PROVIDER env var or defaults to 'gxeai'
        
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider not found or not registered
        """
        load_dotenv()
        
        if provider_name is None:
            provider_name = os.getenv('AI_PROVIDER', 'gxeai')
        
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            available = ', '.join(cls._providers.keys()) or 'none registered'
            raise ValueError(
                f"Provider '{provider_name}' not found. "
                f"Available providers: {available}"
            )
        
        provider_class = cls._providers[provider_name]
        return provider_class()

    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available provider names."""
        return sorted(list(cls._providers.keys()))


# Auto-register providers
def _register_default_providers():
    """Register built-in providers."""
    try:
        from gxeai.gxeai_provider import GXEAIProvider
        ProviderFactory.register('gxeai', GXEAIProvider)
    except (ImportError, ModuleNotFoundError):
        pass

    try:
        from openai_provider.provider import OpenAIProvider
        ProviderFactory.register('openai', OpenAIProvider)
    except (ImportError, ModuleNotFoundError):
        pass

    try:
        from copilot_provider.provider import CopilotProvider
        ProviderFactory.register('copilot', CopilotProvider)
    except (ImportError, ModuleNotFoundError):
        pass

    try:
        from gemini_provider.provider import GeminiProvider
        ProviderFactory.register('gemini', GeminiProvider)
    except (ImportError, ModuleNotFoundError):
        pass


_register_default_providers()
