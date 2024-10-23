from django.db import models

# Create your models here.
class dispacher(models.Model):
    class Meta:
        db_table = "dispacher"
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    