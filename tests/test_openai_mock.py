"""Test OpenAI provider with mocked API calls."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
import yaml


def test_openai_initialization():
    """Test OpenAI provider can be initialized with test key."""
    print("\n" + "="*70)
    print("OpenAI Provider - Mock Test")
    print("="*70)
    
    print("\n[1] Initializing OpenAI provider with test key...")
    
    try:
        os.environ['OPENAI_API_KEY'] = 'sk-test-key-for-testing'
        
        # Mock the OpenAI client
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            from openai_provider.provider import OpenAIProvider
            provider = OpenAIProvider()
            
            print("    SUCCESS - Provider initialized")
            print(f"    Provider: {provider}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_openai_spec_generation():
    """Test spec generation with mocked OpenAI API."""
    print("\n[2] Testing specification generation (mocked)...")
    
    try:
        os.environ['OPENAI_API_KEY'] = 'sk-test-key'
        
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Mock the chat completion response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = """name: TestFunction
spec: A test function that demonstrates specification generation"""
            
            mock_client.chat.completions.create.return_value = mock_response
            
            from openai_provider.provider import OpenAIProvider
            provider = OpenAIProvider()
            
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


def test_openai_procedure_generation():
    """Test procedure generation with mocked OpenAI API."""
    print("\n[3] Testing procedure generation (mocked)...")
    
    try:
        os.environ['OPENAI_API_KEY'] = 'sk-test-key'
        
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Mock the chat completion response with GeneXus procedure format
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = """Procedure TestProc {
#Variables
result[Numeric(11,2)]
#EndVariables

result = 42
}"""
            
            mock_client.chat.completions.create.return_value = mock_response
            
            from openai_provider.provider import OpenAIProvider
            provider = OpenAIProvider()
            
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


def test_openai_model_configuration():
    """Test OpenAI provider respects model configuration."""
    print("\n[4] Testing model configuration...")
    
    try:
        os.environ['OPENAI_API_KEY'] = 'sk-test-key'
        os.environ['OPENAI_SPEC_MODEL'] = 'gpt-4'
        os.environ['OPENAI_PROC_MODEL'] = 'gpt-4o'
        
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            from openai_provider.provider import OpenAIProvider
            provider = OpenAIProvider()
            
            assert provider.spec_model == 'gpt-4', "Should use OPENAI_SPEC_MODEL"
            assert provider.proc_model == 'gpt-4o', "Should use OPENAI_PROC_MODEL"
            
            print("    SUCCESS - Model configuration read correctly")
            print(f"    Spec model: {provider.spec_model}")
            print(f"    Proc model: {provider.proc_model}")
            
            return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("\n\nOpenAI Provider - Mocked Integration Tests")
    print("=" * 70)
    
    results = []
    
    # Test 1
    result = test_openai_initialization()
    results.append(("Initialization", result))
    
    # Test 2
    result = test_openai_spec_generation()
    results.append(("Spec Generation", result))
    
    # Test 3
    result = test_openai_procedure_generation()
    results.append(("Procedure Generation", result))
    
    # Test 4
    result = test_openai_model_configuration()
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
