function freq = theta_to_freq(theta, sampling_freq)
    freq = theta * sampling_freq / (2 * pi);
end
