import numpy as np
from numpy.typing import NDArray


def theta_to_freq(theta: float | NDArray, sampling_freq: float) -> float | NDArray:
    return theta * sampling_freq / (2 * np.pi)


def freq_to_theta(freq: float | NDArray, sampling_freq: float) -> float | NDArray:
    return 2 * np.pi * freq / sampling_freq


def mag_to_db(magnitude: float | NDArray, floor_db: float = -120.0) -> float | NDArray:
    # Add small epsilon to avoid log10(0) = -inf
    eps = 10 ** (floor_db / 20)
    return 20 * np.log10(np.maximum(np.abs(magnitude), eps))
