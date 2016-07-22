from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TipoSoporte(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500,blank=True)
    oculto = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre