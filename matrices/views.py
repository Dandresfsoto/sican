#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from matrices.models import Beneficiario
from matrices.forms import BeneficiarioForm, BeneficiarioUpdateForm
from radicados.models import Radicado


# Create your views here.
class ListadoMatricesView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'matrices/diplomados/lista.html'
    permissions = {
        "any": ("permisos_sican.matrices.matricesdiplomados.ver_innovatic", "permisos_sican.matrices.matricesdiplomados.ver_tecnotic",
                "permisos_sican.matrices.matricesdiplomados.ver_directic", "permisos_sican.matrices.matricesdiplomados.ver_escuelatic")
    }

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.matrices.matricesdiplomados.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.matrices.matricesdiplomados.informes')
        kwargs['diplomado'] = kwargs['diplomado'].upper()
        return super(ListadoMatricesView, self).get_context_data(**kwargs)


class NuevoBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    success_url = '../'
    template_name = 'matrices/diplomados/nuevo.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.crear"

    def get_initial(self):
        return {'diplomado_nombre':self.kwargs['diplomado'].upper()}

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(NuevoBeneficiarioView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.object.diplomado.nombre != 'ESCUELA TIC FAMILIA':
            self.object.radicado = Radicado.objects.get(numero=form.cleaned_data['radicado_text'])
        self.object.save()
        return super(NuevoBeneficiarioView, self).form_valid(form)


class UpdateBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Beneficiario
    form_class = BeneficiarioUpdateForm
    success_url = '../../'
    template_name = 'matrices/diplomados/editar.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.editar"

    def get_initial(self):
        return {'diplomado_nombre':self.kwargs['diplomado'].upper(),'formador_id':self.object.formador.id}

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(UpdateBeneficiarioView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.object.diplomado.nombre != 'ESCUELA TIC FAMILIA':
            self.object.radicado = Radicado.objects.get(numero=form.cleaned_data['radicado_text'])
        self.object.save()
        return super(UpdateBeneficiarioView, self).form_valid(form)


class DeleteBeneficiarioView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Beneficiario
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'matrices/diplomados/eliminar.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(DeleteBeneficiarioView, self).get_context_data(**kwargs)