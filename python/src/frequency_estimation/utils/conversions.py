"""
Unit conversion utilities for frequency estimation.

This module provides functions to convert between different
frequency representations and magnitude scales.
"""

import numpy as np
from numpy.typing import NDArray


def theta_to_freq(theta: float | NDArray, sampling_freq: float) -> float | NDArray:
    """
    Convert normalized frequency θ to Hz.
    
    Converts θ = 2πf/fs (radians) to f = θ·fs/(2π) (Hz).
    
    Args:
        theta: Normalized frequency (radians)
        sampling_freq: Sampling frequency fs (Hz)
        
    Returns:
        Frequency in Hz
        
    Example:
        >>> theta_to_freq(np.pi/4, 8000)  # θ = π/4
        1000.0
    """
    return theta * sampling_freq / (2 * np.pi)


def freq_to_theta(freq: float | NDArray, sampling_freq: float) -> float | NDArray:
    """
    Convert frequency in Hz to normalized θ.
    
    Converts f (Hz) to θ = 2πf/fs (radians).
    
    Args:
        freq: Frequency in Hz
        sampling_freq: Sampling frequency fs (Hz)
        
    Returns:
        Normalized frequency (radians)
        
    Example:
        >>> freq_to_theta(1000, 8000)  # f = 1000 Hz, fs = 8000 Hz
        0.7853981633974483  # π/4
    """
    return 2 * np.pi * freq / sampling_freq


def mag_to_db(magnitude: float | NDArray, floor_db: float = -120.0) -> float | NDArray:
    """
    Convert magnitude to decibels.
    
    dB = 20·log₁₀(|x|), with floor to avoid -inf for zero values.
    
    Args:
        magnitude: Magnitude value(s)
        floor_db: Minimum dB value to return (default: -120 dB)
        
    Returns:
        Value(s) in decibels
        
    Example:
        >>> mag_to_db(1.0)
        0.0
        >>> mag_to_db(0.1)
        -20.0
    """
    # Add small epsilon to avoid log10(0) = -inf
    eps = 10 ** (floor_db / 20)
    return 20 * np.log10(np.maximum(np.abs(magnitude), eps))
