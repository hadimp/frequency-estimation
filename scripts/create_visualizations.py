#!/usr/bin/env python3
"""
Create comprehensive visualizations for the Frequency Estimation algorithm.

This script generates publication-quality figures illustrating:
- Algorithm architecture and flow
- Filter bank structure
- Mathematical concepts
- Performance metrics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.patches import ConnectionPatch
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Set style for publication-quality plots
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300

def create_algorithm_flowchart():
    """Create algorithm flowchart diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Adaptive Frequency Estimation Algorithm', 
            ha='center', fontsize=18, fontweight='bold')
    
    # Phase 1: Initial Estimation
    box1 = FancyBboxPatch((1, 7.5), 2.5, 1, boxstyle="round,pad=0.1", 
                          facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(box1)
    ax.text(2.25, 8, 'Phase 1:\nInitial Estimation', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(2.25, 7.6, 'MSE Search\nθ ∈ [0, π/M]', ha='center', va='center',
            fontsize=9)
    
    # Phase 2: LMS Tracking
    box2 = FancyBboxPatch((5, 7.5), 2.5, 1, boxstyle="round,pad=0.1",
                          facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(box2)
    ax.text(6.25, 8, 'Phase 2:\nLMS Tracking', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(6.25, 7.6, 'θ(n+1) = θ(n) - 2μ·y·β', ha='center', va='center',
            fontsize=9)
    
    # Arrows
    arrow1 = FancyArrowPatch((3.5, 8), (5, 8), arrowstyle='->', 
                             mutation_scale=20, linewidth=2, color='black')
    ax.add_patch(arrow1)
    
    # Input Signal
    input_box = FancyBboxPatch((0.5, 5.5), 1.5, 0.8, boxstyle="round,pad=0.1",
                               facecolor='lightyellow', edgecolor='black', linewidth=1.5)
    ax.add_patch(input_box)
    ax.text(1.25, 5.9, 'Input Signal\nx(n)', ha='center', va='center', fontsize=10)
    
    # Filter Bank
    filter_box = FancyBboxPatch((2.5, 4.5), 5, 2.5, boxstyle="round,pad=0.1",
                                facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(filter_box)
    ax.text(5, 6.5, 'Cascaded Notch Filter Bank', ha='center', va='center',
            fontsize=12, fontweight='bold')
    
    # Filter stages
    for i in range(4):
        stage_box = FancyBboxPatch((3 + i*1.2, 5), 1, 0.6, boxstyle="round,pad=0.05",
                                    facecolor='white', edgecolor='blue', linewidth=1)
        ax.add_patch(stage_box)
        if i == 0:
            ax.text(3.5 + i*1.2, 5.3, f'H₀\nInput', ha='center', va='center', fontsize=8)
        else:
            ax.text(3.5 + i*1.2, 5.3, f'H_{i}\nNotch\n@ {i}f₁', ha='center', va='center', fontsize=8)
    
    # Output
    output_box = FancyBboxPatch((8, 5.5), 1.5, 0.8, boxstyle="round,pad=0.1",
                                facecolor='lightyellow', edgecolor='black', linewidth=1.5)
    ax.add_patch(output_box)
    ax.text(8.75, 5.9, 'Output\ny_M(n)', ha='center', va='center', fontsize=10)
    
    # Arrows to filter bank
    arrow2 = FancyArrowPatch((2, 5.9), (2.5, 5.9), arrowstyle='->',
                            mutation_scale=15, linewidth=1.5, color='black')
    ax.add_patch(arrow2)
    arrow3 = FancyArrowPatch((7.5, 5.9), (8, 5.9), arrowstyle='->',
                            mutation_scale=15, linewidth=1.5, color='black')
    ax.add_patch(arrow3)
    
    # MSE Computation
    mse_box = FancyBboxPatch((2.5, 2), 2, 1, boxstyle="round,pad=0.1",
                             facecolor='lightblue', edgecolor='black', linewidth=1.5)
    ax.add_patch(mse_box)
    ax.text(3.5, 2.5, 'MSE\nComputation', ha='center', va='center', fontsize=10)
    
    # Gradient Computation
    grad_box = FancyBboxPatch((5.5, 2), 2, 1, boxstyle="round,pad=0.1",
                              facecolor='lightgreen', edgecolor='black', linewidth=1.5)
    ax.add_patch(grad_box)
    ax.text(6.5, 2.5, 'Gradient\nβ_M(n)', ha='center', va='center', fontsize=10)
    
    # Arrows from filter to computations
    arrow4 = FancyArrowPatch((4, 4.5), (3.5, 3), arrowstyle='->',
                            mutation_scale=15, linewidth=1.5, color='blue', linestyle='--')
    ax.add_patch(arrow4)
    arrow5 = FancyArrowPatch((6, 4.5), (6.5, 3), arrowstyle='->',
                            mutation_scale=15, linewidth=1.5, color='green', linestyle='--')
    ax.add_patch(arrow5)
    
    # Update arrow
    arrow6 = FancyArrowPatch((7.5, 2.5), (5, 7.5), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color='red', linestyle=':')
    ax.add_patch(arrow6)
    ax.text(6, 5, 'Update θ', ha='center', fontsize=9, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red'))
    
    plt.tight_layout()
    plt.savefig('output/algorithm_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: algorithm_flowchart.png")

def create_filter_structure():
    """Create filter bank structure diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    ax.text(7, 3.5, 'Cascaded Notch Filter Bank Structure', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Input
    input_circle = Circle((1, 2), 0.3, facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(input_circle)
    ax.text(1, 2, 'x(n)', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(1, 1.3, 'Input Signal', ha='center', fontsize=9)
    
    # Filter stages
    for i in range(4):
        x_pos = 3 + i * 2.5
        # Filter box
        filter_rect = FancyBboxPatch((x_pos - 0.8, 1.5), 1.6, 1, 
                                     boxstyle="round,pad=0.1",
                                     facecolor='lightcoral', edgecolor='black', linewidth=2)
        ax.add_patch(filter_rect)
        
        if i == 0:
            ax.text(x_pos, 2, 'H₀\nPass-through', ha='center', va='center',
                   fontsize=9, fontweight='bold')
        else:
            ax.text(x_pos, 2, f'H_{i}\nNotch @ {i}f₁', ha='center', va='center',
                   fontsize=9, fontweight='bold')
        
        # Transfer function
        if i > 0:
            ax.text(x_pos, 1.2, f'H_{i}(z) =', ha='center', fontsize=7)
            ax.text(x_pos, 0.9, f'1-2cos({i}θ)z⁻¹+z⁻²', ha='center', fontsize=7)
            ax.text(x_pos, 0.6, f'1-2r·cos({i}θ)z⁻¹+r²z⁻²', ha='center', fontsize=7)
        
        # Arrow
        if i < 3:
            arrow = FancyArrowPatch((x_pos + 0.8, 2), (x_pos + 1.7, 2),
                                   arrowstyle='->', mutation_scale=20, linewidth=2)
            ax.add_patch(arrow)
    
    # Output
    output_circle = Circle((13, 2), 0.3, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(output_circle)
    ax.text(13, 2, 'y_M(n)', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(13, 1.3, 'Output', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('output/filter_structure.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: filter_structure.png")

def create_mse_landscape():
    """Create MSE cost function landscape visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Simulate MSE landscape
    theta = np.linspace(0, np.pi/3, 1000)
    freq = theta * 8000 / (2 * np.pi)
    
    # Create a realistic MSE curve with minimum near 1000 Hz
    true_freq = 1000
    true_theta = 2 * np.pi * true_freq / 8000
    
    # MSE curve (parabolic with some noise)
    mse = 0.5 + 0.3 * (theta - true_theta)**2 * 1000 + \
          0.1 * np.sin(10 * theta) + 0.05 * np.random.randn(len(theta))
    mse = np.maximum(mse, 0.1)
    
    # MSE1 curve (higher, less sharp)
    mse1 = 0.6 + 0.4 * (theta - true_theta)**2 * 800 + \
           0.15 * np.sin(8 * theta) + 0.08 * np.random.randn(len(theta))
    mse1 = np.maximum(mse1, 0.2)
    
    ax.plot(freq, mse, 'b-', linewidth=2, label='MSE (Total)', alpha=0.8)
    ax.plot(freq, mse1, 'r-', linewidth=2, label='MSE₁ (First Stage)', alpha=0.8)
    
    # Average line
    avg_mse = np.mean(mse)
    ax.axhline(y=avg_mse, color='k', linestyle='--', linewidth=1.5, 
               label='Average MSE', alpha=0.7)
    
    # Mark minimum
    min_idx = np.argmin(mse)
    ax.plot(freq[min_idx], mse[min_idx], 'go', markersize=12, 
           label='Global Minimum', zorder=5)
    ax.annotate(f'Min: {freq[min_idx]:.1f} Hz', 
               xy=(freq[min_idx], mse[min_idx]),
               xytext=(freq[min_idx] + 200, mse[min_idx] + 0.1),
               arrowprops=dict(arrowstyle='->', color='green', lw=2),
               fontsize=11, fontweight='bold', color='green')
    
    # Mark true frequency
    ax.axvline(x=true_freq, color='orange', linestyle=':', linewidth=2,
              label=f'True Frequency: {true_freq} Hz', alpha=0.8)
    
    ax.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Squared Error', fontsize=12, fontweight='bold')
    ax.set_title('MSE Cost Function Landscape', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1400)
    
    plt.tight_layout()
    plt.savefig('output/mse_landscape.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: mse_landscape.png")

def create_convergence_demo():
    """Create LMS convergence demonstration."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Simulate convergence
    iterations = np.arange(1, 401)
    true_freq = 1000
    initial_freq = 970
    
    # Exponential convergence with some noise
    convergence = true_freq - (true_freq - initial_freq) * np.exp(-iterations / 100) + \
                  2 * np.random.randn(len(iterations)) * np.exp(-iterations / 200)
    
    # Plot 1: Frequency tracking
    ax1.plot(iterations, convergence, 'b-', linewidth=2, label='Estimated Frequency', alpha=0.7)
    ax1.axhline(y=true_freq, color='r', linestyle='--', linewidth=2, 
               label=f'True Frequency: {true_freq} Hz', alpha=0.8)
    ax1.axhline(y=initial_freq, color='g', linestyle=':', linewidth=2,
               label=f'Initial Estimate: {initial_freq} Hz', alpha=0.8)
    
    ax1.set_xlabel('Iteration (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax1.set_title('LMS Frequency Tracking Convergence', fontsize=14, fontweight='bold')
    ax1.legend(loc='right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 400)
    ax1.set_ylim(960, 1010)
    
    # Plot 2: Error evolution
    error = np.abs(convergence - true_freq)
    ax2.semilogy(iterations, error, 'r-', linewidth=2, label='Estimation Error', alpha=0.7)
    ax2.axhline(y=0.1, color='g', linestyle='--', linewidth=1.5,
               label='Target Error: 0.1 Hz', alpha=0.7)
    
    ax2.set_xlabel('Iteration (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Absolute Error (Hz)', fontsize=12, fontweight='bold')
    ax2.set_title('Convergence Error Evolution (Log Scale)', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_xlim(0, 400)
    
    plt.tight_layout()
    plt.savefig('output/convergence_demo.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: convergence_demo.png")

def create_frequency_response_plot():
    """Create frequency response visualization."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Frequency axis
    freq = np.linspace(0, 4000, 2000)
    omega = 2 * np.pi * freq / 8000
    
    # Simulate notch filter responses
    theta = 2 * np.pi * 1000 / 8000  # 1 kHz fundamental
    r = 0.95
    
    # Plot 1: Individual stages
    colors = ['blue', 'green', 'red', 'purple']
    for m in range(1, 4):
        # Notch filter response
        H_mag = np.abs((1 - 2*np.cos(m*theta)*np.exp(-1j*omega) + np.exp(-2j*omega)) /
                      (1 - 2*r*np.cos(m*theta)*np.exp(-1j*omega) + r**2*np.exp(-2j*omega)))
        H_mag = H_mag / np.max(H_mag)  # Normalize
        
        ax1.plot(freq, H_mag, linewidth=2, label=f'Stage {m}: Notch @ {m*1000} Hz',
                color=colors[m-1], alpha=0.8)
        ax1.axvline(x=m*1000, color=colors[m-1], linestyle=':', linewidth=1, alpha=0.5)
    
    ax1.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('|H(f)|', fontsize=12, fontweight='bold')
    ax1.set_title('Individual Notch Filter Responses', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 4000)
    ax1.set_ylim(0, 1.2)
    
    # Plot 2: Overall system response
    H_total = np.ones_like(freq)
    for m in range(1, 4):
        H_mag = np.abs((1 - 2*np.cos(m*theta)*np.exp(-1j*omega) + np.exp(-2j*omega)) /
                      (1 - 2*r*np.cos(m*theta)*np.exp(-1j*omega) + r**2*np.exp(-2j*omega)))
        H_total = H_total * H_mag
    
    H_total = H_total / np.max(H_total)
    H_db = 20 * np.log10(H_total + 1e-10)  # Avoid log(0)
    
    ax2.plot(freq, H_db, 'b-', linewidth=2, alpha=0.8)
    for m in range(1, 4):
        ax2.axvline(x=m*1000, color='r', linestyle=':', linewidth=1.5, alpha=0.6)
    
    ax2.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('|H(f)| (dB)', fontsize=12, fontweight='bold')
    ax2.set_title('Overall System Frequency Response (Comb Filter)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 4000)
    ax2.set_ylim(-60, 5)
    
    # Mark notches
    for m in range(1, 4):
        ax2.text(m*1000, -50, f'{m}f₁', ha='center', fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('output/frequency_response_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: frequency_response_plot.png")

def main():
    """Generate all visualizations."""
    print("Generating visualizations for Frequency Estimation Algorithm...")
    print("=" * 60)
    
    create_algorithm_flowchart()
    create_filter_structure()
    create_mse_landscape()
    create_convergence_demo()
    create_frequency_response_plot()
    
    print("=" * 60)
    print("All visualizations created successfully!")
    print("Output directory: output/")

if __name__ == '__main__':
    main()
