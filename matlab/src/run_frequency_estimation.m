function results = run_frequency_estimation(config_input)

    %% LOAD CONFIGURATION
    if nargin < 1 || isempty(config_input)
        cfg = config();
        fprintf('Using default configuration.\n');
    elseif ischar(config_input)
        cfg = config(config_input);
        fprintf('Loaded configuration from: %s\n', config_input);
    elseif isstruct(config_input)
        cfg = config_input;
        fprintf('Using provided configuration structure.\n');
    else
        error('Invalid config input. Provide a filename or struct.');
    end

    %% DISPLAY PARAMETERS
    fprintf('\n');
    fprintf('=======================================================\n');
    fprintf('  ADAPTIVE FREQUENCY ESTIMATION\n');
    fprintf('=======================================================\n');
    fprintf('Signal Parameters:\n');
    fprintf('  Fundamental frequency: %d Hz\n', cfg.signal.fundamental_freq);
    fprintf('  Sampling frequency:    %d Hz\n', cfg.signal.sampling_freq);
    fprintf('  Number of samples:     %d\n', cfg.signal.num_samples);
    fprintf('  Add noise:             %s\n', mat2str(cfg.signal.add_noise));
    if cfg.signal.add_noise
        fprintf('  SNR:                   %d dB\n', cfg.signal.snr_db);
    end
    fprintf('\nFilter Parameters:\n');
    fprintf('  Number of subfilters:  %d\n', cfg.filter.num_subfilters);
    fprintf('  Pole radius:           %.2f\n', cfg.filter.pole_radius);
    fprintf('\nLMS Parameters:\n');
    fprintf('  Step size (mu):        %.6f\n', cfg.lms.step_size);
    fprintf('  Theta search points:   %d\n', cfg.lms.num_theta_points);
    fprintf('=======================================================\n\n');

    %% PHASE 1: INITIAL FREQUENCY ESTIMATION (MSE Search)
    fprintf('Phase 1: Searching for initial frequency estimate...\n');

    [initial_theta, mse_values, mse_first_values, theta_range] = find_initial_theta(cfg);

    initial_freq = theta_to_freq(initial_theta, cfg.signal.sampling_freq);
    fprintf('  Initial estimate: %.2f Hz (theta = %.4f rad)\n', initial_freq, initial_theta);

    % Plot MSE analysis
    plot_mse_analysis(theta_range, mse_values, mse_first_values, cfg);

    %% PHASE 2: LMS FREQUENCY TRACKING
    fprintf('\nPhase 2: Running LMS algorithm for frequency tracking...\n');

    [theta_final, theta_history] = run_lms_algorithm(initial_theta, cfg);

    final_freq = theta_to_freq(theta_final, cfg.signal.sampling_freq);
    fprintf('  Final estimate:   %.2f Hz (theta = %.4f rad)\n', final_freq, theta_final);

    % Calculate estimation error
    true_freq = cfg.signal.fundamental_freq;
    error_hz = abs(final_freq - true_freq);
    error_percent = 100 * error_hz / true_freq;
    fprintf('  Estimation error: %.2f Hz (%.4f%%)\n', error_hz, error_percent);

    % Plot frequency tracking
    plot_frequency_tracking(theta_history, cfg);

    %% PHASE 3: COMPUTE FINAL FILTER OUTPUT
    fprintf('\nPhase 3: Computing final filter bank output...\n');

    y_final = compute_filter_output(theta_final, cfg);

    % Plot filter signals
    plot_filter_signals(y_final, cfg);

    %% PHASE 4: FREQUENCY RESPONSE ANALYSIS
    fprintf('\nPhase 4: Analyzing frequency response...\n');

    plot_frequency_response(theta_final, cfg);

    %% PACKAGE RESULTS
    results.config = cfg;
    results.initial_theta = initial_theta;
    results.initial_freq = initial_freq;
    results.final_theta = theta_final;
    results.final_freq = final_freq;
    results.theta_history = theta_history;
    results.mse_values = mse_values;
    results.mse_first_values = mse_first_values;
    results.theta_range = theta_range;
    results.filter_output = y_final;
    results.error_hz = error_hz;
    results.error_percent = error_percent;

    %% SUMMARY
    fprintf('\n');
    fprintf('=======================================================\n');
    fprintf('  RESULTS SUMMARY\n');
    fprintf('=======================================================\n');
    fprintf('  True frequency:      %d Hz\n', true_freq);
    fprintf('  Estimated frequency: %.2f Hz\n', final_freq);
    fprintf('  Estimation error:    %.4f%%\n', error_percent);
    fprintf('=======================================================\n');

    %% SAVE RESULTS TO FILE
    if cfg.output.save_results
        fprintf('\nSaving results to file...\n');
        save_results(results, cfg);
    end

    if cfg.output.save_figures
        fprintf('\nFigures saved to: %s\n', cfg.output.directory);
    end

    fprintf('\nFrequency estimation complete.\n\n');
end
