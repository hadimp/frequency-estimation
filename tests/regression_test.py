#!/usr/bin/env python3
"""
Regression test to verify MATLAB and Python implementations produce identical results.

This script:
1. Runs the Octave/MATLAB implementation
2. Runs the Python implementation (both OOP and functional)
3. Compares key outputs and verifies they match within tolerance
"""

import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np

# Add Python source to path
PROJECT_ROOT = Path(__file__).parent.parent
MATLAB_SRC = PROJECT_ROOT / "matlab" / "src"
PYTHON_SRC = PROJECT_ROOT / "python" / "src"
sys.path.insert(0, str(PYTHON_SRC))

# Test parameters (must match between implementations)
TEST_CONFIG = {
    "fundamental_freq": 1000,
    "sampling_freq": 8000,
    "num_samples": 400,
    "num_subfilters": 3,
    "pole_radius": 0.95,
    "step_size": 0.0001,
    "num_theta_points": 1400,
}

TOLERANCE = {
    "theta": 1e-4,       # radians
    "freq": 0.1,         # Hz
    "mse": 1e-6,         # MSE values
}


def run_octave():
    """Run Octave implementation and extract results."""
    print("=" * 60)
    print("Running Octave/MATLAB implementation...")
    print("=" * 60)
    
    # Create Octave script to run and export results
    octave_script = f'''
    cd('{MATLAB_SRC}');
    startup;
    
    % Run with specific config (no figures, no save)
    cfg = config();
    cfg.output.save_figures = false;
    cfg.output.save_results = false;
    
    % Run algorithm
    results = run_frequency_estimation(cfg);
    
    % Export key values
    fprintf('\\n=== OCTAVE RESULTS ===\\n');
    fprintf('INITIAL_THETA=%.10f\\n', results.initial_theta);
    fprintf('FINAL_THETA=%.10f\\n', results.final_theta);
    fprintf('INITIAL_FREQ=%.10f\\n', results.initial_freq);
    fprintf('FINAL_FREQ=%.10f\\n', results.final_freq);
    fprintf('ERROR_HZ=%.10f\\n', results.error_hz);
    fprintf('ERROR_PERCENT=%.10f\\n', results.error_percent);
    fprintf('MSE_MIN=%.10e\\n', min(results.mse_values));
    fprintf('MSE_MEAN=%.10e\\n', mean(results.mse_values));
    fprintf('THETA_HISTORY_FIRST=%.10f\\n', results.theta_history(1));
    fprintf('THETA_HISTORY_LAST=%.10f\\n', results.theta_history(end));
    fprintf('=== END OCTAVE RESULTS ===\\n');
    '''
    
    # Run Octave
    result = subprocess.run(
        ["octave", "--no-gui", "--silent", "--eval", octave_script],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        print("Octave STDERR:", result.stderr)
        raise RuntimeError(f"Octave failed with code {result.returncode}")
    
    # Parse results
    output = result.stdout
    print(output)
    
    octave_results = {}
    for line in output.split('\n'):
        if '=' in line and line.startswith(('INITIAL_', 'FINAL_', 'ERROR_', 'MSE_', 'THETA_')):
            key, value = line.strip().split('=')
            octave_results[key] = float(value)
    
    return octave_results


def run_python_oop():
    """Run Python OOP implementation and extract results."""
    print("\n" + "=" * 60)
    print("Running Python OOP implementation (FrequencyEstimator)...")
    print("=" * 60)
    
    import matplotlib
    matplotlib.use('Agg')
    
    from frequency_estimation import FrequencyEstimator, Config
    
    cfg = Config()
    cfg.output.save_figures = False
    cfg.output.save_results = False
    
    estimator = FrequencyEstimator(cfg)
    result = estimator.estimate(verbose=False)
    
    python_results = {
        'INITIAL_THETA': result.initial_theta,
        'FINAL_THETA': result.final_theta,
        'INITIAL_FREQ': result.initial_freq,
        'FINAL_FREQ': result.final_freq,
        'ERROR_HZ': result.error_hz,
        'ERROR_PERCENT': result.error_percent,
        'MSE_MIN': np.min(result.mse_values),
        'MSE_MEAN': np.mean(result.mse_values),
        'THETA_HISTORY_FIRST': result.theta_history[0],
        'THETA_HISTORY_LAST': result.theta_history[-1],
    }
    
    print("\n=== PYTHON OOP RESULTS ===")
    for key, value in python_results.items():
        if 'MSE' in key:
            print(f"{key}={value:.10e}")
        else:
            print(f"{key}={value:.10f}")
    print("=== END PYTHON OOP RESULTS ===")
    
    return python_results


def run_python_functional():
    """Run Python functional implementation and extract results."""
    print("\n" + "=" * 60)
    print("Running Python functional implementation (legacy)...")
    print("=" * 60)
    
    import matplotlib
    matplotlib.use('Agg')
    
    from frequency_estimation import Config
    from frequency_estimation.core import find_initial_theta, run_lms_algorithm
    from frequency_estimation.utils import theta_to_freq
    
    cfg = Config()
    cfg.output.save_figures = False
    cfg.output.save_results = False
    
    # Phase 1: Initial theta search
    initial_theta, mse_values, mse_first_values, theta_range = find_initial_theta(cfg)
    
    # Phase 2: LMS algorithm
    final_theta, theta_history = run_lms_algorithm(initial_theta, cfg)
    
    # Calculate results
    initial_freq = theta_to_freq(initial_theta, cfg.signal.sampling_freq)
    final_freq = theta_to_freq(final_theta, cfg.signal.sampling_freq)
    error_hz = abs(final_freq - cfg.signal.fundamental_freq)
    error_percent = 100 * error_hz / cfg.signal.fundamental_freq
    
    python_results = {
        'INITIAL_THETA': initial_theta,
        'FINAL_THETA': final_theta,
        'INITIAL_FREQ': initial_freq,
        'FINAL_FREQ': final_freq,
        'ERROR_HZ': error_hz,
        'ERROR_PERCENT': error_percent,
        'MSE_MIN': np.min(mse_values),
        'MSE_MEAN': np.mean(mse_values),
        'THETA_HISTORY_FIRST': theta_history[0],
        'THETA_HISTORY_LAST': theta_history[-1],
    }
    
    print("\n=== PYTHON FUNCTIONAL RESULTS ===")
    for key, value in python_results.items():
        if 'MSE' in key:
            print(f"{key}={value:.10e}")
        else:
            print(f"{key}={value:.10f}")
    print("=== END PYTHON FUNCTIONAL RESULTS ===")
    
    return python_results


def compare_results(name1: str, results1: dict, name2: str, results2: dict) -> bool:
    """Compare results and report differences."""
    print(f"\n{'='*60}")
    print(f"COMPARING: {name1} vs {name2}")
    print("=" * 60)
    
    all_passed = True
    
    comparisons = [
        ('INITIAL_THETA', TOLERANCE['theta'], 'Initial theta (rad)'),
        ('FINAL_THETA', TOLERANCE['theta'], 'Final theta (rad)'),
        ('INITIAL_FREQ', TOLERANCE['freq'], 'Initial frequency (Hz)'),
        ('FINAL_FREQ', TOLERANCE['freq'], 'Final frequency (Hz)'),
        ('ERROR_HZ', TOLERANCE['freq'], 'Error (Hz)'),
        ('ERROR_PERCENT', 0.01, 'Error (%)'),
        ('MSE_MIN', TOLERANCE['mse'], 'MSE minimum'),
        ('MSE_MEAN', TOLERANCE['mse'], 'MSE mean'),
        ('THETA_HISTORY_FIRST', TOLERANCE['theta'], 'Theta history (first)'),
        ('THETA_HISTORY_LAST', TOLERANCE['theta'], 'Theta history (last)'),
    ]
    
    print(f"\n{'Metric':<25} {name1[:12]:>15} {name2[:12]:>15} {'Diff':>12} {'Status':>10}")
    print("-" * 77)
    
    for key, tol, label in comparisons:
        val1 = results1.get(key, float('nan'))
        val2 = results2.get(key, float('nan'))
        diff = abs(val1 - val2)
        passed = diff <= tol
        
        status = "✓ PASS" if passed else "✗ FAIL"
        if not passed:
            all_passed = False
        
        if 'MSE' in key:
            print(f"{label:<25} {val1:>15.6e} {val2:>15.6e} {diff:>12.2e} {status:>10}")
        else:
            print(f"{label:<25} {val1:>15.6f} {val2:>15.6f} {diff:>12.6f} {status:>10}")
    
    print("-" * 77)
    
    return all_passed


def main():
    """Run regression test."""
    print("\n" + "=" * 60)
    print("  FREQUENCY ESTIMATION REGRESSION TEST")
    print("  Comparing MATLAB/Octave, Python OOP, and Python Functional")
    print("=" * 60)
    
    try:
        # Run all implementations
        octave_results = run_octave()
        python_oop_results = run_python_oop()
        python_func_results = run_python_functional()
        
        # Compare all pairs
        tests_passed = []
        
        tests_passed.append(compare_results(
            "Octave", octave_results, 
            "Python OOP", python_oop_results
        ))
        
        tests_passed.append(compare_results(
            "Octave", octave_results, 
            "Python Func", python_func_results
        ))
        
        tests_passed.append(compare_results(
            "Python OOP", python_oop_results, 
            "Python Func", python_func_results
        ))
        
        all_passed = all(tests_passed)
        
        print("\n" + "=" * 60)
        if all_passed:
            print("  ✓ ALL REGRESSION TESTS PASSED")
            print("  All implementations produce identical results!")
        else:
            print("  ✗ SOME REGRESSION TESTS FAILED")
            print("  Implementations differ beyond tolerance!")
        print("=" * 60 + "\n")
        
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
