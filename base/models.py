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

class Transport(models.Model):
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='driver_transports')
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dispatcher_transports')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    status_truck = models.CharField(max_length=100)
    status_truck_text = models.CharField(max_length=255)
    status_goods = models.CharField(max_length=100)
    truck_combination = models.CharField(max_length=100)
    status_coupling = models.CharField(max_length=100)
    trailer_type = models.CharField(max_length=100)
    trailer_number = models.CharField(max_length=100)
    status_trailer_wagon = models.CharField(max_length=100)
    status_loaded_truck = models.CharField(max_length=100)
    detraction = models.CharField(max_length=100)
    status_transport = models.CharField(max_length=100, default='not started')
    documents = models.JSONField(default=list)

