function fig_handle = plot_mse_analysis(theta_range, mse_values, mse_first_values, cfg)
    % PLOT_MSE_ANALYSIS Plot MSE analysis over frequency range.
    %
    % Plots MSE(θ), MSE₁(θ), and average MSE to visualize cost function landscape.
    %
    % Args:
    %   theta_range: Theta values (radians)
    %   mse_values: Total MSE values
    %   mse_first_values: First-stage MSE values
    %   cfg: Configuration structure
    %
    % Returns:
    %   fig_handle: Figure handle

    %% Convert theta to frequency for x-axis
    freq_axis = theta_to_freq(theta_range, cfg.signal.sampling_freq);

    %% Calculate running average
    avg_mse = mean(mse_values);

    %% Create figure
    fig_handle = figure('Name', 'MSE Analysis', 'NumberTitle', 'off');

    %% Plot MSE curves
    plot(freq_axis, mse_values, 'b-', 'LineWidth', 1.5, 'DisplayName', 'MSE (Total)');
    hold on;
    plot(freq_axis, mse_first_values, 'r-', 'LineWidth', 1.5, 'DisplayName', 'MSE₁ (First Stage)');
    plot([freq_axis(1), freq_axis(end)], [avg_mse, avg_mse], 'k--', ...
         'LineWidth', 1.0, 'DisplayName', 'Average MSE');
    hold off;

    %% Labels and styling
    xlabel('Frequency (Hz)', 'FontSize', 12);
    ylabel('Mean Squared Error', 'FontSize', 12);
    title('MSE Analysis: Cost Function vs. Frequency', 'FontSize', 14);
    legend('Location', 'best');
    grid on;

    %% Save figure if configured
    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['mse_analysis.', cfg.output.figure_format]);
        saveas(fig_handle, output_path);
    end
end
