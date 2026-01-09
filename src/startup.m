%% STARTUP SCRIPT FOR FREQUENCY ESTIMATION PROJECT
% =======================================================================
% This script sets up the MATLAB/Octave path for the frequency estimation
% project. Run this script once when starting a new session.
%
% Usage:
%   >> startup
%   >> run_frequency_estimation()
%
% =======================================================================

fprintf('Setting up Frequency Estimation project paths...\n');

%% Get the directory containing this script
script_dir = fileparts(mfilename('fullpath'));

%% Add all subdirectories to path
addpath(script_dir);
addpath(fullfile(script_dir, 'config'));
addpath(fullfile(script_dir, 'core'));
addpath(fullfile(script_dir, 'utils'));
addpath(fullfile(script_dir, 'visualization'));

%% Create output directory if needed
output_dir = fullfile(script_dir, '..', 'output');
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
    fprintf('Created output directory: %s\n', output_dir);
end

%% Display success message
fprintf('\n');
fprintf('=======================================================\n');
fprintf('  Frequency Estimation Project Ready\n');
fprintf('=======================================================\n');
fprintf('Available commands:\n');
fprintf('  run_frequency_estimation()     - Run with defaults\n');
fprintf('  cfg = config()                 - Get default config\n');
fprintf('  cfg = config(''file.mat'')      - Load config from file\n');
fprintf('  help <function_name>           - Get help for a function\n');
fprintf('=======================================================\n\n');
