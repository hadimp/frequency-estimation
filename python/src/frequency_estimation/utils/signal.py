import numpy as np
from numpy.typing import NDArray


def add_awgn(
    signal: NDArray[np.float64],
    snr_db: float
) -> NDArray[np.float64]:
    # Calculate signal power
    signal_power = np.mean(signal ** 2)
    
    # Convert SNR from dB to linear scale
    snr_linear = 10 ** (snr_db / 10)
    
    # Calculate noise power and standard deviation
    noise_power = signal_power / snr_linear
    noise_std = np.sqrt(noise_power)
    
    # Generate and add noise
    noise = noise_std * np.random.randn(*signal.shape)
    
    return signal + noise
