function run_dynare_examples(dynare_matlab_dir, examples)
% Runs a selection of the examples shipped with a Dynare installation (MATLAB or Octave)
% and throws an error at the end if any of them failed.
%
% INPUTS
%   dynare_matlab_dir  path to the "matlab" folder of the Dynare installation
%   examples           (optional) cell array of .mod files relative to the "examples" folder
%
% Each example is run in a temporary copy of its folder, so that the installation stays untouched.
% Works with Dynare >= 7 (examples organized in subfolders).
% Examples with known problems under Octave are skipped (and reported) when running with Octave.

if nargin < 2 || isempty(examples)
    examples = {
        'stochastic_simulations/collard_2001_theoretical_moments.mod'
        'stochastic_simulations/collard_2001_simulated_moments.mod'
        'stochastic_simulations/nk_baseline.mod'
        'stochastic_simulations/aguiar_gopinath_2007_trend.mod'
        'perfect_foresight/perfect_foresight_rbc.mod'
        'perfect_foresight/perfect_foresight_expectation_errors.mod'
        'occbin/rbc_occbin.mod'
        'optimal_policy/nk_ramsey_steady_file.mod'
        'macroprocessor/bkk_1992.mod'
        'estimation/rbc_irf_matching.mod'
        'heterogeneity/krusell_smith_1998_steady_state.mod'
        };
end

% Known problems under Octave (checked with Dynare 7.1 and Octave 11.1.0)
octave_known_failures = {
    'estimation/rbc_irf_matching.mod', 'uses the legend property NumColumns, which Octave does not support'
    };

is_octave = exist('OCTAVE_VERSION', 'builtin') > 0;
dynare_matlab_dir = make_absolute(dynare_matlab_dir);
addpath(dynare_matlab_dir);
examples_dir = fullfile(fileparts(dynare_matlab_dir), 'examples');
if ~exist(examples_dir, 'dir')
    error('run_dynare_examples: examples folder not found: %s', examples_dir);
end

% dynare_version.m is part of the binary packages (in source builds it lives in the meson build folder)
if exist('dynare_version', 'file')
    dynver = dynare_version();
else
    dynver = '(source build)';
end
if is_octave
    fprintf('Running Dynare %s examples with Octave %s\n', dynver, OCTAVE_VERSION);
else
    fprintf('Running Dynare %s examples with MATLAB %s\n', dynver, version);
end

% Never open figure windows: on headless CI runners (e.g. Windows) Octave's FLTK toolkit hangs when a figure
% is created, even though the examples are run with the nograph option
set(0, 'defaultfigurevisible', 'off');
if is_octave && any(strcmp(available_graphics_toolkits(), 'gnuplot'))
    graphics_toolkit('gnuplot');
end

start_dir = pwd;
failed = {};
skipped = {};
for i = 1:numel(examples)
    [subdir, name] = fileparts(examples{i});
    known = find(strcmp(octave_known_failures(:, 1), examples{i}));
    if is_octave && ~isempty(known)
        fprintf('\n===== %s: SKIPPED (known Octave problem: %s) =====\n', examples{i}, octave_known_failures{known, 2});
        skipped{end+1} = examples{i}; %#ok<AGROW>
        continue
    end
    work_dir = tempname;
    copyfile(fullfile(examples_dir, subdir), work_dir);
    cd(work_dir);
    fprintf('\n===== %s =====\n', examples{i});
    t0 = tic;
    try
        dynare(name, 'console', 'nograph');
        fprintf('===== %s: OK (%.1fs) =====\n', examples{i}, toc(t0));
    catch err
        fprintf('===== %s: FAILED (%.1fs) =====\n%s\n', examples{i}, toc(t0), err.message);
        failed{end+1} = examples{i}; %#ok<AGROW>
    end
    cd(start_dir);
    close all
    clear global
end

fprintf('\n%d of %d examples passed, %d skipped\n', numel(examples) - numel(failed) - numel(skipped), numel(examples), numel(skipped));
if ~isempty(failed)
    error('run_dynare_examples: the following examples failed:\n  %s', strjoin(failed, '\n  '));
end
end

function p = make_absolute(p)
if ~(numel(p) > 1 && (p(1) == '/' || p(1) == '\' || p(2) == ':'))
    p = fullfile(pwd, p);
end
end
