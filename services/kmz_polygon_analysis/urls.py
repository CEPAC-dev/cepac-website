from django.urls import path
from . import views

app_name = "kmz_polygon_analysis"

urlpatterns = [
    path("", views.form_view, name="form"),
]
