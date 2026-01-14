from .config import Config
from .estimator import FrequencyEstimator
from .visualization import ResultsPlotter


def main():
    import argparse
    import matplotlib
    
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
    
    # Set matplotlib backend if needed
    if args.no_display:
        matplotlib.use('Agg')
    
    # Run algorithm
    estimator = FrequencyEstimator(cfg)
    result = estimator.estimate()
    
    # Generate plots
    plotter = ResultsPlotter(result)
    plotter.plot_all()
    
    # Display if requested
    if not args.no_display:
        import matplotlib.pyplot as plt
        plt.show()
    
    return result


if __name__ == '__main__':
    main()
