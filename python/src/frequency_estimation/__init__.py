"""
Adaptive Frequency Estimation using LMS Algorithm.

A Python implementation of an adaptive IIR filter for frequency estimation 
and tracking based on the paper:

    Li Tan and Jean Jiang, "Novel Adaptive IIR Filter for Frequency
    Estimation and Tracking", IEEE Signal Processing Letters, 2009.

Example (OOP interface - recommended):
    >>> from frequency_estimation import FrequencyEstimator, Config
    >>> estimator = FrequencyEstimator()
    >>> result = estimator.estimate()
    >>> print(f"Estimated frequency: {result.final_freq:.2f} Hz")
    
Example (Functional interface - legacy):
    >>> from frequency_estimation import run_frequency_estimation, Config
    >>> results = run_frequency_estimation()
    >>> print(f"Estimated frequency: {results['final_freq']:.2f} Hz")
"""

# OOP interface (recommended)
from .config import Config
from .estimator import FrequencyEstimator, EstimationResult
from .filters import NotchFilter, CascadedFilterBank
from .signal import SignalGenerator
from .visualization import ResultsPlotter

# Legacy functional interface (for backward compatibility)
from .run import run_frequency_estimation

__version__ = "2.0.0"
__author__ = "Hadi Mohammadpour"

__all__ = [
    # OOP classes
    "Config",
    "FrequencyEstimator",
    "EstimationResult",
    "NotchFilter",
    "CascadedFilterBank",
    "SignalGenerator",
    "ResultsPlotter",
    # Legacy function
    "run_frequency_estimation",
]
