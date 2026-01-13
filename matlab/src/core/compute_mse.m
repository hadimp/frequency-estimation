function [mse_total, mse_first] = compute_mse(y, cfg)
    % COMPUTE_MSE Compute Mean Squared Error of filter bank outputs.
    %
    % MSE = (1/N) Σ y_M(n)². When θ matches true frequency, MSE → 0.
    %
    % Args:
    %   y: Filter outputs (M+1 x N+1)
    %   cfg: Configuration structure
    %
    % Returns:
    %   mse_total: MSE of final filter stage
    %   mse_first: MSE of first filter stage

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
