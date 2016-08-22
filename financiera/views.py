#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from formadores.models import SolicitudTransporte, Desplazamiento
from formadores.forms import SolicitudTransporteForm, SolicitudTransporteAdminForm,SolicitudTransporteUpdateForm
from financiera.tasks import construir_pdf
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
import locale
from django.views.generic.edit import ModelFormMixin
from departamentos.models import Departamento
from municipios.models import Municipio
from formadores.models import Formador
from productos.models import Diplomado, Nivel, Sesion
from productos.forms import DiplomadoForm, UpdateDiplomadoForm, NivelForm, UpdateNivelForm, SesionForm, UpdateSesionForm


# Create your views here.
class TransportesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.financiera.transportes.crear')
        kwargs['reporte_permiso'] = self.request.user.has_perm('permisos_sican.financiera.transportes.informe')
        return super(TransportesView, self).get_context_data(**kwargs)


class TransportesConsignadasFinancieraView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/consignadas/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador'])
        return super(TransportesConsignadasFinancieraView,self).get_context_data(**kwargs)


class TransportesAprobadasFinancieraView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/aprobadasfinanciera/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador'])
        return super(TransportesAprobadasFinancieraView,self).get_context_data(**kwargs)


class TransportesAprobadasLideresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/aprobadaslideres/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador'])
        return super(TransportesAprobadasLideresView,self).get_context_data(**kwargs)


class TransportesRechazadasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/rechazadas/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador'])
        return super(TransportesRechazadasView,self).get_context_data(**kwargs)


class TransportesPendientesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/pendientes/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador'])
        return super(TransportesPendientesView,self).get_context_data(**kwargs)




class TransportesEstadoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SolicitudTransporte
    form_class = SolicitudTransporteForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'financiera/transportes/estado.html'
    permission_required = "permisos_sican.financiera.transportes.estado"

    def form_valid(self, form):
        self.object = form.save()


        self.object.terminada = False
        self.object.valor_aprobado = 0

        valores = self.object.desplazamientos.all().values_list('valor',flat=True)

        valor_aprobado = 0
        for valor in valores:
            valor_aprobado += valor

        if self.object.estado == 'aprobado_lider':
            self.object.valor_aprobado = 0
            self.object.save()

        elif self.object.estado == 'aprobado':
            self.object.valor_aprobado = valor_aprobado
            self.object.save()
            construir_pdf.delay(self.object.id)
            send_mail_templated.delay('email/desplazamiento.tpl',
                                      {
                                          'url_base':'http://sican.asoandes.org/',
                                          'fullname':self.object.formador.get_full_name(),
                                          'nombre_solicitud': self.object.nombre,
                                          'fecha_solicitud': self.object.creacion.strftime('%d/%m/%Y'),
                                          'valor_solicitado': locale.currency(self.object.valor,grouping=True),
                                          'valor_aprobado': locale.currency(valor_aprobado,grouping=True),
                                          'observacion': form.cleaned_data['observacion'],
                                          'estado': 'Solicitud aprobada'
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])


        elif self.object.estado == 'consignado':
            self.object.terminada = True
            self.object.valor_aprobado = valor_aprobado
            self.object.save()
            send_mail_templated.delay('email/desplazamiento.tpl',
                                      {
                                          'url_base':'http://sican.asoandes.org/',
                                          'fullname':self.object.formador.get_full_name(),
                                          'nombre_solicitud': self.object.nombre,
                                          'fecha_solicitud': self.object.creacion.strftime('%d/%m/%Y'),
                                          'valor_solicitado': locale.currency(self.object.valor,grouping=True),
                                          'valor_aprobado': locale.currency(valor_aprobado,grouping=True),
                                          'observacion': form.cleaned_data['observacion'],
                                          'estado': 'Consignado'
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])


        elif self.object.estado == 'rechazado':
            self.object.valor_aprobado = 0
            self.object.save()
            send_mail_templated.delay('email/desplazamiento.tpl',
                                      {
                                          'url_base':'http://sican.asoandes.org/',
                                          'fullname':self.object.formador.get_full_name(),
                                          'nombre_solicitud': self.object.nombre,
                                          'fecha_solicitud': self.object.creacion.strftime('%d/%m/%Y'),
                                          'valor_solicitado': locale.currency(self.object.valor,grouping=True),
                                          'valor_aprobado': locale.currency(0,grouping=True),
                                          'observacion': form.cleaned_data['observacion'],
                                          'estado': 'Solicitud rechazada'
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])

        elif self.object.estado == 'revision':
            self.object.valor_aprobado = 0
            self.object.save()



        return super(ModelFormMixin,self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['valor_solicitado'] = locale.currency(self.object.valor,grouping=True)
        lider = self.object.valor_aprobado_lider
        if lider != None:
            kwargs['valor_aprobado_lider'] = locale.currency(lider,grouping=True)
        else:
            kwargs['valor_aprobado_lider'] = locale.currency(0,grouping=True)
        kwargs['archivo_url'] = self.object.get_archivo_url()
        kwargs['archivo_filename'] = self.object.archivo_filename()
        return super(TransportesEstadoView,self).get_context_data(**kwargs)


class TransportesEliminarView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SolicitudTransporte
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'financiera/transportes/eliminar.html'
    permission_required = "permisos_sican.financiera.transportes.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['valor_solicitado'] = locale.currency(self.object.valor,grouping=True)
        if self.object.valor_aprobado != None:
            kwargs['valor_aprobado'] = locale.currency(self.object.valor_aprobado,grouping=True)
        kwargs['archivo_url'] = self.object.get_archivo_url()
        kwargs['archivo_filename'] = self.object.archivo_filename()
        return super(TransportesEliminarView,self).get_context_data(**kwargs)


class TransportesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               FormView):
    form_class = SolicitudTransporteAdminForm
    success_url = '/financiera/transportes/'
    template_name = 'financiera/transportes/nuevo.html'
    permission_required = "permisos_sican.financiera.transportes.crear"

    def form_valid(self, form):



        desplazamientos = [
            {
                'fecha':form.cleaned_data['fecha_1'],
                'd_origen':form.cleaned_data['departamento_origen_1'],
                'm_origen':form.cleaned_data['municipio_origen_1'],
                'd_destino':form.cleaned_data['departamento_destino_1'],
                'm_destino':form.cleaned_data['municipio_destino_1'],
                'valor':float(form.cleaned_data['valor_1'].replace(',','')) if form.cleaned_data['valor_1'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_2'],
                'd_origen':form.cleaned_data['departamento_origen_2'],
                'm_origen':form.cleaned_data['municipio_origen_2'],
                'd_destino':form.cleaned_data['departamento_destino_2'],
                'm_destino':form.cleaned_data['municipio_destino_2'],
                'valor':float(form.cleaned_data['valor_2'].replace(',','')) if form.cleaned_data['valor_2'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_3'],
                'd_origen':form.cleaned_data['departamento_origen_3'],
                'm_origen':form.cleaned_data['municipio_origen_3'],
                'd_destino':form.cleaned_data['departamento_destino_3'],
                'm_destino':form.cleaned_data['municipio_destino_3'],
                'valor':float(form.cleaned_data['valor_3'].replace(',','')) if form.cleaned_data['valor_3'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_4'],
                'd_origen':form.cleaned_data['departamento_origen_4'],
                'm_origen':form.cleaned_data['municipio_origen_4'],
                'd_destino':form.cleaned_data['departamento_destino_4'],
                'm_destino':form.cleaned_data['municipio_destino_4'],
                'valor':float(form.cleaned_data['valor_4'].replace(',','')) if form.cleaned_data['valor_4'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_5'],
                'd_origen':form.cleaned_data['departamento_origen_5'],
                'm_origen':form.cleaned_data['municipio_origen_5'],
                'd_destino':form.cleaned_data['departamento_destino_5'],
                'm_destino':form.cleaned_data['municipio_destino_5'],
                'valor':float(form.cleaned_data['valor_5'].replace(',','')) if form.cleaned_data['valor_5'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_6'],
                'd_origen':form.cleaned_data['departamento_origen_6'],
                'm_origen':form.cleaned_data['municipio_origen_6'],
                'd_destino':form.cleaned_data['departamento_destino_6'],
                'm_destino':form.cleaned_data['municipio_destino_6'],
                'valor':float(form.cleaned_data['valor_6'].replace(',','')) if form.cleaned_data['valor_6'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_7'],
                'd_origen':form.cleaned_data['departamento_origen_7'],
                'm_origen':form.cleaned_data['municipio_origen_7'],
                'd_destino':form.cleaned_data['departamento_destino_7'],
                'm_destino':form.cleaned_data['municipio_destino_7'],
                'valor':float(form.cleaned_data['valor_7'].replace(',','')) if form.cleaned_data['valor_7'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_8'],
                'd_origen':form.cleaned_data['departamento_origen_8'],
                'm_origen':form.cleaned_data['municipio_origen_8'],
                'd_destino':form.cleaned_data['departamento_destino_8'],
                'm_destino':form.cleaned_data['municipio_destino_8'],
                'valor':float(form.cleaned_data['valor_8'].replace(',','')) if form.cleaned_data['valor_8'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_9'],
                'd_origen':form.cleaned_data['departamento_origen_9'],
                'm_origen':form.cleaned_data['municipio_origen_9'],
                'd_destino':form.cleaned_data['departamento_destino_9'],
                'm_destino':form.cleaned_data['municipio_destino_9'],
                'valor':float(form.cleaned_data['valor_9'].replace(',','')) if form.cleaned_data['valor_9'] != u'' else 0,
            },
            {
                'fecha':form.cleaned_data['fecha_10'],
                'd_origen':form.cleaned_data['departamento_origen_10'],
                'm_origen':form.cleaned_data['municipio_origen_10'],
                'd_destino':form.cleaned_data['departamento_destino_10'],
                'm_destino':form.cleaned_data['municipio_destino_10'],
                'valor':float(form.cleaned_data['valor_10'].replace(',','')) if form.cleaned_data['valor_10'] != u'' else 0,
            },
        ]

        desplazamientos_obj = []

        valor = 0

        for desplazamiento in desplazamientos:
            if desplazamiento['valor'] != None:
                if desplazamiento['fecha'] != '':
                    if desplazamiento['d_origen'] != '':
                        if desplazamiento['m_origen'] != '':
                            if desplazamiento['d_destino'] != '':
                                if desplazamiento['m_destino'] != '':
                                    valor += desplazamiento['valor']
                                    desplazamientos_obj.append(Desplazamiento.objects.create(
                                        departamento_origen=Departamento.objects.get(id=desplazamiento['d_origen']),
                                        municipio_origen=Municipio.objects.get(id=desplazamiento['m_origen']),
                                        departamento_destino=Departamento.objects.get(id=desplazamiento['d_destino']),
                                        municipio_destino=Municipio.objects.get(id=desplazamiento['m_destino']),
                                        valor=desplazamiento['valor'],
                                        fecha = desplazamiento['fecha']
                                    ))

        solicitud = SolicitudTransporte.objects.create(
            formador = Formador.objects.get(id=form.cleaned_data['formador']),
            nombre = form.cleaned_data['nombre'],
            valor = valor
        )

        for desplazamiento_obj in desplazamientos_obj:
            solicitud.desplazamientos.add(desplazamiento_obj)

        solicitud.save()



        return super(TransportesCreateView,self).form_valid(form)


class TransportesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               FormView):
    form_class = SolicitudTransporteUpdateForm
    success_url = '../../'
    template_name = 'financiera/transportes/editar.html'
    permission_required = "permisos_sican.financiera.transportes.editar"

    def get_initial(self):
        return {'pk':self.kwargs['pk']}

    def get_context_data(self, **kwargs):
        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['pk'])
        kwargs['formador'] = Formador.objects.get(id = solicitud.formador.id).get_full_name()
        kwargs['solicitud'] = solicitud.nombre
        return super(TransportesUpdateView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        desplazamientos = [
            {
                'id':form.cleaned_data['id_1'],
                'fecha':form.cleaned_data['fecha_1'],
                'd_origen':form.cleaned_data['departamento_origen_1'],
                'm_origen':form.cleaned_data['municipio_origen_1'],
                'd_destino':form.cleaned_data['departamento_destino_1'],
                'm_destino':form.cleaned_data['municipio_destino_1'],
                'valor':float(form.cleaned_data['valor_1'].replace(',','')) if form.cleaned_data['valor_1'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_1'],
            },
            {
                'id':form.cleaned_data['id_2'],
                'fecha':form.cleaned_data['fecha_2'],
                'd_origen':form.cleaned_data['departamento_origen_2'],
                'm_origen':form.cleaned_data['municipio_origen_2'],
                'd_destino':form.cleaned_data['departamento_destino_2'],
                'm_destino':form.cleaned_data['municipio_destino_2'],
                'valor':float(form.cleaned_data['valor_2'].replace(',','')) if form.cleaned_data['valor_2'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_2'],
            },
            {
                'id':form.cleaned_data['id_3'],
                'fecha':form.cleaned_data['fecha_3'],
                'd_origen':form.cleaned_data['departamento_origen_3'],
                'm_origen':form.cleaned_data['municipio_origen_3'],
                'd_destino':form.cleaned_data['departamento_destino_3'],
                'm_destino':form.cleaned_data['municipio_destino_3'],
                'valor':float(form.cleaned_data['valor_3'].replace(',','')) if form.cleaned_data['valor_3'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_3'],
            },
            {
                'id':form.cleaned_data['id_4'],
                'fecha':form.cleaned_data['fecha_4'],
                'd_origen':form.cleaned_data['departamento_origen_4'],
                'm_origen':form.cleaned_data['municipio_origen_4'],
                'd_destino':form.cleaned_data['departamento_destino_4'],
                'm_destino':form.cleaned_data['municipio_destino_4'],
                'valor':float(form.cleaned_data['valor_4'].replace(',','')) if form.cleaned_data['valor_4'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_4'],
            },
            {
                'id':form.cleaned_data['id_5'],
                'fecha':form.cleaned_data['fecha_5'],
                'd_origen':form.cleaned_data['departamento_origen_5'],
                'm_origen':form.cleaned_data['municipio_origen_5'],
                'd_destino':form.cleaned_data['departamento_destino_5'],
                'm_destino':form.cleaned_data['municipio_destino_5'],
                'valor':float(form.cleaned_data['valor_5'].replace(',','')) if form.cleaned_data['valor_5'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_5'],
            },
            {
                'id':form.cleaned_data['id_6'],
                'fecha':form.cleaned_data['fecha_6'],
                'd_origen':form.cleaned_data['departamento_origen_6'],
                'm_origen':form.cleaned_data['municipio_origen_6'],
                'd_destino':form.cleaned_data['departamento_destino_6'],
                'm_destino':form.cleaned_data['municipio_destino_6'],
                'valor':float(form.cleaned_data['valor_6'].replace(',','')) if form.cleaned_data['valor_6'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_6'],
            },
            {
                'id':form.cleaned_data['id_7'],
                'fecha':form.cleaned_data['fecha_7'],
                'd_origen':form.cleaned_data['departamento_origen_7'],
                'm_origen':form.cleaned_data['municipio_origen_7'],
                'd_destino':form.cleaned_data['departamento_destino_7'],
                'm_destino':form.cleaned_data['municipio_destino_7'],
                'valor':float(form.cleaned_data['valor_7'].replace(',','')) if form.cleaned_data['valor_7'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_7'],
            },
            {
                'id':form.cleaned_data['id_8'],
                'fecha':form.cleaned_data['fecha_8'],
                'd_origen':form.cleaned_data['departamento_origen_8'],
                'm_origen':form.cleaned_data['municipio_origen_8'],
                'd_destino':form.cleaned_data['departamento_destino_8'],
                'm_destino':form.cleaned_data['municipio_destino_8'],
                'valor':float(form.cleaned_data['valor_8'].replace(',','')) if form.cleaned_data['valor_8'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_8'],
            },
            {
                'id':form.cleaned_data['id_9'],
                'fecha':form.cleaned_data['fecha_9'],
                'd_origen':form.cleaned_data['departamento_origen_9'],
                'm_origen':form.cleaned_data['municipio_origen_9'],
                'd_destino':form.cleaned_data['departamento_destino_9'],
                'm_destino':form.cleaned_data['municipio_destino_9'],
                'valor':float(form.cleaned_data['valor_9'].replace(',','')) if form.cleaned_data['valor_9'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_9'],
            },
            {
                'id':form.cleaned_data['id_10'],
                'fecha':form.cleaned_data['fecha_10'],
                'd_origen':form.cleaned_data['departamento_origen_10'],
                'm_origen':form.cleaned_data['municipio_origen_10'],
                'd_destino':form.cleaned_data['departamento_destino_10'],
                'm_destino':form.cleaned_data['municipio_destino_10'],
                'valor':float(form.cleaned_data['valor_10'].replace(',','')) if form.cleaned_data['valor_10'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_10'],
            },
        ]

        valor = 0

        for desplazamiento in desplazamientos:
            if desplazamiento['id'] != '':
                if desplazamiento['valor'] != None:
                    if desplazamiento['fecha'] != '':
                        if desplazamiento['d_origen'] != '':
                            if desplazamiento['m_origen'] != '':
                                if desplazamiento['d_destino'] != '':
                                    if desplazamiento['m_destino'] != '':
                                        valor += desplazamiento['valor']
                                        editar = Desplazamiento.objects.get(id=desplazamiento['id'])
                                        editar.departamento_origen = Departamento.objects.get(id=desplazamiento['d_origen'])
                                        editar.municipio_origen = Municipio.objects.get(id=desplazamiento['m_origen'])
                                        editar.departamento_destino = Departamento.objects.get(id=desplazamiento['d_destino'])
                                        editar.municipio_destino = Municipio.objects.get(id=desplazamiento['m_destino'])
                                        editar.valor = desplazamiento['valor']
                                        editar.fecha = desplazamiento['fecha']
                                        editar.motivo = desplazamiento['motivo']
                                        editar.save()

        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['pk'])
        solicitud.valor_aprobado = valor
        solicitud.observacion = 'Se modificaron los valores de desplazamiento por el eje financiero'
        solicitud.save()



        return super(TransportesUpdateView,self).form_valid(form)


class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/diplomados/lista.html'
    permission_required = "permisos_sican.financiera.diplomados.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.financiera.diplomados.crear')
        return super(DiplomadosListView, self).get_context_data(**kwargs)


class DiplomadoCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Diplomado
    form_class = DiplomadoForm
    success_url = '/financiera/diplomados/'
    template_name = 'financiera/diplomados/nuevo.html'
    permission_required = "permisos_sican.financiera.diplomados.crear"


class DiplomadoUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Diplomado
    form_class = UpdateDiplomadoForm
    pk_url_kwarg = 'pk'
    success_url = '/financiera/diplomados/'
    template_name = 'financiera/diplomados/editar.html'
    permission_required = "permisos_sican.financiera.diplomados.editar"



class NivelesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/niveles/lista.html'
    permission_required = "permisos_sican.financiera.niveles.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.financiera.niveles.crear')
        return super(NivelesListView, self).get_context_data(**kwargs)


class NivelesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Nivel
    form_class = NivelForm
    success_url = '/financiera/niveles/'
    template_name = 'financiera/niveles/nuevo.html'
    permission_required = "permisos_sican.financiera.niveles.crear"


class NivelesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Nivel
    form_class = UpdateNivelForm
    pk_url_kwarg = 'pk'
    success_url = '/financiera/niveles/'
    template_name = 'financiera/niveles/editar.html'
    permission_required = "permisos_sican.financiera.niveles.editar"


class SesionesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/sesiones/lista.html'
    permission_required = "permisos_sican.financiera.sesiones.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.financiera.sesiones.crear')
        return super(SesionesListView, self).get_context_data(**kwargs)


class SesionesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Sesion
    form_class = SesionForm
    success_url = '/financiera/sesiones/'
    template_name = 'financiera/sesiones/nuevo.html'
    permission_required = "permisos_sican.financiera.sesiones.crear"


class SesionesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Sesion
    form_class = UpdateSesionForm
    pk_url_kwarg = 'pk'
    success_url = '/financiera/sesiones/'
    template_name = 'financiera/sesiones/editar.html'
    permission_required = "permisos_sican.financiera.sesiones.editar"