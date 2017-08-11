#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from municipios.models import Municipio
from secretarias.models import Secretaria
from productos.models import Diplomado
from region.models import Region
from formadores.models import Formador, Contrato
from productos.models import Entregable
from usuarios.models import User

# Create your models here.

class DaneSEDE(models.Model):
    dane_sede = models.BigIntegerField(unique=True)
    nombre_sede = models.CharField(max_length=200)
    dane_ie = models.BigIntegerField()
    nombre_ie = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio)
    secretaria = models.ForeignKey(Secretaria)
    zona = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.dane_sede) + " - Sede: " + self.nombre_sede + ", Institución: " + self.nombre_ie

class Grupos(models.Model):
    contrato = models.ForeignKey(Contrato,related_name="contrato_vigencia_2017")
    diplomado = models.ForeignKey(Diplomado)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.get_nombre_grupo()

    def get_nombre_grupo(self):
        return self.contrato.codigo_ruta + "-" + format(self.numero, '02d')


class Beneficiario(models.Model):
    region = models.ForeignKey(Region, related_name='region_beneficiario_vigencia_2017')
    dane_sede_text = models.CharField(max_length=1000, blank=True, null=True)
    dane_sede = models.ForeignKey(DaneSEDE, blank=True, null=True)

    grupo = models.ForeignKey(Grupos, related_name='grupo_beneficiario_vigencia_2017')
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    cedula = models.BigIntegerField(unique=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=100, blank=True, null=True)
    telefono_celular = models.CharField(max_length=100, blank=True, null=True)
    area = models.IntegerField(blank=True,null=True)
    grado = models.IntegerField(blank=True,null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)




class TipoContrato(models.Model):
    nombre = models.CharField(max_length=100)
    diplomados = models.ManyToManyField(Diplomado)

    def __unicode__(self):
        return self.nombre

    def get_diplomado_string(self):
        string = ''
        for diplomado in self.diplomados.all():
            string += diplomado.nombre + ", "
        return string


class ValorEntregableVigencia2017(models.Model):
    entregable = models.ForeignKey(Entregable,related_name='entregable_valor_vigencia_2017')
    tipo_contrato = models.ForeignKey(TipoContrato)
    valor = models.FloatField(null=True,default=0)

    def __unicode__(self):
        return self.entregable.nombre


class CargaMatriz(models.Model):
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='Vigencia 2017/Carga Matriz/Archivo')
    resultado = models.FileField(upload_to='Vigencia 2017/Carga Matriz/Resultado', blank=True, null=True)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

    def get_resultado_url(self):
        try:
            url = self.resultado.url
        except:
            url = ""
        return url


class BeneficiarioCambio(models.Model):
    original = models.ForeignKey(Beneficiario)
    masivo = models.ForeignKey(CargaMatriz)

    region = models.ForeignKey(Region, related_name='region_beneficiario_vigencia_2017_cambio')
    dane_sede_text = models.CharField(max_length=1000, blank=True, null=True)
    dane_sede = models.ForeignKey(DaneSEDE, blank=True, null=True)

    grupo = models.ForeignKey(Grupos, related_name='grupo_beneficiario_vigencia_2017_cambio')
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    cedula = models.BigIntegerField()
    correo = models.EmailField(max_length=100, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=100, blank=True, null=True)
    telefono_celular = models.CharField(max_length=100, blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    grado = models.IntegerField(blank=True, null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)