from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Region(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nombre