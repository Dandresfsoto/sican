#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from formadores.models import Formador
from evidencias.models import Evidencia
from evidencias.forms import EvidenciaForm
from productos.models import Entregable

# Create your views here.

class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_diplomados.html'
    permission_required = "permisos_sican.evidencias.general.ver"



class FormadoresListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_formadores.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        return super(FormadoresListView,self).get_context_data(**kwargs)



class NivelesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_niveles.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        return super(NivelesListView,self).get_context_data(**kwargs)



class SesionesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_sesiones.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        return super(SesionesListView,self).get_context_data(**kwargs)


class EntregablesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_entregables.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        return super(EntregablesListView,self).get_context_data(**kwargs)



class SoportesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_soportes.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(SoportesListView,self).get_context_data(**kwargs)


class NuevoSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.crear"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(NuevoSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(NuevoSoporteView,self).form_valid(form)


class UpdateSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../../'
    pk_url_kwarg = 'id_soporte'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.editar"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(UpdateSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(UpdateSoporteView,self).form_valid(form)


class DeleteSoporteView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Evidencia
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'evidencias/general/eliminar.html'
    permission_required = "permisos_sican.evidencias.general.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(DeleteSoporteView,self).get_context_data(**kwargs)