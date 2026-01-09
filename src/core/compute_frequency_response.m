function [H_total, H_stages, freq_axis] = compute_frequency_response(theta, cfg)
    % COMPUTE_FREQUENCY_RESPONSE Compute frequency response H(ω) of filter bank.
    %
    % H_total = ∏_{m=1}^{M} H_m(e^{jω}) creates comb filter with notches at harmonics.
    %
    % Args:
    %   theta: Frequency parameter θ = 2πf₁/fs (radians)
    %   cfg: Configuration structure
    %
    % Returns:
    %   H_total: Total cascade response (normalized)
    %   H_stages: Individual stage responses (M+1 x num_freq_points)
    %   freq_axis: Frequency axis in Hz

    %% Extract parameters
    num_subfilters = cfg.filter.num_subfilters;
    pole_radius = cfg.filter.pole_radius;
    sampling_freq = cfg.signal.sampling_freq;
    num_points = cfg.lms.num_theta_points;

    total_stages = num_subfilters + 1;
    num_freq_points = num_points * 3;

    %% Define frequency axis
    omega = linspace(-pi, pi, num_freq_points);
    freq_axis = omega * sampling_freq / (2 * pi);

    %% Initialize outputs
    H_stages = zeros(total_stages, num_freq_points);
    H_total = ones(1, num_freq_points);

    %% Compute frequency response for each stage
    for stage = 1:total_stages
        harmonic_idx = stage;

        % Filter coefficients
        b = [1, -2*cos(harmonic_idx * theta), 1];
        a = [1, -2*pole_radius*cos(harmonic_idx * theta), pole_radius^2];

        % Compute frequency response
        [H, ~] = freqz(b, a, omega);

        % Normalize to unity at a reference point
        normalization = 1 / abs(H(num_points));
        H = H * normalization;

        % Store individual response
        H_stages(stage, :) = H;

        % Accumulate total response
        H_total = H_total .* H;
    end

    %% Normalize total response
    total_normalization = 1 / abs(H_total(num_points));
    H_total = H_total * total_normalization;
end
