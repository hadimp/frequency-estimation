"""
Signal generation utilities for frequency estimation.

This module provides functions to generate test signals with harmonics
and add noise to signals.
"""

import numpy as np
from numpy.typing import NDArray


def generate_test_signal(
    fundamental_freq: float,
    sampling_freq: float,
    num_samples: int
) -> NDArray[np.float64]:
    """
    Generate harmonic test signal.
    
    Creates: x(n) = sin(2πf₁n/fs) + 0.5·cos(2π·2f₁n/fs) - 0.25·cos(2π·3f₁n/fs)
    
    Contains fundamental at f₁, 2nd harmonic at 2f₁, and 3rd harmonic at 3f₁.
    
    Args:
        fundamental_freq: Fundamental frequency f₁ (Hz)
        sampling_freq: Sampling frequency fs (Hz)
        num_samples: Number of samples N
        
    Returns:
        Generated test signal (1D array of length num_samples)
        
    Example:
        >>> x = generate_test_signal(1000, 8000, 400)
        >>> x.shape
        (400,)
    """
    # Sample indices (1-indexed to match MATLAB)
    n = np.arange(1, num_samples + 1)
    
    # Normalized frequency: ω₀ = 2πf₁/fs
    omega_0 = 2 * np.pi * fundamental_freq / sampling_freq
    
    # Generate signal components
    fundamental = np.sin(omega_0 * n)
    second_harmonic = 0.5 * np.cos(2 * omega_0 * n)
    third_harmonic = -0.25 * np.cos(3 * omega_0 * n)
    
    return fundamental + second_harmonic + third_harmonic


def add_awgn(
    signal: NDArray[np.float64],
    snr_db: float
) -> NDArray[np.float64]:
    """
    Add Additive White Gaussian Noise to a signal.
    
    Adds noise to achieve the specified SNR level.
    
    Args:
        signal: Input signal
        snr_db: Desired SNR in decibels
        
    Returns:
        Signal with added noise
        
    Example:
        >>> x = np.sin(np.linspace(0, 2*np.pi, 100))
        >>> x_noisy = add_awgn(x, 20)  # 20 dB SNR
    """
    # Calculate signal power
    signal_power = np.mean(signal ** 2)
    
    # Convert SNR from dB to linear scale
    snr_linear = 10 ** (snr_db / 10)
    
    # Calculate noise power and standard deviation
    noise_power = signal_power / snr_linear
    noise_std = np.sqrt(noise_power)
    
    # Generate and add noise
    noise = noise_std * np.random.randn(*signal.shape)
    
    return signal + noise
