function db_value = mag_to_db(magnitude)
    % Try to use MATLAB's mag2db from Signal Processing Toolbox
    if exist('mag2db', 'builtin') || exist('mag2db', 'file')
        db_value = mag2db(magnitude);
    else
        % Fallback: manual calculation
        db_value = 20 * log10(abs(magnitude));
    end
end
