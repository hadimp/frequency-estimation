function theta = freq_to_theta(freq, sampling_freq)
    % FREQ_TO_THETA Convert frequency in Hz to normalized θ.
    %
    % Converts f (Hz) to θ = 2πf/fs (radians).
    %
    % Args:
    %   freq: Frequency in Hz
    %   sampling_freq: Sampling frequency fs (Hz)
    %
    % Returns:
    %   theta: Normalized frequency (radians)
    %
    % See also: THETA_TO_FREQ

    theta = 2 * pi * freq / sampling_freq;
end
