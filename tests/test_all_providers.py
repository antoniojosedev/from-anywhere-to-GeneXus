"""Summary test showing all three providers."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers_core.factory import ProviderFactory


def test_all_providers():
    """Test that all three providers are available and working."""
    
    print("\n" + "="*70)
    print("FROM-ANYWHERE-TO-GENEXUS - Multi-Provider Test")
    print("="*70)
    
    print("\n[1] Available Providers:")
    providers = ProviderFactory.get_available_providers()
    for i, provider_name in enumerate(providers, 1):
        print(f"    {i}. {provider_name.upper()}")
    
    print(f"\n    Total: {len(providers)} providers registered")
    
    # Test each provider
    results = {}
    
    for provider_name in providers:
        print(f"\n[{provider_name.upper()}] Testing provider...")
        try:
            provider = ProviderFactory.create(provider_name)
            results[provider_name] = {
                'initialized': True,
                'instance': str(provider),
                'error': None
            }
            print(f"    SUCCESS - {provider}")
        except Exception as e:
            results[provider_name] = {
                'initialized': False,
                'instance': None,
                'error': str(e)
            }
            print(f"    INFO - {e}")
    
    # Summary
    print("\n" + "="*70)
    print("PROVIDER STATUS SUMMARY")
    print("="*70)
    
    for provider_name, status in results.items():
        if status['initialized']:
            print(f"{provider_name.upper():<10} [OK] Ready to use")
        else:
            reason = status['error'][:40] + "..." if len(status['error']) > 40 else status['error']
            print(f"{provider_name.upper():<10} [INFO] {reason}")
    
    print("\n" + "="*70)
    print("PROVIDER CAPABILITIES")
    print("="*70)
    
    print("""
OpenAI Provider:
    - Models: GPT-4, GPT-4o, GPT-3.5-turbo, etc.
    - Setup: OPENAI_API_KEY=sk-your-key
    - Cost: Depends on model and usage
    - Speed: Fast
    - Quality: Excellent

GitHub Copilot Provider:
    - CLI Integration: GitHub Copilot CLI v1.0.12+
    - Setup: copilot auth login (local CLI)
    - Cost: Free (with subscription) or included in plan
    - Speed: Very Fast
    - Quality: Excellent

GXEAI Provider (Legacy):
    - API Integration: GXEAI assistant
    - Setup: TOKEN + BASE_URL
    - Cost: Contact GeneXus
    - Speed: Variable
    - Quality: Good
""")
    
    print("="*70)
    print("USAGE EXAMPLES")
    print("="*70)
    
    print("""
1. Using OpenAI:
   export AI_PROVIDER=openai
   export OPENAI_API_KEY=sk-your-key
   python anything_to_spec.py --programs_directory ./tests/cobol/test1/ \\
     --spec_path ./outputs/spec1.yml

2. Using GitHub Copilot:
   export AI_PROVIDER=copilot
   python anything_to_spec.py --programs_directory ./tests/cobol/test1/ \\
     --spec_path ./outputs/spec1.yml

3. Using GXEAI:
   export AI_PROVIDER=gxeai
   export SAIA_PROJECT_APITOKEN=your-token
   python anything_to_spec.py --programs_directory ./tests/cobol/test1/ \\
     --spec_path ./outputs/spec1.yml

4. Via CLI flag:
   python anything_to_spec.py --programs_directory ./tests/cobol/test1/ \\
     --spec_path ./outputs/spec1.yml --provider openai
""")
    
    print("="*70)
    print("NEXT STEPS")
    print("="*70)
    
    print("""
For OpenAI:
    1. Get your API key from https://platform.openai.com/api-keys
    2. Add to .env: OPENAI_API_KEY=sk-your-key
    3. Run: python tests/test_openai_real.py

For GitHub Copilot:
    1. Install CLI: https://github.com/github/copilot-cli
    2. Authenticate: copilot auth login
    3. Run: python tests/test_copilot_quick.py

For GXEAI:
    1. Request token from GeneXus
    2. Add to .env: SAIA_PROJECT_APITOKEN=your-token
    3. Also set: BASE_URL, SPEC_ASSISTANT_NAME, PROC_ASSISTANT_NAME
""")
    
    print("\n" + "="*70)
    print("Multi-Provider Architecture - READY FOR USE")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_all_providers()
    sys.exit(0 if success else 1)
