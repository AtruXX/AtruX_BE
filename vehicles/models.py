from django.db import models
from base.models import Company

class Truck(models.Model):
    license_plate = models.CharField(max_length=100, unique=True)
    vin = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_trucks')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    next_service_date = models.DateField()
    last_service_date = models.DateField()
    status = models.CharField(max_length=100, default='free')

class Trailer(models.Model):
    license_plate = models.CharField(max_length=100, unique=True)
    vin = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_trailers')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    next_service_date = models.DateField()
    last_service_date = models.DateField()
    status = models.CharField(max_length=100, default='free')
    type = models.CharField(max_length=100)

class TruckDocument(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to="truck_documents/", blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, default='free')
    description = models.TextField(blank=True, null=True)
    issuing_date = models.DateField(blank=True, null=True)

class TrailerDocument(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to="trailer_documents/", blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, default='free')
    description = models.TextField(blank=True, null=True)
    issuing_date = models.DateField(blank=True, null=True)

