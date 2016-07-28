from __future__ import unicode_literals

from django.db import models
from municipios.models import Municipio
from secretarias.models import Secretaria
# Create your models here.
class Radicado(models.Model):
    secretaria = models.ForeignKey(Secretaria)
    municipio = models.ForeignKey(Municipio)
    numero = models.BigIntegerField()
    nombre_sede = models.CharField(max_length=200)
    dane_sede = models.BigIntegerField()
    tipo = models.IntegerField()
    ubicacion = models.IntegerField()
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre_sede']

    def __unicode__(self):
        return self.nombre_sede