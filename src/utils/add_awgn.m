function noisy_signal = add_awgn(signal, snr_db)
    % ADD_AWGN Add Additive White Gaussian Noise to a signal.
    %
    % Adds AWGN at specified SNR: σ = √(P_signal / 10^(SNR_dB/10))
    % Octave-compatible (doesn't require Communications Toolbox).
    %
    % Args:
    %   signal: Input signal
    %   snr_db: Desired SNR in decibels
    %
    % Returns:
    %   noisy_signal: Signal with added noise

    %% Compute signal power
    signal_power = mean(signal.^2);

    %% Convert SNR from dB to linear scale
    snr_linear = 10^(snr_db / 10);

    %% Calculate required noise power
    noise_power = signal_power / snr_linear;

    %% Generate Gaussian noise with appropriate variance
    noise_std = sqrt(noise_power);
    noise = noise_std * randn(size(signal));

    %% Add noise to signal
    noisy_signal = signal + noise;
end
