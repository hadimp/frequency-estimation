function beta = compute_gradient(theta, y, cfg)
    %% Extract parameters
    num_subfilters = cfg.filter.num_subfilters;
    pole_radius = cfg.filter.pole_radius;
    num_samples = cfg.signal.num_samples;

    %% Initialize beta matrix
    % beta(m, n) stores the gradient at stage m, sample n
    beta_matrix = zeros(num_subfilters, num_samples);

    %% Compute gradient recursively through filter stages
    for stage = 2:num_subfilters
        harmonic_idx = stage - 1;

        % Precompute trigonometric terms for efficiency
        cos_term = cos(harmonic_idx * theta);
        sin_term = sin(harmonic_idx * theta);

        for n = 1:num_samples
            if n == 1
                % Initial condition: inherit from previous stage
                beta_matrix(stage, 1) = beta_matrix(stage - 1, 1);

            elseif n == 2
                % Second sample: partial recursion (n-2 terms are zero)
                beta_matrix(stage, 2) = ...
                    beta_matrix(stage - 1, 2) ...
                    - 2 * cos_term * beta_matrix(stage - 1, 1) ...
                    + 2 * harmonic_idx * sin_term * y(stage - 1, 1) ...
                    + 2 * pole_radius * cos_term * beta_matrix(stage, 1) ...
                    - 2 * pole_radius * harmonic_idx * sin_term * y(stage, 1);

            else
                % Full recursion for n >= 3
                beta_matrix(stage, n) = ...
                    beta_matrix(stage - 1, n) ...
                    - 2 * cos_term * beta_matrix(stage - 1, n - 1) ...
                    + 2 * harmonic_idx * sin_term * y(stage - 1, n - 1) ...
                    + beta_matrix(stage - 1, n - 2) ...
                    + 2 * pole_radius * cos_term * beta_matrix(stage, n - 1) ...
                    - (pole_radius^2) * beta_matrix(stage, n - 2) ...
                    - 2 * pole_radius * harmonic_idx * sin_term * y(stage, n - 1);
            end
        end
    end

    %% Return gradient at final stage
    beta = beta_matrix(num_subfilters, :);
end
