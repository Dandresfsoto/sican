#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
import openpyxl
from matrices.models import CargaMasiva, Beneficiario
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

@app.task
def carga_masiva_matrices(id,email):
    carga = CargaMasiva.objects.get(id = id)
    wb = openpyxl.load_workbook(filename = carga.archivo.file.name)
    sheets = wb.get_sheet_names()

    if 'InnovaTIC' in sheets and 'TecnoTIC' in sheets and 'DirecTIC' in sheets:
        carga.estado = 'Iniciando carga masiva ...'

        titulos = ['DIPLOMADO',
                   'RESULTADO',
                   'REGION',
                   'DEPARTAMENTO',
                   'SECRETARIA DE EDUCACION',
                   'RADICADO',
                   'CODIGO DANE INSTITUCION EDUCATIVA',
                   'NOMBRE INSTITUCION EDUCATIVA',
                   'CODIGO DANE SEDE EDUCATIVA',
                   'NOMBRE DE LA SEDE EDUCATIVA',
                   'MUNICIPIO',
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
                   'GENERO',
                   'ESTADO']

        formatos = ['General',
                    'General',
                   '0',
                   'General',
                   'General',
                   '0',
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
                   'General',
                   'General',
                   'General',
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

            for fila in ws.rows[5:]:

                resultado = ''

                if Diplomado.objects.filter(nombre__icontains = name).count() == 1:
                    diplomado = Diplomado.objects.get(nombre__icontains = name)

                    if Region.objects.filter(numero = fila[0].value if fila[0].value != None else '').count() == 1:
                        region = Region.objects.get(numero = fila[0].value if fila[0].value != None else 0)

                        if Formador.objects.filter(cedula = fila[12].value if fila[12].value != None else 0).count() == 1:
                            formador = Formador.objects.get(cedula = fila[12].value if fila[12].value != None else 0)
                            grupo_list = fila[10].value.split('-') if fila[10].value != None else ['']

                            if len(grupo_list) > 1:
                                try:
                                    grupo_numero = int(grupo_list[-1])
                                except:
                                    resultado = 'No se puede identificar el grupo'
                                else:
                                    grupo, grupo_creado = Grupos.objects.get_or_create(formador=formador,nombre = grupo_numero)

                                    if grupo_creado:
                                        resultado += 'Grupo creado, '

                                    if fila[13].value != None:

                                        if fila[14].value != None:

                                            try:
                                                radicado_numero = int(fila[3].value)
                                            except:
                                                radicado_numero = -1

                                            if Radicado.objects.filter(numero = radicado_numero).count() == 1:
                                                radicado = Radicado.objects.get(numero = radicado_numero)
                                            else:
                                                radicado = None


                                            if Area.objects.filter(numero__icontains = str(fila[19].value).split('.')[0] if fila[19].value != None else '').count() == 1:
                                                area = Area.objects.get(numero__icontains = str(fila[19].value).split('.')[0])
                                            else:
                                                area = None

                                            if Grado.objects.filter(numero__icontains = str(fila[20].value).split('.')[0] if fila[20].value != None else '').count() == 1:
                                                grado = Grado.objects.get(numero__icontains = str(fila[20].value).split('.')[0])
                                            else:
                                                grado = None

                                            radicado_text = str(radicado.numero) if radicado != None else ''


                                            if Beneficiario.objects.filter(cedula = fila[15].value if fila[15].value != None else '').count() == 1:
                                                beneficiario = Beneficiario.objects.get(cedula = fila[15].value)
                                                beneficiario.region = region
                                                beneficiario.radicado = radicado
                                                beneficiario.radicado_text = radicado_text
                                                beneficiario.formador = formador
                                                beneficiario.grupo = grupo
                                                beneficiario.apellidos =fila[13].value
                                                beneficiario.nombres = fila[14].value
                                                beneficiario.cedula=fila[15].value
                                                beneficiario.correo=fila[16].value
                                                beneficiario.telefono_fijo=fila[17].value
                                                beneficiario.telefono_celular=fila[18].value
                                                beneficiario.area = area
                                                beneficiario.grado = grado
                                                beneficiario.genero=fila[22].value
                                                beneficiario.estado=fila[23].value
                                                beneficiario.save()

                                                resultado += 'Docente actualizado'

                                            else:
                                                Beneficiario.objects.create(diplomado = diplomado,region=region,radicado=radicado,radicado_text=radicado_text,
                                                                            formador=formador,grupo=grupo,apellidos=fila[13].value,
                                                                            nombres=fila[14].value,cedula=fila[15].value,correo=fila[16].value,
                                                                            telefono_fijo=fila[17].value,telefono_celular=fila[18].value,
                                                                            area=area,grado=grado,genero=fila[22].value,estado=fila[23].value)
                                                resultado += 'Docente creado'

                                        else:
                                            resultado += 'No hay nombres del docente'

                                    else:
                                        resultado += 'No hay apellidos del docente'

                            else:
                                resultado = 'No se puede identificar el grupo'
                        else:
                            resultado = 'No hay ningun formador con el numero de cedula'

                    else:
                        resultado = 'No existe el código de región'


                else:
                    resultado = 'No existe el diplomado'




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

        usuario = User.objects.get(email=email)
        nombre = "Resultado carga masiva matrices"
        proceso = "FOR-MAS01"
        fecha = pytz.utc.localize(datetime.now())
        output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
        filename = unicode(fecha) + '.xlsx'
        carga.resultado.save(filename,File(output))
        carga.estado = 'Proceso concluido'

    elif 'Matriz revisión documental' in sheets:
        carga.estado = 'Iniciando carga masiva ...'

        titulos = ['DIPLOMADO',
                   'RESULTADO',
                   'REGION',
                   'DEPARTAMENTO',
                   'SECRETARIA DE EDUCACION',
                   'RADICADO',
                   'CODIGO DANE INSTITUCION EDUCATIVA',
                   'NOMBRE INSTITUCION EDUCATIVA',
                   'CODIGO DANE SEDE EDUCATIVA',
                   'NOMBRE DE LA SEDE EDUCATIVA',
                   'MUNICIPIO',
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
                   'GENERO',
                   'ESTADO']

        formatos = ['General',
                    'General',
                   '0',
                   'General',
                   'General',
                   '0',
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
                   'General',
                   'General',
                   'General',
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

        ws = wb.get_sheet_by_name('Matriz revisión documental')

        for fila in ws.rows[9:]:

            resultado = ''

            diplomado = Diplomado.objects.get(id = 4)

            if Region.objects.filter(numero = fila[0].value if fila[0].value != None else '').count() == 1:
                region = Region.objects.get(numero = fila[0].value if fila[0].value != None else 0)

                if Formador.objects.filter(cedula = fila[12].value if fila[12].value != None else 0).count() == 1:
                    formador = Formador.objects.get(cedula = fila[12].value if fila[12].value != None else 0)
                    grupo_list = fila[10].value.split('-') if fila[10].value != None else ['']

                    if len(grupo_list) > 1:
                        try:
                            grupo_numero = int(grupo_list[-1])
                        except:
                            resultado = 'No se puede identificar el grupo'
                        else:
                            try:
                                grupo, grupo_creado = Grupos.objects.get_or_create(formador=formador,nombre = grupo_numero)
                            except:
                                resultado = 'Hay mas de un grupo con el codigo'

                            else:

                                if grupo_creado:
                                    resultado += 'Grupo creado, '

                                if fila[13].value != None:

                                    if fila[14].value != None:

                                        try:
                                            radicado_numero = int(fila[3].value)
                                        except:
                                            radicado_numero = -1

                                        if Radicado.objects.filter(numero = radicado_numero).count() == 1:
                                            radicado = Radicado.objects.get(numero = radicado_numero)
                                        else:
                                            radicado = None


                                        area = None
                                        grado = None

                                        radicado_text = str(radicado.numero) if radicado != None else ''

                                        try:
                                            cedula = long(fila[15].value)
                                        except:
                                            resultado = 'Error en el numero de cedula'

                                        else:

                                            if Beneficiario.objects.filter(cedula = fila[15].value if fila[15].value != None else '').count() == 1:
                                                beneficiario = Beneficiario.objects.get(cedula = fila[15].value)
                                                if beneficiario.diplomado.id == 4:
                                                    beneficiario.region = region
                                                    beneficiario.radicado = radicado
                                                    beneficiario.radicado_text = radicado_text
                                                    beneficiario.formador = formador
                                                    beneficiario.grupo = grupo
                                                    beneficiario.apellidos =fila[13].value
                                                    beneficiario.nombres = fila[14].value
                                                    beneficiario.cedula=fila[15].value
                                                    beneficiario.correo=fila[16].value
                                                    beneficiario.telefono_fijo=fila[17].value
                                                    beneficiario.telefono_celular=fila[18].value
                                                    beneficiario.area = area
                                                    beneficiario.grado = grado
                                                    beneficiario.genero=fila[22].value
                                                    beneficiario.estado=fila[23].value
                                                    beneficiario.save()

                                                    resultado += 'Participante actualizado'

                                                else:
                                                    resultado += 'El participante se encuentra registrado como docente'

                                            else:
                                                Beneficiario.objects.create(diplomado = diplomado,region=region,radicado=radicado,radicado_text=radicado_text,
                                                                                    formador=formador,grupo=grupo,apellidos=fila[13].value,
                                                                                    nombres=fila[14].value,cedula=fila[15].value,correo=fila[16].value,
                                                                                    telefono_fijo=fila[17].value,telefono_celular=fila[18].value,
                                                                                    area=area,grado=grado,genero=fila[22].value,estado=fila[23].value)
                                                resultado += 'Participante creado'

                                    else:
                                        resultado += 'No hay nombres del participante'

                                else:
                                    resultado += 'No hay apellidos del participante'

                    else:
                        resultado = 'No se puede identificar el grupo'
                else:
                    resultado = 'No hay ningun formador con el numero de cedula'

            else:
                resultado = 'No existe el código de región'






            contenidos.append([
                'Escuela TIC',
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

        usuario = User.objects.get(email=email)
        nombre = "Resultado carga masiva matrices"
        proceso = "FOR-MAS01"
        fecha = pytz.utc.localize(datetime.now())
        output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
        filename = unicode(fecha) + '.xlsx'
        carga.resultado.save(filename,File(output))
        carga.estado = 'Proceso concluido'


    else:
        carga.estado = 'El archivo no tiene la estructura necesaria.'

    carga.save()
    return "Carga masiva exitosa"