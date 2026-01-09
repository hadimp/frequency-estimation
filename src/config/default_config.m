function cfg = default_config()
    % DEFAULT_CONFIG Returns default configuration for frequency estimation.
    %
    % Returns configuration structure with signal, filter, LMS, and output parameters.
    % Modify fields to customize behavior.
    %
    % Returns:
    %   cfg: Configuration structure with fields:
    %     cfg.signal.* - Signal parameters (fundamental_freq, sampling_freq, etc.)
    %     cfg.filter.* - Filter parameters (num_subfilters, pole_radius)
    %     cfg.lms.*    - LMS parameters (step_size, num_theta_points)
    %     cfg.output.* - Output parameters (directory, save_figures, figure_format)

    %% Signal Parameters
    % These define the characteristics of the input test signal
    cfg.signal.fundamental_freq = 1000;     % f₁: Fundamental frequency (Hz)
    cfg.signal.sampling_freq = 8000;        % fs: Sampling frequency (Hz)
    cfg.signal.num_samples = 400;           % N: Number of samples
    cfg.signal.add_noise = false;           % Flag to add Gaussian noise
    cfg.signal.snr_db = 18;                 % SNR in dB (if noise enabled)

    %% Filter Bank Parameters
    % Parameters for the cascaded notch filter bank
    % The filter bank consists of M second-order IIR notch filters
    cfg.filter.num_subfilters = 3;          % M: Number of harmonic subfilters
    cfg.filter.pole_radius = 0.95;          % r: Pole radius (controls bandwidth)
                                            %    Closer to 1 = narrower notch

    %% LMS Algorithm Parameters
    % Parameters for the Least Mean Squares adaptation
    cfg.lms.step_size = 0.0001;             % μ: Step size for gradient descent
                                            %    Smaller = more stable, slower
    cfg.lms.num_theta_points = 1400;        % Resolution for initial theta search

    %% Output Configuration
    % Settings for saving results and figures
    cfg.output.directory = fullfile(fileparts(mfilename('fullpath')), ...
                                    '..', '..', 'output');
    cfg.output.save_figures = true;         % Save figures to disk
    cfg.output.figure_format = 'png';       % Output format: 'png', 'eps', 'pdf'

    %% Create output directory if it doesn't exist
    if ~exist(cfg.output.directory, 'dir')
        mkdir(cfg.output.directory);
    end
end
