from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Diplomado(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nombre

class Nivel(models.Model):
    diplomado = models.ForeignKey(Diplomado,related_name="nivel_diplomado")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return ("%s - %s") % (self.diplomado.nombre,self.nombre)

class Sesion(models.Model):
    nivel = models.ForeignKey(Nivel,related_name="sesion_nivel")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return ("%s - %s - %s") % (self.nivel.diplomado.nombre,self.nivel.nombre,self.nombre)

class Entregable(models.Model):
    sesion = models.ForeignKey(Sesion,related_name="entregable_sesion")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=100)