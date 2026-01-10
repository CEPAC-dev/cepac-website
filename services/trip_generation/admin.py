# services/trip_generation/admin.py
from django.contrib import admin
from .models import TripCalculation

@admin.register(TripCalculation)
class TripCalculationAdmin(admin.ModelAdmin):
    list_display = ['country', 'category', 'activity', 'period', 'created_at']
    list_filter = ['country', 'category']
    search_fields = ['country', 'activity']