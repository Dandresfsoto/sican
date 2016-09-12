from __future__ import unicode_literals
from productos.models import Diplomado
from region.models import Region
from django.db import models
from radicados.models import Radicado
from formacion.models import Formador, Grupos

# Create your models here.
class Area(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nombre

class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nombre

class Beneficiario(models.Model):
    diplomado = models.ForeignKey(Diplomado,related_name='diplomado_beneficiario')
    region = models.ForeignKey(Region,related_name='region_beneficiario')
    radicado_text = models.CharField(max_length=1000,blank=True)
    radicado = models.ForeignKey(Radicado,blank=True,null=True,related_name='radicado_beneficiario')
    formador = models.ForeignKey(Formador,related_name='formador_beneficiario')
    grupo = models.ForeignKey(Grupos,related_name='grupo_beneficiario')
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    cedula = models.BigIntegerField(unique=True)
    correo = models.EmailField(max_length=100,blank=True)
    telefono_fijo = models.CharField(max_length=100,blank=True)
    telefono_celular = models.CharField(max_length=100,blank=True)
    area = models.ForeignKey(Area,related_name='area_beneficiario',blank=True,null=True)
    grado = models.ForeignKey(Grado,related_name='grado_beneficiario',blank=True,null=True)
    genero = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.cedula)

class BeneficiarioPendiente(models.Model):
    diplomado = models.ForeignKey(Diplomado,related_name='diplomado_beneficiariopendiente')
    cedula = models.BigIntegerField(unique=True)

    def __unicode__(self):
        return str(self.cedula)