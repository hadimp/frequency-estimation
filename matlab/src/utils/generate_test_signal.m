function x = generate_test_signal(fundamental_freq, sampling_freq, num_samples)
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
