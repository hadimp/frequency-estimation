"""
Gradient computation for LMS algorithm.

This module implements the gradient β_M(n) = ∂y_M(n)/∂θ
used in the LMS update rule.
"""

import numpy as np
from numpy.typing import NDArray

from ..config import Config


def compute_gradient(
    theta: float,
    y: NDArray[np.float64],
    cfg: Config
) -> NDArray[np.float64]:
    """
    Compute gradient β_M(n) = ∂y_M(n)/∂θ for LMS update.
    
    Computes gradient recursively through filter stages. Used in LMS:
    θ(n+1) = θ(n) - 2μ·y_M(n)·β_M(n)
    
    Args:
        theta: Current frequency estimate (radians)
        y: Filter outputs from compute_filter_output() (M+1 × N+1)
        cfg: Configuration object
        
    Returns:
        Gradient values β_M(n) (1D array of length N)
        
    Example:
        >>> cfg = Config()
        >>> y = compute_filter_output(0.785, cfg)
        >>> beta = compute_gradient(0.785, y, cfg)
        >>> beta.shape
        (400,)
    """
    # Extract parameters
    num_subfilters = cfg.filter.num_subfilters
    pole_radius = cfg.filter.pole_radius
    num_samples = cfg.signal.num_samples
    
    # Initialize beta matrix
    # beta[m, n] stores the gradient at stage m, sample n
    beta_matrix = np.zeros((num_subfilters, num_samples))
    
    # Compute gradient recursively through filter stages
    for stage in range(1, num_subfilters):
        harmonic_idx = stage
        
        # Precompute trigonometric terms for efficiency
        cos_term = np.cos(harmonic_idx * theta)
        sin_term = np.sin(harmonic_idx * theta)
        
        for n in range(num_samples):
            if n == 0:
                # Initial condition: inherit from previous stage
                beta_matrix[stage, 0] = beta_matrix[stage - 1, 0]
                
            elif n == 1:
                # Second sample: partial recursion (n-2 terms are zero)
                beta_matrix[stage, 1] = (
                    beta_matrix[stage - 1, 1]
                    - 2 * cos_term * beta_matrix[stage - 1, 0]
                    + 2 * harmonic_idx * sin_term * y[stage - 1, 0]
                    + 2 * pole_radius * cos_term * beta_matrix[stage, 0]
                    - 2 * pole_radius * harmonic_idx * sin_term * y[stage, 0]
                )
                
            else:
                # Full recursion for n >= 2
                beta_matrix[stage, n] = (
                    beta_matrix[stage - 1, n]
                    - 2 * cos_term * beta_matrix[stage - 1, n - 1]
                    + 2 * harmonic_idx * sin_term * y[stage - 1, n - 1]
                    + beta_matrix[stage - 1, n - 2]
                    + 2 * pole_radius * cos_term * beta_matrix[stage, n - 1]
                    - (pole_radius ** 2) * beta_matrix[stage, n - 2]
                    - 2 * pole_radius * harmonic_idx * sin_term * y[stage, n - 1]
                )
    
    # Return gradient at final stage
    return beta_matrix[num_subfilters - 1, :]
