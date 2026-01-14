function [mse_total, mse_first] = compute_mse(y, cfg)
    %% Extract parameters
    num_samples = cfg.signal.num_samples + 1;
    total_stages = cfg.filter.num_subfilters + 1;

    %% Compute MSE of final stage output
    % y(total_stages, :) contains the output after all M notch filters
    final_output = y(total_stages, :);
    mse_total = sum(final_output.^2) / num_samples;

    %% Compute MSE of first stage output
    % y(2, :) contains the output after just the first notch filter
    % This is useful for coarse frequency estimation
    first_output = y(2, :);
    mse_first = sum(first_output.^2) / num_samples;
end
