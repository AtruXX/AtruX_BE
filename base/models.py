from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(primary_key=True, null=False, max_length=100, unique=True)
    
class Point(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class Route(models.Model):
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='driver_routes')
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dispatcher_routes')
    points = models.ManyToManyField(Point)
    date = models.DateField()

