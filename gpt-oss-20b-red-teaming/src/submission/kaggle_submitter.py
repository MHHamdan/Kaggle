"""
Kaggle Submission Handler for GPT-OSS-20B Red-Teaming Challenge

This module handles the submission process to Kaggle, including:
- Dataset creation for findings
- Writeup generation and submission
- Competition interaction via Kaggle API
"""

import os
import json
import zipfile
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger

# Import Kaggle API conditionally to avoid authentication errors
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    KaggleApi = None


class KaggleSubmitter:
    """
    Handles submission to the Kaggle Red-Teaming Challenge.
    
    Features:
    - Automatic dataset creation from findings
    - Writeup generation and submission
    - Submission validation and tracking
    - Kaggle API integration
    """
    
    def __init__(self, username: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the Kaggle submitter.
        
        Args:
            username: Kaggle username (optional, can use env var)
            token: Kaggle API token (optional, can use env var)
        """
        load_dotenv()
        
        self.username = username or os.getenv("KAGGLE_USERNAME")
        self.token = token or os.getenv("KAGGLE_KEY")
        self.competition = os.getenv("KAGGLE_COMPETITION", "red-teaming-challenge-openai-gpt-oss-20b")
        
        # Initialize Kaggle API if available
        if KAGGLE_AVAILABLE:
            self.api = KaggleApi()
            # Set up authentication
            self._setup_authentication()
        else:
            self.api = None
            logger.warning("Kaggle API not available - submission features limited")
        
        # Track submissions
        self.submission_history = []
        
        logger.info(f"KaggleSubmitter initialized for competition: {self.competition}")
    
    def _setup_authentication(self):
        """Set up Kaggle API authentication using environment variables."""
        if not self.api:
            logger.warning("Kaggle API not available")
            return
            
        try:
            # Set environment variables for Kaggle API
            if self.username:
                os.environ['KAGGLE_USERNAME'] = self.username
            if self.token:
                os.environ['KAGGLE_KEY'] = self.token
                
            # Authenticate with Kaggle API
            self.api.authenticate()
            
            logger.info("✅ Kaggle API authentication successful")
            
        except Exception as e:
            logger.warning(f"⚠️  Kaggle authentication failed: {e}")
            logger.info("This is OK - you can still create submission packages manually")
            # Don't raise the error, just warn - we can still validate and package
    
    def create_findings_dataset(
        self,
        findings_files: List[str],
        dataset_title: str,
        dataset_description: str,
        license_name: str = "CC0-1.0"
    ) -> str:
        """
        Create a Kaggle dataset from findings files.
        
        Args:
            findings_files: List of paths to findings JSON files
            dataset_title: Title for the dataset
            dataset_description: Description for the dataset
            license_name: License for the dataset
            
        Returns:
            str: Dataset slug/identifier
        """
        try:
            # Create a temporary directory for dataset files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy findings files to temp directory
                for findings_file in findings_files:
                    src_path = Path(findings_file)
                    if src_path.exists():
                        dst_path = temp_path / src_path.name
                        with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                            dst.write(src.read())
                
                # Create dataset metadata
                dataset_metadata = {
                    "title": dataset_title,
                    "id": f"{self.username}/{dataset_title.lower().replace(' ', '-')}",
                    "licenses": [{"name": license_name}],
                    "description": dataset_description,
                    "keywords": ["ai-safety", "red-teaming", "gpt", "vulnerability"],
                    "collaborators": [],
                    "data": []
                }
                
                # Add files to metadata
                for findings_file in findings_files:
                    file_path = Path(findings_file)
                    if file_path.exists():
                        dataset_metadata["data"].append({
                            "description": f"Findings file: {file_path.name}",
                            "name": file_path.name,
                            "totalBytes": file_path.stat().st_size,
                            "columns": []
                        })
                
                # Write dataset metadata
                metadata_path = temp_path / "dataset-metadata.json"
                with open(metadata_path, 'w') as f:
                    json.dump(dataset_metadata, f, indent=2)
                
                # Create the dataset
                dataset_slug = dataset_metadata["id"]
                
                # Use Kaggle API to create dataset
                self.api.dataset_create_new(
                    folder=str(temp_path),
                    public=False,  # Keep private initially
                    quiet=False
                )
                
                logger.info(f"✅ Dataset created successfully: {dataset_slug}")
                return dataset_slug
                
        except Exception as e:
            logger.error(f"❌ Failed to create dataset: {e}")
            raise e
    
    def submit_writeup(
        self,
        writeup_title: str,
        writeup_content: str,
        attached_datasets: List[str] = None,
        attached_notebooks: List[str] = None
    ) -> str:
        """
        Submit a writeup to the Kaggle competition.
        
        Args:
            writeup_title: Title of the writeup
            writeup_content: Markdown content of the writeup
            attached_datasets: List of dataset slugs to attach
            attached_notebooks: List of notebook paths to attach
            
        Returns:
            str: Writeup/submission identifier
        """
        try:
            # Create a temporary directory for submission
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write the main writeup content
                writeup_path = temp_path / "writeup.md"
                with open(writeup_path, 'w') as f:
                    f.write(writeup_content)
                
                # Copy attached notebooks if any
                if attached_notebooks:
                    for notebook_path in attached_notebooks:
                        src_path = Path(notebook_path)
                        if src_path.exists():
                            dst_path = temp_path / src_path.name
                            with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                                dst.write(src.read())
                
                # Create submission metadata
                submission_metadata = {
                    "title": writeup_title,
                    "subtitle": "GPT-OSS-20B Red-Teaming Findings",
                    "description": "Systematic vulnerability analysis of GPT-OSS-20B model",
                    "evaluation": "Red-teaming analysis with reproducible findings",
                    "datasets": attached_datasets or [],
                    "notebooks": [str(nb) for nb in (attached_notebooks or [])],
                    "tags": ["ai-safety", "red-teaming", "vulnerability-analysis"],
                    "id": f"{self.username}/gpt-oss-20b-red-teaming-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                }
                
                # Write submission metadata
                metadata_path = temp_path / "submission-metadata.json"
                with open(metadata_path, 'w') as f:
                    json.dump(submission_metadata, f, indent=2)
                
                logger.info(f"✅ Writeup prepared for submission: {writeup_title}")
                logger.info(f"📁 Submission files ready in: {temp_path}")
                
                submission_id = submission_metadata["id"]
                
                # Track the submission
                self.submission_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "title": writeup_title,
                    "id": submission_id,
                    "datasets": attached_datasets,
                    "notebooks": attached_notebooks,
                    "status": "prepared"
                })
                
                return submission_id, str(temp_path)
                
        except Exception as e:
            logger.error(f"❌ Failed to prepare writeup submission: {e}")
            raise e
    
    def submit_to_competition(
        self,
        submission_package_path: str,
        submission_message: str = "GPT-OSS-20B Red-Teaming Submission"
    ) -> bool:
        """
        Submit directly to the Kaggle competition.
        
        Args:
            submission_package_path: Path to the submission package directory
            submission_message: Message for the submission
            
        Returns:
            bool: True if submission successful, False otherwise
        """
        if not self.api:
            logger.error("❌ Kaggle API not available")
            return False
            
        try:
            # Create a zip file of the submission package
            package_path = Path(submission_package_path)
            zip_filename = f"submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            zip_path = package_path.parent / zip_filename
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(package_path)
                        zipf.write(file_path, arcname)
            
            logger.info(f"📦 Created submission zip: {zip_path}")
            
            # Submit to competition
            logger.info(f"🚀 Submitting to competition: {self.competition}")
            
            self.api.competition_submit(
                file_name=str(zip_path),
                message=submission_message,
                competition=self.competition
            )
            
            logger.info("✅ Successfully submitted to Kaggle competition!")
            
            # Update submission history
            if self.submission_history:
                self.submission_history[-1]["status"] = "submitted"
                self.submission_history[-1]["submission_file"] = str(zip_path)
            
            # Clean up zip file
            zip_path.unlink()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to submit to competition: {e}")
            
            # Check for common issues
            if "403" in str(e) or "Forbidden" in str(e):
                logger.error("   - Competition may be closed or you don't have permission")
            elif "404" in str(e):
                logger.error(f"   - Competition '{self.competition}' not found")
            elif "authentication" in str(e).lower():
                logger.error("   - Check your Kaggle API credentials")
            
            return False
    
    def check_submission_status(self) -> List[Dict[str, Any]]:
        """
        Check the status of recent submissions to the competition.
        
        Returns:
            List of submission information
        """
        if not self.api:
            logger.warning("Kaggle API not available")
            return []
            
        try:
            submissions = self.api.competition_submissions(competition=self.competition)
            
            logger.info(f"📊 Found {len(submissions)} submissions for {self.competition}")
            
            for i, submission in enumerate(submissions[:5]):  # Show last 5
                status = submission.get('status', 'unknown')
                ref = submission.get('ref', 'unknown')
                date = submission.get('date', 'unknown')
                message = submission.get('description', 'No message')
                
                logger.info(f"   {i+1}. {ref} - {status} ({date})")
                logger.info(f"      Message: {message}")
            
            return submissions
            
        except Exception as e:
            logger.error(f"❌ Failed to check submissions: {e}")
            return []
    
    def validate_findings(self, findings_files: List[str]) -> Dict[str, Any]:
        """
        Validate findings files before submission.
        
        Args:
            findings_files: List of paths to findings JSON files
            
        Returns:
            Dict containing validation results
        """
        validation_results = {
            "total_findings": 0,
            "valid_findings": 0,
            "invalid_findings": 0,
            "errors": [],
            "warnings": [],
            "summary": {}
        }
        
        required_fields = [
            "finding_id", "title", "category", "description",
            "reproduction", "impact_assessment", "methodology"
        ]
        
        valid_categories = [
            "deception", "reward_hacking", "sabotage", "tool_misuse",
            "data_exfiltration", "sandbagging", "evaluation_awareness",
            "cot_issues", "hidden_motivations"
        ]
        
        for findings_file in findings_files:
            try:
                with open(findings_file, 'r') as f:
                    finding = json.load(f)
                
                validation_results["total_findings"] += 1
                
                # Check required fields
                missing_fields = []
                for field in required_fields:
                    if field not in finding:
                        missing_fields.append(field)
                
                if missing_fields:
                    validation_results["invalid_findings"] += 1
                    validation_results["errors"].append({
                        "file": findings_file,
                        "error": f"Missing required fields: {missing_fields}"
                    })
                    continue
                
                # Check category validity
                if finding.get("category") not in valid_categories:
                    validation_results["warnings"].append({
                        "file": findings_file,
                        "warning": f"Category '{finding.get('category')}' not in standard list"
                    })
                
                # Check self-assessed scores
                severity = finding.get("severity_assessment", {}).get("self_assessed_severity")
                breadth = finding.get("severity_assessment", {}).get("self_assessed_breadth")
                
                if severity is not None and not (1 <= severity <= 10):
                    validation_results["warnings"].append({
                        "file": findings_file,
                        "warning": f"Severity score {severity} outside expected range 1-10"
                    })
                
                if breadth is not None and not (1 <= breadth <= 10):
                    validation_results["warnings"].append({
                        "file": findings_file,
                        "warning": f"Breadth score {breadth} outside expected range 1-10"
                    })
                
                validation_results["valid_findings"] += 1
                
            except json.JSONDecodeError as e:
                validation_results["invalid_findings"] += 1
                validation_results["errors"].append({
                    "file": findings_file,
                    "error": f"Invalid JSON format: {str(e)}"
                })
            except Exception as e:
                validation_results["invalid_findings"] += 1
                validation_results["errors"].append({
                    "file": findings_file,
                    "error": f"Validation error: {str(e)}"
                })
        
        # Generate summary
        validation_results["summary"] = {
            "validation_passed": validation_results["invalid_findings"] == 0,
            "ready_for_submission": (
                validation_results["valid_findings"] > 0 and
                validation_results["invalid_findings"] == 0 and
                len(validation_results["errors"]) == 0
            ),
            "total_errors": len(validation_results["errors"]),
            "total_warnings": len(validation_results["warnings"])
        }
        
        logger.info(f"📊 Validation complete: {validation_results['valid_findings']}/{validation_results['total_findings']} findings valid")
        
        return validation_results
    
    def get_submission_status(self) -> Dict[str, Any]:
        """Get the status of current submissions."""
        return {
            "total_submissions": len(self.submission_history),
            "submissions": self.submission_history,
            "competition": self.competition,
            "username": self.username
        }
    
    def export_submission_package(
        self,
        findings_files: List[str],
        writeup_content: str,
        output_dir: str = "submission_package"
    ) -> str:
        """
        Export a complete submission package.
        
        Args:
            findings_files: List of findings JSON files
            writeup_content: Markdown content for writeup
            output_dir: Directory to create submission package
            
        Returns:
            str: Path to the submission package directory
        """
        try:
            # Create output directory
            package_path = Path(output_dir)
            package_path.mkdir(exist_ok=True)
            
            # Copy findings files
            findings_dir = package_path / "findings"
            findings_dir.mkdir(exist_ok=True)
            
            for findings_file in findings_files:
                src_path = Path(findings_file)
                if src_path.exists():
                    dst_path = findings_dir / src_path.name
                    with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                        dst.write(src.read())
            
            # Write the main writeup
            writeup_path = package_path / "writeup.md"
            with open(writeup_path, 'w') as f:
                f.write(writeup_content)
            
            # Create submission instructions
            instructions = f"""# Submission Package for GPT-OSS-20B Red-Teaming Challenge

## Contents
- `writeup.md`: Main submission writeup
- `findings/`: Directory containing individual findings JSON files
- `README.md`: This file with submission instructions

## Submission Instructions
1. Upload findings files as Kaggle datasets (keep private initially)
2. Create a new Kaggle writeup and attach the datasets
3. Copy content from writeup.md into the Kaggle writeup
4. Submit the writeup to the competition

## Validation
- Total findings: {len(findings_files)}
- Generated: {datetime.now().isoformat()}
- Competition: {self.competition}

## Files Included
"""
            
            for findings_file in findings_files:
                file_path = Path(findings_file)
                if file_path.exists():
                    instructions += f"- `findings/{file_path.name}`\n"
            
            readme_path = package_path / "README.md"
            with open(readme_path, 'w') as f:
                f.write(instructions)
            
            logger.info(f"✅ Submission package created: {package_path}")
            return str(package_path)
            
        except Exception as e:
            logger.error(f"❌ Failed to create submission package: {e}")
            raise e
