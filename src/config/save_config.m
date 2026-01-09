function save_config(cfg, filename)
    % SAVE_CONFIG Save configuration structure to MAT file.
    %
    % Args:
    %   cfg: Configuration structure to save
    %   filename: Path to save the configuration
    %
    % See also: LOAD_CONFIG, DEFAULT_CONFIG

    if nargin < 2
        error('Both cfg and filename arguments are required.');
    end

    save(filename, 'cfg');
    fprintf('Configuration saved to: %s\n', filename);
end
