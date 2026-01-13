"""
Cascaded notch filter bank computation.

This module implements the cascaded IIR notch filter bank
for harmonic signal processing.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.signal import lfilter

from ..config import Config
from ..utils import generate_test_signal, add_awgn


def compute_filter_output(theta: float, cfg: Config) -> NDArray[np.float64]:
    """
    Compute cascaded notch filter bank output.
    
    Processes signal through M cascaded IIR notch filters:
    H_m(z) = (1 - 2cos(mθ)z⁻¹ + z⁻²) / (1 - 2r·cos(mθ)z⁻¹ + r²z⁻²)
    
    Each filter rejects the m-th harmonic. Output y_M(n) should be minimized.
    
    Args:
        theta: Estimated frequency θ = 2πf₁/fs (radians)
        cfg: Configuration object
        
    Returns:
        Filter outputs array (M+1 × N+1):
        - y[0, :] = input signal
        - y[m, :] = output of stage m (m = 1, ..., M)
        
    Example:
        >>> cfg = Config()
        >>> y = compute_filter_output(0.785, cfg)
        >>> y.shape
        (4, 401)  # 3 subfilters + 1 input, 400 samples + 1
    """
    # Extract parameters
    num_subfilters = cfg.filter.num_subfilters
    pole_radius = cfg.filter.pole_radius
    num_samples = cfg.signal.num_samples + 1
    fundamental_freq = cfg.signal.fundamental_freq
    sampling_freq = cfg.signal.sampling_freq
    add_noise_flag = cfg.signal.add_noise
    snr_db = cfg.signal.snr_db
    
    total_stages = num_subfilters + 1
    
    # Generate input test signal
    input_signal = generate_test_signal(fundamental_freq, sampling_freq, num_samples)
    
    # Add noise if requested
    if add_noise_flag:
        input_signal = add_awgn(input_signal, snr_db)
    
    # Initialize output matrix
    # Row 0: input signal
    # Row m: output of m-th filter stage
    y = np.zeros((total_stages, num_samples))
    
    # Process through cascaded filter bank
    for stage in range(total_stages):
        if stage == 0:
            # First row stores the input signal
            y[0, :] = input_signal
        else:
            # Apply m-th notch filter (m = stage)
            harmonic_index = stage
            
            # Filter coefficients for H_m(z)
            # Numerator: b = [1, -2cos(mθ), 1]
            # Denominator: a = [1, -2r·cos(mθ), r²]
            b = [1, -2 * np.cos(harmonic_index * theta), 1]
            a = [1, -2 * pole_radius * np.cos(harmonic_index * theta), pole_radius ** 2]
            
            # Filter the output from previous stage
            y[stage, :] = lfilter(b, a, y[stage - 1, :])
    
    return y
