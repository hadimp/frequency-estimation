function freq = theta_to_freq(theta, sampling_freq)
    % THETA_TO_FREQ Convert normalized frequency θ to Hz.
    %
    % Converts θ = 2πf/fs (radians) to f = θ·fs/(2π) (Hz).
    %
    % Args:
    %   theta: Normalized frequency (radians)
    %   sampling_freq: Sampling frequency fs (Hz)
    %
    % Returns:
    %   freq: Frequency in Hz
    %
    % See also: FREQ_TO_THETA

    freq = theta * sampling_freq / (2 * pi);
end
