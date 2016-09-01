#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
from informes.functions import construir_reporte, cronograma_interventoria
from informes.models import InformesExcel
from django.core.files import File
from usuarios.models import User
from formadores.models import Formador, Soporte, SolicitudTransporte
from rh.models import TipoSoporte
from preinscripcion.models import DocentesPreinscritos
from formacion.models import EntradaCronograma
from isoweek import Week
import datetime
from formacion.models import Semana


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
                soporte = Soporte.objects.filter(formador=formador).get(tipo__id=tipo_soporte[0])
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