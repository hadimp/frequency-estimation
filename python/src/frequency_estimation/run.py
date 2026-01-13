"""
Main entry point for frequency estimation algorithm.

This module provides the main function to run the complete
adaptive frequency estimation pipeline.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Any
import json

import numpy as np

from .config import Config
from .core import (
    find_initial_theta,
    run_lms_algorithm,
    compute_filter_output,
)
from .utils import theta_to_freq
from .visualization import (
    plot_mse_analysis,
    plot_frequency_tracking,
    plot_filter_signals,
    plot_frequency_response,
)


def save_results(results: dict[str, Any], cfg: Config) -> None:
    """
    Save frequency estimation results to files.
    
    Saves results in multiple formats:
    - .npz file: Complete results (NumPy arrays)
    - .txt file: Human-readable summary report
    
    Args:
        results: Results dictionary from run_frequency_estimation()
        cfg: Configuration object
    """
    if not cfg.output.save_results:
        return
    
    output_dir = cfg.output.directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f'frequency_estimation_{timestamp}'
    
    # Save complete results as NPZ file
    npz_file = output_dir / f'{base_name}.npz'
    np.savez(
        npz_file,
        initial_theta=results['initial_theta'],
        initial_freq=results['initial_freq'],
        final_theta=results['final_theta'],
        final_freq=results['final_freq'],
        theta_history=results['theta_history'],
        mse_values=results['mse_values'],
        mse_first_values=results['mse_first_values'],
        theta_range=results['theta_range'],
        filter_output=results['filter_output'],
        error_hz=results['error_hz'],
        error_percent=results['error_percent'],
    )
    print(f'Results saved to: {npz_file}')
    
    # Save human-readable summary as text file
    txt_file = output_dir / f'{base_name}_summary.txt'
    with open(txt_file, 'w') as f:
        f.write('=' * 55 + '\n')
        f.write('  FREQUENCY ESTIMATION RESULTS\n')
        f.write('=' * 55 + '\n')
        f.write(f'Generated: {datetime.now()}\n\n')
        
        # Configuration
        f.write('CONFIGURATION:\n')
        f.write('  Signal Parameters:\n')
        f.write(f'    Fundamental frequency: {cfg.signal.fundamental_freq} Hz\n')
        f.write(f'    Sampling frequency:    {cfg.signal.sampling_freq} Hz\n')
        f.write(f'    Number of samples:     {cfg.signal.num_samples}\n')
        f.write(f'    Add noise:             {cfg.signal.add_noise}\n')
        if cfg.signal.add_noise:
            f.write(f'    SNR:                   {cfg.signal.snr_db} dB\n')
        f.write('  Filter Parameters:\n')
        f.write(f'    Number of subfilters:  {cfg.filter.num_subfilters}\n')
        f.write(f'    Pole radius:           {cfg.filter.pole_radius:.4f}\n')
        f.write('  LMS Parameters:\n')
        f.write(f'    Step size (μ):         {cfg.lms.step_size:.6f}\n')
        f.write(f'    Theta search points:   {cfg.lms.num_theta_points}\n')
        f.write('\n')
        
        # Results
        f.write('RESULTS:\n')
        f.write(f'  True frequency:          {cfg.signal.fundamental_freq} Hz\n')
        f.write(f'  Initial estimate:        {results["initial_freq"]:.4f} Hz (θ = {results["initial_theta"]:.6f} rad)\n')
        f.write(f'  Final estimate:          {results["final_freq"]:.4f} Hz (θ = {results["final_theta"]:.6f} rad)\n')
        f.write(f'  Estimation error:        {results["error_hz"]:.4f} Hz ({results["error_percent"]:.4f}%)\n')
        f.write('\n')
        
        # MSE Statistics
        f.write('MSE STATISTICS:\n')
        f.write(f'  Minimum MSE:             {np.min(results["mse_values"]):.6e}\n')
        f.write(f'  Mean MSE:                {np.mean(results["mse_values"]):.6e}\n')
        f.write(f'  Maximum MSE:             {np.max(results["mse_values"]):.6e}\n')
        f.write(f'  Minimum MSE₁:            {np.min(results["mse_first_values"]):.6e}\n')
        f.write(f'  Mean MSE₁:               {np.mean(results["mse_first_values"]):.6e}\n')
        f.write(f'  Maximum MSE₁:            {np.max(results["mse_first_values"]):.6e}\n')
        f.write('\n')
        
        # Convergence Statistics
        f.write('CONVERGENCE STATISTICS:\n')
        freq_history = theta_to_freq(results['theta_history'], cfg.signal.sampling_freq)
        f.write(f'  Initial frequency:       {freq_history[0]:.4f} Hz\n')
        f.write(f'  Final frequency:         {freq_history[-1]:.4f} Hz\n')
        f.write(f'  Frequency change:        {freq_history[-1] - freq_history[0]:.4f} Hz\n')
        f.write(f'  Convergence iterations:  {len(results["theta_history"])}\n')
        f.write('\n')
        
        # File locations
        f.write('OUTPUT FILES:\n')
        f.write(f'  Results (NPZ):           {npz_file}\n')
        if cfg.output.save_figures:
            f.write(f'  Figures directory:       {output_dir}\n')
        f.write('\n')
        
        f.write('=' * 55 + '\n')
        f.write('End of Report\n')
        f.write('=' * 55 + '\n')
    
    print(f'Summary saved to: {txt_file}')


def run_frequency_estimation(config: Optional[Config] = None) -> dict[str, Any]:
    """
    Run adaptive frequency estimation using LMS algorithm.
    
    Main entry point for the frequency estimation algorithm.
    Implements the four-phase algorithm:
    1. Initial frequency estimation (MSE search)
    2. LMS frequency tracking
    3. Filter output analysis
    4. Frequency response analysis
    
    Args:
        config: Configuration object (uses defaults if None)
        
    Returns:
        Dictionary containing all results:
        - config: Configuration used
        - initial_theta: Initial frequency estimate (radians)
        - initial_freq: Initial frequency estimate (Hz)
        - final_theta: Final converged estimate (radians)
        - final_freq: Final converged estimate (Hz)
        - theta_history: History of θ estimates
        - mse_values: MSE values over theta range
        - mse_first_values: First-stage MSE values
        - theta_range: Theta values searched
        - filter_output: Final filter bank output
        - error_hz: Estimation error (Hz)
        - error_percent: Estimation error (%)
        
    Example:
        >>> from frequency_estimation import run_frequency_estimation, Config
        >>> results = run_frequency_estimation()
        >>> print(f"Estimated frequency: {results['final_freq']:.2f} Hz")
        
        >>> # With custom configuration
        >>> cfg = Config()
        >>> cfg.signal.fundamental_freq = 500
        >>> results = run_frequency_estimation(cfg)
    """
    # Load configuration
    if config is None:
        cfg = Config()
        print('Using default configuration.')
    else:
        cfg = config
        print('Using provided configuration.')
    
    # Display parameters
    cfg.display()
    
    # =========================================================================
    # PHASE 1: INITIAL FREQUENCY ESTIMATION (MSE Search)
    # =========================================================================
    print('Phase 1: Searching for initial frequency estimate...')
    
    initial_theta, mse_values, mse_first_values, theta_range = find_initial_theta(cfg)
    
    initial_freq = theta_to_freq(initial_theta, cfg.signal.sampling_freq)
    print(f'  Initial estimate: {initial_freq:.2f} Hz (θ = {initial_theta:.4f} rad)')
    
    # Plot MSE analysis
    plot_mse_analysis(theta_range, mse_values, mse_first_values, cfg)
    
    # =========================================================================
    # PHASE 2: LMS FREQUENCY TRACKING
    # =========================================================================
    print('\nPhase 2: Running LMS algorithm for frequency tracking...')
    
    theta_final, theta_history = run_lms_algorithm(initial_theta, cfg)
    
    final_freq = theta_to_freq(theta_final, cfg.signal.sampling_freq)
    print(f'  Final estimate:   {final_freq:.2f} Hz (θ = {theta_final:.4f} rad)')
    
    # Calculate estimation error
    true_freq = cfg.signal.fundamental_freq
    error_hz = abs(final_freq - true_freq)
    error_percent = 100 * error_hz / true_freq
    print(f'  Estimation error: {error_hz:.2f} Hz ({error_percent:.4f}%)')
    
    # Plot frequency tracking
    plot_frequency_tracking(theta_history, cfg)
    
    # =========================================================================
    # PHASE 3: COMPUTE FINAL FILTER OUTPUT
    # =========================================================================
    print('\nPhase 3: Computing final filter bank output...')
    
    y_final = compute_filter_output(theta_final, cfg)
    
    # Plot filter signals
    plot_filter_signals(y_final, cfg)
    
    # =========================================================================
    # PHASE 4: FREQUENCY RESPONSE ANALYSIS
    # =========================================================================
    print('\nPhase 4: Analyzing frequency response...')
    
    plot_frequency_response(theta_final, cfg)
    
    # =========================================================================
    # PACKAGE RESULTS
    # =========================================================================
    results = {
        'config': cfg,
        'initial_theta': initial_theta,
        'initial_freq': initial_freq,
        'final_theta': theta_final,
        'final_freq': final_freq,
        'theta_history': theta_history,
        'mse_values': mse_values,
        'mse_first_values': mse_first_values,
        'theta_range': theta_range,
        'filter_output': y_final,
        'error_hz': error_hz,
        'error_percent': error_percent,
    }
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print('\n' + '=' * 55)
    print('  RESULTS SUMMARY')
    print('=' * 55)
    print(f'  True frequency:      {true_freq} Hz')
    print(f'  Estimated frequency: {final_freq:.2f} Hz')
    print(f'  Estimation error:    {error_percent:.4f}%')
    print('=' * 55)
    
    # =========================================================================
    # SAVE RESULTS TO FILE
    # =========================================================================
    if cfg.output.save_results:
        print('\nSaving results to file...')
        save_results(results, cfg)
    
    if cfg.output.save_figures:
        print(f'\nFigures saved to: {cfg.output.directory}')
    
    print('\nFrequency estimation complete.\n')
    
    return results


# CLI entry point
def main():
    """Command-line interface entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Adaptive Frequency Estimation using LMS Algorithm'
    )
    parser.add_argument(
        '--freq', '-f',
        type=int,
        default=1000,
        help='Fundamental frequency in Hz (default: 1000)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save figures and results'
    )
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Do not display figures (useful for batch processing)'
    )
    
    args = parser.parse_args()
    
    # Create configuration
    cfg = Config()
    cfg.signal.fundamental_freq = args.freq
    
    if args.no_save:
        cfg.output.save_figures = False
        cfg.output.save_results = False
    
    # Run algorithm
    import matplotlib
    if args.no_display:
        matplotlib.use('Agg')
    
    results = run_frequency_estimation(cfg)
    
    if not args.no_display:
        import matplotlib.pyplot as plt
        plt.show()
    
    return results


if __name__ == '__main__':
    main()
