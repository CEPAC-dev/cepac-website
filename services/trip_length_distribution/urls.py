from django.urls import path
from . import views

app_name = "trip_length_distribution"

urlpatterns = [
    # Choose a method first
    path("", views.choose_method, name="method_choice"),
    # Manual entry (form)
    path("manual/", views.index, name="manual"),
    path("time/", views.time_entry, name="time"),
    path("run-octave/", views.send_to_octave, name="validation"),
    # Excel upload flow
    path("upload-excel/", views.upload_excel_start, name="upload_excel"),
    path("upload-excel/select-column/", views.upload_excel_select_column, name="upload_excel_select_column"),
    path("upload-excel/generate-intervals/", views.upload_excel_generate_intervals, name="upload_excel_generate_intervals"),
    path("upload-excel/process/", views.upload_excel_process, name="upload_excel_process"),
    path("upload-excel-time/", views.upload_excel_time, name="upload_excel_time"),  # legacy redirect
    # Output
    path("output/", views.output, name="output"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),
    path("download-excel/", views.download_excel, name="download_excel"),
]
