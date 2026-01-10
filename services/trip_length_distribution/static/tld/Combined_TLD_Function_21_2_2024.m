% Combined_TLD_Function_21_2_2024.m
% Accepts custom input and output paths as arguments
% Usage: Combined_TLD_Function_21_2_2024(input_path, output_dir)

function Combined_TLD_Function_21_2_2024(input_path, output_dir)
  % If no arguments provided, use default behavior for backward compatibility
  if nargin < 1
    media_root = getenv('MEDIA_ROOT');
    if isempty(media_root)
      base_dir = fileparts(mfilename('fullpath'));
      project_root = fullfile(base_dir, '..', '..', '..', '..', '..');
      media_root = fullfile(project_root, 'media');
    end
    input_path = fullfile(media_root, 'tld_data.json');
    output_dir = fullfile(media_root, 'TLD');
  end

  % Normalize separators
  input_path = strrep(input_path, '\', '/');
  output_dir = strrep(output_dir, '\', '/');

  % Ensure output directory exists
  if ~exist(output_dir, 'dir')
    mkdir(output_dir);
  end

  % Paths
  out_img = fullfile(output_dir, 'Fitting_Results.png');
  out_json = fullfile(output_dir, 'fitting_results.json');

  % Read input JSON
  if ~exist(input_path, 'file')
    error(['Input JSON not found: ' input_path]);
  end
  data = jsondecode(fileread(input_path));
  t = data(:, 1);
  f = data(:, 2);

  % Objective function for a * t^b * e^(c * t), normalized
  objective = @(params) sum( ...
    ((params(1) * t.^params(2) .* exp(params(3) * t)) ./ ...
      sum(params(1) * t.^params(2) .* exp(params(3) * t)) - f).^2 );

  % Initial guess [a, b, c]
  initial_guess = [1, 1, 1];

  % Optimize
  [opt_params, opt_SSE] = fminsearch(objective, initial_guess);
  a = opt_params(1);
  b = opt_params(2);
  c = opt_params(3);

  % Model + stats
  f_model = (a * t.^b .* exp(c * t)) ./ sum(a * t.^b .* exp(c * t));
  SSE = sum((f_model - f).^2);
  R2 = 1 - SSE / sum((f - mean(f)).^2);

  % Console output
  disp('Optimized Parameters:');
  disp(['a = ', num2str(a)]);
  disp(['b = ', num2str(b)]);
  disp(['c = ', num2str(c)]);
  disp(['R^2 = ', num2str(R2)]);

  % Results struct
  results = struct();
  results.inputs = struct('time', t, 'frequency', f);
  results.optimized_parameters = struct('a', a, 'b', b, 'c', c);
  results.statistics = struct('R2', R2, 'SSE', SSE);
  results.plot_image_link = fullfile(output_dir, 'Fitting_Results.png');

  % Plot and save image (headless)
  % Plot and save image (headless)
  fig = figure('visible','off');

  % إعداد بيانات الأعمدة جنب بعض
  Y = [f, f_model];  % مصفوفة (كل صف يمثل عمودين لنفس t)
  % ==== حساب الفترات (Intervals) من t ====
  if numel(t) > 1
    diff_t = diff(t);
    start_points = [t(1) - diff_t(1); t(1:end-1)];
  else
    % لو عندنا قيمة واحدة بس، نخلي الفترة تبدأ من الصفر
    start_points = 0;
  end
  end_points = t;

  % توليد تسميات الفترات كنصوص
  t_labels = arrayfun(@(s,e) sprintf('%g-%g', s, e), start_points, end_points, ...
                      'UniformOutput', false);

  % ==== رسم الأعمدة جنب بعض ====
  fig = figure('visible','off');

  Y = [f, f_model];              % مصفوفة القيم
  bar(t, Y, 'grouped');          % رسم الأعمدة جنب بعض

  % ضبط الألوان لكل مجموعة
  h = get(gca, 'Children');
  set(h(1), 'FaceColor', [0.5 0 0]); % f_model النبيتي
  set(h(2), 'FaceColor', [0 0 0.5]);   % f بالأزرق الغامق

  % تغيير تسميات المحور X إلى الفترات
  xticks(t);
  xticklabels(t_labels);

  % رسم خط الدالة فوق الأعمدة (اختياري)
  hold on;
  plot(t, f_model, 'r--', 'LineWidth', 2);

  legend('Surveyed TLD', 'Function (bar)', 'Function (line)', 'location', 'best');
  xlabel('Time Period');
  ylabel('Frequency');
  title('Fitting Results');
  grid on;

  saveas(fig, out_img);
  close(fig);



  % Save JSON
  fid = fopen(out_json, 'w');
  if fid < 0
    error(['Cannot open output JSON for writing: ' out_json]);
  end
  fprintf(fid, '%s', jsonencode(results));
  fclose(fid);

  disp(['Plot saved to: ', out_img]);
  disp(['Results saved to: ', out_json]);
end