from django.db import models

# Create your models here.
class Transformacion(models.Model):
    latitud= models.FloatField(blank=True)
    longitud = models.FloatField(blank=True)
    altura = models.FloatField(blank=True)
    equis = models.FloatField(blank=True)
    ye = models.FloatField(blank=True)
    zeta = models.FloatField(blank=True)
