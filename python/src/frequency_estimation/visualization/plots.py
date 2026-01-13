"""
Plotting functions for frequency estimation visualization.

This module implements all visualization functions for
analyzing and presenting algorithm results.
"""

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path

from ..config import Config
from ..utils import theta_to_freq, mag_to_db
from ..core import compute_frequency_response


def plot_mse_analysis(
    theta_range: NDArray,
    mse_values: NDArray,
    mse_first_values: NDArray,
    cfg: Config
) -> Figure:
    """
    Plot MSE analysis over frequency range.
    
    Plots MSE(θ), MSE₁(θ), and average MSE to visualize cost function landscape.
    
    Args:
        theta_range: Theta values (radians)
        mse_values: Total MSE values
        mse_first_values: First-stage MSE values
        cfg: Configuration object
        
    Returns:
        Matplotlib figure handle
    """
    # Convert theta to frequency for x-axis
    freq_axis = theta_to_freq(theta_range, cfg.signal.sampling_freq)
    
    # Calculate average MSE
    avg_mse = np.mean(mse_values)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot MSE curves
    ax.plot(freq_axis, mse_values, 'b-', linewidth=1.5, label='MSE (Total)')
    ax.plot(freq_axis, mse_first_values, 'r-', linewidth=1.5, label='MSE₁ (First Stage)')
    ax.axhline(y=avg_mse, color='k', linestyle='--', linewidth=1.0, label='Average MSE')
    
    # Labels and styling
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Mean Squared Error', fontsize=12)
    ax.set_title('MSE Analysis: Cost Function vs. Frequency', fontsize=14)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure if configured
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'mse_analysis.{cfg.output.figure_format}'
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_frequency_tracking(
    theta_history: NDArray,
    cfg: Config
) -> Figure:
    """
    Plot LMS frequency tracking convergence.
    
    Plots estimated frequency vs. iteration showing convergence trajectory.
    
    Args:
        theta_history: History of theta estimates (1D array)
        cfg: Configuration object
        
    Returns:
        Matplotlib figure handle
    """
    # Convert theta history to frequency
    freq_history = theta_to_freq(theta_history, cfg.signal.sampling_freq)
    
    # Create iteration axis
    num_iterations = len(theta_history)
    iteration_axis = np.arange(1, num_iterations + 1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot frequency tracking
    ax.plot(iteration_axis, freq_history, 'b-', linewidth=1.5, label='Estimated')
    
    # Add reference line for true frequency
    true_freq = cfg.signal.fundamental_freq
    ax.axhline(y=true_freq, color='r', linestyle='--', linewidth=1.0, label='True Frequency')
    
    # Labels and styling
    ax.set_xlabel('Iteration (n)', fontsize=12)
    ax.set_ylabel('Estimated Frequency (Hz)', fontsize=12)
    ax.set_title('LMS Frequency Tracking Convergence', fontsize=14)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Set y-axis limits
    freq_min = np.min(freq_history)
    freq_max = np.max(freq_history)
    margin = 100
    ax.set_ylim([freq_min - margin, freq_max + margin])
    
    plt.tight_layout()
    
    # Save figure if configured
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'frequency_tracking.{cfg.output.figure_format}'
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_filter_signals(
    y: NDArray,
    cfg: Config
) -> Figure:
    """
    Plot input signal and filter stage outputs.
    
    Multi-panel plot: input signal x(n) and outputs y_m(n) from each stage.
    
    Args:
        y: Filter outputs (M+1 × N+1)
        cfg: Configuration object
        
    Returns:
        Matplotlib figure handle
    """
    # Extract parameters
    num_samples = cfg.signal.num_samples + 1
    num_subfilters = cfg.filter.num_subfilters
    total_stages = num_subfilters + 1
    
    # Create sample index
    sample_index = np.arange(1, num_samples + 1)
    
    # Create figure with subplots
    fig, axes = plt.subplots(total_stages, 1, figsize=(12, 2.5 * total_stages))
    
    # Plot each stage
    for stage in range(total_stages):
        ax = axes[stage]
        ax.plot(sample_index, y[stage, :], 'b-', linewidth=1.0)
        ax.set_xlabel('Sample Index (n)', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        if stage == 0:
            ax.set_ylabel('x(n)', fontsize=9)
            ax.set_title('Input Signal', fontsize=10)
        else:
            ax.set_ylabel(f'y_{stage}(n)', fontsize=9)
            ax.set_title(f'Output of Filter Stage {stage}', fontsize=10)
    
    plt.tight_layout()
    
    # Save figure if configured
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'filter_signals.{cfg.output.figure_format}'
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_frequency_response(
    theta: float,
    cfg: Config
) -> tuple[Figure, Figure, Figure, Figure]:
    """
    Plot frequency response of filter bank.
    
    Creates four figures: individual stage responses, overall (linear), 
    overall (dB), and combined plot.
    
    Args:
        theta: Converged frequency estimate (radians)
        cfg: Configuration object
        
    Returns:
        Tuple of (fig_stages, fig_total, fig_db, fig_combined)
    """
    # Compute frequency response
    H_total, H_stages, freq_axis = compute_frequency_response(theta, cfg)
    
    # Extract parameters
    num_subfilters = cfg.filter.num_subfilters
    total_stages = num_subfilters + 1
    sampling_freq = cfg.signal.sampling_freq
    
    # Normalize frequency axis
    omega = freq_axis * 2 * np.pi / sampling_freq
    omega_norm = omega / np.pi
    
    # Figure 1: Individual stage responses
    fig_stages, axes = plt.subplots(total_stages, 1, figsize=(12, 2.5 * total_stages))
    
    for stage in range(total_stages):
        ax = axes[stage]
        ax.plot(omega_norm, np.abs(H_stages[stage, :]), 'b-', linewidth=1.5)
        ax.set_xlabel('ω / π', fontsize=9)
        ax.set_ylabel('|H(f)|', fontsize=9)
        ax.set_title(f'Stage {stage + 1}: Notch at {stage + 1}×f₁', fontsize=10)
        ax.set_ylim([0, 1.2])
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'stage_responses.{cfg.output.figure_format}'
        fig_stages.savefig(output_path, dpi=150, bbox_inches='tight')
    
    # Figure 2: Overall response (linear scale, Hz)
    fig_total, ax = plt.subplots(figsize=(10, 6))
    ax.plot(freq_axis, np.abs(H_total), 'b-', linewidth=1.5)
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('|H(f)|', fontsize=12)
    ax.set_title('Overall System Frequency Response', fontsize=14)
    ax.set_ylim([0, 1.2])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'overall_response.{cfg.output.figure_format}'
        fig_total.savefig(output_path, dpi=150, bbox_inches='tight')
    
    # Figure 3: Overall response (dB scale)
    fig_db, ax = plt.subplots(figsize=(10, 6))
    H_db = mag_to_db(H_total)
    ax.plot(freq_axis, H_db, 'b-', linewidth=1.5)
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('|H(f)| (dB)', fontsize=12)
    ax.set_title('Overall System Frequency Response (Decibels)', fontsize=14)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'overall_response_db.{cfg.output.figure_format}'
        fig_db.savefig(output_path, dpi=150, bbox_inches='tight')
    
    # Figure 4: Combined frequency response plot
    fig_combined, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Top subplot: Individual stage responses
    colors = ['b', 'g', 'r', 'm', 'c', 'y']
    fundamental_freq = theta_to_freq(theta, sampling_freq)
    
    for stage in range(num_subfilters):
        color = colors[stage % len(colors)]
        ax1.plot(freq_axis, np.abs(H_stages[stage + 1, :]), '-', 
                linewidth=1.5, color=color, label=f'Stage {stage + 1}')
    
    ax1.set_xlabel('Frequency (Hz)', fontsize=11)
    ax1.set_ylabel('|H(f)|', fontsize=11)
    ax1.set_title('Individual Notch Filter Responses', fontsize=12)
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([0, min(4000, sampling_freq / 2)])
    ax1.set_ylim([0, 1.2])
    
    # Bottom subplot: Overall system response
    H_db_total = mag_to_db(H_total)
    ax2.plot(freq_axis, H_db_total, 'b-', linewidth=1.5)
    
    # Mark harmonic frequencies with vertical lines
    for m in range(1, num_subfilters + 1):
        harmonic_freq = m * fundamental_freq
        ax2.axvline(x=harmonic_freq, color='r', linestyle=':', linewidth=1.0)
    
    # Add text labels for harmonics
    # Filter out invalid values (inf, nan) for computing limits
    valid_db = H_db_total[np.isfinite(H_db_total)]
    if len(valid_db) > 0:
        y_min = np.min(valid_db)
        y_max = np.max(valid_db)
    else:
        y_min, y_max = -60, 0
    
    y_pos = y_min + 0.1 * (y_max - y_min)
    
    for m in range(1, num_subfilters + 1):
        harmonic_freq = m * fundamental_freq
        ax2.text(harmonic_freq, y_pos, f'{m}f₁', 
                ha='center', fontsize=10, fontweight='bold', color='red')
    
    ax2.set_xlabel('Frequency (Hz)', fontsize=11)
    ax2.set_ylabel('|H(f)| (dB)', fontsize=11)
    ax2.set_title('Overall System Frequency Response (Comb Filter)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, min(4000, sampling_freq / 2)])
    ax2.set_ylim([max(y_min - 5, -80), 5])
    
    plt.tight_layout()
    
    if cfg.output.save_figures:
        output_path = cfg.output.directory / f'frequency_response_plot.{cfg.output.figure_format}'
        fig_combined.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig_stages, fig_total, fig_db, fig_combined
