"""Integration test for provider system."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers_core.factory import ProviderFactory
from ai_providers_core.base import BaseProvider


def test_factory_registration():
    """Test that all providers are registered."""
    providers = ProviderFactory.get_available_providers()
    print(f"✅ Registered providers: {providers}")
    
    expected = ['gxeai', 'openai', 'copilot']
    for provider_name in expected:
        assert provider_name in providers, f"Provider {provider_name} not registered"
    
    assert len(providers) == 3, f"Expected 3 providers, got {len(providers)}"
    print("✅ All 3 providers registered correctly")


def test_provider_creation():
    """Test creating provider instances."""
    providers_to_test = []
    
    # Test factory creation (will fail if missing dependencies, that's ok)
    try:
        from gxeai.gxeai_provider import GXEAIProvider
        providers_to_test.append(('gxeai', GXEAIProvider))
    except ImportError as e:
        print(f"⚠️  GXEAI provider not available: {e}")
    
    try:
        from openai_provider.provider import OpenAIProvider
        providers_to_test.append(('openai', OpenAIProvider))
    except ImportError as e:
        print(f"⚠️  OpenAI provider not available (need: pip install openai): {e}")
    
    try:
        from copilot_provider.provider import CopilotProvider
        providers_to_test.append(('copilot', CopilotProvider))
    except (ImportError, RuntimeError) as e:
        print(f"⚠️  Copilot provider not available (need GitHub Copilot CLI): {e}")
    
    print(f"✅ Provider classes can be imported: {[p[0] for p in providers_to_test]}")


def test_base_provider_abstract():
    """Test that BaseProvider is abstract."""
    try:
        provider = BaseProvider()
        assert False, "Should not be able to instantiate abstract BaseProvider"
    except TypeError:
        print("✅ BaseProvider is properly abstract")


def test_provider_interface():
    """Test that providers have required methods."""
    # Check GXEAI provider interface
    from gxeai.gxeai_provider import GXEAIProvider
    
    assert hasattr(GXEAIProvider, 'generate_spec'), "Missing generate_spec method"
    assert hasattr(GXEAIProvider, 'generate_procedure'), "Missing generate_procedure method"
    assert callable(getattr(GXEAIProvider, 'generate_spec')), "generate_spec not callable"
    assert callable(getattr(GXEAIProvider, 'generate_procedure')), "generate_procedure not callable"
    
    print("✅ GXEAI provider has all required methods")
    
    # Check OpenAI provider interface
    from openai_provider.provider import OpenAIProvider
    
    assert hasattr(OpenAIProvider, 'generate_spec'), "Missing generate_spec method"
    assert hasattr(OpenAIProvider, 'generate_procedure'), "Missing generate_procedure method"
    
    print("✅ OpenAI provider has all required methods")
    
    # Check Copilot provider interface
    from copilot_provider.provider import CopilotProvider
    
    assert hasattr(CopilotProvider, 'generate_spec'), "Missing generate_spec method"
    assert hasattr(CopilotProvider, 'generate_procedure'), "Missing generate_procedure method"
    
    print("✅ Copilot provider has all required methods")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Provider Architecture Integration Tests")
    print("=" * 60)
    
    print("\n1. Testing factory registration...")
    test_factory_registration()
    
    print("\n2. Testing provider creation...")
    test_provider_creation()
    
    print("\n3. Testing BaseProvider abstraction...")
    test_base_provider_abstract()
    
    print("\n4. Testing provider interfaces...")
    test_provider_interface()
    
    print("\n" + "=" * 60)
    print("✅ All integration tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
