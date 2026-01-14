# Frequency Estimation - Python Implementation

A Python implementation of an adaptive IIR filter for frequency estimation and tracking.



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

