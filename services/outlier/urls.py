from django.urls import path
from . import views
app_name = "outLiers_Data"

urlpatterns = [
    path('', views.outlier_detection, name='outlier_detection'),
    path("download/<str:excel_filename>", views.download_result, name="outlier_download"),
]
