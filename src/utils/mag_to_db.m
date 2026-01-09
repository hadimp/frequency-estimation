function db_value = mag_to_db(magnitude)
    % MAG_TO_DB Convert magnitude to decibels.
    %
    % Converts magnitude to dB: dB = 20·log₁₀(|x|)
    % Octave-compatible replacement for MATLAB's mag2db.
    %
    % Args:
    %   magnitude: Magnitude value(s)
    %
    % Returns:
    %   db_value: Value(s) in decibels

    db_value = 20 * log10(abs(magnitude));
end
