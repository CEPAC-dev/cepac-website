from django.urls import path
from . import views

app_name = "pdf_to_word"

urlpatterns = [
    path("", views.form_view, name="form"),
]
