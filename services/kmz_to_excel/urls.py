from django.urls import path
from . import views

app_name = "kmz_to_excel"

urlpatterns = [
    path("", views.form_view, name="form"),
]
