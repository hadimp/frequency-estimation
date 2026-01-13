# Frequency Estimation - Python Implementation

A Python implementation of an adaptive IIR filter for frequency estimation and tracking.

## Installation

```bash
# From the python directory
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

## Quick Start

### OOP Interface (Recommended)

```python
from frequency_estimation import FrequencyEstimator, Config, ResultsPlotter

# Run with default configuration
estimator = FrequencyEstimator()
result = estimator.estimate()
print(f"Estimated frequency: {result.final_freq:.2f} Hz")

# Visualize results
plotter = ResultsPlotter(result)
plotter.plot_all()

# Custom configuration
cfg = Config()
cfg.signal.fundamental_freq = 500
cfg.signal.add_noise = True
estimator = FrequencyEstimator(cfg)
result = estimator.estimate()
```

### Legacy Functional Interface

```python
from frequency_estimation import run_frequency_estimation, Config

results = run_frequency_estimation()
print(f"Estimated frequency: {results['final_freq']:.2f} Hz")
```

## Command Line Interface

```bash
# Run with defaults
frequency-estimation

# Run with custom frequency
frequency-estimation --freq 500

# Run without display (batch mode)
frequency-estimation --no-display

# Don't save figures/results
frequency-estimation --no-save
```

## Package Structure

```
python/src/frequency_estimation/
├── __init__.py              # Package exports
├── config.py                # Configuration dataclass
├── estimator.py             # FrequencyEstimator + EstimationResult
├── filters/                 # Filter classes
│   ├── notch_filter.py      # NotchFilter class
│   └── filter_bank.py       # CascadedFilterBank class
├── signal/                  # Signal generation
│   └── generator.py         # SignalGenerator class
├── visualization/           # Plotting
│   ├── plots.py             # Legacy functional plots
│   └── plotter.py           # ResultsPlotter class
├── core/                    # Legacy functional modules
└── utils/                   # Utility functions
```

## API Reference

### Classes

- `FrequencyEstimator`: Main estimator class
- `EstimationResult`: Results container with computed properties
- `NotchFilter`: Single IIR notch filter
- `CascadedFilterBank`: M-stage filter cascade
- `SignalGenerator`: Harmonic test signal generator
- `ResultsPlotter`: Visualization class
- `Config`: Configuration dataclass

### Configuration

```python
from frequency_estimation import Config

cfg = Config()

# Signal parameters
cfg.signal.fundamental_freq = 1000  # Hz
cfg.signal.sampling_freq = 8000     # Hz
cfg.signal.num_samples = 400
cfg.signal.add_noise = False
cfg.signal.snr_db = 18              # dB

# Filter parameters
cfg.filter.num_subfilters = 3
cfg.filter.pole_radius = 0.95

# LMS parameters
cfg.lms.step_size = 0.0001
cfg.lms.num_theta_points = 1400

# Output parameters
cfg.output.save_figures = True
cfg.output.save_results = True
cfg.output.figure_format = 'png'
```

## License

MIT License
