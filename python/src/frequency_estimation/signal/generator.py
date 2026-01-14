import numpy as np
from numpy.typing import NDArray

from ..config import SignalConfig
from ..utils import add_awgn


class SignalGenerator:
    
    def __init__(self, config: SignalConfig):
        self.config = config
        self._validate_config()
    
    @property
    def omega_0(self) -> float:
        return 2 * np.pi * self.config.fundamental_freq / self.config.sampling_freq
    
    def generate(self, num_samples: int) -> NDArray[np.float64]:
        # Generate sample indices (1-indexed to match MATLAB)
        n = np.arange(1, num_samples + 1)
        omega_0 = self.omega_0
        
        # Generate signal components
        fundamental = self.config.harmonic_amplitude_1 * np.sin(omega_0 * n)
        second_harmonic = self.config.harmonic_amplitude_2 * np.cos(2 * omega_0 * n)
        third_harmonic = self.config.harmonic_amplitude_3 * np.cos(3 * omega_0 * n)
        
        signal = fundamental + second_harmonic + third_harmonic
        
        # Add noise if requested
        if self.config.add_noise:
            signal = add_awgn(signal, self.config.snr_db)
        
        return signal
    
    def _validate_config(self) -> None:
        if self.config.fundamental_freq <= 0:
            raise ValueError("Fundamental frequency must be positive")
        if self.config.sampling_freq <= 0:
            raise ValueError("Sampling frequency must be positive")
        if self.config.fundamental_freq >= self.config.sampling_freq / 2:
            raise ValueError("Fundamental frequency must be below Nyquist")
    
    def __repr__(self) -> str:
        return (
            f"SignalGenerator(f1={self.config.fundamental_freq}Hz, "
            f"fs={self.config.sampling_freq}Hz, noise={self.config.add_noise})"
        )
