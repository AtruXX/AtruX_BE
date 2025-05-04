from django.db import models
from django.contrib.auth import get_user_model
from vehicles.models import Truck, Trailer
from base.models import Company

class GoodsPhoto(models.Model):
    photo = models.FileField(upload_to="goods_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Transport(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='transports')
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='driver_transports')
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dispatcher_transports')
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='transports', null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE, related_name='transports', null=True, blank=True)
    status_truck = models.CharField(max_length=100, default='ok')
    status_truck_text = models.CharField(max_length=255, blank=True, null=True)
    status_goods = models.CharField(max_length=100, default='ok')
    truck_combination = models.CharField(max_length=100)
    status_coupling = models.CharField(max_length=100, default='ok')
    trailer_type = models.CharField(max_length=100)
    trailer_number = models.CharField(max_length=100)
    status_trailer_wagon = models.CharField(max_length=100, default='ok')
    status_trailer_wagon_description = models.TextField(blank=True, null=True)
    status_loaded_truck = models.CharField(max_length=100, default='ok')
    detraction = models.CharField(max_length=100)
    status_transport = models.CharField(max_length=100, default='not started')
    goods_photos = models.ManyToManyField('GoodsPhoto', blank=True)
    delay_estimation = models.DurationField(max_length=100, blank=True, null=True)
    time_estimation = models.DateTimeField(max_length=100, blank=True, null=True)
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    goods_type = models.CharField(max_length=100)

class Point(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class Route(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='routes')
    points = models.ManyToManyField(Point)
    date = models.DateField()

class TransportDocument(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to="transport_documents/", blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)

class CMR(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='cmrs')
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cmr_driver')
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cmr_dispatcher')
    expeditor_nume = models.CharField(max_length=255)
    expeditor_adresa = models.CharField(max_length=255)
    expeditor_tara = models.CharField(max_length=100)
    destinatar_nume = models.CharField(max_length=255)
    destinatar_adresa = models.CharField(max_length=255)
    destinatar_tara = models.CharField(max_length=100)
    loc_livrare = models.CharField(max_length=255)
    loc_incarcare = models.CharField(max_length=255)
    data_incarcare = models.DateField()
    marci_numere = models.CharField(max_length=255)
    numar_colete = models.IntegerField()
    mod_ambalare = models.CharField(max_length=255)
    natura_marfii = models.CharField(max_length=255)
    nr_static = models.CharField(max_length=100)
    greutate_bruta = models.DecimalField(max_digits=10, decimal_places=2)
    cubaj = models.DecimalField(max_digits=10, decimal_places=2)
    instructiuni_expeditor = models.TextField(blank=True, null=True)
    conventii_speciale = models.TextField(blank=True, null=True)
