# services/trip_generation/models.py
from django.db import models

class TripCalculation(models.Model):
    country = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    activity_code = models.CharField(max_length=50)
    day_type = models.CharField(max_length=20)
    period = models.CharField(max_length=10)
    variable = models.CharField(max_length=100)
    rate = models.FloatField(default=0)
    in_value = models.FloatField(default=0)
    out_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.country} - {self.activity}"