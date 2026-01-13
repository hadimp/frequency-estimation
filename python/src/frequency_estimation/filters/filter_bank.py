"""
Cascaded notch filter bank implementation.

This module provides the CascadedFilterBank class for processing
signals through multiple notch filter stages.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Optional

from .notch_filter import NotchFilter


class CascadedFilterBank:
    """
    Cascaded notch filter bank for harmonic signal processing.
    
    Processes signal through M cascaded IIR notch filters, each tuned
    to reject the m-th harmonic (m = 1, 2, ..., M).
    
    Attributes:
        num_stages: Number of filter stages M
        pole_radius: Pole radius r for all filters
        filters: List of NotchFilter instances
        
    Example:
        >>> bank = CascadedFilterBank(num_stages=3, pole_radius=0.95)
        >>> outputs = bank.process(signal, theta=0.785)
        >>> final_output = outputs[-1, :]  # Output after all stages
    """
    
    def __init__(self, num_stages: int, pole_radius: float = 0.95):
        """
        Initialize cascaded filter bank.
        
        Args:
            num_stages: Number of notch filter stages M
            pole_radius: Pole radius r (0 < r < 1)
        """
        self.num_stages = num_stages
        self.pole_radius = pole_radius
        self.filters = [
            NotchFilter(harmonic_index=m, pole_radius=pole_radius)
            for m in range(1, num_stages + 1)
        ]
        self._last_outputs: Optional[NDArray[np.float64]] = None
    
    def process(
        self, 
        signal: NDArray[np.float64], 
        theta: float
    ) -> NDArray[np.float64]:
        """
        Process signal through all filter stages.
        
        Args:
            signal: Input signal array
            theta: Normalized frequency θ = 2πf₁/fs (radians)
            
        Returns:
            Output matrix (num_stages+1 × num_samples):
            - Row 0: input signal
            - Row m: output after stage m (m = 1, ..., num_stages)
        """
        num_samples = len(signal)
        outputs = np.zeros((self.num_stages + 1, num_samples))
        outputs[0, :] = signal
        
        for i, notch in enumerate(self.filters):
            outputs[i + 1, :] = notch.filter(outputs[i, :], theta)
        
        self._last_outputs = outputs
        return outputs
    
    @property
    def last_outputs(self) -> Optional[NDArray[np.float64]]:
        """Get outputs from the last process() call."""
        return self._last_outputs
    
    @property
    def final_output(self) -> Optional[NDArray[np.float64]]:
        """Get final stage output from the last process() call."""
        if self._last_outputs is not None:
            return self._last_outputs[-1, :]
        return None
    
    def compute_mse(
        self, 
        signal: NDArray[np.float64], 
        theta: float
    ) -> tuple[float, float]:
        """
        Compute Mean Squared Error of filter bank output.
        
        MSE = (1/N) Σ y_M(n)². When θ matches true frequency, MSE → 0.
        
        Args:
            signal: Input signal array
            theta: Normalized frequency (radians)
            
        Returns:
            Tuple of (mse_total, mse_first):
            - mse_total: MSE of final stage output
            - mse_first: MSE of first stage output
        """
        outputs = self.process(signal, theta)
        num_samples = outputs.shape[1]
        
        mse_total = np.sum(outputs[-1, :] ** 2) / num_samples
        mse_first = np.sum(outputs[1, :] ** 2) / num_samples
        
        return mse_total, mse_first
    
    def frequency_response(
        self, 
        theta: float, 
        omega: NDArray[np.float64],
        normalize: bool = True
    ) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
        """
        Compute frequency response of filter bank.
        
        Args:
            theta: Normalized frequency (radians)
            omega: Frequency points for evaluation
            normalize: Whether to normalize responses
            
        Returns:
            Tuple of (H_total, H_stages):
            - H_total: Overall cascade response
            - H_stages: Individual stage responses (num_stages+1 × len(omega))
        """
        num_freq_points = len(omega)
        H_stages = np.zeros((self.num_stages + 1, num_freq_points), dtype=complex)
        H_total = np.ones(num_freq_points, dtype=complex)
        
        ref_idx = num_freq_points // 3  # Reference point for normalization
        
        for i, notch in enumerate(self.filters):
            H = notch.frequency_response(theta, omega)
            
            if normalize:
                H = H / np.abs(H[ref_idx])
            
            H_stages[i, :] = H
            H_total = H_total * H
        
        if normalize:
            H_total = H_total / np.abs(H_total[ref_idx])
        
        return H_total, H_stages
    
    def __repr__(self) -> str:
        return f"CascadedFilterBank(stages={self.num_stages}, r={self.pole_radius})"
    
    def __len__(self) -> int:
        return self.num_stages
