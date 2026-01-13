"""
Signal generator implementation.

This module provides the SignalGenerator class for creating
harmonic test signals with optional noise.
"""

import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from typing import Optional


@dataclass
class SignalGenerator:
    """
    Generator for harmonic test signals.
    
    Creates signals of the form:
    x(n) = sin(ω₀n) + 0.5·cos(2ω₀n) - 0.25·cos(3ω₀n)
    
    where ω₀ = 2πf₁/fs is the normalized fundamental frequency.
    
    Attributes:
        fundamental_freq: Fundamental frequency f₁ (Hz)
        sampling_freq: Sampling frequency fs (Hz)
        add_noise: Whether to add Gaussian noise
        snr_db: Signal-to-noise ratio in dB (if add_noise=True)
        
    Example:
        >>> gen = SignalGenerator(fundamental_freq=1000, sampling_freq=8000)
        >>> signal = gen.generate(400)
        >>> signal.shape
        (400,)
    """
    fundamental_freq: float
    sampling_freq: float
    add_noise: bool = False
    snr_db: float = 18.0
    
    _cached_signal: Optional[NDArray[np.float64]] = None
    _cached_num_samples: Optional[int] = None
    
    def __post_init__(self):
        """Validate parameters."""
        if self.fundamental_freq <= 0:
            raise ValueError("Fundamental frequency must be positive")
        if self.sampling_freq <= 0:
            raise ValueError("Sampling frequency must be positive")
        if self.fundamental_freq >= self.sampling_freq / 2:
            raise ValueError("Fundamental frequency must be below Nyquist")
    
    @property
    def omega_0(self) -> float:
        """Normalized fundamental frequency ω₀ = 2πf₁/fs."""
        return 2 * np.pi * self.fundamental_freq / self.sampling_freq
    
    def generate(
        self, 
        num_samples: int, 
        use_cache: bool = False
    ) -> NDArray[np.float64]:
        """
        Generate harmonic test signal.
        
        Args:
            num_samples: Number of samples to generate
            use_cache: If True, return cached signal if available
            
        Returns:
            Generated signal array of shape (num_samples,)
        """
        # Return cached signal if available and requested
        if use_cache and self._cached_signal is not None:
            if self._cached_num_samples == num_samples:
                return self._cached_signal.copy()
        
        # Generate sample indices (1-indexed to match MATLAB)
        n = np.arange(1, num_samples + 1)
        omega_0 = self.omega_0
        
        # Generate signal components
        fundamental = np.sin(omega_0 * n)
        second_harmonic = 0.5 * np.cos(2 * omega_0 * n)
        third_harmonic = -0.25 * np.cos(3 * omega_0 * n)
        
        signal = fundamental + second_harmonic + third_harmonic
        
        # Add noise if requested
        if self.add_noise:
            signal = self._add_awgn(signal)
        
        # Cache the signal
        self._cached_signal = signal.copy()
        self._cached_num_samples = num_samples
        
        return signal
    
    def _add_awgn(self, signal: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Add Additive White Gaussian Noise to signal.
        
        Args:
            signal: Clean input signal
            
        Returns:
            Signal with added noise at specified SNR
        """
        signal_power = np.mean(signal ** 2)
        snr_linear = 10 ** (self.snr_db / 10)
        noise_power = signal_power / snr_linear
        noise_std = np.sqrt(noise_power)
        
        noise = noise_std * np.random.randn(*signal.shape)
        return signal + noise
    
    def clear_cache(self) -> None:
        """Clear cached signal."""
        self._cached_signal = None
        self._cached_num_samples = None
    
    def __repr__(self) -> str:
        return (
            f"SignalGenerator(f1={self.fundamental_freq}Hz, "
            f"fs={self.sampling_freq}Hz, noise={self.add_noise})"
        )
