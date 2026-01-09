function cfg = config(config_file)
    % CONFIG Get or load configuration for frequency estimation.
    %
    % Usage:
    %   cfg = config()              % Returns default configuration
    %   cfg = config('file.mat')     % Loads configuration from file
    %   cfg = config([])             % Returns default configuration
    %
    % Returns:
    %   cfg: Configuration structure with fields:
    %     cfg.signal.* - Signal parameters (fundamental_freq, sampling_freq, etc.)
    %     cfg.filter.* - Filter parameters (num_subfilters, pole_radius)
    %     cfg.lms.*    - LMS parameters (step_size, num_theta_points)
    %     cfg.output.* - Output parameters (directory, save_figures, figure_format)

    if nargin < 1 || isempty(config_file)
        cfg = default_config();
        return;
    end

    %% Load configuration from file
    if ~exist(config_file, 'file')
        warning('Config file not found: %s. Using defaults.', config_file);
        cfg = default_config();
        return;
    end

    loaded = load(config_file);
    if ~isfield(loaded, 'cfg')
        warning('Config file does not contain ''cfg'' variable. Using defaults.');
        cfg = default_config();
        return;
    end

    cfg = loaded.cfg;

    %% Merge with defaults to ensure all fields exist
    default_cfg = default_config();
    cfg = merge_structs(default_cfg, cfg);
end


function cfg = default_config()
    % DEFAULT_CONFIG Returns default configuration structure.

    %% Signal Parameters
    cfg.signal.fundamental_freq = 1000;     % f₁: Fundamental frequency (Hz)
    cfg.signal.sampling_freq = 8000;        % fs: Sampling frequency (Hz)
    cfg.signal.num_samples = 400;           % N: Number of samples
    cfg.signal.add_noise = false;           % Flag to add Gaussian noise
    cfg.signal.snr_db = 18;                 % SNR in dB (if noise enabled)

    %% Filter Bank Parameters
    cfg.filter.num_subfilters = 3;          % M: Number of harmonic subfilters
    cfg.filter.pole_radius = 0.95;          % r: Pole radius (controls bandwidth)

    %% LMS Algorithm Parameters
    cfg.lms.step_size = 0.0001;             % μ: Step size for gradient descent
    cfg.lms.num_theta_points = 1400;        % Resolution for initial theta search

    %% Output Configuration
    cfg.output.directory = fullfile(fileparts(mfilename('fullpath')), ...
                                    '..', '..', 'output');
    cfg.output.save_figures = true;         % Save figures to disk
    cfg.output.figure_format = 'png';       % Output format: 'png', 'eps', 'pdf'

    %% Create output directory if it does not exist
    if ~exist(cfg.output.directory, 'dir')
        mkdir(cfg.output.directory);
    end
end


function save_config(cfg, filename)
    % SAVE_CONFIG Save configuration structure to MAT file.
    %
    % Args:
    %   cfg: Configuration structure to save
    %   filename: Path to save the configuration

    if nargin < 2
        error('Both cfg and filename arguments are required.');
    end

    save(filename, 'cfg');
    fprintf('Configuration saved to: %s\n', filename);
end


function merged = merge_structs(base, override)
    % MERGE_STRUCTS Recursively merge two structs, with override taking precedence.

    merged = base;
    fields = fieldnames(override);

    for i = 1:length(fields)
        field = fields{i};
        if isfield(base, field) && isstruct(base.(field)) && isstruct(override.(field))
            merged.(field) = merge_structs(base.(field), override.(field));
        else
            merged.(field) = override.(field);
        end
    end
end
