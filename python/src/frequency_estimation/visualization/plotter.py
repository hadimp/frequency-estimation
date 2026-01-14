import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path
from typing import Optional

from ..estimator import EstimationResult, theta_to_freq
from ..filters import CascadedFilterBank
from ..utils import mag_to_db


class ResultsPlotter:
    
    def __init__(
        self, 
        result: EstimationResult,
        output_dir: Optional[Path] = None,
        figure_format: str = "png",
        save_figures: bool = True
    ):
        self.result = result
        self.output_dir = output_dir or result.config.output.directory
        self.figure_format = figure_format
        self.save_figures = save_figures
    
    def plot_mse_analysis(self) -> Figure:
        freq_axis = theta_to_freq(self.result.theta_range, self.result.sampling_freq)
        avg_mse = np.mean(self.result.mse_values)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(freq_axis, self.result.mse_values, 'b-', linewidth=1.5, label='MSE (Total)')
        ax.plot(freq_axis, self.result.mse_first_values, 'r-', linewidth=1.5, label='MSE₁ (First Stage)')
        ax.axhline(y=avg_mse, color='k', linestyle='--', linewidth=1.0, label='Average MSE')
        
        ax.set_xlabel('Frequency (Hz)', fontsize=12)
        ax.set_ylabel('Mean Squared Error', fontsize=12)
        ax.set_title('MSE Analysis: Cost Function vs. Frequency', fontsize=14)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self._save_figure(fig, 'mse_analysis')
        
        return fig
    
    def plot_frequency_tracking(self) -> Figure:
        num_iterations = len(self.result.theta_history)
        iteration_axis = np.arange(1, num_iterations + 1)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(iteration_axis, self.result.freq_history, 'b-', linewidth=1.5, label='Estimated')
        ax.axhline(y=self.result.true_freq, color='r', linestyle='--', linewidth=1.0, label='True Frequency')
        
        ax.set_xlabel('Iteration (n)', fontsize=12)
        ax.set_ylabel('Estimated Frequency (Hz)', fontsize=12)
        ax.set_title('LMS Frequency Tracking Convergence', fontsize=14)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Set y-axis limits
        freq_min = np.min(self.result.freq_history)
        freq_max = np.max(self.result.freq_history)
        margin = 100
        ax.set_ylim([freq_min - margin, freq_max + margin])
        
        plt.tight_layout()
        self._save_figure(fig, 'frequency_tracking')
        
        return fig
    
    def plot_filter_signals(self) -> Figure:
        y = self.result.filter_output
        num_samples = y.shape[1]
        total_stages = y.shape[0]
        sample_index = np.arange(1, num_samples + 1)
        
        fig, axes = plt.subplots(total_stages, 1, figsize=(12, 2.5 * total_stages))
        
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
        self._save_figure(fig, 'filter_signals')
        
        return fig
    
    def plot_frequency_response(self) -> tuple[Figure, Figure, Figure, Figure]:
        cfg = self.result.config
        theta = self.result.final_theta
        sampling_freq = cfg.signal.sampling_freq
        num_subfilters = cfg.filter.num_subfilters
        num_points = cfg.lms.num_theta_points
        
        # Create filter bank for frequency response
        filter_bank = CascadedFilterBank(
            num_stages=num_subfilters,
            pole_radius=cfg.filter.pole_radius
        )
        
        # Frequency axis
        num_freq_points = num_points * 3
        omega = np.linspace(-np.pi, np.pi, num_freq_points)
        freq_axis = omega * sampling_freq / (2 * np.pi)
        omega_norm = omega / np.pi
        
        # Compute frequency response
        H_total, H_stages = filter_bank.frequency_response(theta, omega)
        
        # Figure 1: Individual stage responses
        total_stages = num_subfilters + 1
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
        self._save_figure(fig_stages, 'stage_responses')
        
        # Figure 2: Overall response (linear)
        fig_total, ax = plt.subplots(figsize=(10, 6))
        ax.plot(freq_axis, np.abs(H_total), 'b-', linewidth=1.5)
        ax.set_xlabel('Frequency (Hz)', fontsize=12)
        ax.set_ylabel('|H(f)|', fontsize=12)
        ax.set_title('Overall System Frequency Response', fontsize=14)
        ax.set_ylim([0, 1.2])
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        self._save_figure(fig_total, 'overall_response')
        
        # Figure 3: Overall response (dB)
        fig_db, ax = plt.subplots(figsize=(10, 6))
        H_db = mag_to_db(H_total)
        ax.plot(freq_axis, H_db, 'b-', linewidth=1.5)
        ax.set_xlabel('Frequency (Hz)', fontsize=12)
        ax.set_ylabel('|H(f)| (dB)', fontsize=12)
        ax.set_title('Overall System Frequency Response (Decibels)', fontsize=14)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        self._save_figure(fig_db, 'overall_response_db')
        
        # Figure 4: Combined plot
        fig_combined, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
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
        
        H_db_total = mag_to_db(H_total)
        ax2.plot(freq_axis, H_db_total, 'b-', linewidth=1.5)
        
        for m in range(1, num_subfilters + 1):
            harmonic_freq = m * fundamental_freq
            ax2.axvline(x=harmonic_freq, color='r', linestyle=':', linewidth=1.0)
        
        valid_db = H_db_total[np.isfinite(H_db_total)]
        y_min = np.min(valid_db) if len(valid_db) > 0 else -60
        y_max = np.max(valid_db) if len(valid_db) > 0 else 0
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
        self._save_figure(fig_combined, 'frequency_response_plot')
        
        return fig_stages, fig_total, fig_db, fig_combined
    
    def plot_all(self) -> dict[str, Figure]:
        figures = {}
        
        figures['mse_analysis'] = self.plot_mse_analysis()
        figures['frequency_tracking'] = self.plot_frequency_tracking()
        figures['filter_signals'] = self.plot_filter_signals()
        
        fig_stages, fig_total, fig_db, fig_combined = self.plot_frequency_response()
        figures['stage_responses'] = fig_stages
        figures['overall_response'] = fig_total
        figures['overall_response_db'] = fig_db
        figures['frequency_response_plot'] = fig_combined
        
        return figures
    
    def _save_figure(self, fig: Figure, name: str) -> None:
        if self.save_figures:
            path = Path(self.output_dir) / f"{name}.{self.figure_format}"
            fig.savefig(path, dpi=150, bbox_inches='tight')
    
    def __repr__(self) -> str:
        return f"ResultsPlotter(result={self.result})"
