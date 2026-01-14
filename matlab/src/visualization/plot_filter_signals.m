function fig_handle = plot_filter_signals(y, cfg)
    %% Extract parameters
    num_samples = cfg.signal.num_samples + 1;
    num_subfilters = cfg.filter.num_subfilters;
    total_stages = num_subfilters + 1;

    %% Create sample index
    sample_index = 1:num_samples;

    %% Create figure with larger size for better vertical spacing
    fig_handle = figure('Name', 'Filter Signals', 'NumberTitle', 'off', ...
                        'Position', [100, 100, 1200, 1100]);

    % Calculate spacing to prevent overlap
    % Leave more space between subplots and at top for title
    bottom_margin = 0.05;
    top_margin = 0.08;  % Increased to prevent title cropping at top
    vertical_spacing = 0.08;
    subplot_height = (1 - bottom_margin - top_margin - (total_stages - 1) * vertical_spacing) / total_stages;

    %% Plot each stage
    for stage = 1:total_stages
        % Calculate position for each subplot with proper spacing
        bottom_pos = bottom_margin + (total_stages - stage) * (subplot_height + vertical_spacing);
        
        subplot('Position', [0.1, bottom_pos, 0.85, subplot_height]);
        plot(sample_index, y(stage, :), 'b-', 'LineWidth', 1.0);

        xlabel('Sample Index (n)', 'FontSize', 9);

        if stage == 1
            ylabel('x(n)', 'FontSize', 9);
            title('Input Signal', 'FontSize', 10);
        else
            ylabel(sprintf('y_{%d}(n)', stage - 1), 'FontSize', 9);
            title(sprintf('Output of Filter Stage %d', stage - 1), 'FontSize', 10);
        end

        grid on;
        
        % Set smaller font size for tick labels to prevent overlap
        set(gca, 'FontSize', 8);
    end

    %% Adjust layout (sgtitle not available in Octave, use figure name instead)

    %% Save figure if configured
    if cfg.output.save_figures
        output_path = fullfile(cfg.output.directory, ...
                               ['filter_signals.', cfg.output.figure_format]);
        saveas(fig_handle, output_path);
    end
end
