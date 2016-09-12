#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from productos.forms import DiplomadoForm, UpdateDiplomadoForm, NivelForm, UpdateNivelForm, SesionForm, UpdateSesionForm
from productos.forms import EntregableForm, UpdateEntregableForm
from productos.models import Entregable

# Create your views here.

class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_diplomados.html'
    permission_required = "permisos_sican.evidencias.general.ver"