function [fig_stages, fig_total, fig_db] = plot_frequency_response(theta, cfg)
    % PLOT_FREQUENCY_RESPONSE Plot frequency response of filter bank.
    %
    % Creates three figures: individual stage responses, overall (linear), overall (dB).
    %
    % Args:
    %   theta: Converged frequency estimate (radians)
    %   cfg: Configuration structure
    %
    % Returns:
    %   fig_stages: Individual stage responses figure
    %   fig_total: Overall response (linear) figure
    %   fig_db: Overall response (dB) figure

    %% Compute frequency response
    [H_total, H_stages, freq_axis] = compute_frequency_response(theta, cfg);

    %% Extract parameters
    num_subfilters = cfg.filter.num_subfilters;
    total_stages = num_subfilters + 1;

    %% Normalize frequency axis
    omega = freq_axis * 2 * pi / cfg.signal.sampling_freq;
    omega_norm = omega / pi;

    %% Figure 1: Individual stage responses
    % Use larger figure size for better vertical spacing
    fig_stages = figure('Name', 'Individual Filter Responses', 'NumberTitle', 'off', ...
                        'Position', [100, 100, 1200, 1100]);

    % Calculate spacing to prevent overlap
    % Leave more space between subplots and at top for title
    bottom_margin = 0.05;
    top_margin = 0.08;  % Increased to prevent title cropping at top
    vertical_spacing = 0.08;
    subplot_height = (1 - bottom_margin - top_margin - (total_stages - 1) * vertical_spacing) / total_stages;

    for stage = 1:total_stages
        % Calculate position for each subplot with proper spacing
        bottom_pos = bottom_margin + (total_stages - stage) * (subplot_height + vertical_spacing);
        
        subplot('Position', [0.1, bottom_pos, 0.85, subplot_height]);
        plot(omega_norm, abs(H_stages(stage, :)), 'b-', 'LineWidth', 1.5);

        xlabel('\omega / \pi', 'FontSize', 9);
        ylabel('|H(f)|', 'FontSize', 9);
        title(sprintf('Stage %d: Notch at %d×f_1', stage, stage), 'FontSize', 10);
        ylim([0, 1.2]);
        grid on;
        
        % Set smaller font size for tick labels to prevent overlap
        set(gca, 'FontSize', 8);
    end

    %% sgtitle not available in Octave - title set in figure name

    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['stage_responses.', cfg.output.figure_format]);
        saveas(fig_stages, output_path);
    end

    %% Figure 2: Overall response (linear scale, Hz)
    fig_total = figure('Name', 'Overall System Response', 'NumberTitle', 'off');

    plot(freq_axis, abs(H_total), 'b-', 'LineWidth', 1.5);

    xlabel('Frequency (Hz)', 'FontSize', 12);
    ylabel('|H(f)|', 'FontSize', 12);
    title('Overall System Frequency Response', 'FontSize', 14);
    ylim([0, 1.2]);
    grid on;

    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['overall_response.', cfg.output.figure_format]);
        saveas(fig_total, output_path);
    end

    %% Figure 3: Overall response (dB scale)
    fig_db = figure('Name', 'Overall System Response (dB)', 'NumberTitle', 'off');

    H_db = mag_to_db(H_total);
    plot(freq_axis, H_db, 'b-', 'LineWidth', 1.5);

    xlabel('Frequency (Hz)', 'FontSize', 12);
    ylabel('|H(f)| (dB)', 'FontSize', 12);
    title('Overall System Frequency Response (Decibels)', 'FontSize', 14);
    grid on;

    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['overall_response_db.', cfg.output.figure_format]);
        saveas(fig_db, output_path);
    end
end
