from __future__ import unicode_literals

from django.db import models
from rh.models import TipoSoporte
from region.models import Region
from cargos.models import Cargo
from bancos.models import Banco
from departamentos.models import Departamento
from municipios.models import Municipio
import os
from usuarios.models import User

class Lideres(models.Model):
    lider = models.ForeignKey(User,blank=True,null=True)
    departamentos = models.ManyToManyField(Departamento,related_name="departamento_lider",blank=True)
    codigo_ruta = models.CharField(max_length=100,blank=True,null=True)
    #---------- REGION----------------------
    region = models.ForeignKey(Region)

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

    class Meta:
        ordering = ['nombres']

    def __unicode__(self):
        return self.nombres

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('nombre',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]

    def get_interventoria_region(self):
        value = ''
        for region in self.region.values_list('numero',flat=True):
            value = value + "R" + unicode(region) + ', '
        return value[:-2]

    def get_departamentos_string(self):
        value = ''
        for departamento in self.departamentos.values_list('nombre',flat=True):
            value = value + unicode(departamento) + ', '
        return value[:-2]


    def get_full_name(self):
        return self.nombres + " " + self.apellidos

class Soporte(models.Model):
    lider = models.ForeignKey(Lideres)
    creacion = models.DateField(auto_now=True)
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoSoporte,related_name='soporte_lider')
    descripcion = models.TextField(max_length=1000,blank=True)
    oculto = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Lideres/Soportes/',blank=True)

    class Meta:
        ordering = ['lider']

    def __unicode__(self):
        return str(self.lider.cedula)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)