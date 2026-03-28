"""Test OpenAI provider with REAL API calls (optional).

Set OPENAI_API_KEY environment variable to enable this test.
This test will make actual API calls and consume credits.

Usage:
    export OPENAI_API_KEY=sk-your-key-here
    python tests/test_openai_real.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import yaml


def test_openai_with_real_api():
    """Test with real OpenAI API (requires valid API key)."""
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key.startswith('sk-test'):
        print("\n" + "="*70)
        print("OpenAI Provider - REAL API Test (Requires Valid Key)")
        print("="*70)
        print("\n[INFO] No valid OpenAI API key found")
        print("       To enable this test:")
        print("       1. Set OPENAI_API_KEY=sk-your-real-key in .env")
        print("       2. Run: python tests/test_openai_real.py")
        print("\n" + "="*70 + "\n")
        return False
    
    print("\n" + "="*70)
    print("OpenAI Provider - REAL API Test")
    print("="*70)
    
    try:
        from ai_providers_core.factory import ProviderFactory
        
        print("\n[1] Initializing OpenAI provider...")
        provider = ProviderFactory.create('openai')
        print(f"    SUCCESS - {provider}")
        print(f"    Using model: {provider.spec_model} for specs")
        
        print("\n[2] Generating specification with OpenAI...")
        code = """
def fibonacci(n):
    '''Calculate fibonacci number at position n'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        
        print(f"    Code: {code[:50]}...")
        print("    Calling OpenAI API...")
        
        spec = provider.generate_spec('fibonacci.py', code)
        
        if spec:
            print("    SUCCESS - Specification generated!")
            print(f"    Response:")
            print(yaml.dump(spec, default_flow_style=False))
        else:
            print("    FAILED - No spec returned")
            return False
        
        print("\n[3] Generating procedure with OpenAI...")
        spec_text = spec.get('spec', 'Generate a GeneXus procedure')
        
        print(f"    Spec: {spec_text[:50]}...")
        print("    Calling OpenAI API...")
        
        procedure = provider.generate_procedure('Fibonacci', spec_text)
        
        if procedure and 'Parts' in procedure:
            print("    SUCCESS - Procedure generated!")
            print(f"    Procedure: {procedure.get('name')}")
            source = procedure['Parts'].get('Source', '')
            print(f"    Source length: {len(source)} chars")
            if source:
                print(f"    Sample:\n{source[:200]}...")
        else:
            print("    FAILED - Invalid procedure")
            return False
        
        print("\n" + "="*70)
        print("OpenAI Provider - REAL API Test PASSED!")
        print("="*70 + "\n")
        
        print("Usage information:")
        print("  - Both spec_model and proc_model can be configured via env vars")
        print("  - Supported models: gpt-4, gpt-4o, gpt-3.5-turbo, etc.")
        print("  - Set OPENAI_SPEC_MODEL and OPENAI_PROC_MODEL to override defaults")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n    ERROR: {e}")
        print("\n" + "="*70)
        print("OpenAI Provider - REAL API Test FAILED!")
        print("="*70 + "\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run real API test."""
    success = test_openai_with_real_api()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
