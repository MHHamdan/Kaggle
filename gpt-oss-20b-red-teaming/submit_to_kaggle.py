#!/usr/bin/env python3
"""
Kaggle Submission Script for GPT-OSS-20B Red-Teaming Challenge

This script handles the submission of findings to the Kaggle competition.
It validates findings, creates datasets, and prepares the submission package.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.append('src')

from submission.kaggle_submitter import KaggleSubmitter
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="Submit findings to Kaggle Red-Teaming Challenge")
    parser.add_argument("--validate-only", action="store_true", help="Only validate findings without submitting")
    parser.add_argument("--findings-dir", default="findings", help="Directory containing findings JSON files")
    parser.add_argument("--writeup", default="docs/final_writeup.md", help="Path to writeup markdown file")
    parser.add_argument("--package-only", action="store_true", help="Only create submission package")
    
    args = parser.parse_args()
    
    print("🚀 KAGGLE SUBMISSION PROCESS")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Find findings files
    findings_dir = Path(args.findings_dir)
    findings_files = list(findings_dir.glob("*.json"))
    
    # Filter out template files
    findings_files = [f for f in findings_files if "template" not in f.name.lower()]
    
    print(f"📁 Found {len(findings_files)} findings files:")
    for f in findings_files:
        print(f"   - {f.name}")
    
    if not findings_files:
        print("❌ No findings files found! Please create your findings first.")
        print("   Use the template: findings/finding_template.json")
        return 1
    
    try:
        # Initialize submitter
        submitter = KaggleSubmitter()
        
        # Validate findings
        print(f"\n🔍 VALIDATING FINDINGS")
        print("-" * 30)
        
        validation_results = submitter.validate_findings([str(f) for f in findings_files])
        
        print(f"Total findings: {validation_results['total_findings']}")
        print(f"Valid findings: {validation_results['valid_findings']}")
        print(f"Invalid findings: {validation_results['invalid_findings']}")
        print(f"Errors: {len(validation_results['errors'])}")
        print(f"Warnings: {len(validation_results['warnings'])}")
        
        # Show errors and warnings
        if validation_results['errors']:
            print(f"\n❌ ERRORS:")
            for error in validation_results['errors']:
                print(f"   {error['file']}: {error['error']}")
        
        if validation_results['warnings']:
            print(f"\n⚠️  WARNINGS:")
            for warning in validation_results['warnings']:
                print(f"   {warning['file']}: {warning['warning']}")
        
        if not validation_results['summary']['validation_passed']:
            print(f"\n❌ Validation failed! Please fix errors before submitting.")
            return 1
        
        if args.validate_only:
            print(f"\n✅ Validation complete - all findings are valid!")
            return 0
        
        # Prepare writeup content
        writeup_content = "# GPT-OSS-20B Red-Teaming Challenge Submission\n\n"
        
        if Path(args.writeup).exists():
            with open(args.writeup, 'r') as f:
                writeup_content = f.read()
        else:
            print(f"⚠️  Writeup file not found: {args.writeup}")
            print("   Generating basic writeup from findings...")
            
            writeup_content = generate_basic_writeup(findings_files)
        
        # Create submission package
        print(f"\n📦 CREATING SUBMISSION PACKAGE")
        print("-" * 30)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_dir = f"submission_package_{timestamp}"
        
        package_path = submitter.export_submission_package(
            findings_files=[str(f) for f in findings_files],
            writeup_content=writeup_content,
            output_dir=package_dir
        )
        
        print(f"✅ Submission package created: {package_path}")
        
        if args.package_only:
            print(f"\n📋 MANUAL SUBMISSION INSTRUCTIONS:")
            print("1. Go to the competition page on Kaggle")
            print("2. Create datasets from the findings files (keep private)")
            print("3. Create a new writeup and attach the datasets")
            print("4. Copy content from the writeup.md file")
            print("5. Submit the writeup to the competition")
            return 0
        
        # Try to create datasets (this requires Kaggle authentication)
        print(f"\n📊 CREATING KAGGLE DATASETS")
        print("-" * 30)
        
        try:
            dataset_slug = submitter.create_findings_dataset(
                findings_files=[str(f) for f in findings_files],
                dataset_title=f"GPT-OSS-20B Red-Teaming Findings {timestamp}",
                dataset_description="Vulnerability findings from systematic red-teaming of GPT-OSS-20B model"
            )
            
            print(f"✅ Dataset created: {dataset_slug}")
            
            # Prepare writeup submission
            print(f"\n📝 PREPARING WRITEUP SUBMISSION")
            print("-" * 30)
            
            submission_id, submission_path = submitter.submit_writeup(
                writeup_title=f"GPT-OSS-20B Red-Teaming Analysis {timestamp}",
                writeup_content=writeup_content,
                attached_datasets=[dataset_slug]
            )
            
            print(f"✅ Writeup prepared: {submission_id}")
            
            # Now submit directly to competition
            print(f"\n🚀 SUBMITTING DIRECTLY TO KAGGLE COMPETITION")
            print("=" * 60)
            
            success = submitter.submit_to_competition(
                submission_package_path=submission_path,
                submission_message=f"GPT-OSS-20B Red-Teaming Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            if success:
                print(f"\n🎉 SUCCESS! SUBMISSION SENT TO KAGGLE!")
                print("=" * 50)
                print("Your submission has been automatically sent to the competition!")
                
                # Check submission status
                print(f"\n📊 CHECKING SUBMISSION STATUS...")
                submitter.check_submission_status()
                
            else:
                print(f"\n⚠️  DIRECT SUBMISSION FAILED")
                print("=" * 40)
                print("Your findings have been prepared for submission.")
                print("Please review the generated content and submit through Kaggle's web interface.")
            
        except Exception as e:
            print(f"⚠️  Automatic submission failed: {e}")
            print("Falling back to manual submission package...")
            print(f"Use the files in: {package_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Submission process failed: {e}")
        return 1


def generate_basic_writeup(findings_files):
    """Generate a basic writeup from findings files."""
    
    writeup = """# GPT-OSS-20B Red-Teaming Challenge Submission

## Executive Summary

This submission presents the results of a systematic red-teaming analysis of the OpenAI GPT-OSS-20B model. Through comprehensive testing across multiple vulnerability categories, we identified several concerning behaviors that warrant attention.

## Methodology

Our approach followed a structured methodology covering:

1. **Model Exploration**: Baseline behavior establishment
2. **Capability Assessment**: Understanding model strengths and limitations  
3. **Safety Mechanism Analysis**: Testing built-in protections
4. **Systematic Vulnerability Testing**: Probing across 9 key categories:
   - Reward Hacking
   - Deception
   - Hidden Motivations (Deceptive Alignment)
   - Sabotage
   - Inappropriate Tool Use
   - Data Exfiltration
   - Sandbagging
   - Evaluation Awareness
   - Chain of Thought Issues

## Key Findings

"""
    
    # Analyze findings and add summaries
    categories = {}
    total_findings = 0
    
    for findings_file in findings_files:
        try:
            with open(findings_file, 'r') as f:
                finding = json.load(f)
            
            category = finding.get('category', 'unknown')
            if category not in categories:
                categories[category] = []
            
            categories[category].append({
                'title': finding.get('title', 'Untitled'),
                'severity': finding.get('severity_assessment', {}).get('self_assessed_severity', 'N/A'),
                'description': finding.get('description', {}).get('summary', 'No description')
            })
            
            total_findings += 1
            
        except Exception as e:
            continue
    
    writeup += f"We discovered **{total_findings} distinct vulnerabilities** across **{len(categories)} categories**:\n\n"
    
    for category, findings in categories.items():
        writeup += f"### {category.title()}\n\n"
        for finding in findings:
            writeup += f"- **{finding['title']}** (Severity: {finding['severity']})\n"
            writeup += f"  {finding['description']}\n\n"
    
    writeup += """
## Impact Assessment

The discovered vulnerabilities present varying levels of risk:

- **High Severity**: Issues that could lead to significant harm or misuse
- **Medium Severity**: Concerning behaviors requiring mitigation
- **Low Severity**: Edge cases that may become problematic at scale

## Reproducibility

All findings include:
- Exact prompts used to trigger the behavior
- Expected outputs demonstrating the vulnerability
- Step-by-step reproduction instructions
- Environmental conditions and success rates

## Recommendations

Based on our analysis, we recommend:

1. **Immediate**: Address high-severity vulnerabilities with content filtering
2. **Short-term**: Implement additional safety measures for identified categories
3. **Long-term**: Enhance training procedures to prevent similar issues

## Conclusion

This systematic red-teaming effort has identified several concerning behaviors in GPT-OSS-20B that warrant attention. The documented vulnerabilities provide valuable insights for improving model safety and alignment.

## Data Availability

All findings are provided in structured JSON format with detailed reproduction instructions and supporting evidence.
"""
    
    return writeup


if __name__ == "__main__":
    exit(main())
