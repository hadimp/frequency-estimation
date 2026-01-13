function [theta_final, theta_history] = run_lms_algorithm(initial_theta, cfg)
    % RUN_LMS_ALGORITHM Execute LMS algorithm for frequency estimation.
    %
    % LMS update: θ(n+1) = θ(n) - 2μ·y_M(n)·β_M(n)
    % Minimizes MSE cost function J(θ) = E[y_M²(n)].
    %
    % Args:
    %   initial_theta: Initial frequency estimate (radians)
    %   cfg: Configuration structure
    %
    % Returns:
    %   theta_final: Final converged estimate
    %   theta_history: History of θ estimates (N x 1)

    %% Extract parameters
    step_size = cfg.lms.step_size;
    num_samples = cfg.signal.num_samples;
    num_subfilters = cfg.filter.num_subfilters;

    %% Initialize
    theta_current = initial_theta;
    theta_history = zeros(num_samples, 1);

    %% LMS iteration loop
    for iteration = 1:num_samples
        % Compute filter bank output for current theta estimate
        y = compute_filter_output(theta_current, cfg);

        % Compute gradient β_M(n)
        beta = compute_gradient(theta_current, y, cfg);
        beta_n = beta(iteration);

        % Get current output sample y_M(n)
        y_n = y(num_subfilters + 1, iteration);

        % LMS update: θ(n+1) = θ(n) - 2μ · y_M(n) · β_M(n)
        theta_current = theta_current - (2 * step_size * y_n * beta_n);

        % Store history
        theta_history(iteration) = theta_current;
    end

    theta_final = theta_current;
end
