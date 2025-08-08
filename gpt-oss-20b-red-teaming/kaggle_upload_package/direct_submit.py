#!/usr/bin/env python3
"""
Direct Kaggle Competition Submission Script

This script performs a direct submission to the Kaggle competition
with automatic validation, package creation, and competition submission.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Set Kaggle credentials in environment before importing
kaggle_username = os.getenv('KAGGLE_USERNAME')
kaggle_key = os.getenv('KAGGLE_KEY')

if kaggle_username and kaggle_key:
    os.environ['KAGGLE_USERNAME'] = kaggle_username
    os.environ['KAGGLE_KEY'] = kaggle_key

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from submission import KaggleSubmitter

def main():
    parser = argparse.ArgumentParser(description="Submit directly to Kaggle Red-Teaming Competition")
    parser.add_argument("--findings-dir", default="findings", help="Directory containing findings JSON files")
    parser.add_argument("--writeup", default="docs/final_writeup.md", help="Path to writeup markdown file")
    parser.add_argument("--message", default="", help="Custom submission message")
    parser.add_argument("--check-status", action="store_true", help="Only check submission status")
    
    args = parser.parse_args()
    
    try:
        print("🚀 DIRECT KAGGLE SUBMISSION")
        print("=" * 50)
        
        # Initialize submitter
        submitter = KaggleSubmitter()
        
        if args.check_status:
            print("📊 CHECKING SUBMISSION STATUS...")
            submitter.check_submission_status()
            return 0
        
        # Find findings files
        findings_dir = Path(args.findings_dir)
        if not findings_dir.exists():
            print(f"❌ Findings directory not found: {findings_dir}")
            return 1
        
        findings_files = list(findings_dir.glob("*.json"))
        if not findings_files:
            print(f"❌ No findings files found in: {findings_dir}")
            return 1
        
        print(f"📁 Found {len(findings_files)} findings files:")
        for f in findings_files:
            print(f"   - {f.name}")
        
        # Validate findings
        print(f"\n🔍 VALIDATING FINDINGS")
        print("-" * 30)
        
        validation_results = submitter.validate_findings([str(f) for f in findings_files])
        
        if not validation_results['summary']['validation_passed']:
            print(f"\n❌ Validation failed! Please fix errors before submitting.")
            for error in validation_results['summary']['errors']:
                print(f"   - {error}")
            return 1
        
        print(f"✅ All {len(findings_files)} findings validated successfully!")
        
        # Prepare writeup content
        writeup_content = generate_writeup_content(args.writeup, findings_files)
        
        # Create submission package with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n📦 CREATING SUBMISSION PACKAGE")
        print("-" * 30)
        
        package_path = submitter.export_submission_package(
            findings_files=[str(f) for f in findings_files],
            writeup_content=writeup_content,
            output_dir=f"submission_package_{timestamp}"
        )
        
        print(f"✅ Submission package created: {package_path}")
        
        # Create Kaggle datasets
        print(f"\n📊 CREATING KAGGLE DATASETS")
        print("-" * 30)
        
        dataset_slug = submitter.create_findings_dataset(
            findings_files=[str(f) for f in findings_files],
            dataset_title=f"GPT-OSS-20B Red-Teaming Findings {timestamp}",
            dataset_description="Vulnerability findings from systematic red-teaming of GPT-OSS-20B model"
        )
        
        print(f"✅ Dataset created: {dataset_slug}")
        
        # Prepare writeup
        print(f"\n📝 PREPARING WRITEUP")
        print("-" * 30)
        
        submission_id, submission_path = submitter.submit_writeup(
            writeup_title=f"GPT-OSS-20B Red-Teaming Analysis {timestamp}",
            writeup_content=writeup_content,
            attached_datasets=[dataset_slug]
        )
        
        print(f"✅ Writeup prepared: {submission_id}")
        
        # Direct submission to competition
        print(f"\n🚀 SUBMITTING TO KAGGLE COMPETITION")
        print("=" * 50)
        
        submission_message = args.message or f"GPT-OSS-20B Red-Teaming Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        success = submitter.submit_to_competition(
            submission_package_path=submission_path,
            submission_message=submission_message
        )
        
        if success:
            print(f"\n🎉 SUCCESS! SUBMISSION COMPLETED!")
            print("=" * 40)
            print("Your submission has been sent to the Kaggle competition!")
            
            # Show submission status
            print(f"\n📊 SUBMISSION STATUS:")
            submitter.check_submission_status()
            
            print(f"\n🏆 NEXT STEPS:")
            print("1. Check your submission on Kaggle's competition page")
            print("2. Monitor for any feedback from judges")
            print("3. Continue improving your findings for better scores")
            
        else:
            print(f"\n❌ SUBMISSION FAILED!")
            print("=" * 30)
            print("The submission package was created but couldn't be sent.")
            print("You can still submit manually through Kaggle's web interface.")
            print(f"Files prepared in: {package_path}")
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Direct submission failed: {e}")
        print("You can try manual submission using: python submit_to_kaggle.py --package-only")
        return 1


def generate_writeup_content(writeup_path, findings_files):
    """Generate or load writeup content."""
    
    if Path(writeup_path).exists():
        with open(writeup_path, 'r') as f:
            return f.read()
    else:
        print(f"⚠️  Writeup file not found: {writeup_path}")
        print("   Generating basic writeup from findings...")
        
        return f"""# GPT-OSS-20B Red-Teaming Challenge Submission

## Executive Summary

This submission presents the results of a systematic red-teaming analysis of the OpenAI GPT-OSS-20B model. Through comprehensive testing across multiple vulnerability categories, we identified {len(findings_files)} distinct issues that warrant attention.

## Methodology

Our red-teaming approach focused on the nine key vulnerability categories outlined in the competition:

1. **Reward Hacking** - Testing for shortcuts that maximize metrics without solving tasks
2. **Deception** - Probing for strategic lying and falsehood generation  
3. **Hidden Motivations** - Detecting covert objectives and deceptive alignment
4. **Sabotage** - Evaluating potential for intentional disruption
5. **Inappropriate Tool Use** - Testing function-calling safety boundaries
6. **Data Exfiltration** - Probing for information leakage vulnerabilities
7. **Sandbagging** - Detecting capability hiding behaviors
8. **Evaluation Awareness** - Testing for context-dependent behavior changes
9. **Chain of Thought Issues** - Analyzing reasoning transparency problems

## Key Findings

We discovered {len(findings_files)} distinct vulnerabilities across these categories, each with varying levels of severity and reproducibility. Our findings demonstrate systematic weaknesses that could be exploited in real-world deployments.

## Technical Approach

- **Automated Testing Framework**: Custom tooling for systematic vulnerability probing
- **Reproducible Methodology**: All findings include precise reproduction steps
- **Quantitative Analysis**: Severity and breadth scoring for each vulnerability
- **Documentation**: Comprehensive logging and evidence collection

## Impact Assessment

The identified vulnerabilities pose varying levels of risk to users and systems that might deploy GPT-OSS-20B in production environments. We recommend immediate attention to the highest-severity findings.

## Conclusion

This analysis contributes to the broader effort of making AI systems safer and more reliable. The identified vulnerabilities provide valuable insights for improving model training and deployment practices.

---

*Submission generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""


if __name__ == "__main__":
    exit(main())
