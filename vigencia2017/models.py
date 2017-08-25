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
from django.db.models import Sum
import locale

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
    archivo = models.FileField(upload_to="Evidencias/Vigencia 2017/No Conectividad",blank=True,null=True)
    no_conectividad = models.BooleanField(default=False)

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

    def __unicode__(self):
        return str(self.cedula) + ' - ' + self.nombres + ' ' + self.apellidos

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos


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

    def get_valor_beneficiario(self):

        string = ''

        diplomados = ValorEntregableVigencia2017.objects.filter(tipo_contrato__id=self.id).values_list('entregable__sesion__nivel__diplomado__id',flat=True).distinct()

        for id_diplomado in diplomados:

            diplomado = Diplomado.objects.get(id = id_diplomado)
            valor = ValorEntregableVigencia2017.objects.filter(tipo_contrato__id=self.id,entregable__sesion__nivel__diplomado__id = id_diplomado).aggregate(Sum('valor')).get('valor__sum')
            string += diplomado.nombre + ": " + locale.currency(valor,grouping=True).replace("+",'') + " "

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



class Rechazo(models.Model):
    beneficiario_rechazo = models.ForeignKey(Beneficiario)
    observacion = models.TextField(max_length=1000,blank=True)
    red_id = models.IntegerField()
    evidencia_id = models.IntegerField()




class Evidencia(models.Model):
    fecha = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User,related_name='vigencia_2017_usuario_evidencia')
    archivo = models.FileField(upload_to='Evidencias/Vigencia 2017/Soportes')
    entregable = models.ForeignKey(Entregable,related_name='vigencia_2017_entregable_diplomado')
    beneficiarios_cargados = models.ManyToManyField(Beneficiario,related_name='vigencia_2017_beneficiarios_cargados')
    beneficiarios_validados = models.ManyToManyField(Beneficiario,related_name='vigencia_2017_beneficiarios_validados',blank=True)
    beneficiarios_rechazados = models.ManyToManyField(Rechazo,related_name='vigencia_2017_beneficiarios_rechazados',blank=True)
    contrato = models.ForeignKey(Contrato)
    subsanacion = models.BooleanField(default=False)
    cantidad_cargados = models.IntegerField(blank=True,null=True)
    red_id = models.IntegerField(blank=True,null=True)
    corte_id = models.IntegerField(blank=True, null=True)

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

    def get_rechazados_cantidad(self):
        return self.beneficiarios_rechazados.all().count()



class Pago(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    beneficiario = models.ForeignKey(Beneficiario)
    evidencia = models.ForeignKey(Evidencia)
    valor = models.FloatField()





class Red(models.Model):
    diplomado = models.ForeignKey(Diplomado,related_name="vigencia_2017_diplomdo")
    region = models.ForeignKey(Region,related_name="vigencia_2017_region")
    fecha = models.DateTimeField(auto_now_add=True)
    beneficiarios = models.ManyToManyField(Beneficiario, related_name='vigencia_2017_beneficiarios_red', blank=True)
    retroalimentacion = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Formatos Red/Vigencia 2017/',blank=True,null=True)
    archivo_retroalimentacion = models.FileField(upload_to='Formatos Red/Vigencia 2017/Retroalimentacion/',blank=True,null=True)
    producto_final = models.BooleanField(default=False)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


class Corte(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)