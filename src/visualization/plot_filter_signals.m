function fig_handle = plot_filter_signals(y, cfg)
    % PLOT_FILTER_SIGNALS Plot input signal and filter stage outputs.
    %
    % Multi-panel plot: input signal x(n) and outputs y_m(n) from each stage.
    %
    % Args:
    %   y: Filter outputs (M+1 x N+1)
    %   cfg: Configuration structure
    %
    % Returns:
    %   fig_handle: Figure handle

    %% Extract parameters
    num_samples = cfg.signal.num_samples + 1;
    num_subfilters = cfg.filter.num_subfilters;
    total_stages = num_subfilters + 1;

    %% Create sample index
    sample_index = 1:num_samples;

    %% Create figure
    fig_handle = figure('Name', 'Filter Signals', 'NumberTitle', 'off');

    %% Plot each stage
    for stage = 1:total_stages
        subplot(total_stages, 1, stage);
        plot(sample_index, y(stage, :), 'b-', 'LineWidth', 1.0);

        xlabel('Sample Index (n)', 'FontSize', 10);

        if stage == 1
            ylabel('x(n)', 'FontSize', 10);
            title('Input Signal', 'FontSize', 12);
        else
            ylabel(sprintf('y_{%d}(n)', stage - 1), 'FontSize', 10);
            title(sprintf('Output of Filter Stage %d', stage - 1), 'FontSize', 12);
        end

        grid on;
    end

    %% Adjust layout (sgtitle not available in Octave, use figure name instead)

    %% Save figure if configured
    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['filter_signals.', cfg.output.figure_format]);
        saveas(fig_handle, output_path);
    end
end
