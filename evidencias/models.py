from __future__ import unicode_literals

from django.db import models
from productos.models import Entregable, Diplomado
from matrices.models import Beneficiario

# Create your models here.
class Red(models.Model):
    diplomado = models.ForeignKey(Diplomado)
    fecha = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(max_length=1000,blank=True)


class CodigoEvidencia(models.Model):
    archivo = models.FileField(upload_to='Evidencias/Soportes')
    entregable = models.ForeignKey(Entregable,related_name='entregable_diplomado')
    beneficiarios = models.ManyToManyField(Beneficiario)
    red = models.ForeignKey(Red,blank=True,null=True,related_name='red_evidencia')

    def __unicode__(self):
        return self.entregable.nombre