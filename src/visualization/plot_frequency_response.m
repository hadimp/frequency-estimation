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
    fig_stages = figure('Name', 'Individual Filter Responses', 'NumberTitle', 'off');

    for stage = 1:total_stages
        subplot(total_stages, 1, stage);
        plot(omega_norm, abs(H_stages(stage, :)), 'b-', 'LineWidth', 1.5);

        xlabel('\omega / \pi', 'FontSize', 10);
        ylabel('|H(f)|', 'FontSize', 10);
        title(sprintf('Stage %d: Notch at %d×f_1', stage, stage), 'FontSize', 12);
        ylim([0, 1.2]);
        grid on;
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

    H_db = 20 * log10(abs(H_total));
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
