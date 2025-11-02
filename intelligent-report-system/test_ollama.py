"""
Quick test to verify Ollama installation and connectivity
"""
import sys

def test_ollama():
    """Test Ollama connection and models"""
    
    print("="*60)
    print("  OLLAMA INSTALLATION TEST")
    print("="*60)
    
    # Test 1: Import ollama
    print("\n[1/4] Testing ollama import...")
    try:
        import ollama
        print("✓ ollama library imported successfully")
    except ImportError:
        print("✗ ollama library not found")
        print("  Install with: pip install ollama")
        return False
    
    # Test 2: Connect to Ollama
    print("\n[2/4] Testing Ollama connection...")
    try:
        response = ollama.list()
        print("✓ Connected to Ollama successfully")
    except Exception as e:
        print(f"✗ Cannot connect to Ollama: {str(e)}")
        print("\n  Ollama is not running. Please:")
        print("  1. Install Ollama: https://ollama.ai")
        print("  2. Start Ollama: ollama serve")
        print("  3. Run this test again")
        return False
    
    # Test 3: List models
    print("\n[3/4] Checking installed models...")
    try:
        models = response.get('models', [])
        if not models:
            print("✗ No models installed")
            print("\n  Install a model:")
            print("  ollama pull llama2")
            return False
        
        print(f"✓ Found {len(models)} model(s):")
        for model in models:
            print(f"  • {model['name']}")
    except Exception as e:
        print(f"✗ Error listing models: {str(e)}")
        return False
    
    # Test 4: Test generation
    print("\n[4/4] Testing model generation...")
    try:
        model_name = models[0]['name'].split(':')[0]
        print(f"  Using model: {model_name}")
        
        response = ollama.generate(
            model=model_name,
            prompt="Say hello in one sentence.",
            options={'num_predict': 50}
        )
        
        print(f"✓ Model response: {response['response'][:100]}")
    except Exception as e:
        print(f"✗ Error testing generation: {str(e)}")
        return False
    
    # Success!
    print("\n" + "="*60)
    print("  ALL TESTS PASSED! ✓")
    print("="*60)
    print("\nOllama is ready to use!")
    print(f"Model: {model_name}")
    print("\nYou can now run: python test_module4.py")
    
    return True

if __name__ == "__main__":
    success = test_ollama()
    sys.exit(0 if success else 1)