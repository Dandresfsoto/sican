#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from formadores.models import Formador
from productos.forms import DiplomadoForm, UpdateDiplomadoForm, NivelForm, UpdateNivelForm, SesionForm, UpdateSesionForm
from productos.forms import EntregableForm, UpdateEntregableForm
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