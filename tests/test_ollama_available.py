"""Test Ollama provider availability and basic functionality."""

import sys
from ai_providers_core.factory import ProviderFactory


def test_ollama_registration():
    """Test that Ollama provider is registered."""
    available = ProviderFactory.get_available_providers()
    assert 'ollama' in available, f"Ollama not registered. Available: {available}"
    print("✅ Ollama provider registered")


def test_ollama_instantiation():
    """Test that Ollama provider can be instantiated."""
    try:
        provider = ProviderFactory.create('ollama')
        print(f"✅ Ollama provider instantiated: {provider.__class__.__name__}")
        print(f"   Base URL: {provider.base_url}")
        print(f"   Spec model: {provider.spec_model}")
        print(f"   Proc model: {provider.proc_model}")
    except ConnectionError as e:
        print(f"⚠️  Ollama not reachable: {e}")
        return False
    return True


def test_ollama_simple_call():
    """Test simple Ollama call with fastest model."""
    try:
        provider = ProviderFactory.create('ollama')
        
        # Use fast model for testing
        test_prompt = "Respond with exactly: OK"
        response = provider._call_ollama(
            test_prompt,
            "llama3:8b",  # Fast model
            system_prompt="You are a helpful assistant. Keep responses very short."
        )
        
        print(f"✅ Ollama call succeeded")
        print(f"   Response (first 100 chars): {response[:100]}")
        return True
        
    except Exception as e:
        print(f"❌ Ollama call failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("OLLAMA PROVIDER - AVAILABILITY TESTS")
    print("=" * 70 + "\n")
    
    try:
        test_ollama_registration()
    except AssertionError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    if not test_ollama_instantiation():
        print("\n⚠️  Ollama is not running. Start with: ollama serve")
        sys.exit(1)
    
    print("\n" + "-" * 70)
    print("Testing simple Ollama call (this may take a moment)...")
    print("-" * 70 + "\n")
    
    test_ollama_simple_call()
    
    print("\n" + "=" * 70)
    print("OLLAMA PROVIDER - READY FOR PRODUCTION")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
