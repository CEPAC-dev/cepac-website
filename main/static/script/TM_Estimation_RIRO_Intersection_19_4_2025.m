pkg load optim;  % تحميل حزمة linprog

% --- قراءة البيانات من ملف JSON بدون استخدام loadjson ---
input_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\inputRIRO.json';
fid = fopen(input_path, 'r');
if fid == -1
    error(['❌ Error: Could not open ', input_path]);
end
raw = fread(fid, '*char')';
fclose(fid);

if isempty(raw)
    error('❌ JSON file is empty! Check your data source.');
end

data = jsondecode(raw);

% --- استخراج البيانات ---
Inflows = data.Inflows(:);
Outflows = data.Outflows(:);
U_Turns = data.U_Turns(:);
TM_Class = data.TM_Class;

% --- تعديل التوازن بين In و Out ---
InTotal = sum(Inflows);
OutTotal = sum(Outflows);
if InTotal ~= OutTotal
    avTotal = mean([InTotal, OutTotal]);
    Inflows = Inflows * avTotal / InTotal;
    Outflows = Outflows * avTotal / OutTotal;
end


% --- ترتيب SN ---
SN = reshape(1:16, 4, 4)';  % مصفوفة 4x4

% --- تحديد الحدود العليا والدنيا ---
LB = zeros(16, 1);
UB = zeros(16, 1);
for i = 1:4
    for j = 1:4
        if TM_Class(i, j) ~= 0
            UB((i-1)*4 + j) = min(Inflows(i), Outflows(j));
        end
    end
end

% قيود الدوران U-Turn
U = U_Turns(1);
UB([10, 11, 14, 15, 1, 4, 5, 8]) = min(U, UB([10, 11, 14, 15, 1, 4, 5, 8]));

% --- قيود المساواة ---
Aeq = zeros(12, 16);
Beq = [Inflows; Outflows; U_Turns];

i1 = find(TM_Class(1,:) > 0); Aeq(1, i1) = 1;
i2 = 4 + find(TM_Class(2,:) > 0); Aeq(2, i2) = 1;
i3 = 8 + find(TM_Class(3,:) > 0); Aeq(3, i3) = 1;
i4 = 12 + find(TM_Class(4,:) > 0); Aeq(4, i4) = 1;

for k = 1:4
    j = find(TM_Class(:,k) ~= 0);
    Aeq(4 + k, SN(j,k)) = 1;
end

Aeq(9, [10 11 14 15]) = 1;
Aeq(10, 6) = 1;
Aeq(11, [1 4 5 8]) = 1;
Aeq(12, 16) = 1;

% --- قيود عدم المساواة ---
Ain = [];
Bin = [];
Ain0 = zeros(1, 16);
Classes = {TM_Class(1,:), TM_Class(2,:), TM_Class(3,:), TM_Class(4,:)};

for e = 1:4
    C = Classes{e};
    i1 = find(C == 1); i2 = find(C == 2); i3 = find(C == 3);
    for i = i2
        for j = i3
            temp = Ain0; temp(SN(e, i)) = 1; temp(SN(e, j)) = -1;
            Ain(end+1, :) = temp; Bin(end+1, 1) = 0;
        end
    end
    for i = i1
        for j = i3
            temp = Ain0; temp(SN(e, i)) = 1; temp(SN(e, j)) = -1;
            Ain(end+1, :) = temp; Bin(end+1, 1) = 0;
        end
    end
    for i = i1
        for j = i2
            temp = Ain0; temp(SN(e, i)) = 1; temp(SN(e, j)) = -1;
            Ain(end+1, :) = temp; Bin(end+1, 1) = 0;
        end
    end
end

R = [];
N = 100;
for i = 1:N
    f = -1 + 2 * rand(16, 1);  % متجه عشوائي
    [sol, fval] = linprog(f, Ain, Bin, Aeq, Beq, LB, UB);
    if ~isempty(sol)
        R(:, end+1) = sol;
    end
end


% --- إخراج النتائج ---




% --- إخراج النتائج ---
if isempty(R)
    Solution = [];
    Standard_Division = [];
else
    Solution = mean(R, 2);
    Standard_Division = std(R, 0, 2);
end

% --- حفظ النتائج في ملف JSON يدويًا ---
fid = fopen('E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\resultsRIRO.json', 'w');
fprintf(fid, '{\n');
if isempty(Solution)
    fprintf(fid, '  "Solution": "No valid solution",\n');
    fprintf(fid, '  "Standard_Division": "No valid solution"\n');
else
    fprintf(fid, '  "Solution": [%s],\n', num2str(Solution', '%.4f, '));
    fprintf(fid, '  "Standard_Division": [%s]\n', num2str(Standard_Division', '%.4f, '));
end
fprintf(fid, '}\n');
fclose(fid);

