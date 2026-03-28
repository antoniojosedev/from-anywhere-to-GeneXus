"""End-to-end test with GitHub Copilot provider."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers_core.factory import ProviderFactory
import yaml


def test_copilot_spec_generation():
    """Test generating specification with GitHub Copilot."""
    print("\n" + "="*70)
    print("GitHub Copilot Provider - End-to-End Test")
    print("="*70)
    
    # Simple test code
    test_code = """
def double(n):
    '''Double a number and return it'''
    return n * 2
"""
    
    print("\n[CODE] Test Code:")
    print(test_code)
    
    try:
        # Create Copilot provider
        print("\n[INIT] Initializing GitHub Copilot provider...")
        provider = ProviderFactory.create('copilot')
        print(f"[OK] Provider created: {provider}")
        
        # Generate specification
        print("\n[SPEC] Generating specification from code...")
        print("   (Calling GitHub Copilot...)")
        
        spec = provider.generate_spec('test_double.py', test_code)
        
        if spec:
            print("[OK] Specification generated!")
            print("\n[OUTPUT] Generated Spec:")
            print(yaml.dump(spec, default_flow_style=False))
            
            # Verify spec structure
            assert 'name' in spec, "Missing 'name' field"
            assert 'spec' in spec, "Missing 'spec' field"
            assert 'file_name' in spec, "Missing 'file_name' field"
            
            print("[OK] Spec structure validated")
            
            return True
        else:
            print("[FAIL] Failed to generate specification")
            return False
            
    except RuntimeError as e:
        print(f"[FAIL] Runtime Error: {e}")
        print("   Make sure GitHub Copilot CLI is installed and authenticated")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_copilot_procedure_generation():
    """Test generating procedure with GitHub Copilot."""
    print("\n" + "="*70)
    print("GitHub Copilot - Procedure Generation Test")
    print("="*70)
    
    spec = "Create a procedure that receives a number and doubles it, returning the result"
    
    print(f"\n[SPEC] Specification: {spec}")
    
    try:
        # Create Copilot provider
        print("\n[INIT] Initializing GitHub Copilot provider...")
        provider = ProviderFactory.create('copilot')
        
        # Generate procedure
        print("\n[BUILD] Generating GeneXus procedure...")
        print("   (Calling GitHub Copilot...)")
        
        procedure = provider.generate_procedure('DoubleNumber', spec)
        
        if procedure:
            print("[OK] Procedure generated!")
            print(f"\n[SPEC] Procedure Name: {procedure.get('name')}")
            
            if 'Parts' in procedure and 'Source' in procedure['Parts']:
                print(f"\n[CODE] Generated Source Code:\n")
                print(procedure['Parts']['Source'][:500])
                if len(procedure['Parts']['Source']) > 500:
                    print("...")
            
            # Verify procedure structure
            assert 'name' in procedure, "Missing 'name' field"
            assert 'Parts' in procedure, "Missing 'Parts' field"
            
            print("\n[OK] Procedure structure validated")
            return True
        else:
            print("[FAIL] Failed to generate procedure")
            return False
            
    except RuntimeError as e:
        print(f"[FAIL] Runtime Error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_copilot_with_real_spec():
    """Test with real spec file."""
    print("\n" + "="*70)
    print("GitHub Copilot - Real Spec File Test")
    print("="*70)
    
    spec_file = 'tests/testSet1.yaml'
    
    if not os.path.exists(spec_file):
        print(f"[FAIL] Spec file not found: {spec_file}")
        return False
    
    try:
        # Load spec
        print(f"\n[FILE] Loading spec file: {spec_file}")
        with open(spec_file, 'r') as f:
            specs = yaml.safe_load(f)
        
        print(f"[OK] Loaded {len(specs)} specification(s)")
        
        # Create provider
        provider = ProviderFactory.create('copilot')
        
        # Process each spec
        for spec_data in specs:
            name = spec_data.get('name')
            spec_text = spec_data.get('spec')
            
            print(f"\n[BUILD] Generating procedure for: {name}")
            print(f"   Spec: {spec_text}")
            
            procedure = provider.generate_procedure(name, spec_text)
            
            if procedure:
                print(f"   [OK] Generated successfully")
                print(f"   Name: {procedure.get('name')}")
                if 'Parts' in procedure:
                    print(f"   Parts: {list(procedure['Parts'].keys())}")
            else:
                print(f"   [FAIL] Failed to generate")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("GitHub Copilot Provider - End-to-End Testing")
    print("="*70)
    
    results = []
    
    # Test 1: Spec generation
    print("\n[TEST 1/3] Specification Generation")
    result1 = test_copilot_spec_generation()
    results.append(("Spec Generation", result1))
    
    # Test 2: Procedure generation
    print("\n[TEST 2/3] Procedure Generation")
    result2 = test_copilot_procedure_generation()
    results.append(("Procedure Generation", result2))
    
    # Test 3: Real spec file
    print("\n[TEST 3/3] Real Spec File Processing")
    result3 = test_copilot_with_real_spec()
    results.append(("Real Spec File", result3))
    
    # Summary
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<50} {status:>15}")
    
    print("-"*70)
    total_pass = sum(1 for _, r in results if r)
    print(f"Total: {total_pass}/{len(results)} tests passed")
    print("="*70 + "\n")
    
    return all(r for _, r in results)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
