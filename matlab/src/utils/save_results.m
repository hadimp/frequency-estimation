function save_results(results, cfg)
    % SAVE_RESULTS Save frequency estimation results to file.
    %
    % Saves results in multiple formats:
    %   - .mat file: Complete results structure (all data)
    %   - .txt file: Human-readable summary report
    %
    % Args:
    %   results: Results structure from run_frequency_estimation()
    %   cfg: Configuration structure

    if ~cfg.output.save_results
        return;
    end

    output_dir = cfg.output.directory;
    timestamp = datestr(now, 'yyyymmdd_HHMMSS');
    base_name = sprintf('frequency_estimation_%s', timestamp);

    %% Save complete results as MAT file
    mat_file = fullfile(output_dir, [base_name, '.mat']);
    try
        % Try v7.3 format (MATLAB, supports large files)
        save(mat_file, 'results', '-v7.3');
    catch
        % Fallback to v7 format (Octave compatible)
        save(mat_file, 'results', '-v7');
    end
    fprintf('Results saved to: %s\n', mat_file);

    %% Save human-readable summary as text file
    txt_file = fullfile(output_dir, [base_name, '_summary.txt']);
    fid = fopen(txt_file, 'w');
    if fid == -1
        warning('Could not create summary file: %s', txt_file);
        return;
    end

    %% Write summary report
    fprintf(fid, '=======================================================\n');
    fprintf(fid, '  FREQUENCY ESTIMATION RESULTS\n');
    fprintf(fid, '=======================================================\n');
    fprintf(fid, 'Generated: %s\n\n', datestr(now));

    %% Configuration
    fprintf(fid, 'CONFIGURATION:\n');
    fprintf(fid, '  Signal Parameters:\n');
    fprintf(fid, '    Fundamental frequency: %d Hz\n', cfg.signal.fundamental_freq);
    fprintf(fid, '    Sampling frequency:    %d Hz\n', cfg.signal.sampling_freq);
    fprintf(fid, '    Number of samples:     %d\n', cfg.signal.num_samples);
    fprintf(fid, '    Add noise:             %s\n', mat2str(cfg.signal.add_noise));
    if cfg.signal.add_noise
        fprintf(fid, '    SNR:                   %d dB\n', cfg.signal.snr_db);
    end
    fprintf(fid, '  Filter Parameters:\n');
    fprintf(fid, '    Number of subfilters:  %d\n', cfg.filter.num_subfilters);
    fprintf(fid, '    Pole radius:           %.4f\n', cfg.filter.pole_radius);
    fprintf(fid, '  LMS Parameters:\n');
    fprintf(fid, '    Step size (mu):        %.6f\n', cfg.lms.step_size);
    fprintf(fid, '    Theta search points:   %d\n', cfg.lms.num_theta_points);
    fprintf(fid, '\n');

    %% Results
    fprintf(fid, 'RESULTS:\n');
    fprintf(fid, '  True frequency:          %d Hz\n', cfg.signal.fundamental_freq);
    fprintf(fid, '  Initial estimate:        %.4f Hz (theta = %.6f rad)\n', ...
            results.initial_freq, results.initial_theta);
    fprintf(fid, '  Final estimate:          %.4f Hz (theta = %.6f rad)\n', ...
            results.final_freq, results.final_theta);
    fprintf(fid, '  Estimation error:       %.4f Hz (%.4f%%)\n', ...
            results.error_hz, results.error_percent);
    fprintf(fid, '\n');

    %% MSE Statistics
    fprintf(fid, 'MSE STATISTICS:\n');
    fprintf(fid, '  Minimum MSE:            %.6e\n', min(results.mse_values));
    fprintf(fid, '  Mean MSE:                %.6e\n', mean(results.mse_values));
    fprintf(fid, '  Maximum MSE:            %.6e\n', max(results.mse_values));
    fprintf(fid, '  Minimum MSE₁:           %.6e\n', min(results.mse_first_values));
    fprintf(fid, '  Mean MSE₁:               %.6e\n', mean(results.mse_first_values));
    fprintf(fid, '  Maximum MSE₁:           %.6e\n', max(results.mse_first_values));
    fprintf(fid, '\n');

    %% Convergence Statistics
    fprintf(fid, 'CONVERGENCE STATISTICS:\n');
    freq_history = results.theta_history * cfg.signal.sampling_freq / (2 * pi);
    initial_freq = freq_history(1);
    final_freq = freq_history(end);
    fprintf(fid, '  Initial frequency:       %.4f Hz\n', initial_freq);
    fprintf(fid, '  Final frequency:        %.4f Hz\n', final_freq);
    fprintf(fid, '  Frequency change:       %.4f Hz\n', final_freq - initial_freq);
    fprintf(fid, '  Convergence iterations: %d\n', length(results.theta_history));
    fprintf(fid, '\n');

    %% File locations
    fprintf(fid, 'OUTPUT FILES:\n');
    fprintf(fid, '  Results (MAT):          %s\n', mat_file);
    if cfg.output.save_figures
        fprintf(fid, '  Figures directory:       %s\n', output_dir);
    end
    fprintf(fid, '\n');

    fprintf(fid, '=======================================================\n');
    fprintf(fid, 'End of Report\n');
    fprintf(fid, '=======================================================\n');

    fclose(fid);
    fprintf('Summary saved to: %s\n', txt_file);
end
