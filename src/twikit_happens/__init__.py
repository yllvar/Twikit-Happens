"""
Twikit Happens - A framework for building Twitter/X bots and automation tools.

This package provides a simplified interface for interacting with Twitter/X
using the Twikit library, with added utilities for rate limiting, error handling,
and common Twitter operations.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import TwikitClient
from .utils import handle_rate_limit, TwitterError, safe_request

__all__ = ["TwikitClient", "handle_rate_limit", "TwitterError", "safe_request"]