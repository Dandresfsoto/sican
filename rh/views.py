from administrativos.models import Administrativo, Soporte
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm, NuevoSoporteForm
from cargos.models import Cargo
from cargos.forms import NuevoCargoForm, EditarCargoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from administrativos.forms import UpdateSoporteAdministrativoForm
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


class SoporteAdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/soportes/soportes.html'
    permission_required = "administrativos.rh"

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_administrativo'] = kwargs['pk']
        return super(SoporteAdministrativoView, self).get_context_data(**kwargs)



class NuevoSoporteAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Soporte
    form_class = NuevoSoporteForm
    success_url = '../'
    template_name = 'rh/soportes/nuevo.html'
    permission_required = "administrativos.rh"

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(NuevoSoporteAdministrativoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'administrativo':self.kwargs['pk']}


class UpdateSoporteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Soporte
    form_class = UpdateSoporteAdministrativoForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/soportes/editarSoporte.html'
    permission_required = "administrativos.rh"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteAdministrativoView, self).get_context_data(**kwargs)


class DeleteSoporteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Soporte
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/soportes/eliminarSoporte.html'
    permission_required = "administrativos.rh"

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteAdministrativoView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)


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