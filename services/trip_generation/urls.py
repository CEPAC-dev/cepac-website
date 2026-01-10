from django.urls import path
from . import views

app_name = 'trip_generation'

urlpatterns = [
    path('', views.index, name='index'),
    path('showReport/', views.showReport, name='showReport'),
    path('tripGeneration/', views.tripGeneration, name='tripGeneration'),
    path('showReport/export-trip-generation-excel/', views.export_trip_generation_excel, name='export_trip_generation_excel'),
]
