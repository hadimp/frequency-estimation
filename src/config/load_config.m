function cfg = load_config(config_file)
    % LOAD_CONFIG Load configuration from file or return defaults.
    %
    % Args:
    %   config_file: (optional) Path to .mat file containing 'cfg' structure
    %
    % Returns:
    %   cfg: Configuration structure
    %
    % See also: DEFAULT_CONFIG, SAVE_CONFIG

    if nargin < 1 || isempty(config_file)
        cfg = default_config();
        return;
    end

    %% Load configuration from file
    if ~exist(config_file, 'file')
        warning('Config file not found: %s. Using defaults.', config_file);
        cfg = default_config();
        return;
    end

    loaded = load(config_file);
    if ~isfield(loaded, 'cfg')
        warning('Config file does not contain ''cfg'' variable. Using defaults.');
        cfg = default_config();
        return;
    end

    cfg = loaded.cfg;

    %% Merge with defaults to ensure all fields exist
    default_cfg = default_config();
    cfg = merge_structs(default_cfg, cfg);
end


function merged = merge_structs(base, override)
    % MERGE_STRUCTS Recursively merge two structs, with override taking precedence.
    %
    % Args:
    %   base: struct     - Base structure with default values
    %   override: struct - Override structure (values take precedence)
    %
    % Returns:
    %   merged: struct - Merged structure

    merged = base;
    fields = fieldnames(override);

    for i = 1:length(fields)
        field = fields{i};
        if isfield(base, field) && isstruct(base.(field)) && isstruct(override.(field))
            merged.(field) = merge_structs(base.(field), override.(field));
        else
            merged.(field) = override.(field);
        end
    end
end
