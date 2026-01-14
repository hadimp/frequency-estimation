import numpy as np
from numpy.typing import NDArray
from scipy.signal import lfilter, freqz
from dataclasses import dataclass


@dataclass
class NotchFilter:
    harmonic_index: int
    pole_radius: float = 0.95
    
    def get_coefficients(self, theta: float) -> tuple[list[float], list[float]]:
        m = self.harmonic_index
        r = self.pole_radius
        
        cos_term = np.cos(m * theta)
        b = [1.0, -2.0 * cos_term, 1.0]
        a = [1.0, -2.0 * r * cos_term, r ** 2]
        
        return b, a
    
    def filter(self, signal: NDArray[np.float64], theta: float) -> NDArray[np.float64]:
        b, a = self.get_coefficients(theta)
        return lfilter(b, a, signal)
    
    def frequency_response(
        self, 
        theta: float, 
        omega: NDArray[np.float64]
    ) -> NDArray[np.complex128]:
        b, a = self.get_coefficients(theta)
        _, H = freqz(b, a, worN=omega, fs=2*np.pi)
        return H
    
    def __repr__(self) -> str:
        return f"NotchFilter(m={self.harmonic_index}, r={self.pole_radius})"
