"""Test Google Gemini provider with mocked API calls."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
import yaml


def test_gemini_initialization():
    """Test Gemini provider can be initialized with test key."""
    print("\n" + "="*70)
    print("Google Gemini Provider - Mock Test")
    print("="*70)
    
    print("\n[1] Initializing Gemini provider with test key...")
    
    try:
        os.environ['GEMINI_API_KEY'] = 'test-gemini-key-for-testing'
        
        # Mock the Google GenAI module
        with patch('google.genai') as mock_genai:
            from gemini_provider.provider import GeminiProvider
            provider = GeminiProvider()
            
            print("    SUCCESS - Provider initialized")
            print(f"    Provider: {provider}")
            print(f"    Spec model: {provider.spec_model}")
            print(f"    Proc model: {provider.proc_model}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_spec_generation():
    """Test spec generation with mocked Gemini API."""
    print("\n[2] Testing specification generation (mocked)...")
    
    try:
        os.environ['GEMINI_API_KEY'] = 'test-key'
        
        with patch('google.genai') as mock_genai:
            # Mock the GenerativeModel
            mock_model = MagicMock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            # Mock the response
            mock_response = MagicMock()
            mock_response.text = """name: TestFunction
spec: A test function that demonstrates specification generation"""
            
            mock_model.generate_content.return_value = mock_response
            
            from gemini_provider.provider import GeminiProvider
            provider = GeminiProvider()
            
            # Call generate_spec
            result = provider.generate_spec('test.py', 'def test(): pass')
            
            assert result is not None, "Result should not be None"
            assert 'name' in result, "Should have name field"
            assert 'spec' in result, "Should have spec field"
            assert 'file_name' in result, "Should have file_name field"
            
            print("    SUCCESS - Spec generated with mocked API")
            print(f"    Result: {result}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_procedure_generation():
    """Test procedure generation with mocked Gemini API."""
    print("\n[3] Testing procedure generation (mocked)...")
    
    try:
        os.environ['GEMINI_API_KEY'] = 'test-key'
        
        with patch('google.genai') as mock_genai:
            # Mock the GenerativeModel
            mock_model = MagicMock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            # Mock the response with GeneXus procedure format
            mock_response = MagicMock()
            mock_response.text = """Procedure TestProc {
#Variables
result[Numeric(11,2)]
#EndVariables

result = 42
}"""
            
            mock_model.generate_content.return_value = mock_response
            
            from gemini_provider.provider import GeminiProvider
            provider = GeminiProvider()
            
            # Call generate_procedure
            result = provider.generate_procedure('TestProc', 'Generate a test procedure')
            
            assert result is not None, "Result should not be None"
            assert 'name' in result, "Should have name field"
            assert 'Parts' in result, "Should have Parts field"
            
            print("    SUCCESS - Procedure generated with mocked API")
            print(f"    Procedure name: {result.get('name')}")
            print(f"    Has source: {'Source' in result.get('Parts', {})}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_model_configuration():
    """Test Gemini provider respects model configuration."""
    print("\n[4] Testing model configuration...")
    
    try:
        os.environ['GEMINI_API_KEY'] = 'test-key'
        os.environ['GEMINI_SPEC_MODEL'] = 'gemini-1.5-pro'
        os.environ['GEMINI_PROC_MODEL'] = 'gemini-2.0-flash'
        
        with patch('google.genai') as mock_genai:
            from gemini_provider.provider import GeminiProvider
            provider = GeminiProvider()
            
            assert provider.spec_model == 'gemini-1.5-pro', "Should use GEMINI_SPEC_MODEL"
            assert provider.proc_model == 'gemini-2.0-flash', "Should use GEMINI_PROC_MODEL"
            
            print("    SUCCESS - Model configuration read correctly")
            print(f"    Spec model: {provider.spec_model}")
            print(f"    Proc model: {provider.proc_model}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("\n\nGoogle Gemini Provider - Mocked Integration Tests")
    print("=" * 70)
    
    results = []
    
    # Test 1
    result = test_gemini_initialization()
    results.append(("Initialization", result))
    
    # Test 2
    result = test_gemini_spec_generation()
    results.append(("Spec Generation", result))
    
    # Test 3
    result = test_gemini_procedure_generation()
    results.append(("Procedure Generation", result))
    
    # Test 4
    result = test_gemini_model_configuration()
    results.append(("Model Configuration", result))
    
    # Summary
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<45} {status:>20}")
    
    print("-"*70)
    total_pass = sum(1 for _, r in results if r)
    print(f"Total: {total_pass}/{len(results)} tests passed")
    print("="*70 + "\n")
    
    return all(r for _, r in results)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
