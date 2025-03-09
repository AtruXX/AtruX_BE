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

class Transport(models.Model):
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='driver_transports')
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dispatcher_transports')
    status_truck = models.CharField(max_length=100)
    status_truck_text = models.CharField(max_length=255, blank=True, null=True)
    status_goods = models.CharField(max_length=100)
    truck_combination = models.CharField(max_length=100)
    status_coupling = models.CharField(max_length=100)
    trailer_type = models.CharField(max_length=100)
    trailer_number = models.CharField(max_length=100)
    status_trailer_wagon = models.CharField(max_length=100)
    status_loaded_truck = models.CharField(max_length=100)
    detraction = models.CharField(max_length=100)
    status_transport = models.CharField(max_length=100, default='not started')

class Route(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='routes')
    points = models.ManyToManyField(Point)
    date = models.DateField()

class TransportDocument(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to="transport_documents/", blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)

