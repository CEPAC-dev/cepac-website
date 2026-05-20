from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('projects/', views.projects_list, name='projects_list'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]
