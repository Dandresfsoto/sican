#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from preinscripcion.models import DocentesPreinscritos
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from administrativos.forms import NuevoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from preinscripcion.forms import DocentesPreinscritosForm, DocentesPreinscritosUpdateForm
from docentes.models import DocentesMinEducacion
from formadores.models import Formador
from formadores.models import SolicitudTransporte
from formadores.forms import SolicitudTransporteLiderForm, SolicitudTransporteUpdateForm
from municipios.models import Municipio
from departamentos.models import Departamento
from formadores.models import SolicitudTransporte, Desplazamiento
from django.views.generic.edit import ModelFormMixin
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
import locale


class ListaPreinscritosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/preinscritos/lista.html'
    permission_required = "permisos_sican.formacion.preinscritos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.informes')
        return super(ListaPreinscritosView, self).get_context_data(**kwargs)

class NuevoPreinscritoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosForm
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/nuevo.html'
    permission_required = "permisos_sican.formacion.preinscritos.crear"


    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(NuevoPreinscritoView,self).form_valid(form)

class UpdatePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosUpdateForm
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/editar.html'
    permission_required = "permisos_sican.formacion.preinscritos.editar"

    def get_initial(self):
        return {'departamento':self.object.departamento.id,'municipio':self.object.municipio.id}

    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(UpdatePreinscritoView,self).form_valid(form)

class DeletePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = DocentesPreinscritos
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/eliminar.html'
    permission_required = "permisos_sican.formacion.preinscritos.eliminar"

class ListaRevisionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/revision/lista.html'
    permission_required = "permisos_sican.formacion.revision.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.masivo')
        return super(ListaRevisionView, self).get_context_data(**kwargs)

class ListaTransportesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"


class ListaTransportesAprobadasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/aprobadas/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesAprobadasView,self).get_context_data(**kwargs)



class ListaTransportesRechazadasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/rechazadas/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesRechazadasView,self).get_context_data(**kwargs)


class ListaTransportesPendientesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/pendientes/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesPendientesView,self).get_context_data(**kwargs)

class TransporteFormView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SolicitudTransporte
    form_class = SolicitudTransporteLiderForm
    pk_url_kwarg = 'id_solicitud'
    success_url = '../../'
    template_name = 'formacion/transportes/pendientes/estado.html'
    permission_required = "permisos_sican.formacion.transportesformacion.estado"

    def form_valid(self, form):
        self.object = form.save()
        valores = self.object.desplazamientos.all().values_list('valor',flat=True)
        valor_aprobado = 0

        for valor in valores:
            valor_aprobado += valor

        if self.object.estado == 'aprobado_lider':
            self.object.valor_aprobado_lider = valor_aprobado
            self.object.save()

        if self.object.estado == 'rechazado':
            self.object.valor_aprobado_lider = 0
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
                                          'estado': 'Solicitud rechazada'
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])

        else:
            self.object.valor_aprobado_lider = 0
            self.object.save()

        return super(ModelFormMixin,self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['formador'] = self.object.formador.get_full_name()
        return super(TransporteFormView,self).get_context_data(**kwargs)



class TransporteFormUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               FormView):
    form_class = SolicitudTransporteUpdateForm
    success_url = '../../'
    template_name = 'formacion/transportes/pendientes/editar.html'
    permission_required = "permisos_sican.formacion.transportesformacion.editar"

    def get_initial(self):
        return {'pk':self.kwargs['id_solicitud']}

    def get_context_data(self, **kwargs):
        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['id_solicitud'])
        kwargs['formador'] = Formador.objects.get(id = solicitud.formador.id).get_full_name()
        kwargs['nombre_solicitud'] = solicitud.nombre
        return super(TransporteFormUpdateView,self).get_context_data(**kwargs)

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
                                        if desplazamiento['motivo'] != '':
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

        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['id_solicitud'])
        solicitud.valor_aprobado_lider = valor
        solicitud.observacion = 'Se modificaron los valores de desplazamiento por el lider'
        solicitud.save()



        return super(TransporteFormUpdateView,self).form_valid(form)