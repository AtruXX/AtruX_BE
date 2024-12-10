from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(primary_key=True, null=False, max_length=100, unique=True)
    

    