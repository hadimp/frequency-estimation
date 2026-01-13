"""
Visualization classes and functions for frequency estimation.

This module provides the ResultsPlotter class for visualizing
algorithm results and analysis.
"""

from .plotter import ResultsPlotter
from .plots import (
    plot_mse_analysis,
    plot_frequency_tracking,
    plot_filter_signals,
    plot_frequency_response,
)

__all__ = [
    "ResultsPlotter",
    "plot_mse_analysis",
    "plot_frequency_tracking",
    "plot_filter_signals",
    "plot_frequency_response",
]
