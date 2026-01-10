% قراءة البيانات من JSON (مع مسار مطلق)
input_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\traffic_data.json';
fid = fopen(input_path, 'r');
if fid == -1
    error(['❌ Error: Could not open ', input_path]);
end
raw = fread(fid, '*char')';
fclose(fid);

% طباعة البيانات الخام للتحقق
fprintf('🔹 Raw JSON Content:\n%s\n', raw);

% التحقق من أن الملف ليس فارغًا
if isempty(raw)
    error('❌ JSON file is empty! Check your data source.');
end

% محاولة فك ترميز JSON
json_data = jsondecode(raw);

% استخراج القيم
user_id = json_data.user_id;
Inflows = json_data.inflows;
Outflows = json_data.outflows;
TM_Class = json_data.class; % يجب أن تكون 4x4

% التحقق من أبعاد TM_Class
fprintf('🔹 TM_Class size: [%d, %d]\n', size(TM_Class, 1), size(TM_Class, 2));

% التحقق من توازن التدفقات (من الكود الجديد)
InTotal = sum(Inflows);
OutTotal = sum(Outflows);
if abs(InTotal - OutTotal) > 1e-6
    avgTotal = (InTotal + OutTotal) / 2;
    Inflows = Inflows * avgTotal / InTotal;
    Outflows = Outflows * avgTotal / OutTotal;
end

% إعداد مصفوفة التوزيع الاحتمالي المحسن (من الكود الجديد)
Flow_Matrix = zeros(4, 4);
for i = 1:4
    total_flow = Inflows(i);
    class_weights = TM_Class(i, :) / max(sum(TM_Class(i, :)), 1); % استخدام max من الكود الجديد
    distributed_flow = total_flow * class_weights;
    for j = 1:4
        if TM_Class(i, j) > 0
            Flow_Matrix(i, j) = min(distributed_flow(j), Outflows(j));
        end
    end
end

% إعادة ضبط القيم لتحسين دقة التوزيع (من الكود الجديد)
for j = 1:4
    col_sum = sum(Flow_Matrix(:, j));
    if col_sum > 0
        Flow_Matrix(:, j) = Flow_Matrix(:, j) * (Outflows(j) / col_sum);
    end
end

% تحسين توزيع القيم لتجنب القيم غير المنطقية (من الكود الجديد)
for i = 1:4
    row_sum = sum(Flow_Matrix(i, :));
    if row_sum > 0
        Flow_Matrix(i, :) = Flow_Matrix(i, :) * (Inflows(i) / row_sum);
    end
end

% حساب الانحراف المعياري لكل نقطة (من الكود الجديد)
Standard_Deviation = std(Flow_Matrix, 0, 2);

% إعداد النتائج (مثل fourLeg.m)
results.user_id = user_id;
results.solution = round(Flow_Matrix);
results.standard_deviation = round(Standard_Deviation * 100) / 100;

% حفظ النتائج في JSON (مع مسار مطلق مثل fourLeg.m)
output_path = 'E:\\work from hom\\New folder (2)\\CEPAC\\storage\\app\\octave\\results.json';
json_text = jsonencode(results);
fid = fopen(output_path, 'w');
if fid == -1
    error(['❌ Error: Could not write to ', output_path]);
end
fwrite(fid, json_text);
fclose(fid);

fprintf('✅ Results saved to %s\n', output_path);
