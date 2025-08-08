"""
Model interaction modules for the red-teaming challenge.

This module provides client interfaces and wrappers for interacting
with the gpt-oss-20b model safely and efficiently.
"""

from .gpt_oss_client import GPTOSSClient

__all__ = ["GPTOSSClient"]
