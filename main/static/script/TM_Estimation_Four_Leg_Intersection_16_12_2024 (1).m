% برنامج محسن لحساب تدفقات المرور عند التقاطع
% باستخدام توزيع احتمالي محسن يعتمد على نسب التدفقات والفئات

%% المدخلات
Inflows = [2070 2700 2170 1770]; % التدفقات الداخلة
Outflows = [1320 1870 2570 2950]; % التدفقات الخارجة

Class_E = [1 1 3 2];
Class_N = [2 1 2 3];
Class_W = [3 3 1 2];
Class_S = [2 3 3 1];

%% التحقق من توازن التدفقات
InTotal = sum(Inflows);
OutTotal = sum(Outflows);

if abs(InTotal - OutTotal) > 1e-6
    avgTotal = (InTotal + OutTotal) / 2;
    Inflows = Inflows * avgTotal / InTotal;
    Outflows = Outflows * avgTotal / OutTotal;
end

%% إعداد مصفوفة التوزيع الاحتمالي المحسن
TM_Class = [Class_E; Class_N; Class_W; Class_S];
Flow_Matrix = zeros(4, 4);

for i = 1:4
    total_flow = Inflows(i);
    class_weights = TM_Class(i, :) / max(sum(TM_Class(i, :)), 1);
    distributed_flow = total_flow * class_weights;
    for j = 1:4
        if TM_Class(i, j) > 0
            Flow_Matrix(i, j) = min(distributed_flow(j), Outflows(j));
        end
    end
end

%% إعادة ضبط القيم لتحسين دقة التوزيع
for j = 1:4
    col_sum = sum(Flow_Matrix(:, j));
    if col_sum > 0
        Flow_Matrix(:, j) = Flow_Matrix(:, j) * (Outflows(j) / col_sum);
    end
end

%% تحسين توزيع القيم لتجنب القيم غير المنطقية
for i = 1:4
    row_sum = sum(Flow_Matrix(i, :));
    if row_sum > 0
        Flow_Matrix(i, :) = Flow_Matrix(i, :) * (Inflows(i) / row_sum);
    end
end

%% حساب الانحراف المعياري لكل نقطة
Standard_Deviation = std(Flow_Matrix, 0, 2); % لكل نقطة على حدة

%% عرض النتائج
disp('Solution:');
disp(round(Flow_Matrix));
disp('Standard Deviation for each point:');
disp(Standard_Deviation);
