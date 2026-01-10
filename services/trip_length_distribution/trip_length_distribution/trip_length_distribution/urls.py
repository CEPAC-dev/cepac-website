from django.urls import path
from . import views

app_name = "trip_length_distribution"

urlpatterns = [
    path("", views.index, name="index"),
    path("time/", views.time_entry, name="time"),
    path("run-octave/", views.send_to_octave, name="validation"),
    path("output/", views.output, name="output"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),
    path("download-excel/", views.download_excel, name="download_excel"),
]
