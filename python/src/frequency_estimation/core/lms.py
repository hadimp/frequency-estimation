"""
LMS algorithm for frequency tracking.

This module implements the Least Mean Squares (LMS) adaptive
algorithm for frequency estimation and tracking.
"""

import numpy as np
from numpy.typing import NDArray

from ..config import Config
from .filter_output import compute_filter_output
from .gradient import compute_gradient


def run_lms_algorithm(
    initial_theta: float,
    cfg: Config
) -> tuple[float, NDArray[np.float64]]:
    """
    Execute LMS algorithm for frequency estimation.
    
    LMS update: θ(n+1) = θ(n) - 2μ·y_M(n)·β_M(n)
    Minimizes MSE cost function J(θ) = E[y_M²(n)].
    
    Args:
        initial_theta: Initial frequency estimate (radians)
        cfg: Configuration object
        
    Returns:
        Tuple of (theta_final, theta_history):
        - theta_final: Final converged estimate
        - theta_history: History of θ estimates (1D array of length N)
        
    Example:
        >>> cfg = Config()
        >>> initial_theta, _, _, _ = find_initial_theta(cfg)
        >>> theta_final, theta_history = run_lms_algorithm(initial_theta, cfg)
        >>> print(f"Final theta: {theta_final:.4f} rad")
    """
    # Extract parameters
    step_size = cfg.lms.step_size
    num_samples = cfg.signal.num_samples
    num_subfilters = cfg.filter.num_subfilters
    
    # Initialize
    theta_current = initial_theta
    theta_history = np.zeros(num_samples)
    
    # LMS iteration loop
    for iteration in range(num_samples):
        # Compute filter bank output for current theta estimate
        y = compute_filter_output(theta_current, cfg)
        
        # Compute gradient β_M(n)
        beta = compute_gradient(theta_current, y, cfg)
        beta_n = beta[iteration]
        
        # Get current output sample y_M(n)
        y_n = y[num_subfilters, iteration]
        
        # LMS update: θ(n+1) = θ(n) - 2μ · y_M(n) · β_M(n)
        theta_current = theta_current - (2 * step_size * y_n * beta_n)
        
        # Store history
        theta_history[iteration] = theta_current
    
    return theta_current, theta_history
