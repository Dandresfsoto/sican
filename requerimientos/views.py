#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from requerimientos.forms import RequerimientoForm
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from requerimientos.models import Requerimiento


class RequerimientosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'requerimientos/interventoria/lista.html'
    permission_required = "permisos_sican.requerimientos.proyecto.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.requerimientos.proyecto.crear')
        return super(RequerimientosListView, self).get_context_data(**kwargs)


class NuevoRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/nuevo.html'
    permission_required = "permisos_sican.requerimientos.proyecto.crear"


class UpdateRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/editar.html'
    permission_required = "permisos_sican.requerimientos.proyecto.editar"


class DeleteRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              DeleteView):
    model = Requerimiento
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/eliminar.html'
    permission_required = "permisos_sican.requerimientos.proyecto.editar"