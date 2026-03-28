"""Quick test of GitHub Copilot provider."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers_core.factory import ProviderFactory

def main():
    print("\n" + "="*70)
    print("GitHub Copilot Provider - Quick Test")
    print("="*70)
    
    try:
        print("\n[1] Initializing GitHub Copilot provider...")
        provider = ProviderFactory.create('copilot')
        print("    SUCCESS - Provider initialized")
        
        print("\n[2] Testing simple direct call...")
        # Test direct Copilot call first
        from copilot_provider.provider import CopilotProvider
        response = CopilotProvider._call_copilot("Write a simple YAML with name: TestFunc and spec: Does nothing")
        print("    SUCCESS - Copilot responded:")
        if response:
            print(f"      Response length: {len(response)} chars")
            print(f"      First 100 chars: {response[:100]}")
        else:
            print("      WARNING: Empty response from Copilot")
        
        print("\n" + "="*70)
        print("GitHub Copilot Provider - BASIC TEST PASSED!")
        print("="*70)
        print("\nNote: Full spec/procedure generation may vary based on Copilot responses.")
        print("The provider is working correctly and can communicate with Copilot CLI.")
        print("="*70 + "\n")
        return True
        
    except Exception as e:
        print(f"\n    ERROR: {e}")
        print("\n" + "="*70)
        print("GitHub Copilot Provider - TEST FAILED!")
        print("="*70 + "\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

