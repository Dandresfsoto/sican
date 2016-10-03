from __future__ import unicode_literals

from django.db import models
from region.models import Region
from usuarios.models import User

# Create your models here.

class Requerimiento(models.Model):
    creacion = models.DateTimeField(auto_created = True)

    recepcion_solicitud = models.DateField()
    region = models.ManyToManyField(Region,related_name='region_requerimiento')
    entidad_remitente = models.CharField(max_length=100)
    funcionario_remitente = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    archivo_solicitud = models.FileField(upload_to='Requerimientos/Interventoria')
    descripcion = models.TextField(max_length=5000)

    tiempo_respuesta = models.IntegerField()
    encargados = models.ManyToManyField(User,related_name='encargados_requerimiento')
    estado = models.CharField(max_length=100)
    fecha_respuesta = models.DateField()
    medio_entrega = models.CharField(max_length=100)
    observaciones = models.TextField(max_length=1000)
    archivo_respuesta = models.FileField(upload_to='Requerimientos/Interventoria')

    def __unicode__(self):
        return self.nombre

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('numero',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]