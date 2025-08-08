#!/usr/bin/env python3
"""
Quick Test Script for GPT-OSS-20B Red-Teaming Setup

This script verifies that everything is working correctly before starting
the full red-teaming process.
"""

import sys
import os
sys.path.append('src')

from models.gpt_oss_client import GPTOSSClient, ModelResponse
from dotenv import load_dotenv
import time

def test_api_connection():
    """Test basic API connection and model response."""
    print("🔍 Testing GPT-OSS-20B API Connection...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ API key not set!")
        print("Please edit .env file and set your OpenAI API key")
        print("Get your key from: https://platform.openai.com/api-keys")
        return False
    
    try:
        # Initialize client
        print("🚀 Initializing GPT-OSS client...")
        client = GPTOSSClient(
            model="gpt-4",  # Using gpt-4 as fallback since gpt-oss-20b might not be available yet
            temperature=0.7,
            max_tokens=500,
            safe_mode=True,
            enable_logging=True
        )
        print("✅ Client initialized successfully!")
        
        # Test basic connectivity
        print("\n🧪 Testing basic model interaction...")
        test_prompt = "Hello! Please introduce yourself briefly and confirm you're working correctly."
        
        response = client.generate_response(
            prompt=test_prompt,
            cache_key="quick_test_connectivity"
        )
        
        print("✅ Model responded successfully!")
        print(f"Model: {response.model}")
        print(f"Response length: {len(response.content)} characters")
        print(f"Usage: {response.usage}")
        
        print("\n📝 Model Response:")
        print("-" * 30)
        print(response.content)
        print("-" * 30)
        
        # Test usage statistics
        stats = client.get_usage_stats()
        print(f"\n📊 Usage Statistics:")
        print(f"Total requests: {stats['total_requests']}")
        print(f"Successful requests: {stats['successful_requests']}")
        print(f"Total tokens: {stats['total_tokens']}")
        print(f"Estimated cost: ${stats['total_cost']:.4f}")
        
        print("\n🎉 SUCCESS! Ready for red-teaming!")
        print("Next step: Run 'jupyter notebook notebooks/01_model_exploration.ipynb'")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API key in .env file")
        print("2. Ensure you have OpenAI API credits")
        print("3. Check your internet connection")
        return False

def show_project_status():
    """Show the current project status and next steps."""
    print("\n🏗️  PROJECT STATUS")
    print("=" * 50)
    
    # Check virtual environment
    if 'gpt-oss' in sys.executable:
        print("✅ Virtual environment 'gpt-oss' is active")
    else:
        print("⚠️  Virtual environment may not be active")
        print("   Run: source gpt-oss/bin/activate")
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is configured")
    else:
        print("❌ OpenAI API key not configured")
        print("   Get key from: https://platform.openai.com/api-keys")
        print("   Edit .env file to add your key")
    
    # Check directories
    required_dirs = ['src', 'notebooks', 'findings', 'docs', 'results', 'logs']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
            os.makedirs(dir_name, exist_ok=True)
            print(f"   Created '{dir_name}'")
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Ensure API key is set in .env file")
    print("2. Run this script: python quick_test.py")
    print("3. If test passes, open: jupyter notebook notebooks/01_model_exploration.ipynb")
    print("4. Begin systematic vulnerability testing")

if __name__ == "__main__":
    print("🚀 GPT-OSS-20B Red-Teaming Quick Test")
    print("=" * 50)
    
    # Show project status first
    show_project_status()
    
    # Ask user if they want to test API connection
    print(f"\n🔑 API Connection Test")
    print("This will test your OpenAI API key and model access.")
    
    # Test API connection
    success = test_api_connection()
    
    if success:
        print(f"\n🏁 ALL SYSTEMS GO!")
        print("You're ready to start red-teaming the GPT-OSS-20B model!")
    else:
        print(f"\n🔧 SETUP NEEDED")
        print("Please fix the issues above and run this script again.")
