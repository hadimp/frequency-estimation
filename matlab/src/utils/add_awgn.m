function noisy_signal = add_awgn(signal, snr_db)
    % Try to use MATLAB's awgn from Communications Toolbox
    if exist('awgn', 'builtin') || exist('awgn', 'file')
        noisy_signal = awgn(signal, snr_db);
    else
        % Fallback: manual implementation
        % σ = √(P_signal / 10^(SNR_dB/10))
        signal_power = mean(signal.^2);
        snr_linear = 10^(snr_db / 10);
        noise_power = signal_power / snr_linear;
        noise_std = sqrt(noise_power);
        noise = noise_std * randn(size(signal));
        noisy_signal = signal + noise;
    end
end
