from administrativos.models import Administrativo, Soporte
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm, NuevoSoporteForm
from cargos.models import Cargo
from cargos.forms import NuevoCargoForm, EditarCargoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from administrativos.forms import UpdateSoporteAdministrativoForm
from rh.models import TipoSoporte
from rh.forms import NuevoTipoSoporteForm


class AdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/administrativos/lista.html'
    permission_required = "permisos_sican.rh.cargos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.cargos.crear')
        return super(AdministrativoView, self).get_context_data(**kwargs)

class NuevoAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Administrativo
    form_class = NuevoForm
    success_url = '/rh/administrativos/'
    template_name = 'rh/administrativos/nuevo.html'
    permission_required = "permisos_sican.rh.cargos.crear"

class DeleteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Administrativo
    pk_url_kwarg = 'pk'
    success_url = '/rh/administrativos/'
    template_name = 'rh/administrativos/eliminar.html'
    permission_required = "permisos_sican.rh.cargos.eliminar"

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
    template_name = 'rh/administrativos/editar.html'
    permission_required = "permisos_sican.rh.cargos.editar"



class SoporteAdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/soportes/lista.html'
    permission_required = "permisos_sican.rh.administrativos_soportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_administrativo'] = kwargs['pk']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.administrativos_soportes.crear')
        return super(SoporteAdministrativoView, self).get_context_data(**kwargs)



class NuevoSoporteAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Soporte
    form_class = NuevoSoporteForm
    success_url = '../'
    template_name = 'rh/soportes/nuevo.html'
    permission_required = "permisos_sican.rh.administrativos_soportes.crear"

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
    template_name = 'rh/soportes/editar.html'
    permission_required = "permisos_sican.rh.administrativos_soportes.editar"

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
    template_name = 'rh/soportes/eliminar.html'
    permission_required = "permisos_sican.rh.administrativos_soportes.eliminar"

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
    template_name = 'rh/cargos/lista.html'
    permission_required = "permisos_sican.rh.cargos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.cargos.crear')
        return super(CargosView, self).get_context_data(**kwargs)

class NuevoCargoView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     CreateView):
    model = Cargo
    form_class = NuevoCargoForm
    success_url = '/rh/cargos/'
    template_name = 'rh/cargos/nuevo.html'
    permission_required = "permisos_sican.rh.cargos.crear"

class DeleteCargoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = Cargo
    pk_url_kwarg = 'pk'
    success_url = '/rh/cargos/'
    template_name = 'rh/cargos/eliminar.html'
    permission_required = "permisos_sican.rh.cargos.eliminar"

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
    template_name = 'rh/cargos/editar.html'
    permission_required = "permisos_sican.rh.cargos.editar"

    def get_context_data(self, **kwargs):
        try:
            url = self.object.manual.url
        except:
            url = ""
        kwargs['manual_link'] = url
        kwargs['manual_filename'] = self.object.manual_filename
        return super(UpdateCargoView, self).get_context_data(**kwargs)




class TipoSoporteAdministrativoView(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 TemplateView):
    template_name = 'rh/tipo_soporte/lista.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.crear')
        return super(TipoSoporteAdministrativoView, self).get_context_data(**kwargs)


class NuevoTipoSoporteAdministrativoView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     CreateView):
    model = TipoSoporte
    form_class = NuevoTipoSoporteForm
    success_url = '/rh/tipo_soporte/'
    template_name = 'rh/tipo_soporte/nuevo.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.crear"

class DeleteTipoSoporteAdministrativoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = TipoSoporte
    pk_url_kwarg = 'pk'
    success_url = '/rh/tipo_soporte/'
    template_name = 'rh/tipo_soporte/eliminar.html'
    permission_required = "permisos_sican.rh.cargos.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class UpdateTipoSoporteAdministrativoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      UpdateView):
    model = TipoSoporte
    form_class = NuevoTipoSoporteForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/tipo_soporte/'
    template_name = 'rh/tipo_soporte/editar.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.editar"