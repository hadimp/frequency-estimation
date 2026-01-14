from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SignalConfig:
    fundamental_freq: int = 1000      # f₁: Fundamental frequency (Hz)
    sampling_freq: int = 8000         # fs: Sampling frequency (Hz)
    num_samples: int = 400            # N: Number of samples
    add_noise: bool = False           # Flag to add Gaussian noise
    snr_db: float = 18.0              # SNR in dB (if noise enabled)
    # Harmonic amplitudes: x(n) = A₁·sin(ω₀n) + A₂·cos(2ω₀n) + A₃·cos(3ω₀n)
    harmonic_amplitude_1: float = 1.0    # A₁: Fundamental amplitude
    harmonic_amplitude_2: float = 0.5   # A₂: 2nd harmonic amplitude
    harmonic_amplitude_3: float = -0.25 # A₃: 3rd harmonic amplitude


@dataclass
class FilterConfig:
    num_subfilters: int = 3           # M: Number of harmonic subfilters
    pole_radius: float = 0.95         # r: Pole radius (controls bandwidth)


@dataclass
class LMSConfig:
    step_size: float = 0.0001         # μ: Step size for gradient descent
    num_theta_points: int = 1400      # Resolution for initial theta search


@dataclass
class OutputConfig:
    directory: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent / "output")
    save_figures: bool = True         # Save figures to disk
    save_results: bool = True         # Save results to file
    figure_format: str = "png"        # Output format: 'png', 'eps', 'pdf'

    def __post_init__(self):
        self.directory = Path(self.directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    signal: SignalConfig = field(default_factory=SignalConfig)
    filter: FilterConfig = field(default_factory=FilterConfig)
    lms: LMSConfig = field(default_factory=LMSConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def display(self) -> None:
        print("\n" + "=" * 55)
        print("  ADAPTIVE FREQUENCY ESTIMATION")
        print("=" * 55)
        print("Signal Parameters:")
        print(f"  Fundamental frequency: {self.signal.fundamental_freq} Hz")
        print(f"  Sampling frequency:    {self.signal.sampling_freq} Hz")
        print(f"  Number of samples:     {self.signal.num_samples}")
        print(f"  Harmonic amplitudes:  A₁={self.signal.harmonic_amplitude_1}, "
              f"A₂={self.signal.harmonic_amplitude_2}, A₃={self.signal.harmonic_amplitude_3}")
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
