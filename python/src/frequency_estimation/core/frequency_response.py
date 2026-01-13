"""
Frequency response computation for filter bank.

This module implements frequency response analysis for
the cascaded notch filter bank.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.signal import freqz

from ..config import Config


def compute_frequency_response(
    theta: float,
    cfg: Config
) -> tuple[NDArray[np.complex128], NDArray[np.complex128], NDArray[np.float64]]:
    """
    Compute frequency response H(ω) of filter bank.
    
    H_total = ∏_{m=1}^{M} H_m(e^{jω}) creates comb filter with notches at harmonics.
    
    Args:
        theta: Frequency parameter θ = 2πf₁/fs (radians)
        cfg: Configuration object
        
    Returns:
        Tuple of (H_total, H_stages, freq_axis):
        - H_total: Total cascade response (normalized, complex)
        - H_stages: Individual stage responses (M+1 × num_freq_points, complex)
        - freq_axis: Frequency axis in Hz
        
    Example:
        >>> cfg = Config()
        >>> H_total, H_stages, freq = compute_frequency_response(0.785, cfg)
    """
    # Extract parameters
    num_subfilters = cfg.filter.num_subfilters
    pole_radius = cfg.filter.pole_radius
    sampling_freq = cfg.signal.sampling_freq
    num_points = cfg.lms.num_theta_points
    
    total_stages = num_subfilters + 1
    num_freq_points = num_points * 3
    
    # Define frequency axis
    omega = np.linspace(-np.pi, np.pi, num_freq_points)
    freq_axis = omega * sampling_freq / (2 * np.pi)
    
    # Initialize outputs
    H_stages = np.zeros((total_stages, num_freq_points), dtype=complex)
    H_total = np.ones(num_freq_points, dtype=complex)
    
    # Compute frequency response for each stage
    for stage in range(total_stages):
        harmonic_idx = stage + 1  # 1-indexed harmonic
        
        # Filter coefficients
        b = [1, -2 * np.cos(harmonic_idx * theta), 1]
        a = [1, -2 * pole_radius * np.cos(harmonic_idx * theta), pole_radius ** 2]
        
        # Compute frequency response
        _, H = freqz(b, a, worN=omega, fs=2*np.pi)
        
        # Normalize to unity at a reference point
        normalization = 1 / np.abs(H[num_points])
        H = H * normalization
        
        # Store individual response
        H_stages[stage, :] = H
        
        # Accumulate total response
        H_total = H_total * H
    
    # Normalize total response
    total_normalization = 1 / np.abs(H_total[num_points])
    H_total = H_total * total_normalization
    
    return H_total, H_stages, freq_axis
