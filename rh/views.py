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
from formadores.models import Formador
from formadores.forms import FormadorForm, NuevoSoporteFormadorForm
from formadores.models import Soporte as SoporteFormador
from lideres.models import Soporte as SoporteLider
from lideres.models import Lideres
from lideres.forms import LideresForm, NuevoSoporteLiderForm
from negociadores.models import Negociador
from negociadores.forms import NegociadorForm
from rh.models import RequerimientoPersonal
from rh.forms import RequerimientoPersonalRh
import datetime
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL,RECURSO_HUMANO_EMAIL

class AdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/administrativos/lista.html'
    permission_required = "permisos_sican.rh.administrativos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.administrativos.crear')
        return super(AdministrativoView, self).get_context_data(**kwargs)

class NuevoAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Administrativo
    form_class = NuevoForm
    success_url = '/rh/administrativos/'
    template_name = 'rh/administrativos/nuevo.html'
    permission_required = "permisos_sican.rh.administrativos.crear"

class DeleteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Administrativo
    pk_url_kwarg = 'pk'
    success_url = '/rh/administrativos/'
    template_name = 'rh/administrativos/eliminar.html'
    permission_required = "permisos_sican.rh.administrativos.eliminar"

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
    permission_required = "permisos_sican.rh.administrativos.editar"


class SoporteAdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/administrativos/soportes/lista.html'
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
    template_name = 'rh/administrativos/soportes/nuevo.html'
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
    template_name = 'rh/administrativos/soportes/editar.html'
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
    template_name = 'rh/administrativos/soportes/eliminar.html'
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

class FormadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/formadores/lista.html'
    permission_required = "permisos_sican.rh.formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.masivo')
        return super(FormadoresView, self).get_context_data(**kwargs)

class NuevoFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Formador
    form_class = FormadorForm
    success_url = '/rh/formadores/'
    template_name = 'rh/formadores/nuevo.html'
    permission_required = "permisos_sican.rh.formadores.crear"

class UpdateFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Formador
    form_class = FormadorForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/formadores/'
    template_name = 'rh/formadores/editar.html'
    permission_required = "permisos_sican.rh.formadores.editar"

class DeleteFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Formador
    pk_url_kwarg = 'pk'
    success_url = '/rh/formadores/'
    template_name = 'rh/formadores/eliminar.html'
    permission_required = "permisos_sican.rh.formadores.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class SoporteFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/formadores/soportes/lista.html'
    permission_required = "permisos_sican.rh.formadores_soportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_formador'] = kwargs['pk']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores_soportes.crear')
        return super(SoporteFormadorView, self).get_context_data(**kwargs)

class NuevoSoporteFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SoporteFormador
    form_class = NuevoSoporteFormadorForm
    success_url = '../'
    template_name = 'rh/formadores/soportes/nuevo.html'
    permission_required = "permisos_sican.rh.formadores_soportes.crear"

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(NuevoSoporteFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'formador':self.kwargs['pk']}

class UpdateSoporteFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SoporteFormador
    form_class = NuevoSoporteFormadorForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/formadores/soportes/editar.html'
    permission_required = "permisos_sican.rh.formadores_soportes.editar"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'formador':self.kwargs['pk']}

class DeleteSoporteFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SoporteFormador
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/formadores/soportes/eliminar.html'
    permission_required = "permisos_sican.rh.formadores_soportes.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteFormadorView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class LideresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/lideres/lista.html'
    permission_required = "permisos_sican.rh.lideres.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.lideres.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.lideres.masivo')
        return super(LideresView, self).get_context_data(**kwargs)

class NuevoLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Lideres
    form_class = LideresForm
    success_url = '/rh/lideres/'
    template_name = 'rh/lideres/nuevo.html'
    permission_required = "permisos_sican.rh.lideres.crear"

class UpdateLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Lideres
    form_class = LideresForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/lideres/'
    template_name = 'rh/lideres/editar.html'
    permission_required = "permisos_sican.rh.lideres.editar"

class DeleteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Lideres
    pk_url_kwarg = 'pk'
    success_url = '/rh/lideres/'
    template_name = 'rh/lideres/eliminar.html'
    permission_required = "permisos_sican.rh.lideres.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class SoporteLiderView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/lideres/soportes/lista.html'
    permission_required = "permisos_sican.rh.lideres_soportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_lider'] = kwargs['pk']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.lideres_soportes.crear')
        return super(SoporteLiderView, self).get_context_data(**kwargs)

class NuevoSoporteLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SoporteFormador
    form_class = NuevoSoporteLiderForm
    success_url = '../'
    template_name = 'rh/lideres/soportes/nuevo.html'
    permission_required = "permisos_sican.rh.lideres_soportes.crear"

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name()
        return super(NuevoSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}

class UpdateSoporteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SoporteLider
    form_class = NuevoSoporteLiderForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/formadores/soportes/editar.html'
    permission_required = "permisos_sican.rh.lideres_soportes.editar"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}

class DeleteSoporteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SoporteLider
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/lideres/soportes/eliminar.html'
    permission_required = "permisos_sican.rh.lideres_soportes.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteLiderView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class NegociadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/negociadores/lista.html'
    permission_required = "permisos_sican.rh.negociadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.negociadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.negociadores.masivo')
        return super(NegociadoresView, self).get_context_data(**kwargs)

class NuevoNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Negociador
    form_class = NegociadorForm
    success_url = '/rh/negociadores/'
    template_name = 'rh/negociadores/nuevo.html'
    permission_required = "permisos_sican.rh.negociadores.crear"

class UpdateNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Negociador
    form_class = NegociadorForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/negociadores/'
    template_name = 'rh/negociadores/editar.html'
    permission_required = "permisos_sican.rh.negociadores.editar"

class DeleteNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Negociador
    pk_url_kwarg = 'pk'
    success_url = '/rh/negociadores/'
    template_name = 'rh/negociadores/eliminar.html'
    permission_required = "permisos_sican.rh.negociadores.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ListaRequerimientosContratacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/requerimientosrh/lista.html'
    permission_required = "permisos_sican.rh.requerimientosrhrespuesta.ver"

class NuevoRequerimientoContratacionView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = RequerimientoPersonal
    form_class = RequerimientoPersonalRh
    pk_url_kwarg = 'pk'
    success_url = '/rh/requerimientoscontratacion/'
    template_name = 'rh/requerimientosrh/editar.html'
    permission_required = "permisos_sican.rh.requerimientosrhrespuesta.editar"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        return super(NuevoRequerimientoContratacionView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.remitido_respuesta = True
        self.object.fecha_respuesta = datetime.datetime.now()
        self.object.save()
        destinatarios = [self.object.solicitante,self.object.encargado]
        url_base = self.request.META['HTTP_ORIGIN']
        for destinatario in list(set(destinatarios)):
            send_mail_templated.delay('email/requerimiento_contratacion_rh.tpl', {'id_requerimiento':self.object.id,
                                                                              'first_name': destinatario.first_name,
                                                                              'last_name': destinatario.last_name,
                                                                              'url_base': url_base,
                                                                }, DEFAULT_FROM_EMAIL, [destinatario.email])

        return super(NuevoRequerimientoContratacionView, self).form_valid(form)