function [initial_theta, mse_values, mse_first_values, theta_range] = find_initial_theta(cfg)
    %% Extract parameters
    num_points = cfg.lms.num_theta_points;
    num_subfilters = cfg.filter.num_subfilters;

    %% Define search range: θ ∈ [0, π/M]
    theta_range = linspace(0, pi / num_subfilters, num_points);

    %% Initialize MSE arrays
    mse_values = zeros(1, num_points);
    mse_first_values = zeros(1, num_points);
    running_average = 0;

    %% Compute MSE for each theta value
    for k = 1:num_points
        theta = theta_range(k);

        % Compute filter output
        y = compute_filter_output(theta, cfg);

        % Compute MSE values
        [mse_values(k), mse_first_values(k)] = compute_mse(y, cfg);

        % Update running average
        running_average = running_average + (mse_values(k) / num_points);
    end

    %% Find global minimum
    [min_mse, ~] = min(mse_values);

    %% Identify capture range
    % Points where both MSE curves are below average and near minimum
    tolerance_avg = 0.0001;
    tolerance_min = 0.2;

    in_capture_range = (mse_first_values - running_average < tolerance_avg) & ...
                       (mse_values - running_average < tolerance_avg) & ...
                       (mse_values - min_mse < tolerance_min);

    capture_thetas = theta_range(in_capture_range);

    %% Return initial estimate
    if isempty(capture_thetas)
        % Fallback: use theta at minimum MSE
        [~, min_idx] = min(mse_values);
        initial_theta = theta_range(min_idx);
        warning('Capture range not found. Using minimum MSE point.');
    else
        initial_theta = capture_thetas(1);
    end
end
