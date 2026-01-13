import numpy as np
from numpy.typing import NDArray
from typing import Optional

from .notch_filter import NotchFilter


class CascadedFilterBank:
    
    def __init__(self, num_stages: int, pole_radius: float = 0.95):
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
        num_samples = len(signal)
        outputs = np.zeros((self.num_stages + 1, num_samples))
        outputs[0, :] = signal
        
        for i, notch in enumerate(self.filters):
            outputs[i + 1, :] = notch.filter(outputs[i, :], theta)
        
        self._last_outputs = outputs
        return outputs
    
    def frequency_response(
        self, 
        theta: float, 
        omega: NDArray[np.float64],
        normalize: bool = True
    ) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
        num_freq_points = len(omega)
        H_stages = np.zeros((self.num_stages + 1, num_freq_points), dtype=complex)
        H_total = np.ones(num_freq_points, dtype=complex)
        
        # Stage 0 is the input (all ones)
        H_stages[0, :] = 1.0
        
        ref_idx = num_freq_points // 3  # Reference point for normalization
        
        for i, notch in enumerate(self.filters):
            H = notch.frequency_response(theta, omega)
            
            if normalize:
                H = H / np.abs(H[ref_idx])
            
            # Store at index i+1 since index 0 is input
            H_stages[i + 1, :] = H
            H_total = H_total * H
        
        if normalize:
            H_total = H_total / np.abs(H_total[ref_idx])
        
        return H_total, H_stages
    
    @property
    def last_outputs(self) -> Optional[NDArray[np.float64]]:
        return self._last_outputs
    
    @property
    def final_output(self) -> Optional[NDArray[np.float64]]:
        if self._last_outputs is not None:
            return self._last_outputs[-1, :]
        return None
    
    def __repr__(self) -> str:
        return f"CascadedFilterBank(stages={self.num_stages}, r={self.pole_radius})"
    
    def __len__(self) -> int:
        return self.num_stages
