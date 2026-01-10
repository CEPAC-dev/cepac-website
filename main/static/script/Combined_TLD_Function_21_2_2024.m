% Resolve project media directory from this script's location
this_dir = fileparts(mfilename('fullpath'));
media_dir = fullfile(this_dir, '..', '..', '..', 'media');
media_dir = strrep(media_dir, '\', '/');  % Windows slash-fix

in_json  = fullfile(media_dir, 'tld_data.json');
out_png  = fullfile(media_dir, 'TLD', 'Fitting_Results.png');
out_json = fullfile(media_dir, 'TLD', 'fitting_results.json');

% Ensure TLD directory exists
tld_dir = fullfile(media_dir, 'TLD');
if ~exist(tld_dir, 'dir')
  mkdir(tld_dir);
end

% Read data
data = jsondecode(fileread(in_json));
t = data(:,1);
f = data(:,2);

objective = @(params) sum(((params(1)*t.^params(2).*exp(params(3)*t)) / ...
  sum(params(1)*t.^params(2).*exp(params(3)*t)) - f).^2);

initial_guess = [0.01, 1, -0.01];
[opt_params, opt_SSE] = fminsearch(objective, initial_guess);

a = opt_params(1); b = opt_params(2); c = opt_params(3);
f_model = (a * t.^b .* exp(c*t)) / sum(a * t.^b .* exp(c*t));
SSE = sum((f_model - f).^2);
R2 = 1 - SSE / sum((f - mean(f)).^2);

% Plot
figure('visible','off');
plot(t, f, 'r-', 'LineWidth', 2); hold on;
plot(t, f_model, 'b--', 'LineWidth', 2);
legend('Surveyed TLD', 'Model');
xlabel('Time'); ylabel('Frequency'); title('Fitting Results'); grid on;
saveas(gcf, out_png);

% Export json
results.inputs.time = t;
results.inputs.frequency = f;
results.optimized_parameters = struct('a', a, 'b', b, 'c', c);
results.statistics = struct('R2', R2, 'SSE', SSE);
results.plot_image_link = out_png;

fid = fopen(out_json, 'w');
fprintf(fid, jsonencode(results, 'PrettyPrint', true));
fclose(fid);
