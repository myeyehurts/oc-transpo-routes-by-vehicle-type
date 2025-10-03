from django.db import models

# Create your models here.

class Route(models.Model):
    number = models.CharField(max_length=10)
    destination = models.CharField(max_length=200)
    colour = models.CharField(max_length=10)