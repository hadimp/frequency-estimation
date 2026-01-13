"""
Configuration management for frequency estimation algorithm.

This module provides the Config dataclass for managing algorithm parameters.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SignalConfig:
    """Signal generation parameters."""
    fundamental_freq: int = 1000      # f₁: Fundamental frequency (Hz)
    sampling_freq: int = 8000         # fs: Sampling frequency (Hz)
    num_samples: int = 400            # N: Number of samples
    add_noise: bool = False           # Flag to add Gaussian noise
    snr_db: float = 18.0              # SNR in dB (if noise enabled)


@dataclass
class FilterConfig:
    """Filter bank parameters."""
    num_subfilters: int = 3           # M: Number of harmonic subfilters
    pole_radius: float = 0.95         # r: Pole radius (controls bandwidth)


@dataclass
class LMSConfig:
    """LMS algorithm parameters."""
    step_size: float = 0.0001         # μ: Step size for gradient descent
    num_theta_points: int = 1400      # Resolution for initial theta search


@dataclass
class OutputConfig:
    """Output configuration."""
    directory: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent / "output")
    save_figures: bool = True         # Save figures to disk
    save_results: bool = True         # Save results to file
    figure_format: str = "png"        # Output format: 'png', 'eps', 'pdf'

    def __post_init__(self):
        self.directory = Path(self.directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """
    Complete configuration for frequency estimation algorithm.
    
    Attributes:
        signal: Signal generation parameters
        filter: Filter bank parameters
        lms: LMS algorithm parameters
        output: Output configuration
        
    Example:
        >>> cfg = Config()
        >>> cfg.signal.fundamental_freq = 500
        >>> cfg.lms.step_size = 0.00005
    """
    signal: SignalConfig = field(default_factory=SignalConfig)
    filter: FilterConfig = field(default_factory=FilterConfig)
    lms: LMSConfig = field(default_factory=LMSConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def display(self) -> None:
        """Display configuration parameters."""
        print("\n" + "=" * 55)
        print("  ADAPTIVE FREQUENCY ESTIMATION")
        print("=" * 55)
        print("Signal Parameters:")
        print(f"  Fundamental frequency: {self.signal.fundamental_freq} Hz")
        print(f"  Sampling frequency:    {self.signal.sampling_freq} Hz")
        print(f"  Number of samples:     {self.signal.num_samples}")
        print(f"  Add noise:             {self.signal.add_noise}")
        if self.signal.add_noise:
            print(f"  SNR:                   {self.signal.snr_db} dB")
        print("\nFilter Parameters:")
        print(f"  Number of subfilters:  {self.filter.num_subfilters}")
        print(f"  Pole radius:           {self.filter.pole_radius:.2f}")
        print("\nLMS Parameters:")
        print(f"  Step size (μ):         {self.lms.step_size:.6f}")
        print(f"  Theta search points:   {self.lms.num_theta_points}")
        print("=" * 55 + "\n")
