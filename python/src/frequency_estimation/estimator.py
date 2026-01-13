"""
Main frequency estimator class.

This module provides the FrequencyEstimator class that orchestrates
the complete LMS-based frequency estimation algorithm.
"""

import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from typing import Optional
import warnings

from .config import Config
from .filters import CascadedFilterBank
from .signal import SignalGenerator
from .utils import theta_to_freq


@dataclass
class EstimationResult:
    """
    Results from frequency estimation.
    
    Contains all outputs from the estimation process including
    initial estimates, final converged values, and intermediate data.
    
    Attributes:
        initial_theta: Initial frequency estimate (radians)
        final_theta: Final converged frequency estimate (radians)
        theta_history: History of θ estimates during LMS iterations
        mse_values: MSE values over theta search range
        mse_first_values: First-stage MSE values
        theta_range: Theta values searched during initial estimation
        filter_output: Final filter bank output matrix
        config: Configuration used for estimation
    """
    initial_theta: float
    final_theta: float
    theta_history: NDArray[np.float64]
    mse_values: NDArray[np.float64]
    mse_first_values: NDArray[np.float64]
    theta_range: NDArray[np.float64]
    filter_output: NDArray[np.float64]
    config: Config
    
    @property
    def sampling_freq(self) -> float:
        """Sampling frequency from config."""
        return self.config.signal.sampling_freq
    
    @property
    def true_freq(self) -> float:
        """True fundamental frequency from config."""
        return self.config.signal.fundamental_freq
    
    @property
    def initial_freq(self) -> float:
        """Initial frequency estimate in Hz."""
        return theta_to_freq(self.initial_theta, self.sampling_freq)
    
    @property
    def final_freq(self) -> float:
        """Final frequency estimate in Hz."""
        return theta_to_freq(self.final_theta, self.sampling_freq)
    
    @property
    def freq_history(self) -> NDArray[np.float64]:
        """Frequency history in Hz."""
        return theta_to_freq(self.theta_history, self.sampling_freq)
    
    @property
    def error_hz(self) -> float:
        """Absolute estimation error in Hz."""
        return abs(self.final_freq - self.true_freq)
    
    @property
    def error_percent(self) -> float:
        """Relative estimation error as percentage."""
        return 100 * self.error_hz / self.true_freq
    
    def summary(self) -> str:
        """Generate summary string."""
        return (
            f"FrequencyEstimation Results:\n"
            f"  True frequency:      {self.true_freq:.2f} Hz\n"
            f"  Initial estimate:    {self.initial_freq:.2f} Hz\n"
            f"  Final estimate:      {self.final_freq:.2f} Hz\n"
            f"  Error:               {self.error_hz:.4f} Hz ({self.error_percent:.4f}%)"
        )
    
    def __repr__(self) -> str:
        return f"EstimationResult(final_freq={self.final_freq:.2f}Hz, error={self.error_percent:.4f}%)"


class FrequencyEstimator:
    """
    Adaptive frequency estimator using LMS algorithm.
    
    Implements the algorithm from:
    Li Tan and Jean Jiang, "Novel Adaptive IIR Filter for Frequency
    Estimation and Tracking", IEEE Signal Processing Magazine, 2009.
    
    The algorithm operates in phases:
    1. Initial frequency search via MSE minimization
    2. LMS-based frequency tracking
    3. Final filter output computation
    
    Attributes:
        config: Configuration parameters
        filter_bank: Cascaded notch filter bank
        signal_generator: Test signal generator
        
    Example:
        >>> estimator = FrequencyEstimator()
        >>> result = estimator.estimate()
        >>> print(f"Estimated: {result.final_freq:.2f} Hz")
        
        >>> # With custom configuration
        >>> from frequency_estimation import Config
        >>> cfg = Config()
        >>> cfg.signal.fundamental_freq = 500
        >>> estimator = FrequencyEstimator(cfg)
        >>> result = estimator.estimate()
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize frequency estimator.
        
        Args:
            config: Configuration object (uses defaults if None)
        """
        self.config = config if config is not None else Config()
        
        # Initialize components
        self.filter_bank = CascadedFilterBank(
            num_stages=self.config.filter.num_subfilters,
            pole_radius=self.config.filter.pole_radius
        )
        
        self.signal_generator = SignalGenerator(
            fundamental_freq=self.config.signal.fundamental_freq,
            sampling_freq=self.config.signal.sampling_freq,
            add_noise=self.config.signal.add_noise,
            snr_db=self.config.signal.snr_db
        )
    
    def generate_signal(self, num_samples: Optional[int] = None) -> NDArray[np.float64]:
        """
        Generate test signal.
        
        Args:
            num_samples: Number of samples (uses config default if None)
            
        Returns:
            Generated signal array
        """
        if num_samples is None:
            num_samples = self.config.signal.num_samples + 1
        return self.signal_generator.generate(num_samples)
    
    def find_initial_theta(
        self
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """
        Find initial frequency estimate via MSE minimization.
        
        Searches θ ∈ [0, π/M] to find initial estimate within capture range.
        
        Returns:
            Tuple of (initial_theta, mse_values, mse_first_values, theta_range)
        """
        num_points = self.config.lms.num_theta_points
        num_subfilters = self.config.filter.num_subfilters
        
        # Define search range: θ ∈ [0, π/M]
        theta_range = np.linspace(0, np.pi / num_subfilters, num_points)
        
        # Initialize MSE arrays
        mse_values = np.zeros(num_points)
        mse_first_values = np.zeros(num_points)
        running_average = 0.0
        
        # Generate signal for MSE computation
        signal = self.generate_signal()
        
        # Compute MSE for each theta value
        for k in range(num_points):
            theta = theta_range[k]
            mse_values[k], mse_first_values[k] = self.filter_bank.compute_mse(signal, theta)
            running_average += mse_values[k] / num_points
        
        # Find global minimum
        min_mse = np.min(mse_values)
        
        # Identify capture range
        tolerance_avg = 0.0001
        tolerance_min = 0.2
        
        in_capture_range = (
            (mse_first_values - running_average < tolerance_avg) &
            (mse_values - running_average < tolerance_avg) &
            (mse_values - min_mse < tolerance_min)
        )
        
        capture_thetas = theta_range[in_capture_range]
        
        # Return initial estimate
        if len(capture_thetas) == 0:
            min_idx = np.argmin(mse_values)
            initial_theta = theta_range[min_idx]
            warnings.warn("Capture range not found. Using minimum MSE point.")
        else:
            initial_theta = capture_thetas[0]
        
        return initial_theta, mse_values, mse_first_values, theta_range
    
    def run_lms(
        self, 
        initial_theta: float
    ) -> tuple[float, NDArray[np.float64]]:
        """
        Run LMS algorithm for frequency tracking.
        
        LMS update: θ(n+1) = θ(n) - 2μ·y_M(n)·β_M(n)
        
        Args:
            initial_theta: Initial frequency estimate (radians)
            
        Returns:
            Tuple of (theta_final, theta_history)
        """
        step_size = self.config.lms.step_size
        num_samples = self.config.signal.num_samples
        num_subfilters = self.config.filter.num_subfilters
        
        theta_current = initial_theta
        theta_history = np.zeros(num_samples)
        
        # LMS iteration loop
        for iteration in range(num_samples):
            # Compute filter bank output
            signal = self.generate_signal()
            y = self.filter_bank.process(signal, theta_current)
            
            # Compute gradient β_M(n)
            beta = self._compute_gradient(theta_current, y)
            beta_n = beta[iteration]
            
            # Get current output sample y_M(n)
            y_n = y[num_subfilters, iteration]
            
            # LMS update
            theta_current = theta_current - (2 * step_size * y_n * beta_n)
            theta_history[iteration] = theta_current
        
        return theta_current, theta_history
    
    def _compute_gradient(
        self, 
        theta: float, 
        y: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """
        Compute gradient β_M(n) = ∂y_M(n)/∂θ for LMS update.
        
        Args:
            theta: Current frequency estimate (radians)
            y: Filter outputs (M+1 × N+1)
            
        Returns:
            Gradient values β_M(n)
        """
        num_subfilters = self.config.filter.num_subfilters
        pole_radius = self.config.filter.pole_radius
        num_samples = self.config.signal.num_samples
        
        # Initialize beta matrix
        beta_matrix = np.zeros((num_subfilters, num_samples))
        
        # Compute gradient recursively through filter stages
        for stage in range(1, num_subfilters):
            harmonic_idx = stage
            
            cos_term = np.cos(harmonic_idx * theta)
            sin_term = np.sin(harmonic_idx * theta)
            
            for n in range(num_samples):
                if n == 0:
                    beta_matrix[stage, 0] = beta_matrix[stage - 1, 0]
                elif n == 1:
                    beta_matrix[stage, 1] = (
                        beta_matrix[stage - 1, 1]
                        - 2 * cos_term * beta_matrix[stage - 1, 0]
                        + 2 * harmonic_idx * sin_term * y[stage - 1, 0]
                        + 2 * pole_radius * cos_term * beta_matrix[stage, 0]
                        - 2 * pole_radius * harmonic_idx * sin_term * y[stage, 0]
                    )
                else:
                    beta_matrix[stage, n] = (
                        beta_matrix[stage - 1, n]
                        - 2 * cos_term * beta_matrix[stage - 1, n - 1]
                        + 2 * harmonic_idx * sin_term * y[stage - 1, n - 1]
                        + beta_matrix[stage - 1, n - 2]
                        + 2 * pole_radius * cos_term * beta_matrix[stage, n - 1]
                        - (pole_radius ** 2) * beta_matrix[stage, n - 2]
                        - 2 * pole_radius * harmonic_idx * sin_term * y[stage, n - 1]
                    )
        
        return beta_matrix[num_subfilters - 1, :]
    
    def estimate(self, verbose: bool = True) -> EstimationResult:
        """
        Run complete frequency estimation pipeline.
        
        Args:
            verbose: Whether to print progress messages
            
        Returns:
            EstimationResult containing all outputs
        """
        if verbose:
            self.config.display()
        
        # Phase 1: Initial frequency search
        if verbose:
            print("Phase 1: Searching for initial frequency estimate...")
        
        initial_theta, mse_values, mse_first_values, theta_range = self.find_initial_theta()
        
        if verbose:
            initial_freq = theta_to_freq(initial_theta, self.config.signal.sampling_freq)
            print(f"  Initial estimate: {initial_freq:.2f} Hz (θ = {initial_theta:.4f} rad)")
        
        # Phase 2: LMS tracking
        if verbose:
            print("\nPhase 2: Running LMS algorithm for frequency tracking...")
        
        final_theta, theta_history = self.run_lms(initial_theta)
        
        if verbose:
            final_freq = theta_to_freq(final_theta, self.config.signal.sampling_freq)
            true_freq = self.config.signal.fundamental_freq
            error_hz = abs(final_freq - true_freq)
            error_percent = 100 * error_hz / true_freq
            print(f"  Final estimate:   {final_freq:.2f} Hz (θ = {final_theta:.4f} rad)")
            print(f"  Estimation error: {error_hz:.2f} Hz ({error_percent:.4f}%)")
        
        # Phase 3: Final filter output
        if verbose:
            print("\nPhase 3: Computing final filter bank output...")
        
        signal = self.generate_signal()
        filter_output = self.filter_bank.process(signal, final_theta)
        
        # Create result object
        result = EstimationResult(
            initial_theta=initial_theta,
            final_theta=final_theta,
            theta_history=theta_history,
            mse_values=mse_values,
            mse_first_values=mse_first_values,
            theta_range=theta_range,
            filter_output=filter_output,
            config=self.config
        )
        
        if verbose:
            print("\n" + "=" * 55)
            print("  RESULTS SUMMARY")
            print("=" * 55)
            print(f"  True frequency:      {result.true_freq} Hz")
            print(f"  Estimated frequency: {result.final_freq:.2f} Hz")
            print(f"  Estimation error:    {result.error_percent:.4f}%")
            print("=" * 55)
        
        return result
    
    def __repr__(self) -> str:
        return (
            f"FrequencyEstimator(f1={self.config.signal.fundamental_freq}Hz, "
            f"stages={self.config.filter.num_subfilters})"
        )
