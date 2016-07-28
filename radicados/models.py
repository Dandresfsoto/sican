from __future__ import unicode_literals

from django.db import models
from municipios.models import Municipio
from secretarias.models import Secreatia
# Create your models here.
class Radicado(models.Model):
    municipio = models.ForeignKey(Municipio)
    secretaria = models.ForeignKey(Secreatia)
    numero = models.BigIntegerField()
    nombre_sede = models.CharField(max_length=200)
    dane_sede = models.BigIntegerField()
    tipo = models.IntegerField()
    ubicacion = models.IntegerField()

    class Meta:
        ordering = ['nombre_sede']

    def __unicode__(self):
        return self.nombre_sede