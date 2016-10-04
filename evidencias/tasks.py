#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
from evidencias.models import Red
import openpyxl
from sican.settings import base as settings
from StringIO import StringIO
from django.core.files import File
from matrices.models import Beneficiario

@app.task
def build_red(id_red):

    red = Red.objects.get(id = id_red)
    output = StringIO()

    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ids = []
    inicia = 0

    if red.diplomado.numero == 1:
        ids = [{'id':8,'letter':'M'},
               {'id':9,'letter':'N'},
               {'id':20,'letter':'O'},
               {'id':12,'letter':'P'},
               {'id':21,'letter':'Q'},
               {'id':22,'letter':'R'},
               {'id':14,'letter':'S'},
               {'id':15,'letter':'T'},
               {'id':16,'letter':'U'},
               {'id':23,'letter':'V'},
               {'id':17,'letter':'W'},
               {'id':27,'letter':'X'},
               {'id':28,'letter':'Y'},
               {'id':40,'letter':'Z'},
               {'id':30,'letter':'AA'},
               {'id':31,'letter':'AB'},
               {'id':33,'letter':'AC'},
               {'id':34,'letter':'AD'},
               {'id':35,'letter':'AE'},
               {'id':36,'letter':'AF'},
               {'id':46,'letter':'AG'},
               {'id':58,'letter':'AH'},
               {'id':49,'letter':'AI'},
               {'id':59,'letter':'AJ'},
               {'id':52,'letter':'AK'},
               {'id':60,'letter':'AL'},
               {'id':55,'letter':'AM'},
               {'id':63,'letter':'AN'},
               {'id':64,'letter':'AO'},
               {'id':66,'letter':'AP'},
               {'id':67,'letter':'AQ'}]
        wb = openpyxl.load_workbook(filename=settings.STATICFILES_DIRS[0]+'/documentos/RED INNOVATIC.xlsx')
        ws = wb.get_sheet_by_name('RED InnovaTIC')
        inicia = 6
    elif red.diplomado.numero == 2:
        ids = [72,73,75,74,76,77,84,85,78,89,97,98,93,92,99,94,100,95,104,112,106,109,108,110,119,124,118,120,121]
        wb = openpyxl.load_workbook(filename=settings.STATICFILES_DIRS[0]+'/documentos/RED TECNOTIC.xlsx')
        ws = wb.get_sheet_by_name('RED TecnoTIC')
        inicia = 6
    elif red.diplomado.numero == 3:
        ids = [127,128,131,132,134,133,142,143,135,144,137,140,139,147,146,152,148,149,151,150,156,155,157,164,165,159,162,161,166,167,171,171,172]
        wb = openpyxl.load_workbook(filename=settings.STATICFILES_DIRS[0]+'/documentos/RED DIRECTIC.xlsx')
        ws = wb.get_sheet_by_name('RED DirecTIC')
        inicia = 6
    elif red.diplomado.numero == 4:
        ids = [221,221,221,224,228]
        wb = openpyxl.load_workbook(filename=settings.STATICFILES_DIRS[0]+'/documentos/RED FAMILIA.xlsx')
        ws = wb.get_sheet_by_name('RED Familia')
        inicia = 2


    beneficiarios_id = red.evidencias.values_list('beneficiarios_cargados__id',flat=True)


    i = 0 + inicia
    for beneficiario_id in beneficiarios_id:
        beneficiario = Beneficiario.objects.get(id = beneficiario_id)
        evidencias = red.evidencias.filter(beneficiarios_cargados__id = beneficiario_id)

        ws.cell('A'+str(i)).value = i - inicia + 1
        ws.cell('B'+str(i)).value = beneficiario.region.nombre
        ws.cell('C'+str(i)).value = beneficiario.radicado.municipio.departamento.nombre
        ws.cell('D'+str(i)).value = beneficiario.radicado.municipio.nombre
        ws.cell('E'+str(i)).value = beneficiario.grupo.formador.codigo_ruta + '-' + beneficiario.grupo.nombre
        ws.cell('F'+str(i)).value = beneficiario.formador.get_full_name()
        ws.cell('G'+str(i)).value = beneficiario.formador.cedula
        ws.cell('G'+str(i)).number_format = '0'
        ws.cell('H'+str(i)).value = beneficiario.nombres
        ws.cell('I'+str(i)).value = beneficiario.apellidos
        ws.cell('J'+str(i)).value = beneficiario.cedula
        ws.cell('J'+str(i)).number_format = '0'
        ws.cell('K'+str(i)).value = 'SICAN'
        ws.cell('L'+str(i)).value = 'I'

        for id in ids:
            evidencia = evidencias.filter(entregable__id = id['id'])
            if evidencia.count() == 1:
                ws.cell( id['letter'] + str(i)).value = 'SIC-' + str(evidencia[0].id)
                ws.cell( id['letter'] + str(i)).hyperlink = 'https://sican.asoandes.org' + evidencia[0].get_archivo_url()

        i += 1


    wb.save(output)
    filename = 'RED-' + unicode(red.id) + '-'+ red.region.nombre +'.xlsx'
    red.archivo.save(filename,File(output))

    return "Generado RED-" + str(id_red)