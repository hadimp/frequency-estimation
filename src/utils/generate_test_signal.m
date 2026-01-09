function x = generate_test_signal(fundamental_freq, sampling_freq, num_samples)
    % GENERATE_TEST_SIGNAL Generate harmonic test signal.
    %
    % Creates: x(n) = sin(2πf₁n/fs) + 0.5·cos(2π·2f₁n/fs) - 0.25·cos(2π·3f₁n/fs)
    % Contains fundamental at f₁, 2nd harmonic at 2f₁, and 3rd harmonic at 3f₁.
    %
    % Args:
    %   fundamental_freq: Fundamental frequency f₁ (Hz)
    %   sampling_freq: Sampling frequency fs (Hz)
    %   num_samples: Number of samples N
    %
    % Returns:
    %   x: Generated test signal (1 x num_samples)

    %% Initialize output
    x = zeros(1, num_samples);

    %% Generate harmonic signal
    for n = 1:num_samples
        % Normalized frequency: ω₀ = 2πf₁/fs
        omega_0 = 2 * pi * fundamental_freq / sampling_freq;

        % Fundamental component: sin(ω₀n)
        fundamental = sin(omega_0 * n);

        % Second harmonic: 0.5·cos(2ω₀n)
        second_harmonic = 0.5 * cos(2 * omega_0 * n);

        % Third harmonic: -0.25·cos(3ω₀n)
        third_harmonic = -0.25 * cos(3 * omega_0 * n);

        % Sum all components
        x(n) = fundamental + second_harmonic + third_harmonic;
    end
end
