from __future__ import unicode_literals

from django.db import models
from productos.models import Entregable, Diplomado
from matrices.models import Beneficiario
from region.models import Region
from formadores.models import Formador
from usuarios.models import User

# Create your models here.

class Evidencia(models.Model):
    fecha = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User)
    archivo = models.FileField(upload_to='Evidencias/Soportes')
    entregable = models.ForeignKey(Entregable,related_name='entregable_diplomado')
    beneficiarios_cargados = models.ManyToManyField(Beneficiario,related_name='beneficiarios_cargados')
    beneficiarios_validados = models.ManyToManyField(Beneficiario,related_name='beneficiarios_validados',blank=True)
    formador = models.ForeignKey(Formador)

    def __unicode__(self):
        return self.entregable.nombre

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

    def get_beneficiarios_cantidad(self):
        return self.beneficiarios_cargados.all().count()

    def get_validados_cantidad(self):
        return self.beneficiarios_validados.all().count()

class Red(models.Model):
    diplomado = models.ForeignKey(Diplomado)
    region = models.ForeignKey(Region)
    fecha = models.DateTimeField(auto_now_add=True)
    evidencias = models.ManyToManyField(Evidencia,related_name='evidencia_red',blank=True)
    retroalimentacion = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Formatos Red/',blank=True,null=True)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url