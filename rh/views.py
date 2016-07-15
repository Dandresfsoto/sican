from administrativos.models import Administrativo
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm
from cargos.models import Cargo
from cargos.forms import NuevoCargoForm, EditarCargoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class AdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/administrativos.html'
    permission_required = "administrativos.rh"

class NuevoAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Administrativo
    form_class = NuevoForm
    success_url = '/rh/administrativos/'
    template_name = 'rh/nuevo.html'
    permission_required = "administrativos.rh"

class DeleteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Administrativo
    pk_url_kwarg = 'pk'
    success_url = '/rh/administrativos/'
    template_name = 'rh/eliminarAdministrativo.html'
    permission_required = "administrativos.rh"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class UpdateAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Administrativo
    form_class = NuevoForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/administrativos/'
    template_name = 'rh/editarAdministrativo.html'
    permission_required = "administrativos.rh"



class CargosView(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 TemplateView):
    template_name = 'rh/cargos.html'
    permission_required = "rh"

class NuevoCargoView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     CreateView):
    model = Cargo
    form_class = NuevoCargoForm
    success_url = '/rh/cargos/'
    template_name = 'rh/nuevoCargo.html'
    permission_required = "rh"

class DeleteCargoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = Cargo
    pk_url_kwarg = 'pk'
    success_url = '/rh/cargos/'
    template_name = 'rh/eliminarCargo.html'
    permission_required = "rh"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class UpdateCargoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      UpdateView):
    model = Cargo
    form_class = EditarCargoForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/cargos/'
    template_name = 'rh/editarCargo.html'
    permission_required = "rh"

    def get_context_data(self, **kwargs):
        try:
            url = self.object.manual.url
        except:
            url = ""
        kwargs['manual_link'] = url
        kwargs['manual_filename'] = self.object.manual_filename
        return super(UpdateCargoView, self).get_context_data(**kwargs)