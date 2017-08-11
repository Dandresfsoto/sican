#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
import openpyxl
from informes.functions import construir_reporte
from datetime import datetime
from usuarios.models import User
from django.core.files import File
import pytz
from productos.models import Diplomado
from region.models import Region
from formadores.models import Formador
from formadores.models import Grupos
from matrices.models import Beneficiario, Area, Grado
from radicados.models import Radicado
from sican.settings import base as settings
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import StringIO
from django.core.files import File
from django.utils import timezone
from vigencia2017.models import CargaMatriz, DaneSEDE, Grupos, Beneficiario, BeneficiarioCambio
from formadores.models import Contrato
from validate_email import validate_email

@app.task
def carga_masiva_matrices(id,email_user):
    print(id)
    print(email_user)
    carga = CargaMatriz.objects.get(id = id)
    wb = openpyxl.load_workbook(filename = carga.archivo.file.name,read_only=True)
    sheets = wb.get_sheet_names()

    if 'InnovaTIC' in sheets and 'TecnoTIC' in sheets and 'DirecTIC' in sheets:

        titulos = ['DIPLOMADO',
                   'RESULTADO',
                   'REGION',
                   'CODIGO DANE SEDE EDUCATIVA',
                   'NOMBRE DE LA SEDE EDUCATIVA',
                   'CODIGO DANE INSTITUCION EDUCATIVA',
                   'NOMBRE INSTITUCION EDUCATIVA',
                   'CODIGO MUNICIPIO',
                   'MUNICIPIO',
                   'CODIGO DEPARTAMENTO',
                   'DEPARTAMENTO',
                   'SECRETARIA DE EDUCACION',
                   'ZONA (URBANA/RURAL)',
                   'CODIGO DEL GRUPO',
                   'NOMBRE DEL FORMADOR',
                   'NUMERO DE CEDULA DEL FORMADOR',
                   'APELLIDOS DEL DOCENTE',
                   'NOMBRES DEL DOCENTE',
                   'NUMERO DE CEDULA DEL DOCENTE',
                   'CORREO ELECTRONICO',
                   'TELEFONO FIJO',
                   'TELEFONO CELULAR',
                   'AREA CURRICULAR',
                   'GRADO',
                   'TIPO DE BENEFICIARIO',
                   'GENERO']

        formatos = ['General',
                   'General',
                   'General',
                   '0',
                   'General',
                   '0',
                   'General',
                   '0',
                   'General',
                   '0',
                   'General',
                   'General',
                   'General',
                   'General',
                   'General',
                   '0',
                   'General',
                   'General',
                   '0',
                   'General',
                   'General',
                   'General',
                   '0',
                   '0',
                   'General',
                   'General']

        ancho_columnas =  [30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           30,
                           ]

        contenidos = []

        for name in ['InnovaTIC','TecnoTIC','DirecTIC']:
            ws = wb.get_sheet_by_name(name)

            for fila in ws.iter_rows(row_offset=5):

                resultado = ''


                try:
                    diplomado = Diplomado.objects.get(nombre__icontains = name)
                except:
                    resultado = 'No existe el diplomado'
                else:

                    try:
                        region = Region.objects.get(id = fila[0].value)
                    except:
                        resultado = 'Codigo invalido de región'
                    else:

                        try:
                            dane_sede = DaneSEDE.objects.get(dane_sede = fila[1].value)
                        except:
                            resultado = 'No existe el codigo DANE de la sede'
                        else:

                            ruta_archivo = fila[11].value.split('-')

                            if len(ruta_archivo) == 3:

                                ruta = ruta_archivo[0]+"-"+ruta_archivo[1]

                                try:
                                    formador = Formador.objects.get(cedula=fila[13].value)
                                except:
                                    resultado = 'No existe el numero de cedula del formador'
                                else:
                                    try:
                                        contrato = Contrato.objects.get(formador=formador, codigo_ruta = ruta)
                                    except:
                                        resultado = "No se pudo identificar el contrato del formador (contacte a sistemas)"
                                    else:
                                        try:
                                            numero_grupo = int(ruta_archivo[2])
                                        except:
                                            resultado = "Numero de grupo invalido"
                                        else:
                                            grupo, created = Grupos.objects.get_or_create(contrato = contrato,
                                                                                 diplomado = diplomado,
                                                                                 numero = numero_grupo)
                                            try:
                                                cedula = long(fila[16].value)
                                            except:
                                                resultado = "Error en el numero de cedula"
                                            else:

                                                if fila[14].value != None and fila[15].value != None:

                                                    nombres = fila[15].value.upper()
                                                    apellidos = fila[14].value.upper()

                                                    email = ''
                                                    telefono_fijo = fila[18].value
                                                    telefono_celular = fila[19].value

                                                    genero = fila[23].value

                                                    if validate_email(fila[17].value):
                                                        email = fila[17].value

                                                    try:
                                                        area = int(fila[20].value)
                                                    except:
                                                        area = None

                                                    try:
                                                        grado = int(fila[21].value)
                                                    except:
                                                        grado = None


                                                    beneficiario = Beneficiario.objects.filter(cedula = cedula)

                                                    if beneficiario.count() == 0:
                                                        resultado = "Beneficiario creado"
                                                        Beneficiario.objects.create(region = region,
                                                                                    dane_sede = dane_sede,
                                                                                    grupo = grupo,
                                                                                    apellidos = apellidos,
                                                                                    nombres = nombres,
                                                                                    cedula=cedula,
                                                                                    correo=email,
                                                                                    telefono_fijo=telefono_fijo,
                                                                                    telefono_celular=telefono_celular,
                                                                                    area=area,
                                                                                    grado=grado,
                                                                                    genero=genero
                                                                                    )
                                                    else:
                                                        resultado = "Solicitud de cambio"
                                                        if beneficiario.nombres != nombres and beneficiario.apellidos != apellidos:
                                                            if beneficiario.dane_sede != dane_sede and beneficiario.grupo != grupo:

                                                                BeneficiarioCambio.objects.create(original = beneficiario[0],
                                                                                                  masivo = carga,
                                                                                                  region = region,
                                                                                                  dane_sede = dane_sede,
                                                                                                  grupo = grupo,
                                                                                                  apellidos = apellidos,
                                                                                                  nombres = nombres,
                                                                                                  cedula=cedula,
                                                                                                  correo=email,
                                                                                                  telefono_fijo=telefono_fijo,
                                                                                                  telefono_celular=telefono_celular,
                                                                                                  area=area,
                                                                                                  grado=grado,
                                                                                                  genero=genero
                                                                                                  )
                                                        else:
                                                            beneficiario.dane_sede = dane_sede
                                                            beneficiario.grupo = grupo
                                                            beneficiario.apellidos = apellidos
                                                            beneficiario.nombres = nombres
                                                            beneficiario.correo = email
                                                            beneficiario.telefono_fijo = telefono_fijo
                                                            beneficiario.telefono_celular = telefono_celular
                                                            beneficiario.area = area
                                                            beneficiario.grado = grado
                                                            beneficiario.genero = genero
                                                            beneficiario.save()

                                                else:
                                                    resultado = "Error en los nombres o apellidos del docente"


                            else:
                                resultado = 'El codigo de ruta no se encuentra bien parametrizado'






                contenidos.append([
                    name,
                    resultado,
                    fila[0].value,
                    fila[1].value,
                    fila[2].value,
                    fila[3].value,
                    fila[4].value,
                    fila[5].value,
                    fila[6].value,
                    fila[7].value,
                    fila[8].value,
                    fila[9].value,
                    fila[10].value,
                    fila[11].value,
                    fila[12].value,
                    fila[13].value,
                    fila[14].value,
                    fila[15].value,
                    fila[16].value,
                    fila[17].value,
                    fila[18].value,
                    fila[19].value,
                    fila[20].value,
                    fila[21].value,
                    fila[22].value,
                    fila[23].value
                ])

        usuario = User.objects.get(email=email_user)
        nombre = "Resultado carga masiva matrices"
        proceso = "FOR-MAS01"
        fecha = pytz.utc.localize(datetime.now())
        output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
        filename = unicode(fecha) + '.xlsx'
        carga.resultado.save(filename,File(output))

    elif 'Matriz revisión documental' in sheets:
        titulos = ['DIPLOMADO',
                   'RESULTADO',
                   'REGION',
                   'CODIGO DANE SEDE EDUCATIVA',
                   'NOMBRE DE LA SEDE EDUCATIVA',
                   'CODIGO DANE INSTITUCION EDUCATIVA',
                   'NOMBRE INSTITUCION EDUCATIVA',
                   'CODIGO MUNICIPIO',
                   'MUNICIPIO',
                   'CODIGO DEPARTAMENTO',
                   'DEPARTAMENTO',
                   'SECRETARIA DE EDUCACION',
                   'ZONA (URBANA/RURAL)',
                   'CODIGO DEL GRUPO',
                   'NOMBRE DEL FORMADOR',
                   'NUMERO DE CEDULA DEL FORMADOR',
                   'APELLIDOS DEL DOCENTE',
                   'NOMBRES DEL DOCENTE',
                   'NUMERO DE CEDULA DEL DOCENTE',
                   'CORREO ELECTRONICO',
                   'TELEFONO FIJO',
                   'TELEFONO CELULAR',
                   'AREA CURRICULAR',
                   'GRADO',
                   'TIPO DE BENEFICIARIO',
                   'GENERO']

        formatos = ['General',
                    'General',
                    'General',
                    '0',
                    'General',
                    '0',
                    'General',
                    '0',
                    'General',
                    '0',
                    'General',
                    'General',
                    'General',
                    'General',
                    'General',
                    '0',
                    'General',
                    'General',
                    '0',
                    'General',
                    'General',
                    'General',
                    '0',
                    '0',
                    'General',
                    'General']

        ancho_columnas = [30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          30,
                          ]

        contenidos = []

        for name in ['Matriz revisión documental']:
            ws = wb.get_sheet_by_name(name)

            for fila in ws.iter_rows(row_offset=9):

                resultado = ''

                try:
                    diplomado = Diplomado.objects.get(id = 4)
                except:
                    resultado = 'No existe el diplomado'
                else:

                    try:
                        region = Region.objects.get(id=fila[0].value)
                    except:
                        resultado = 'Codigo invalido de región'
                    else:

                        try:
                            dane_sede = "N/A"
                        except:
                            resultado = 'No existe el codigo DANE de la sede'
                        else:

                            ruta_archivo = fila[11].value.split('-')

                            if len(ruta_archivo) == 3:

                                ruta = ruta_archivo[0] + "-" + ruta_archivo[1]

                                try:
                                    formador = Formador.objects.get(cedula=fila[13].value)
                                except:
                                    resultado = 'No existe el numero de cedula del formador'
                                else:
                                    try:
                                        contrato = Contrato.objects.get(formador=formador, codigo_ruta=ruta)
                                    except:
                                        resultado = "No se pudo identificar el contrato del formador (contacte a sistemas)"
                                    else:
                                        try:
                                            numero_grupo = int(ruta_archivo[2])
                                        except:
                                            resultado = "Numero de grupo invalido"
                                        else:
                                            grupo, created = Grupos.objects.get_or_create(contrato=contrato,
                                                                                          diplomado=diplomado,
                                                                                          numero=numero_grupo)
                                            try:
                                                cedula = long(fila[16].value)
                                            except:
                                                resultado = "Error en el numero de cedula"
                                            else:

                                                if fila[14].value != None and fila[15].value != None:

                                                    nombres = fila[15].value.upper()
                                                    apellidos = fila[14].value.upper()

                                                    email = ''
                                                    telefono_fijo = fila[18].value
                                                    telefono_celular = fila[19].value

                                                    genero = fila[23].value

                                                    if validate_email(fila[17].value):
                                                        email = fila[17].value

                                                    try:
                                                        area = int(fila[20].value)
                                                    except:
                                                        area = None

                                                    try:
                                                        grado = int(fila[21].value)
                                                    except:
                                                        grado = None

                                                    beneficiario = Beneficiario.objects.filter(cedula=cedula)

                                                    if beneficiario.count() == 0:
                                                        resultado = "Beneficiario creado"
                                                        Beneficiario.objects.create(region=region,
                                                                                    dane_sede=dane_sede,
                                                                                    grupo=grupo,
                                                                                    apellidos=apellidos,
                                                                                    nombres=nombres,
                                                                                    cedula=cedula,
                                                                                    correo=email,
                                                                                    telefono_fijo=telefono_fijo,
                                                                                    telefono_celular=telefono_celular,
                                                                                    area=area,
                                                                                    grado=grado,
                                                                                    genero=genero
                                                                                    )
                                                    else:
                                                        resultado = "Solicitud de cambio"
                                                        if beneficiario.nombres != nombres and beneficiario.apellidos != apellidos:
                                                            if beneficiario.grupo != grupo:
                                                                BeneficiarioCambio.objects.create(
                                                                    original=beneficiario[0],
                                                                    masivo=carga,
                                                                    region=region,
                                                                    dane_sede=dane_sede,
                                                                    grupo=grupo,
                                                                    apellidos=apellidos,
                                                                    nombres=nombres,
                                                                    cedula=cedula,
                                                                    correo=email,
                                                                    telefono_fijo=telefono_fijo,
                                                                    telefono_celular=telefono_celular,
                                                                    area=area,
                                                                    grado=grado,
                                                                    genero=genero
                                                                    )
                                                        else:
                                                            beneficiario.dane_sede = dane_sede
                                                            beneficiario.grupo = grupo
                                                            beneficiario.apellidos = apellidos
                                                            beneficiario.nombres = nombres
                                                            beneficiario.correo = email
                                                            beneficiario.telefono_fijo = telefono_fijo
                                                            beneficiario.telefono_celular = telefono_celular
                                                            beneficiario.area = area
                                                            beneficiario.grado = grado
                                                            beneficiario.genero = genero
                                                            beneficiario.save()

                                                else:
                                                    resultado = "Error en los nombres o apellidos del docente"


                            else:
                                resultado = 'El codigo de ruta no se encuentra bien parametrizado'

                contenidos.append([
                    name,
                    resultado,
                    fila[0].value,
                    fila[1].value,
                    fila[2].value,
                    fila[3].value,
                    fila[4].value,
                    fila[5].value,
                    fila[6].value,
                    fila[7].value,
                    fila[8].value,
                    fila[9].value,
                    fila[10].value,
                    fila[11].value,
                    fila[12].value,
                    fila[13].value,
                    fila[14].value,
                    fila[15].value,
                    fila[16].value,
                    fila[17].value,
                    fila[18].value,
                    fila[19].value,
                    fila[20].value,
                    fila[21].value,
                    fila[22].value,
                    fila[23].value
                ])

        usuario = User.objects.get(email=email_user)
        nombre = "Resultado carga masiva matrices"
        proceso = "FOR-MAS01"
        fecha = pytz.utc.localize(datetime.now())
        output = construir_reporte(titulos, contenidos, formatos, ancho_columnas, nombre, fecha, usuario, proceso)
        filename = unicode(fecha) + '.xlsx'
        carga.resultado.save(filename, File(output))


    return "Carga masiva exitosa"