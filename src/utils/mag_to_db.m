function db_value = mag_to_db(magnitude)
    % MAG_TO_DB Convert magnitude to decibels.
    %
    % Uses MATLAB's mag2db from Signal Processing Toolbox if available,
    % otherwise falls back to manual calculation: dB = 20·log₁₀(|x|)
    %
    % Args:
    %   magnitude: Magnitude value(s)
    %
    % Returns:
    %   db_value: Value(s) in decibels

    % Try to use MATLAB's mag2db from Signal Processing Toolbox
    if exist('mag2db', 'builtin') || exist('mag2db', 'file')
        db_value = mag2db(magnitude);
    else
        % Fallback: manual calculation
        db_value = 20 * log10(abs(magnitude));
    end
end
