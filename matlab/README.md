# Frequency Estimation - MATLAB/Octave Implementation

A MATLAB/Octave implementation of an adaptive IIR filter for frequency estimation and tracking.

## Quick Start

```matlab
% Navigate to the matlab/src directory
cd matlab/src

% Run startup to set up paths
startup

% Run with default configuration
results = run_frequency_estimation();
```

## Structure

```
matlab/
└── src/
    ├── config/              # Configuration management
    │   └── config.m
    ├── core/                # Core algorithm functions
    │   ├── compute_filter_output.m
    │   ├── compute_frequency_response.m
    │   ├── compute_gradient.m
    │   ├── compute_mse.m
    │   ├── find_initial_theta.m
    │   └── run_lms_algorithm.m
    ├── utils/               # Utility functions
    │   ├── add_awgn.m
    │   ├── freq_to_theta.m
    │   ├── generate_test_signal.m
    │   ├── mag_to_db.m
    │   ├── save_results.m
    │   └── theta_to_freq.m
    ├── visualization/       # Plotting functions
    │   ├── plot_filter_signals.m
    │   ├── plot_frequency_response.m
    │   ├── plot_frequency_tracking.m
    │   └── plot_mse_analysis.m
    ├── run_frequency_estimation.m
    └── startup.m
```

## Configuration

All parameters are configured through the `config()` function:

```matlab
% Get default configuration
cfg = config();

% Modify parameters
cfg.signal.fundamental_freq = 500;  % Hz
cfg.signal.add_noise = true;
cfg.signal.snr_db = 20;             % dB

% Run with custom configuration
results = run_frequency_estimation(cfg);
```

### Available Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cfg.signal.fundamental_freq` | 1000 | Fundamental frequency f₁ (Hz) |
| `cfg.signal.sampling_freq` | 8000 | Sampling frequency fs (Hz) |
| `cfg.signal.num_samples` | 400 | Number of samples N |
| `cfg.signal.add_noise` | false | Add Gaussian noise flag |
| `cfg.signal.snr_db` | 18 | SNR in dB (if noise enabled) |
| `cfg.filter.num_subfilters` | 3 | Number of harmonic subfilters M |
| `cfg.filter.pole_radius` | 0.95 | Pole radius r (0 < r < 1) |
| `cfg.lms.step_size` | 0.0001 | Step size μ |
| `cfg.lms.num_theta_points` | 1400 | Resolution for theta search |

## Compatibility

- MATLAB R2019b or later
- GNU Octave 6.0 or later

## License

MIT License
