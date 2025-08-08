"""
Kaggle submission module for the OpenAI gpt-oss-20b Red-Teaming Challenge.

This module handles the submission of findings to the Kaggle competition,
including dataset creation, writeup formatting, and submission validation.
"""

from .kaggle_submitter import KaggleSubmitter

__all__ = ["KaggleSubmitter"]
