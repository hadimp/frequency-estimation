function y = compute_filter_output(theta, cfg)
    % COMPUTE_FILTER_OUTPUT Compute cascaded notch filter bank output.
    %
    % Processes signal through M cascaded IIR notch filters:
    % H_m(z) = (1 - 2cos(mθ)z⁻¹ + z⁻²) / (1 - 2r·cos(mθ)z⁻¹ + r²z⁻²)
    % Each filter rejects the m-th harmonic. Output y_M(n) should be minimized.
    %
    % Args:
    %   theta: Estimated frequency θ = 2πf₁/fs (radians)
    %   cfg: Configuration structure
    %
    % Returns:
    %   y: Filter outputs (M+1 x N+1), y(1,:)=input, y(m,:)=stage m-1 output

    %% Extract parameters from config
    num_subfilters = cfg.filter.num_subfilters;
    pole_radius = cfg.filter.pole_radius;
    num_samples = cfg.signal.num_samples + 1;
    fundamental_freq = cfg.signal.fundamental_freq;
    sampling_freq = cfg.signal.sampling_freq;
    add_noise = cfg.signal.add_noise;
    snr_db = cfg.signal.snr_db;

    total_stages = num_subfilters + 1;

    %% Generate input test signal
    input_signal = generate_test_signal(fundamental_freq, sampling_freq, num_samples);

    %% Add noise if requested
    if add_noise
        % Add AWGN: σ = √(P_signal / 10^(SNR_dB/10))
        signal_power = mean(input_signal.^2);
        snr_linear = 10^(snr_db / 10);
        noise_std = sqrt(signal_power / snr_linear);
        input_signal = input_signal + noise_std * randn(size(input_signal));
    end

    %% Initialize output matrix
    % Row 1: input signal
    % Row m+1: output of m-th filter stage
    y = zeros(total_stages, num_samples);

    %% Process through cascaded filter bank
    for stage = 1:total_stages
        if stage == 1
            % First row stores the input signal
            y(1, :) = input_signal;
        else
            % Apply m-th notch filter (m = stage - 1)
            harmonic_index = stage - 1;

            % Filter coefficients for H_m(z)
            % Numerator: b = [1, -2cos(mθ), 1]
            % Denominator: a = [1, -2r·cos(mθ), r²]
            b = [1, -2*cos(harmonic_index * theta), 1];
            a = [1, -2*pole_radius*cos(harmonic_index * theta), pole_radius^2];

            % Filter the output from previous stage
            y(stage, :) = filter(b, a, y(stage - 1, :));
        end
    end
end
