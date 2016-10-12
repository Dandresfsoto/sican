#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
from informes.functions import construir_reporte, cronograma_interventoria
from informes.models import InformesExcel
from django.core.files import File
from usuarios.models import User
from formadores.models import Formador, SolicitudTransporte
from formadores.models import Soporte as SoporteFormadores
from rh.models import TipoSoporte
from preinscripcion.models import DocentesPreinscritos
from formacion.models import EntradaCronograma
from isoweek import Week
import datetime
from formacion.models import Semana
from lideres.models import Lideres, Soporte
from encuestas.models import PercepcionInicial
from radicados.models import Radicado
from formadores.models import Cortes
from formadores.models import Revision
import zipfile
import shutil
import os
from rh.models import RequerimientoPersonal

@app.task
def nueva_semana():
    x, created = Semana.objects.get_or_create(numero = datetime.datetime.now().isocalendar()[1]+1)
    return "Semana actualizada"

@app.task
def formadores(email):
    usuario = User.objects.get(email=email)
    nombre = "Directorio de formadores"
    proceso = "RH-INF01"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Nombres','Apellidos','Cedula','Región','Correo','Celular','Cargo','Profesión','Inicio contrato',
               'Fin contrato','Banco','Tipo cuenta','Numero cuenta','Eps','Pensión','Arl']

    formatos = ['General','General','General','General','General','General','General','General','General','d/m/yy',
               'd/m/yy','General','General','General','General','General','General']


    ancho_columnas =  [30,20,20,15,15,50,25,20,20,10,
                       10,20,20,20,20,20,20]

    contenidos = []

    for formador in Formador.objects.exclude(oculto=True):
        contenidos.append([
            'FOR-'+unicode(formador.id),
            formador.nombres,
            formador.apellidos,
            formador.cedula,
            formador.get_region_string(),
            formador.correo_personal,
            formador.celular_personal,
            formador.cargo.nombre if formador.cargo != None else '',
            formador.profesion,
            formador.fecha_contratacion,
            formador.fecha_terminacion,
            formador.banco.nombre if formador.banco != None else '',
            formador.tipo_cuenta,
            formador.numero_cuenta,
            formador.eps,
            formador.pension,
            formador.arl
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"


@app.task
def reporte_requerimientos_contratacion(email):
    usuario = User.objects.get(email=email)
    nombre = "Requerimientos de contratacion"
    proceso = "RH-INF05"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Fecha Solicitud','Solicitante','Departamento','Municipios','Codigo Ruta','Encargado','Observación Solicitante',
               'Fecha Respuesta','Nombre','Cedula','Celular','Email','Hoja de vida','Observación respuesta','Fecha solicitud de contratación',
               'Observacion final','Estado']

    formatos = ['General','d/m/yy','General','General','General','General','General','General',
                'd/m/yy','General','0','General','General','General','General','d/m/yy',
                'General','General']


    ancho_columnas =  [30,15,20,15,30,15,20,30,
                       15,20,15,15,20,20,30,20,
                       30,30]

    contenidos = []

    for requerimiento in RequerimientoPersonal.objects.all():

        estado = ''

        if requerimiento.remitido_respuesta == False and requerimiento.remitido_contratacion == False and requerimiento.contratar == False and requerimiento.desierto == False and requerimiento.contratado == False:
            estado = 'Remitido a RH'

        elif requerimiento.remitido_respuesta == True and requerimiento.remitido_contratacion == False and requerimiento.contratar == False and requerimiento.desierto == False and requerimiento.contratado == False:
            estado = 'Listo para capacitar'

        elif requerimiento.remitido_respuesta == True and requerimiento.remitido_contratacion == True and requerimiento.contratar == True and requerimiento.desierto == False and requerimiento.contratado == False:
            estado = 'Proceder a contrato'

        elif requerimiento.remitido_respuesta == True and requerimiento.remitido_contratacion == True and requerimiento.contratar == False and requerimiento.desierto == True and requerimiento.contratado == False:
            estado = 'Aspirante deserta'

        elif requerimiento.contratado == True:
            estado = 'Contratado'


        contenidos.append([
            'REQ-'+unicode(requerimiento.id),
            requerimiento.fecha_solicitud,
            requerimiento.solicitante.get_full_name_string(),
            requerimiento.departamento.nombre,
            requerimiento.get_municipios_string(),
            requerimiento.codigo_ruta,
            requerimiento.encargado.get_full_name_string(),
            requerimiento.observacion_solicitante,
            requerimiento.fecha_respuesta,
            requerimiento.nombre,
            requerimiento.cedula,
            requerimiento.celular,
            requerimiento.email,
            'Si' if str(requerimiento.hv) != '' else 'No',
            requerimiento.observacion_respuesta,
            requerimiento.fecha_solicitud_contratacion,
            requerimiento.observacion_final,
            estado
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"


@app.task
def formadores_soportes(email):
    usuario = User.objects.get(email=email)
    nombre = "Soportes cargados por formador"
    proceso = "RH-INF02"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Nombres','Apellidos','Cedula','Región']

    formatos = ['General','General','General','General','General']


    ancho_columnas =  [30,20,20,15,15]

    contenidos = []

    tipos_soportes = TipoSoporte.objects.exclude(oculto=True).values_list('id','nombre')

    for tipo_soporte in tipos_soportes:
        titulos.append(tipo_soporte[1])
        formatos.append('General')
        ancho_columnas.append(30)

    for formador in Formador.objects.exclude(oculto=True):
        row =[
                'FOR-'+unicode(formador.id),
                formador.nombres,
                formador.apellidos,
                formador.cedula,
                formador.get_region_string(),
            ]
        for tipo_soporte in tipos_soportes:
            try:
                soporte = SoporteFormadores.objects.filter(formador=formador).get(tipo__id=tipo_soporte[0])
            except:
                row.append('No')
            else:
                if soporte.get_archivo_url() != "":
                    row.append('Si')
                else:
                    row.append('No')

        contenidos.append(row)

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def preinscritos(email):
    usuario = User.objects.get(email=email)
    nombre = "Reporte de docentes preinscritos"
    proceso = "FOR-INF01"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Cedula','Primer apellido','Segundo apellido','Primer nombre','Segundo nombre','Cargo','Correo',
               'Telefono fijo','Celular','Departamento','Municipio','Radicado','Base Mineducación','Fecha registro',
               'Secretaria Radicado','Municipio Radicado','Nombre Sede','Dane Sede','Tipo Sede','Ubicación']

    formatos = ['General','0','General','General','General','General','General','General',
                'General','General','General','General','0','General','d/m/yy',
                'General','General','General','General','General','General']


    ancho_columnas =  [30,20,15,15,15,15,15,30,
                       15,15,20,20,15,10,15,
                       20,20,20,20,20,20]

    contenidos = []

    for docente in DocentesPreinscritos.objects.all():
        contenidos.append([
            'PRE-'+unicode(docente.id),
            docente.cedula,
            docente.primer_apellido,
            docente.segundo_apellido,
            docente.primer_nombre,
            docente.segundo_nombre,
            docente.cargo,
            docente.correo,
            docente.telefono_fijo,
            docente.telefono_celular,
            docente.departamento.nombre if docente.departamento != None else '',
            docente.municipio.nombre if docente.municipio != None else '',
            docente.radicado.numero if docente.radicado != None else '',
            'Si' if docente.verificado else 'No',
            docente.fecha,
            docente.radicado.secretaria.nombre,
            docente.radicado.municipio.nombre,
            docente.radicado.nombre_sede,
            docente.radicado.dane_sede,
            docente.radicado.tipo,
            docente.radicado.ubicacion,
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def transportes(email):
    usuario = User.objects.get(email=email)
    nombre = "Reporte de solicitudes de desplazamiento"
    proceso = "FIN-INF01"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Formador','Cedula','Región','Cargo','Banco','Tipo de cuenta','Numero de cuenta',
               'Nombre solicitud','Fecha','Estado','Valor solicitado','Valor Aprobado','Observación']

    formatos = ['General','General','General','General','General','General','General','General',
                'General','d/m/yy h:mm:ss AM/PM','General','"$"#,##0_);("$"#,##0)','"$"#,##0_);("$"#,##0)','General']


    ancho_columnas =  [30,30,15,15,15,15,15,20,
                       50,15,20,15,15,60]

    contenidos = []

    for solicitud in SolicitudTransporte.objects.all():
        contenidos.append([
            'PRE-'+unicode(solicitud.id),
            solicitud.formador.get_full_name(),
            solicitud.formador.cedula,
            solicitud.formador.get_region_string(),
            solicitud.formador.cargo.nombre if solicitud.formador.cargo != None else "",
            solicitud.formador.banco.nombre if solicitud.formador.banco != None else "",
            solicitud.formador.tipo_cuenta,
            solicitud.formador.numero_cuenta,
            solicitud.nombre,
            solicitud.creacion,
            solicitud.estado,
            solicitud.valor,
            solicitud.valor_aprobado,
            solicitud.observacion
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def cronograma_general(email,semana_id):
    usuario = User.objects.get(email=email)
    nombre = "Cronograma consolidado general"

    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    semana = Semana.objects.get(id=semana_id)

    innovatics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 1").order_by('formador__region').values_list('id',flat=True)
    tecnotics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 2").order_by('formador__region').values_list('id',flat=True)
    directics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 3").order_by('formador__region').values_list('id',flat=True)
    escuelatics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 4").order_by('formador__region').values_list('id',flat=True)

    inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).monday()
    fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).sunday()
    rango = inicio.strftime("Del dia %d de %B del %Y") + ' - ' + fin.strftime(" al dia %d de %B del %Y")

    output = cronograma_interventoria(innovatics,tecnotics,directics,escuelatics,rango)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def cronograma_lider(email,semana_id):
    usuario = User.objects.get(email=email)
    nombre = "Cronograma semanal lider"

    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    semana = Semana.objects.get(id=semana_id)

    innovatics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 1",formador__lider__email = email).values_list('id',flat=True)
    tecnotics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 2",formador__lider__email = email).values_list('id',flat=True)
    directics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 3",formador__lider__email = email).values_list('id',flat=True)
    escuelatics = EntradaCronograma.objects.filter(semana=semana,formador__cargo__nombre="Formador Tipo 4",formador__lider__email = email).values_list('id',flat=True)

    inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).monday()
    fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).sunday()
    rango = inicio.strftime("Del dia %d de %B del %Y") + ' - ' + fin.strftime(" al dia %d de %B del %Y")

    output = cronograma_interventoria(innovatics,tecnotics,directics,escuelatics,rango)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def lideres(email):
    usuario = User.objects.get(email=email)
    nombre = "Directorio de lideres"
    proceso = "RH-INF03"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Nombres','Apellidos','Cedula','Región','Correo','Celular','Cargo','Profesión','Inicio contrato',
               'Fin contrato','Banco','Tipo cuenta','Numero cuenta','Eps','Pensión','Arl']

    formatos = ['General','General','General','General','General','General','General','General','General','d/m/yy',
               'd/m/yy','General','General','General','General','General','General']


    ancho_columnas =  [30,20,20,15,15,50,25,20,20,10,
                       10,20,20,20,20,20,20]

    contenidos = []

    for lider in Lideres.objects.exclude(oculto=True):
        contenidos.append([
            'LID-'+unicode(lider.id),
            lider.nombres,
            lider.apellidos,
            lider.cedula,
            lider.region.nombre,
            lider.correo_personal,
            lider.celular_personal,
            lider.cargo.nombre if lider.cargo != None else '',
            lider.profesion,
            lider.fecha_contratacion,
            lider.fecha_terminacion,
            lider.banco.nombre if lider.banco != None else '',
            lider.tipo_cuenta,
            lider.numero_cuenta,
            lider.eps,
            lider.pension,
            lider.arl
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def lideres_soportes(email):
    usuario = User.objects.get(email=email)
    nombre = "Soportes cargados por lider"
    proceso = "RH-INF04"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Nombres','Apellidos','Cedula','Región']

    formatos = ['General','General','General','General','General']


    ancho_columnas =  [30,20,20,15,15]

    contenidos = []

    tipos_soportes = TipoSoporte.objects.exclude(oculto=True).values_list('id','nombre')

    for tipo_soporte in tipos_soportes:
        titulos.append(tipo_soporte[1])
        formatos.append('General')
        ancho_columnas.append(30)

    for lider in Lideres.objects.exclude(oculto=True):
        row =[
                'LID-'+unicode(lider.id),
                lider.nombres,
                lider.apellidos,
                lider.cedula,
                lider.region.nombre,
            ]
        for tipo_soporte in tipos_soportes:
            try:
                soporte = Soporte.objects.filter(lider=lider).get(tipo__id=tipo_soporte[0])
            except:
                row.append('No')
            else:
                if soporte.get_archivo_url() != "":
                    row.append('Si')
                else:
                    row.append('No')

        contenidos.append(row)

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def encuesta_percepcion_inicial(email):
    usuario = User.objects.get(email=email)
    nombre = "Base de datos respuestas percepción inicial"
    proceso = "ENC-INF01"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Cedula','Primer Apellido','Segundo Apellido','Primer Nombre','Segundo Nombre','Cargo','Correo','Telefono Fijo','Telefono Celular',
               'Departamento','Municipio','Verificado','Fecha','Radicado','Secretaria','Municipio Radicado','Nombre Sede','Dane Sede','Ubicación',
               'Area','Area Otras','Antiguedad','Pregunta 1','Pregunta 1 Opcional','Pregunta 2','Pregunta 3','Pregunta 4','Pregunta 5','Pregunta 6',
               'Pregunta 6 Opcional','Pregunta 7','Pregunta 8','Pregunta 9','Pregunta 10','Pregunta 11','Pregunta 12','Pregunta 12 Opcional','Pregunta 13']

    formatos = ['General','0','General','General','General','General','General','General','General','General',
                'General','General','General','d/m/yy','0','General','General','General','0','General',
                'General','General','General','General','General','General','General','General','General','General',
                'General','General','General','General','General','General','General','General','General',]


    ancho_columnas =  [30,20,15,15,15,40,40,40,40,40,
                       40,40,40,40,40,40,40,40,40,40,
                       60,60,60,60,60,60,60,60,60,60,
                       60,60,60,60,60,60,60,60,60]

    contenidos = []

    for encuestado in PercepcionInicial.objects.all():
        contenidos.append([
            'ENC-'+unicode(encuestado.id),
            encuestado.docente_preinscrito.cedula,
            encuestado.docente_preinscrito.primer_apellido,
            encuestado.docente_preinscrito.segundo_apellido,
            encuestado.docente_preinscrito.primer_nombre,
            encuestado.docente_preinscrito.segundo_nombre,
            encuestado.docente_preinscrito.cargo,
            encuestado.docente_preinscrito.correo,
            encuestado.docente_preinscrito.telefono_fijo,
            encuestado.docente_preinscrito.telefono_celular,
            encuestado.docente_preinscrito.departamento.nombre if encuestado.docente_preinscrito.departamento != None else '',
            encuestado.docente_preinscrito.municipio.nombre if encuestado.docente_preinscrito.municipio != None else '',
            'SI' if encuestado.docente_preinscrito.verificado else 'NO',
            encuestado.docente_preinscrito.fecha,
            encuestado.docente_preinscrito.radicado.numero if encuestado.docente_preinscrito.radicado != None else '',
            encuestado.docente_preinscrito.radicado.secretaria.nombre if encuestado.docente_preinscrito.radicado.secretaria != None else '',
            encuestado.docente_preinscrito.radicado.municipio.nombre if encuestado.docente_preinscrito.radicado.municipio != None else '',
            encuestado.docente_preinscrito.radicado.nombre_sede if encuestado.docente_preinscrito.radicado != None else '',
            encuestado.docente_preinscrito.radicado.dane_sede if encuestado.docente_preinscrito.radicado != None else '',
            encuestado.docente_preinscrito.radicado.ubicacion if encuestado.docente_preinscrito.radicado != None else '',
            encuestado.area,
            encuestado.area_1,
            encuestado.antiguedad,
            encuestado.pregunta_1,
            encuestado.pregunta_1_1,
            encuestado.pregunta_2,
            encuestado.pregunta_3,
            encuestado.pregunta_4,
            encuestado.pregunta_5,
            encuestado.pregunta_6,
            encuestado.pregunta_6_1,
            encuestado.pregunta_7,
            encuestado.pregunta_8,
            encuestado.pregunta_9,
            encuestado.pregunta_10,
            encuestado.pregunta_11,
            encuestado.pregunta_12,
            encuestado.pregunta_12_1,
            encuestado.pregunta_13,
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def radicados(email):
    usuario = User.objects.get(email=email)
    nombre = "Base de datos radicados"
    proceso = "DB-INF01"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion

    titulos = ['ID','Numero','Municipio','Departamento','Secretaria','Nombre Sede','Dane Sede','Tipo','Ubicación']

    formatos = ['General','General','General','General','General','General','General','General','General']


    ancho_columnas =  [30,30,30,30,30,30,30,30,30]

    contenidos = []

    for radicado in Radicado.objects.exclude(oculto=True):
        contenidos.append([
            'RAD-'+unicode(radicado.id),
            radicado.numero,
            radicado.municipio.nombre if radicado.municipio != None else '',
            radicado.municipio.departamento.nombre if radicado.municipio.departamento != None else '',
            radicado.secretaria.nombre if radicado.secretaria != None else '',
            radicado.nombre_sede,
            radicado.dane_sede,
            radicado.tipo,
            radicado.ubicacion
        ])

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def pagos_mensual(email):
    usuario = User.objects.get(email=email)
    nombre = "Reporte mensual de pago a formadores"
    proceso = "COR-INF02"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")
    fecha = informe.creacion
    cortes = Cortes.objects.all()
    fechas = []

    for corte in cortes:
        fecha_corte = '01/' + str(corte.mes) + '/' + str(corte.year)
        fecha_corte = datetime.datetime.strptime(fecha_corte,"%d/%m/%Y").date()
        fechas.append(fecha_corte)

    fechas = list(set(fechas))


    titulos = ['ID','Nombres','Apellidos','Cedula','Región',
               'Correo','Celular','Cargo','Banco','Tipo cuenta','Numero cuenta']


    formatos = ['General','General','General','General','General',
               'General','General','General','General','General','General']


    ancho_columnas =  [30,20,20,15,15,
                       40,20,20,20,20,20]


    for fecha_corte in fechas:
        titulos.append(fecha_corte.strftime("%B de %Y"))
        formatos.append('"$"#,##0_);("$"#,##0)')
        ancho_columnas.append(30)

    contenidos = []



    for formador in Formador.objects.all():
        row =[
                'FOR-'+unicode(formador.id),
                formador.nombres,
                formador.apellidos,
                formador.cedula,
                formador.get_region_string(),
                formador.correo_personal,
                formador.celular_personal,
                formador.cargo.nombre if formador.cargo != None else '',
                formador.banco.nombre if formador.banco != None else '',
                formador.tipo_cuenta,
                formador.numero_cuenta,
            ]
        for fecha_corte in fechas:
            valor = 0
            for corte in Cortes.objects.filter(mes = str(fecha_corte.month).zfill(2), year = fecha_corte.year):
                revisiones = Revision.objects.filter(corte = corte, formador_revision = formador)
                for revision in revisiones:
                    for producto in revision.productos.all():
                        valor += producto.cantidad * producto.valor_entregable.valor

            row.append(valor)

        contenidos.append(row)

    output = construir_reporte(titulos,contenidos,formatos,ancho_columnas,nombre,fecha,usuario,proceso)
    filename = unicode(informe.creacion) + '.xlsx'
    informe.archivo.save(filename,File(output))
    return "Reporte generado exitosamente"

@app.task
def zip_hv(email):

    if os.path.exists("C:\\Temp\\hv.zip"):
        os.remove("C:\\Temp\\hv.zip")

    usuario = User.objects.get(email=email)
    nombre = "Zip: Hojas de vida"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")

    zip = zipfile.ZipFile('C:\\Temp\\hv.zip',"w",allowZip64=True)

    for soporte in SoporteFormadores.objects.filter(tipo__id = 3).exclude(oculto = True):
        if str(soporte.archivo) != '':
            if os.path.exists(soporte.archivo.path):
                zip.write(soporte.archivo.path,soporte.formador.get_full_name()+'/'+os.path.basename(soporte.archivo.path))

    zip.close()
    informe.archivo = File(open('C:\\Temp\\hv.zip'))
    informe.save()

    shutil.copy('C:\\Temp\\hv.zip',informe.archivo.path)

    return "Zip creado HV"

@app.task
def zip_contrato(email):

    if os.path.exists("C:\\Temp\\contratos.zip"):
        os.remove("C:\\Temp\\contratos.zip")

    usuario = User.objects.get(email=email)
    nombre = "Zip: Contratos"
    informe = InformesExcel.objects.create(usuario = usuario,nombre=nombre,progreso="0%")


    zip = zipfile.ZipFile('C:\\Temp\\contratos.zip',"w",allowZip64=True)

    for soporte in SoporteFormadores.objects.filter(tipo__id = 10).exclude(oculto = True):
        if str(soporte.archivo) != '':
            if os.path.exists(soporte.archivo.path):
                zip.write(soporte.archivo.path,soporte.formador.get_full_name()+'/'+os.path.basename(soporte.archivo.path))

    zip.close()
    informe.archivo = File(open('C:\\Temp\\contratos.zip'))
    informe.save()

    shutil.copy('C:\\Temp\\contratos.zip',informe.archivo.path)

    return "Zip creado Contrato"