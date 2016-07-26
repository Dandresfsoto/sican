from __future__ import unicode_literals

from django.db import models
from rh.models import TipoSoporte
from region.models import Region
from cargos.models import Cargo
from bancos.models import Banco
import os

# Create your models here.
class Formador(models.Model):
    #---------- REGION----------------------
    region = models.ManyToManyField(Region)

    #---------- DATOS PERSONALES----------------------
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.BigIntegerField()
    correo_personal = models.EmailField(max_length=100,blank=True)
    celular_personal = models.CharField(max_length=100,blank=True)

    #---------- INFORMACION PROFESIONAL ----------------------
    cargo = models.ForeignKey(Cargo)
    profesion = models.CharField(max_length=100,blank=True)

    fecha_contratacion = models.DateField(null=True,blank=True)
    fecha_terminacion = models.DateField(null=True,blank=True)

    #---------- INFORMACION BANCARIA Y SEGURIDAD SOCIAL ----------------------
    banco = models.ForeignKey(Banco,blank=True,null=True)
    tipo_cuenta = models.CharField(max_length=100,blank=True)
    numero_cuenta = models.CharField(max_length=100,blank=True)

    eps = models.CharField(max_length=100,blank=True)
    pension = models.CharField(max_length=100,blank=True)
    arl = models.CharField(max_length=100,blank=True)

    oculto = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombres

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('nombre',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]

    def get_full_name(self):
        return self.nombres + " " + self.apellidos

class Soporte(models.Model):
    formador = models.ForeignKey(Formador)
    creacion = models.DateField(auto_now=True)
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoSoporte,related_name='soporte_formador')
    descripcion = models.TextField(max_length=1000,blank=True)
    oculto = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Formadores/Soportes/',blank=True)

    def __unicode__(self):
        return self.administrativo.get_full_name()

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)