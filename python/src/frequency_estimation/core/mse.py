"""
Mean Squared Error computation.

This module implements MSE computation for the filter bank outputs.
"""

import numpy as np
from numpy.typing import NDArray

from ..config import Config


def compute_mse(
    y: NDArray[np.float64],
    cfg: Config
) -> tuple[float, float]:
    """
    Compute Mean Squared Error of filter bank outputs.
    
    MSE = (1/N) Σ y_M(n)². When θ matches true frequency, MSE → 0.
    
    Args:
        y: Filter outputs (M+1 × N+1)
        cfg: Configuration object
        
    Returns:
        Tuple of (mse_total, mse_first):
        - mse_total: MSE of final filter stage
        - mse_first: MSE of first filter stage
        
    Example:
        >>> cfg = Config()
        >>> y = compute_filter_output(0.785, cfg)
        >>> mse_total, mse_first = compute_mse(y, cfg)
    """
    # Extract parameters
    num_samples = cfg.signal.num_samples + 1
    total_stages = cfg.filter.num_subfilters + 1
    
    # Compute MSE of final stage output
    # y[total_stages-1, :] contains the output after all M notch filters
    final_output = y[total_stages - 1, :]
    mse_total = np.sum(final_output ** 2) / num_samples
    
    # Compute MSE of first stage output
    # y[1, :] contains the output after just the first notch filter
    # This is useful for coarse frequency estimation
    first_output = y[1, :]
    mse_first = np.sum(first_output ** 2) / num_samples
    
    return mse_total, mse_first
