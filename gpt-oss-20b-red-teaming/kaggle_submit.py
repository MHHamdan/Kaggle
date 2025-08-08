#!/usr/bin/env python3
"""
Kaggle Submission Wrapper Script

This script automatically loads Kaggle credentials from .env file
and runs the submission process with proper authentication.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Kaggle credentials from .env
    kaggle_username = os.getenv('KAGGLE_USERNAME')
    kaggle_key = os.getenv('KAGGLE_KEY')
    
    if not kaggle_username or not kaggle_key:
        print("❌ Kaggle credentials not found in .env file!")
        print("Please ensure KAGGLE_USERNAME and KAGGLE_KEY are set in .env")
        return 1
    
    # Set environment variables for the subprocess
    env = os.environ.copy()
    env['KAGGLE_USERNAME'] = kaggle_username
    env['KAGGLE_KEY'] = kaggle_key
    
    print(f"🔑 Using Kaggle credentials for user: {kaggle_username}")
    
    # Pass all command line arguments to the actual submission script
    cmd = [sys.executable, 'submit_to_kaggle.py'] + sys.argv[1:]
    
    # Run the submission script with Kaggle credentials
    try:
        result = subprocess.run(cmd, env=env, check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running submission script: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
