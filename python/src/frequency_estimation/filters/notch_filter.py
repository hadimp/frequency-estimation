"""
Single IIR notch filter implementation.

This module provides the NotchFilter class for rejecting
a specific harmonic frequency.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.signal import lfilter, freqz
from dataclasses import dataclass


@dataclass
class NotchFilter:
    """
    Single IIR notch filter for harmonic rejection.
    
    Transfer function:
    H_m(z) = (1 - 2cos(mθ)z⁻¹ + z⁻²) / (1 - 2r·cos(mθ)z⁻¹ + r²z⁻²)
    
    Attributes:
        harmonic_index: The harmonic number m (1 for fundamental, 2 for 2nd harmonic, etc.)
        pole_radius: Pole radius r controlling filter bandwidth (0 < r < 1)
        
    Example:
        >>> notch = NotchFilter(harmonic_index=1, pole_radius=0.95)
        >>> filtered = notch.filter(signal, theta=0.785)
    """
    harmonic_index: int
    pole_radius: float = 0.95
    
    def get_coefficients(self, theta: float) -> tuple[list[float], list[float]]:
        """
        Get filter coefficients for given theta.
        
        Args:
            theta: Normalized frequency θ = 2πf₁/fs (radians)
            
        Returns:
            Tuple of (b, a) coefficient lists:
            - b: Numerator coefficients [1, -2cos(mθ), 1]
            - a: Denominator coefficients [1, -2r·cos(mθ), r²]
        """
        m = self.harmonic_index
        r = self.pole_radius
        
        cos_term = np.cos(m * theta)
        b = [1.0, -2.0 * cos_term, 1.0]
        a = [1.0, -2.0 * r * cos_term, r ** 2]
        
        return b, a
    
    def filter(self, signal: NDArray[np.float64], theta: float) -> NDArray[np.float64]:
        """
        Apply notch filter to signal.
        
        Args:
            signal: Input signal array
            theta: Normalized frequency (radians)
            
        Returns:
            Filtered signal array
        """
        b, a = self.get_coefficients(theta)
        return lfilter(b, a, signal)
    
    def frequency_response(
        self, 
        theta: float, 
        omega: NDArray[np.float64]
    ) -> NDArray[np.complex128]:
        """
        Compute frequency response H(e^jω).
        
        Args:
            theta: Normalized frequency (radians)
            omega: Frequency points for evaluation
            
        Returns:
            Complex frequency response array
        """
        b, a = self.get_coefficients(theta)
        _, H = freqz(b, a, worN=omega, fs=2*np.pi)
        return H
    
    def __repr__(self) -> str:
        return f"NotchFilter(m={self.harmonic_index}, r={self.pole_radius})"
