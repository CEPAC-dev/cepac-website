
# import os
# import uuid
# import tempfile
# import base64
# from django.http import FileResponse, Http404
# from django.conf import settings
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill, Font, Alignment
# from openpyxl.drawing.image import Image as XLImage
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# import matplotlib
# matplotlib.use('Agg')


# # Temporary folder
# TMP_DIR = os.path.join(tempfile.gettempdir(), 'outlier_results')
# os.makedirs(TMP_DIR, exist_ok=True)
# TMP_DIR = "services/outlier/media"


# @login_required
# def outlier_detection(request):
#     if request.method == "POST":
#         if "file" not in request.FILES:
#             return render(request, "outlier/upload.html", {"error": "Please choose file"})

#         excel_file = request.FILES["file"]

#         # ============================ قراءة الملف ============================
#         try:
#             if excel_file.name.endswith(".csv"):
#                 df = pd.read_csv(excel_file)
#             else:
#                 df = pd.read_excel(excel_file)
#         except Exception as e:
#             return HttpResponse(f"Failed to read file: {e}")

#         # ============================ أعمدة الـ Rate ============================
#         rate_columns = [col for col in df.columns if 'rate' in col.lower()]
#         if not rate_columns:
#             return render(request, "outlier/upload.html", {"error": "No 'Rate' columns found"})

#         results = {}
#         if not os.path.exists(TMP_DIR):
#             os.makedirs(TMP_DIR)

#         # ============================ تحليل كل عمود ============================
#         for rate_col in rate_columns:
#             data = pd.to_numeric(df[rate_col], errors="coerce").dropna()
#             total = len(data)
#             if total < 3:
#                 continue

#             iteration = 0
#             current = data.copy()
#             global_outliers = pd.Series(False, index=data.index)
#             summary_rows = []

#             while True:
#                 mean_val = current.mean()
#                 std_val = current.std()

#                 # قاعدة ±2.5 انحراف معياري
#                 outliers = (current < mean_val - 2 * std_val) | (current > mean_val + 2* std_val)
#                 num_outliers = outliers.sum()

#                 summary_rows.append([
#                     f"Iteration {iteration + 1}",
#                     round(float(mean_val), 4),
#                     round(float(std_val), 4),
#                     int(num_outliers)
#                 ])

#                 if num_outliers == 0:
#                     break

#                 global_outliers.loc[outliers.index] = True
#                 current = current[~outliers]
#                 iteration += 1

#             cleaned_total = len(current)
#             total_outliers = total - cleaned_total
#             outlier_percentage = (total_outliers / total) * 100 if total > 0 else 0

#             # إضافة عمود الـ Outlier
#             df[f"Outlier_{rate_col}"] = global_outliers.astype(int)

#             # ============================ رسم البيانات ============================
#             plt.figure(figsize=(9, 4))
#             plt.scatter(range(len(data)), data, color="blue", label="Data")
#             plt.scatter(data[global_outliers].index, data[global_outliers], color="red", label="Outliers")
#             plt.axhline(y=current.mean(), color="green", linestyle="--", label="Mean (Final)")
#             plt.legend()
#             plt.title(f"Outlier Detection - {rate_col}")
#             plt.xlabel("Index")
#             plt.ylabel(rate_col)

#             buffer = BytesIO()
#             plt.savefig(buffer, format="png")
#             buffer.seek(0)
#             plot_data = base64.b64encode(buffer.getvalue()).decode()
#             plt.close()

#             # ============================ إنشاء ملف Excel ============================
#             excel_filename = f"{uuid.uuid4().hex}.xlsx"
#             excel_path = os.path.join(TMP_DIR, excel_filename)
#             df.to_excel(excel_path, sheet_name="Data", index=False)

#             book = load_workbook(excel_path)
#             ws = book["Data"]

#             # تلوين القيم الشاذة
#             red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
#             rate_idx = df.columns.get_loc(rate_col) + 1
#             outlier_idx = df.columns.get_loc(f"Outlier_{rate_col}")

#             for r in range(len(df)):
#                 if df.iloc[r, outlier_idx] == 1:
#                     ws.cell(row=r + 2, column=rate_idx).fill = red_fill

#             # ============================ ورقة Summary ============================
#             summary = book.create_sheet(f"Summary_{rate_col}")
#             summary["A1"] = "Iteration"
#             summary["B1"] = "Mean"
#             summary["C1"] = "Std"
#             summary["D1"] = "Outliers Found"

#             for row in summary_rows:
#                 summary.append(row)

#             # إحصائيات عامة في نهاية الـ Summary
#             summary.append([])
#             summary.append(["Total Values", total])
#             summary.append(["Cleaned Total", cleaned_total])
#             summary.append(["Total Outliers", total_outliers])
#             summary.append(["Outlier %", f"{outlier_percentage:.2f}%"])
#             summary.append(["Final Mean", round(float(current.mean()), 4)])
#             summary.append(["Final Std", round(float(current.std()), 4)])

#             # إدراج الصورة
#             png_path = os.path.join(TMP_DIR, f"{uuid.uuid4().hex}.png")
#             with open(png_path, "wb") as f:
#                 f.write(buffer.getvalue())
#             img = XLImage(png_path)
#             summary.add_image(img, "F2")

#             # تنسيق الأعمدة
#             summary.column_dimensions["A"].width = 20
#             summary.column_dimensions["B"].width = 15
#             summary.column_dimensions["C"].width = 15
#             summary.column_dimensions["D"].width = 18

#             book.save(excel_path)

#             results[rate_col] = {
#                 "cleaned_total": cleaned_total,
#                 "total": total,
#                 "total_outliers": total_outliers,
#                 "outlier_percentage": round(outlier_percentage, 2),
#                 "final_mean": round(float(current.mean()), 4),
#                 "final_std": round(float(current.std()), 4),
#                 "plot_data": plot_data,
#                 "iterations": summary_rows,
#                 "excel_filename": excel_filename,
#             }

#         if not results:
#             return render(request, "outlier/upload.html", {"error": "No columns have enough data (minimum 3 values required)"})

#         return render(
#             request,
#             "outlier/result.html",
#             {
#                 "results": results,
#                 "excel_filename": excel_filename,  
#             }
#         )
#     return render(request, "outlier/upload.html")



# # ============================ تحميل ملف النتيجة ============================
# def download_result(request, excel_filename):
#     # مجلد حفظ نتائج outliers المؤقت
#     TMP_DIR = "services/outlier/media"
#     safe_path = os.path.join(TMP_DIR, excel_filename)

#     # حماية المسار
#     safe_path = os.path.normpath(safe_path)
#     if not safe_path.startswith(os.path.abspath(TMP_DIR)):
#         raise Http404("Unauthorized file access")

#     # التأكد من وجود الملف
#     if not os.path.exists(safe_path):
#         raise Http404("File not found")

#     # إرسال الملف كـ تحميل
#     response = FileResponse(open(safe_path, "rb"), as_attachment=True)
#     response["Content-Disposition"] = f'attachment; filename="{excel_filename}"'
#     return response































# # import os
# # import uuid
# # import tempfile
# # import base64
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from io import BytesIO
# # from openpyxl import load_workbook
# # from openpyxl.drawing.image import Image as XLImage
# # from django.shortcuts import render
# # from django.http import HttpResponse
# # import matplotlib
# # matplotlib.use('Agg')
# # from django.contrib.auth.decorators import login_required

# # # Temporary folder
# # TMP_DIR = os.path.join(tempfile.gettempdir(), 'outlier_results')
# # os.makedirs(TMP_DIR, exist_ok=True)

# # TMP_DIR = "media/tmp"  


# # @login_required 








# # def outlier_detection(request):
# #     if request.method == "POST":
# #         if "file" not in request.FILES:
# #             return  render(request, "outlier/upload.html", {"error": "Please choose file "})

# #         excel_file = request.FILES["file"]

# #         # Read Excel or CSV file
# #         try:
# #             if excel_file.name.endswith(".csv"):
# #                 df = pd.read_csv(excel_file)
# #             else:
# #                 df = pd.read_excel(excel_file)
# #         except Exception as e:
# #             return HttpResponse(f"Failed to read file: {e}")

# #         # Find all columns that contain 'Rate' (case insensitive)
# #         rate_columns = [col for col in df.columns if 'rate' in col.lower()]
# #         if not rate_columns:
# #             return render(request, "outlier/upload.html", {"error": "No columns named 'Rate' found"})

# #         results = {}
# #         for rate_col in rate_columns:
# #             data = df[rate_col].dropna()
# #             total = len(data)
# #             if total < 3:
# #                 continue

# #             summary_rows = []
# #             iteration = 0
# #             current = data.copy()
# #             global_outliers = pd.Series(False, index=data.index)

# #             while True:
# #                 mean_val = current.mean()
# #                 std_val = current.std()

# #                 # Detect outliers using 2.5 standard deviation rule
# #                 outliers = (current < mean_val - 2* std_val) | (current > mean_val + 2* std_val)
# #                 num_outliers = outliers.sum()

# #                 summary_rows.append([
# #                     f"Iteration {iteration + 1}",
# #                     round(float(mean_val), 4),
# #                     round(float(std_val), 4),
# #                     int(num_outliers)
# #                 ])

# #                 if num_outliers == 0:
# #                     break

# #                 global_outliers.loc[outliers.index] = global_outliers.loc[outliers.index] | outliers
# #                 current = current[~outliers]
# #                 iteration += 1

# #             cleaned_total = len(current)

# #             # Plot data with outliers
# #             plt.figure(figsize=(10, 5))
# #             plt.scatter(range(len(data)), data, color="blue", label="Data")
# #             plt.scatter(data[global_outliers].index, data[global_outliers], color="red", label="Outliers")
# #             plt.axhline(y=current.mean(), color="green", linestyle="--", label="Mean (Final)")
# #             plt.legend()
# #             plt.title(f"Outlier Detection for {rate_col}")
# #             plt.xlabel("Index")
# #             plt.ylabel(rate_col)
# #             buffer = BytesIO()
# #             plt.savefig(buffer, format="png")
# #             buffer.seek(0)
# #             plot_data = base64.b64encode(buffer.getvalue()).decode()
# #             plt.close()

# #             total_outliers = total - cleaned_total
# #             outlier_percentage = (total_outliers / total) * 100 if total > 0 else 0

# #             df[f"Outlier_{rate_col}"] = global_outliers.astype(int)

# #             if not os.path.exists(TMP_DIR):
# #                 os.makedirs(TMP_DIR)
# #             excel_filename = f"{uuid.uuid4().hex}.xlsx"
# #             excel_path = os.path.join(TMP_DIR, excel_filename)

# #             df.to_excel(excel_path, sheet_name="Data", index=False)

# #             book = load_workbook(excel_path)
# #             summary = book.create_sheet(f"Summary_{rate_col}")
# #             summary["A1"] = "Iteration"
# #             summary["B1"] = "Mean"
# #             summary["C1"] = "Std"
# #             summary["D1"] = "Outliers Found"

# #             for row in summary_rows:
# #                 summary.append(row)

# #             png_filename = f"{uuid.uuid4().hex}.png"
# #             png_path = os.path.join(TMP_DIR, png_filename)
# #             with open(png_path, "wb") as f:
# #                 f.write(buffer.getvalue())

# #             img = XLImage(png_path)
# #             summary.add_image(img, "F2")

# #             book.save(excel_path)

# #             results[rate_col] = {
# #                 "cleaned_total": cleaned_total,
# #                 "plot_data": plot_data,
# #                 "iterations": summary_rows,
# #                 "final_mean": round(float(current.mean()), 4) if cleaned_total > 0 else "N/A",
# #                 "final_std": round(float(current.std()), 4) if cleaned_total > 0 else "N/A",
# #                 "total": total,
# #                 "total_outliers": total_outliers,
# #                 "outlier_percentage": round(outlier_percentage, 2),
# #                 "excel_filename": excel_filename
# #             }
# #         if not results:
# #             return render(request, "outlier/upload.html", {"error": "No columns have enough data (minimum 3 values required)"})

# #         print(results)

# #         # return render(request, 'outlier/result.html', {"results": results})

# #     return render(request, "outlier/upload.html")







# # # def outlier_detection(request):
# # #     if request.method == "POST":
# # #         excel_file = request.FILES["file"]

# # #         # ============================
# # #         #  (CSV أو Excel)
# # #         # ============================
# # #         try:
# # #             if excel_file.name.endswith(".csv"):
# # #                 df = pd.read_csv(excel_file)
# # #             else:
# # #                 df = pd.read_excel(excel_file)
# # #         except Exception as e:
# # #             return HttpResponse(f"Failed to read file: {e}")

# # #         # ============================
# # #         # "Rate"
# # #         # ============================
# # #         rate_cols = [c for c in df.columns if str(c).startswith("Rate")]
# # #         if not rate_cols:
# # #             return render(request, "outlier.html", {"error": "No columns start with 'Rate' found."})

# # #         summary_rows = []
# # #         plot_images = []

# # #         if not os.path.exists(TMP_DIR):
# # #             os.makedirs(TMP_DIR)

# # #         # ============================
# # #         # 3️⃣ تحليل كل عمود على حدة
# # #         # ============================
# # #         for col in rate_cols:
# # #             data = pd.to_numeric(df[col], errors="coerce").dropna()
# # #             if len(data) < 3:
# # #                 continue

# # #             iteration = 0
# # #             current = data.copy()
# # #             global_outliers = pd.Series(False, index=data.index)

# # #             while True:
# # #                 mean_val = current.mean()
# # #                 std_val = current.std()

# # #                 outliers = (current < mean_val - 2.5 * std_val) | (current > mean_val + 2.5 * std_val)
# # #                 num_outliers = outliers.sum()

# # #                 summary_rows.append([
# # #                     f"{col} - Iter {iteration + 1}",
# # #                     round(float(mean_val), 4),
# # #                     round(float(std_val), 4),
# # #                     int(num_outliers)
# # #                 ])

# # #                 if num_outliers == 0:
# # #                     break

# # #                 global_outliers.loc[outliers.index] = global_outliers.loc[outliers.index] | outliers
# # #                 current = current[~outliers]
# # #                 iteration += 1

# # #             # === Plot لكل عمود ===
# # #             plt.figure(figsize=(9, 4))
# # #             plt.scatter(range(len(data)), data, color="blue", label="Data")
# # #             plt.scatter(data[global_outliers].index, data[global_outliers], color="red", label="Outliers")
# # #             plt.axhline(y=current.mean(), color="green", linestyle="--", label="Mean (Final)")
# # #             plt.legend()
# # #             plt.title(f"Outlier Detection - {col}")
# # #             plt.xlabel("Index")
# # #             plt.ylabel(col)

# # #             buffer = BytesIO()
# # #             plt.savefig(buffer, format="png")
# # #             buffer.seek(0)
# # #             plot_data = base64.b64encode(buffer.getvalue()).decode()
# # #             plot_images.append((col, plot_data))
# # #             plt.close()

# # #             # إضافة عمود Outlier
# # #             df[f"{col}_Outlier"] = global_outliers.astype(int)

# # #         # ============================
# # #         # 4️⃣ إنشاء ملف Excel
# # #         # ============================
# # #         excel_filename = f"{uuid.uuid4().hex}.xlsx"
# # #         excel_path = os.path.join(TMP_DIR, excel_filename)
# # #         df.to_excel(excel_path, sheet_name="Data", index=False)

# # #         book = load_workbook(excel_path)
# # #         summary = book.create_sheet("Summary")

# # #         summary["A1"] = "Column / Iteration"
# # #         summary["B1"] = "Mean"
# # #         summary["C1"] = "Std"
# # #         summary["D1"] = "Outliers Found"

# # #         for row in summary_rows:
# # #             summary.append(row)

# # #         # إدراج الصور في الشيت
# # #         for idx, (col, plot_data) in enumerate(plot_images):
# # #             png_path = os.path.join(TMP_DIR, f"{uuid.uuid4().hex}.png")
# # #             with open(png_path, "wb") as f:
# # #                 f.write(base64.b64decode(plot_data))
# # #             img = XLImage(png_path)
# # #             summary.add_image(img, f"F{2 + idx * 20}")

# # #         book.save(excel_path)

# # #         # ============================
# # #         # 5️⃣ إرسال النتائج للواجهة
# # #         # ============================
# # #         context = {
# # #             "rate_cols": rate_cols,
# # #             "plots": plot_images,
# # #             "summary": summary_rows,
# # #             "excel_filename": excel_filename,
# # #         }

# # #         return render(request, "outlier/result.html", context)

# # #     return render(request, "outlier/upload.html")




















# # def download_result(request, filename):
# #     safe_path = os.path.join(TMP_DIR, filename)
# #     if not os.path.exists(safe_path):
# #         return HttpResponse("File not found or expired.", status=404)

# #     with open(safe_path, "rb") as f:
# #         data = f.read()

# #     response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# #     response['Content-Disposition'] = 'attachment; filename="outliers.xlsx"'

# #     try:
# #         os.remove(safe_path)
# #     except Exception:
# #         pass

# #     return response









import os
import uuid
import base64
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.drawing.image import Image as XLImage

# Base temporary folder

TMP_DIR_BASE = "services/outlier/media"
os.makedirs(TMP_DIR_BASE, exist_ok=True)

@login_required
def outlier_detection(request):
    if request.method == "POST":
        if "file" not in request.FILES:
          return render(request, "outlier/upload.html", {"error": "Please choose a file."})

        excel_file = request.FILES["file"]

        try:
            if excel_file.name.endswith(".csv"):
                df = pd.read_csv(excel_file)
            else:
                df = pd.read_excel(excel_file)
        except Exception as e:
            return HttpResponse(f"Failed to read file: {e}")

        rate_columns = [col for col in df.columns if 'rate' in col.lower()]
        if not rate_columns:
            return render(request, "outlier/upload.html", {"error": "No 'Rate' columns found."})

        # Create a unique temporary folder for this processing
        user_tmp_dir = os.path.join(TMP_DIR_BASE, str(request.user.id), str(uuid.uuid4().hex))
        os.makedirs(user_tmp_dir, exist_ok=True)

        results = {}

        for rate_col in rate_columns:
            data = pd.to_numeric(df[rate_col], errors="coerce").dropna()
            if len(data) < 3:
                continue

            iteration = 0
            current = data.copy()
            global_outliers = pd.Series(False, index=data.index)
            summary_rows = []

            while True:
                mean_val = current.mean()
                std_val = current.std()

                outliers = (current < mean_val - 2*std_val) | (current > mean_val + 2*std_val)
                num_outliers = outliers.sum()

                summary_rows.append([
                    f"Iteration {iteration + 1}",
                    round(float(mean_val), 4),
                    round(float(std_val), 4),
                    int(num_outliers)
                ])

                if num_outliers == 0:
                    break

                global_outliers.loc[outliers.index] = True
                current = current[~outliers]
                iteration += 1

            df[f"Outlier_{rate_col}"] = global_outliers.astype(int)

            # Plot data
            plt.figure(figsize=(9, 4))
            plt.scatter(range(len(data)), data, color="blue", label="Data")
            plt.scatter(data[global_outliers].index, data[global_outliers], color="red", label="Outliers")
            plt.axhline(y=current.mean(), color="green", linestyle="--", label="Mean (Final)")
            plt.legend()
            plt.title(f"Outlier Detection - {rate_col}")
            plt.xlabel("Index")
            plt.ylabel(rate_col)
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

            # Create Excel if not exists yet
            excel_filename = f"{uuid.uuid4().hex}.xlsx"
            excel_path = os.path.join(user_tmp_dir, excel_filename)
            if not os.path.exists(excel_path):
                df.to_excel(excel_path, sheet_name="Data", index=False)
            book = load_workbook(excel_path)
            ws = book["Data"]

            # Highlight outliers
            red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            rate_idx = df.columns.get_loc(rate_col) + 1
            outlier_idx = df.columns.get_loc(f"Outlier_{rate_col}") + 1
            for r in range(len(df)):
                if df.iloc[r, outlier_idx - 1] == 1:
                    ws.cell(row=r + 2, column=rate_idx).fill = red_fill

            # Summary sheet
            summary = book.create_sheet(f"Summary_{rate_col}")
            summary["A1"], summary["B1"], summary["C1"], summary["D1"] = "Iteration", "Mean", "Std", "Outliers Found"
            for row in summary_rows:
                summary.append(row)

            # Insert plot image from memory
            img = XLImage(buffer)
            summary.add_image(img, "F2")

            # Format columns
            summary.column_dimensions["A"].width = 20
            summary.column_dimensions["B"].width = 15
            summary.column_dimensions["C"].width = 15
            summary.column_dimensions["D"].width = 18

            book.save(excel_path)

            # Save results for frontend
            cleaned_total = len(current)
            total = len(data)
            total_outliers = total - cleaned_total
            outlier_percentage = (total_outliers / total) * 100 if total > 0 else 0

            results[rate_col] = {
                "cleaned_total": cleaned_total,
                "total": total,
                "total_outliers": total_outliers,
                "outlier_percentage": round(outlier_percentage, 2),
                "final_mean": round(float(current.mean()), 4),
                "final_std": round(float(current.std()), 4),
                "plot_data": plot_data,
                "iterations": summary_rows,
                "excel_filename": excel_filename,
                "tmp_folder": user_tmp_dir
            }

        if not results:
            return render(request, "outlier/upload.html", {"error": "No columns have enough data (minimum 3 values)."})

        return render(request, "outlier/result.html", {
            "results": results,
            "excel_filename": excel_filename,
        })
    return render(request, "outlier/upload.html")

    
@login_required
def download_result(request, excel_filename):
    # The request can include the tmp_folder for safety
    tmp_folder = request.GET.get("tmp_folder")
    if not tmp_folder:
        raise Http404("Temporary folder not specified.")

    
    safe_path = os.path.join(tmp_folder, excel_filename)
    safe_path = os.path.normpath(safe_path)
    if not os.path.exists(safe_path):
        raise Http404("File not found")

    response = FileResponse(open(safe_path, "rb"), as_attachment=True)
    response["Content-Disposition"] = f'attachment; filename="{excel_filename}"'
    return response
    
