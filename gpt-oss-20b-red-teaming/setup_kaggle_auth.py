#!/usr/bin/env python3
"""
Kaggle Authentication Setup

This script helps set up Kaggle API authentication for the red-teaming challenge.
"""

import os
import json
from pathlib import Path

def setup_kaggle_auth():
    print("🔑 KAGGLE API AUTHENTICATION SETUP")
    print("=" * 50)
    
    print("To submit to Kaggle, you need:")
    print("1. Kaggle username")
    print("2. Kaggle API key")
    print()
    print("📋 How to get your Kaggle API credentials:")
    print("1. Go to: https://www.kaggle.com/account")
    print("2. Scroll down to 'API' section")
    print("3. Click 'Create New Token'")
    print("4. This downloads kaggle.json with your credentials")
    print()
    
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        print("✅ Found existing kaggle.json file")
        try:
            with open(kaggle_json, 'r') as f:
                config = json.load(f)
            print(f"   Username: {config.get('username', 'Not set')}")
            print(f"   Key: {'*' * 20 if config.get('key') else 'Not set'}")
            
            # Test connection
            try:
                import kaggle
                print("✅ Kaggle API import successful")
                
                # Try to authenticate
                from kaggle.api.kaggle_api_extended import KaggleApi
                api = KaggleApi()
                api.authenticate()
                print("✅ Kaggle authentication successful")
                
                # Try to get user info
                user_info = api.get_user()
                print(f"✅ Connected as: {user_info}")
                
                return True
                
            except Exception as e:
                print(f"❌ Kaggle authentication failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error reading kaggle.json: {e}")
            return False
    else:
        print("❌ No kaggle.json found")
        print()
        print("🛠️  MANUAL SETUP:")
        print("1. Download kaggle.json from your Kaggle account settings")
        print("2. Place it in: ~/.kaggle/kaggle.json")
        print("3. Or enter credentials manually below:")
        print()
        
        # Manual setup option
        username = input("Enter your Kaggle username (or press Enter to skip): ").strip()
        if username:
            key = input("Enter your Kaggle API key: ").strip()
            
            if username and key:
                # Create directory
                kaggle_dir.mkdir(exist_ok=True)
                
                # Create kaggle.json
                config = {
                    "username": username,
                    "key": key
                }
                
                with open(kaggle_json, 'w') as f:
                    json.dump(config, f)
                
                # Set permissions
                os.chmod(kaggle_json, 0o600)
                
                print(f"✅ Created kaggle.json at {kaggle_json}")
                
                # Test the new credentials
                try:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi()
                    api.authenticate()
                    print("✅ Authentication successful!")
                    return True
                except Exception as e:
                    print(f"❌ Authentication failed: {e}")
                    return False
        
        return False

def show_submission_process():
    print("\n🚀 SUBMISSION PROCESS OVERVIEW")
    print("=" * 50)
    print("Once Kaggle authentication is set up, you can:")
    print()
    print("1. 🔍 Validate findings:")
    print("   python submit_to_kaggle.py --validate-only")
    print()
    print("2. 📦 Create submission package:")
    print("   python submit_to_kaggle.py --package-only")
    print()
    print("3. 🚀 Full submission process:")
    print("   python submit_to_kaggle.py")
    print()
    print("📋 For the competition, you need:")
    print("- Up to 5 distinct vulnerability findings (JSON format)")
    print("- A comprehensive writeup (3000 words max)")
    print("- Reproducible demonstrations")
    print("- Optional: Open-source tools/notebooks")

if __name__ == "__main__":
    success = setup_kaggle_auth()
    show_submission_process()
    
    if not success:
        print("\n⚠️  Kaggle authentication not complete.")
        print("You can still work on finding vulnerabilities and use --package-only for manual submission.")
    else:
        print("\n🎉 Ready for Kaggle submissions!")
