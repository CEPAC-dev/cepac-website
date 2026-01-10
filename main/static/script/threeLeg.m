pkg load optim

% Read data from JSON
input_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\traffic_data_three.json';
try
    % Read and parse JSON file
    fid = fopen(input_path, 'r');
    if fid == -1
        error(['❌ Error: Could not open ', input_path]);
    end
    raw = fread(fid, '*char')';
    fclose(fid);

    if isempty(raw)
        error('❌ JSON file is empty! Check your data source.');
    end

    json_data = jsondecode(raw);

    % Extract and validate data
    user_id = json_data.user_id;
    Inflows = json_data.inflows(:)'; % Ensure row vector
    Outflows = json_data.outflows(:)'; % Ensure row vector
    TM_Class = json_data.class;

    % Validate matrix size (3x3 for three legs)
    [rows, cols] = size(TM_Class);
    if rows ~= 3 || cols ~= 3
        error('❌ TM_Class must be 3x3 for three-leg intersection');
    end

    % Flow balance adjustment
    InTotal = sum(Inflows);
    OutTotal = sum(Outflows);
    if abs(InTotal - OutTotal) > 1e-6
        avgTotal = (InTotal + OutTotal) / 2;
        Inflows = Inflows * avgTotal / InTotal;
        Outflows = Outflows * avgTotal / OutTotal;
    end

    % Prepare constraints
    Aeq = zeros(6,9);
    Beq = [Inflows'; Outflows'];

    % Set up equality constraints for inflows (rows)
    for i = 1:3
        Aeq(i, (i-1)*3+1:i*3) = 1;
    end

    % Set up equality constraints for outflows (columns)
    for j = 1:3
        Aeq(3+j, j:3:9) = 1;
    end

    % Optimization process - Octave compatible version
    R = [];
    N = 100; % Reduced iterations for faster execution

    for i = 1:N
        f = rand(9,1); % Random objective function

        % Octave's linprog has different syntax:
        [xopt, ~, err, ~] = linprog(f, [], [], Aeq, Beq, zeros(9,1), []);

        if err == 1 % Success
            R(:,end+1) = round(xopt);
        end
    end

    if isempty(R)
        error('No valid solution found after 100 iterations');
    end

    % Get the average solution
    final_solution = round(mean(R, 2));

    % Create output structure
    output = struct();
    output.message = "Script executed successfully";
    output.results = struct();
    output.results.solution = final_solution'; % Transpose to row vector

    % Save to JSON
    output_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\results_three.json';
    json_text = jsonencode(output, 'PrettyPrint', true);

    fid = fopen(output_path, 'w');
    if fid == -1
        error(['❌ Error: Could not write to ', output_path]);
    end
    fputs(fid, json_text);
    fclose(fid);

    fprintf('✅ Results successfully saved to %s\n', output_path);
    disp('Final Solution:');
    disp(final_solution');

catch err
    % Error handling
    error_output = struct();
    error_output.message = "Script execution failed";
    error_output.error = err.message;
    error_output.timestamp = datestr(now);

    % Save error information
    error_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\error_three.json';
    fid = fopen(error_path, 'w');
    if fid ~= -1
        fputs(fid, jsonencode(error_output));
        fclose(fid);
        fprintf('⚠️ Error details saved to %s\n', error_path);
    end

    % Re-throw error to see it in command window
    rethrow(err);
end
