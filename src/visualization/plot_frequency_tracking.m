function fig_handle = plot_frequency_tracking(theta_history, cfg)
    % PLOT_FREQUENCY_TRACKING Plot LMS frequency tracking convergence.
    %
    % Plots estimated frequency vs. iteration showing convergence trajectory.
    %
    % Args:
    %   theta_history: History of theta estimates (N x 1)
    %   cfg: Configuration structure
    %
    % Returns:
    %   fig_handle: Figure handle

    %% Convert theta history to frequency
    freq_history = theta_to_freq(theta_history, cfg.signal.sampling_freq);

    %% Create iteration axis
    num_iterations = length(theta_history);
    iteration_axis = 1:num_iterations;

    %% Create figure
    fig_handle = figure('Name', 'Frequency Tracking', 'NumberTitle', 'off');

    %% Plot frequency tracking
    plot(iteration_axis, freq_history, 'b-', 'LineWidth', 1.5);
    hold on;

    %% Add reference line for true frequency
    true_freq = cfg.signal.fundamental_freq;
    plot([1, num_iterations], [true_freq, true_freq], 'r--', ...
         'LineWidth', 1.0, 'DisplayName', 'True Frequency');
    hold off;

    %% Labels and styling
    xlabel('Iteration (n)', 'FontSize', 12);
    ylabel('Estimated Frequency (Hz)', 'FontSize', 12);
    title('LMS Frequency Tracking Convergence', 'FontSize', 14);
    legend('Estimated', 'True', 'Location', 'best');
    grid on;

    %% Set y-axis limits
    freq_min = min(freq_history);
    freq_max = max(freq_history);
    margin = 100;
    ylim([freq_min - margin, freq_max + margin]);

    %% Save figure if configured
    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['frequency_tracking.', cfg.output.figure_format]);
        saveas(fig_handle, output_path);
    end
end
