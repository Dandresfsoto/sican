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
    usuario = models.ForeignKey(User,blank=True,null=True,related_name='usuario_sistema_lider')

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

class SolicitudSoportes(models.Model):
    nombre = models.CharField(max_length=200)
    soportes_requeridos = models.ManyToManyField(TipoSoporte,related_name='tipo_soporte_lider')

    def __unicode__(self):
        return self.nombre

class Contrato(models.Model):
    nombre = models.CharField(max_length=200)
    lider = models.ForeignKey(Lideres)
    soportes_requeridos = models.ForeignKey(SolicitudSoportes)
    fecha = models.DateTimeField(auto_now_add = True)
    fecha_inicio = models.DateField(blank=True,null=True)
    fecha_fin = models.DateField(blank=True,null=True)
    renuncia = models.BooleanField(default=False)
    soporte_renuncia = models.FileField(upload_to='Contratos/Lideres/Soporte Renuncia/',blank=True,null=True)
    liquidado = models.BooleanField(default=False)
    soporte_liquidacion = models.FileField(upload_to='Contratos/Lideres/Soporte Liquidacion/',blank=True,null=True)

class Soporte(models.Model):
    lider = models.ForeignKey(Lideres)
    creacion = models.DateField(auto_now=True)
    fecha = models.DateField(blank=True,null=True)
    tipo = models.ForeignKey(TipoSoporte,related_name='soporte_lider')
    descripcion = models.TextField(max_length=1000,blank=True)
    oculto = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Lideres/Soportes/',blank=True)
    contrato = models.ForeignKey(Contrato,blank=True,null=True)

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

class Desplazamiento(models.Model):
    departamento_origen = models.ForeignKey(Departamento,related_name="departamento_origen_desplazamiento_lider")
    municipio_origen = models.ForeignKey(Municipio,related_name="municipio_origen_desplazamiento_lider")
    departamento_destino = models.ForeignKey(Departamento,related_name="departamento_destino_desplazamiento_lider")
    municipio_destino = models.ForeignKey(Municipio,related_name="municipio_destino_desplazamiento_lider")
    valor = models.BigIntegerField()
    creacion = models.DateTimeField(auto_now=True)
    fecha = models.DateField()
    motivo = models.CharField(max_length=600)

    def __unicode__(self):
        return unicode(self.id)

class SolicitudTransporte(models.Model):
    lider = models.ForeignKey(Lideres,related_name="lider_solicitud_transporte_lider")
    nombre = models.CharField(max_length=100)
    creacion = models.DateTimeField(auto_now_add=True)
    creacion_date = models.DateTimeField(blank=True,null=True)
    aprobacion_lider = models.DateTimeField(blank=True,null=True)
    desplazamientos = models.ManyToManyField(Desplazamiento,blank=True)
    estado = models.CharField(max_length=100,default="revision")
    observacion = models.TextField(max_length=1000,blank=True,null=True)
    valor = models.BigIntegerField()
    terminada = models.BooleanField(default=False)
    valor_aprobado = models.BigIntegerField(blank=True,null=True)
    valor_aprobado_lider = models.BigIntegerField(blank=True,null=True)
    archivo = models.FileField(upload_to='Transportes/Solicitudes/',blank=True,null=True)
    pdf = models.FileField(upload_to = 'Transportes/Pdf/',blank=True,null=True)


    def __unicode__(self):
        return unicode(self.lider.cedula)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

    def get_pdf_url(self):
        try:
            url = self.pdf.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)