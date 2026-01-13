"""
Utility functions for frequency estimation.

This module provides helper functions for signal generation,
noise addition, and unit conversions.
"""

from .signal import generate_test_signal, add_awgn
from .conversions import theta_to_freq, freq_to_theta, mag_to_db

__all__ = [
    "generate_test_signal",
    "add_awgn",
    "theta_to_freq",
    "freq_to_theta",
    "mag_to_db",
]
