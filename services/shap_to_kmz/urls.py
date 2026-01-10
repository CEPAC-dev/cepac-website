# services/shap_to_kmz/urls.py

from django.urls import path
from . import views

app_name = "shap_to_kmz"

urlpatterns = [
    path("", views.form_view, name="form"),
]
