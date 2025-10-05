from django.db import models

# Create your models here.

class Route(models.Model):
    number = models.CharField(max_length=10)
    destination = models.CharField(max_length=200)
    bg_colour = models.CharField(max_length=10)
    text_colour = models.CharField(max_length=10)

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=10)
    time_entered = models.TimeField()