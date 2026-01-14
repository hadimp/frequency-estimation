function [fig_stages, fig_total, fig_db, fig_combined] = plot_frequency_response(theta, cfg)
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

    %% Figure 4: Combined frequency response plot (for README)
    fig_combined = figure('Name', 'Frequency Response Plot', 'NumberTitle', 'off', ...
                          'Position', [100, 100, 1200, 800]);

    % Top subplot: Individual stage responses
    subplot(2, 1, 1);
    colors = {'b', 'g', 'r', 'm'};
    fundamental_freq = theta_to_freq(theta, cfg.signal.sampling_freq);
    
    for stage = 1:num_subfilters
        plot(freq_axis, abs(H_stages(stage + 1, :)), '-', 'LineWidth', 1.5, ...
             'Color', colors{mod(stage - 1, length(colors)) + 1}, ...
             'DisplayName', sprintf('Stage %d', stage));
        hold on;
    end
    hold off;
    
    xlabel('Frequency (Hz)', 'FontSize', 11);
    ylabel('|H(f)|', 'FontSize', 11);
    title('Individual Notch Filter Responses', 'FontSize', 12);
    legend('Location', 'best', 'FontSize', 9);
    grid on;
    xlim([0, min(4000, cfg.signal.sampling_freq / 2)]);
    ylim([0, 1.2]);

    % Bottom subplot: Overall system response
    subplot(2, 1, 2);
    H_db_total = mag_to_db(H_total);
    plot(freq_axis, H_db_total, 'b-', 'LineWidth', 1.5);
    hold on;
    
    % Mark harmonic frequencies with vertical lines
    for m = 1:num_subfilters
        harmonic_freq = m * fundamental_freq;
        plot([harmonic_freq, harmonic_freq], ylim, 'r:', 'LineWidth', 1.0);
    end
    hold off;
    
    % Add text labels for harmonics without boxes
    y_min = min(H_db_total);
    y_max = max(H_db_total);
    y_pos = y_min + 0.1 * (y_max - y_min);
    
    for m = 1:num_subfilters
        harmonic_freq = m * fundamental_freq;
        text(harmonic_freq, y_pos, sprintf('%df₁', m), ...
             'HorizontalAlignment', 'center', 'FontSize', 10, ...
             'FontWeight', 'bold', 'Color', 'red');
    end
    
    xlabel('Frequency (Hz)', 'FontSize', 11);
    ylabel('|H(f)| (dB)', 'FontSize', 11);
    title('Overall System Frequency Response (Comb Filter)', 'FontSize', 12);
    grid on;
    xlim([0, min(4000, cfg.signal.sampling_freq / 2)]);
    ylim([y_min - 5, 5]);

    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['frequency_response_plot.', cfg.output.figure_format]);
        saveas(fig_combined, output_path);
    end
end
