#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_tables2 as tables
from formadores.models import SolicitudTransporte
from django.utils.safestring import mark_safe
import locale

class SolicitudTable(tables.Table):
    nombre = tables.Column('Nombre')
    creacion = tables.Column('Fecha')
    valor = tables.Column('Valor solicitado')
    estado = tables.Column('Estado')
    terminada = tables.Column('Soporte')
    desplazamientos = tables.Column('Excel')
    observacion = tables.Column('Observación')
    valor_aprobado = tables.Column('Valor aprobado')


    def render_estado(self,value,record):
        if value == 'revision' or value == 'aprobado_lider':
            return mark_safe('<img src="/static/img/reloj.png" height="32" width="32">'
                             '<p>Esperando aprobación</p>')

        if value == 'aprobado' or value == 'consignado':
            if record.get_archivo_url() != '':
                if record.terminada:
                    return mark_safe('<img src="/static/img/true.png" height="32" width="32">'
                                 '<p>Consignado</p>')
                else:
                    return mark_safe('<img src="/static/img/esperando.png" height="32" width="32">'
                                 '<p>Esperando consignación</p>')
            else:
                return mark_safe('<img src="/static/img/alert.png" height="32" width="32">'
                                 '<p>Esperando firma de soporte</p>')

        if value == 'rechazado':
            return mark_safe('<img src="/static/img/delete.png" height="32" width="32">'
                             '<p>Solicitud rechazada</p>')


    def render_valor(self,value):
        return locale.currency(value,grouping=True)

    def render_desplazamientos(self,value,record):
        if record.estado == 'revision':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            return mark_safe('<a href="'+ record.get_pdf_url() +'"><img src="/static/img/file.png" height="32" width="32"><p>Descargar archivo</p></a>')
        if record.estado == 'rechazado':
            return ''
        else:
            return ''

    def render_terminada(self,value,record):
        if record.estado == 'revision':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            if record.get_archivo_url() == '':
                return mark_safe('<a href="soporte/'+ unicode(record.id) +'">Clic para subir soporte</a>')
            else:
                return mark_safe('<a target="_blank" href="'+ record.get_archivo_url() +'"><img src="/static/img/file.png" height="32" width="32"><p>Ver soporte</p></a>')
        if record.estado == 'rechazado':
            return ''
        else:
            return ''

    def render_valor_aprobado(self,value,record):
        if record.estado == 'revision' or record.estado == 'aprobado_lider':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            return locale.currency(value,grouping=True)
        if record.estado == 'rechazado':
            return ''


    class Meta:
        model = SolicitudTransporte
        fields = ['nombre','creacion','valor','estado','desplazamientos','terminada','observacion','valor_aprobado']