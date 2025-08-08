"""
OpenAI gpt-oss-20b Red-Teaming Challenge
========================================

A comprehensive framework for discovering vulnerabilities and harmful behaviors
in the OpenAI gpt-oss-20b model through systematic red-teaming approaches.

This package provides tools and utilities for:
- Model interaction and testing
- Vulnerability discovery and analysis
- Findings documentation and validation
- Automated testing harnesses
- Research methodology implementation

Modules:
--------
- models: Model interaction wrappers and clients
- testing: Vulnerability testing frameworks and tools
- analysis: Response analysis and evaluation utilities
- utils: Common utilities and helper functions

Author: MH Hamdan
License: MIT
"""

__version__ = "1.0.0"
__author__ = "MH Hamdan"
__email__ = "mhhamdan@example.com"
__license__ = "MIT"

# Core imports for easy access
from .models import GPTOSSClient
from .testing import VulnerabilityTester
from .analysis import ResponseAnalyzer
from .utils import FindingValidator, HarnessGenerator

__all__ = [
    "GPTOSSClient",
    "VulnerabilityTester", 
    "ResponseAnalyzer",
    "FindingValidator",
    "HarnessGenerator"
]
