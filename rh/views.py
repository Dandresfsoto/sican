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
from negociadores.models import Soporte as SoporteNegociador
from lideres.models import Lideres
from lideres.forms import LideresForm, NuevoSoporteLiderForm
from negociadores.models import Negociador
from negociadores.forms import NegociadorForm, NuevoSoporteNegociadorForm
from rh.models import RequerimientoPersonal
from rh.forms import RequerimientoPersonalRh,RequerimientoPersonalRhEspera, RequerimientoPersonalRhContratar,RequerimientoPersonalRhDeserta
import datetime
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL,RECURSO_HUMANO_EMAIL
from formadores.models import Contrato as ContratoFormador
from formadores.forms import ContratoForm as ContratoFormadorForm
from formadores.models import SolicitudSoportes as SolicitudSoportesFormador
from formadores.forms import SolicitudSoportesFormadorForm
from lideres.models import Contrato as ContratoLider
from lideres.forms import ContratoForm as ContratoLiderForm
from lideres.models import SolicitudSoportes as SolicitudSoportesLider
from lideres.forms import SolicitudSoportesLiderForm
from negociadores.models import Contrato as ContratoNegociador
from negociadores.forms import ContratoForm as ContratoNegociadorForm
from negociadores.models import SolicitudSoportes as SolicitudSoportesNegociador
from negociadores.forms import SolicitudSoportesNegociadorForm



class PersonalView(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   TemplateView):
    template_name = 'rh/personal/lista.html'
    permission_required = "permisos_sican.rh.personal.ver"

    def get_context_data(self, **kwargs):
        kwargs['permiso_administrativo'] = self.request.user.has_perm('permisos_sican.rh.administrativos.ver')
        kwargs['permiso_acceso'] = self.request.user.has_perm('permisos_sican.rh.acceso.ver')
        kwargs['permiso_formacion'] = self.request.user.has_perm('permisos_sican.rh.formacion.ver')
        kwargs['permiso_general'] = self.request.user.has_perm('permisos_sican.rh.general.ver')
        return super(PersonalView,self).get_context_data(**kwargs)


class ContratacionView(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   TemplateView):
    template_name = 'rh/contratacion/lista.html'
    permission_required = "permisos_sican.rh.personal.ver"

    def get_context_data(self, **kwargs):
        kwargs['permiso_formadores'] = self.request.user.has_perm('permisos_sican.rh.contratacion_formadores.ver')
        kwargs['permiso_lideres'] = self.request.user.has_perm('permisos_sican.rh.contratacion_lideres.ver')
        kwargs['permiso_negociadores'] = self.request.user.has_perm('permisos_sican.rh.contratacion_negociadores.ver')
        return super(ContratacionView,self).get_context_data(**kwargs)



class AccesoView(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   TemplateView):
    template_name = 'rh/personal/acceso/links.html'
    permission_required = "permisos_sican.rh.acceso.ver"

    def get_context_data(self, **kwargs):
        kwargs['permiso_lideres'] = self.request.user.has_perm('permisos_sican.rh.lideres.ver')
        kwargs['permiso_negociadores'] = self.request.user.has_perm('permisos_sican.rh.negociadores.ver')
        return super(AccesoView,self).get_context_data(**kwargs)




class AdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/administrativos/lista.html'
    permission_required = "permisos_sican.rh.administrativos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.administrativos.crear')
        return super(AdministrativoView, self).get_context_data(**kwargs)


#------------------------------------------------- FORMADORES ----------------------------------------------------------


class ContratosFormadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'rh/contratacion/contratos_formadores/lista.html'
    permission_required = "permisos_sican.rh.contratos_formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_formadores.informes')
        return super(ContratosFormadoresView, self).get_context_data(**kwargs)


class ContratoFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada al listado de contratos de cada formador.
    '''
    template_name = 'rh/contratacion/contratos_formadores/lista_contratos.html'
    permission_required = "permisos_sican.rh.contratos_formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_formadores.informes')
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        return super(ContratoFormadorView, self).get_context_data(**kwargs)


class NuevoContratoFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    '''
    Vista para la creacion de un nuevo contrato para el formador
    '''
    model = ContratoFormador
    form_class = ContratoFormadorForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_formadores/nuevo.html'
    permission_required = "permisos_sican.rh.contratos_formadores.crear"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        return super(NuevoContratoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador']}


class UpdateContratoFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    '''
    Vista para actualizar el contrato de un formador
    '''
    model = ContratoFormador
    form_class = ContratoFormadorForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_formadores/editar.html'
    permission_required = "permisos_sican.rh.contratos_formadores.editar"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_contrato'] = ContratoFormador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador']}


class SolicitudSoportesFormadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_formadores/lista.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_formadores.informes')

        return super(SolicitudSoportesFormadoresView, self).get_context_data(**kwargs)


class NuevaSolicitudSoportesFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SolicitudSoportesFormador
    form_class = SolicitudSoportesFormadorForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_formadores/nuevo.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_formadores.crear"


class UpdateSolicitudSoportesFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesFormador
    form_class = SolicitudSoportesFormadorForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_formadores/editar.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_formadores.editar"

    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesFormador.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesFormadorView, self).get_context_data(**kwargs)


#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------------------- FORMADORES ----------------------------------------------------------
class ContratosLideresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de lideres y cantidad de contratos de cada uno
    '''
    template_name = 'rh/contratacion/contratos_lideres/lista.html'
    permission_required = "permisos_sican.rh.contratos_lideres.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_lideres.informes')
        return super(ContratosLideresView, self).get_context_data(**kwargs)


class ContratoLiderView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada al listado de contratos de cada lider.
    '''
    template_name = 'rh/contratacion/contratos_lideres/lista_contratos.html'
    permission_required = "permisos_sican.rh.contratos_lideres.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_lideres.informes')
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        return super(ContratoLiderView, self).get_context_data(**kwargs)


class NuevoContratoLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    '''
    Vista para la creacion de un nuevo contrato para el lider
    '''
    model = ContratoLider
    form_class = ContratoLiderForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_lideres/nuevo.html'
    permission_required = "permisos_sican.rh.contratos_lideres.crear"


    def get_context_data(self, **kwargs):
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        return super(NuevoContratoLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_lider':self.kwargs['id_lider']}


class UpdateContratoLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    '''
    Vista para actualizar el contrato de un lider
    '''
    model = ContratoLider
    form_class = ContratoLiderForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_lideres/editar.html'
    permission_required = "permisos_sican.rh.contratos_lideres.editar"


    def get_context_data(self, **kwargs):
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        kwargs['nombre_contrato'] = ContratoFormador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_lider':self.kwargs['id_lider']}


class SolicitudSoportesLideresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_lideres/lista.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_lideres.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_lideres.informes')

        return super(SolicitudSoportesLideresView, self).get_context_data(**kwargs)


class NuevaSolicitudSoportesLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SolicitudSoportesLider
    form_class = SolicitudSoportesLiderForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_lideres/nuevo.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_lideres.crear"


class UpdateSolicitudSoportesLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesLider
    form_class = SolicitudSoportesLiderForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_lideres/editar.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_lideres.editar"

    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesLider.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesLiderView, self).get_context_data(**kwargs)

#-----------------------------------------------------------------------------------------------------------------------






class ContratosNegociadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/contratos_negociadores/lista.html'
    permission_required = "permisos_sican.rh.contratos_negociadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_negociadores.informes')
        return super(ContratosNegociadoresView, self).get_context_data(**kwargs)












class ContratoNegociadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/contratos_negociadores/lista_contratos.html'
    permission_required = "permisos_sican.rh.contratos_negociadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.contratos_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.contratos_negociadores.informes')
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        return super(ContratoNegociadorView, self).get_context_data(**kwargs)




















class SolicitudSoportesNegociadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/lista.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_negociadoress.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.solicitud_soportes_negociadores.informes')

        return super(SolicitudSoportesNegociadoresView, self).get_context_data(**kwargs)



























class NuevoContratoNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = ContratoNegociador
    form_class = ContratoNegociadorForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_negociadores/nuevo.html'
    permission_required = "permisos_sican.rh.contratos_negociadores.crear"


    def get_context_data(self, **kwargs):
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        return super(NuevoContratoNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_negociador':self.kwargs['id_negociador']}















class NuevaSolicitudSoportesNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SolicitudSoportesNegociador
    form_class = SolicitudSoportesNegociadorForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/nuevo.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_negociadores.crear"




















class UpdateSolicitudSoportesNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesNegociador
    form_class = SolicitudSoportesNegociadorForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/editar.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_negociadores.editar"

    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesNegociador.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesNegociadorView, self).get_context_data(**kwargs)




















class UpdateContratoNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = ContratoNegociador
    form_class = ContratoNegociadorForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_negociadores/editar.html'
    permission_required = "permisos_sican.rh.contratos_negociadores.editar"


    def get_context_data(self, **kwargs):
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        kwargs['nombre_contrato'] = ContratoNegociador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_negociador':self.kwargs['id_negociador']}





class NuevoAdministrativoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Administrativo
    form_class = NuevoForm
    success_url = '/rh/administrativos/'
    template_name = 'rh/personal/administrativos/nuevo.html'
    permission_required = "permisos_sican.rh.administrativos.crear"

class DeleteAdministrativoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Administrativo
    pk_url_kwarg = 'pk'
    success_url = '/rh/administrativos/'
    template_name = 'rh/personal/administrativos/eliminar.html'
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
    template_name = 'rh/personal/administrativos/editar.html'
    permission_required = "permisos_sican.rh.administrativos.editar"


class SoporteAdministrativoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/administrativos/soportes/lista.html'
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
    template_name = 'rh/personal/administrativos/soportes/nuevo.html'
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
    template_name = 'rh/personal/administrativos/soportes/editar.html'
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
    template_name = 'rh/personal/administrativos/soportes/eliminar.html'
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
    template_name = 'rh/personal/cargos/lista.html'
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
    template_name = 'rh/personal/cargos/nuevo.html'
    permission_required = "permisos_sican.rh.cargos.crear"

class DeleteCargoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = Cargo
    pk_url_kwarg = 'pk'
    success_url = '/rh/cargos/'
    template_name = 'rh/personal/cargos/eliminar.html'
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
    template_name = 'rh/personal/cargos/editar.html'
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
    template_name = 'rh/personal/tipo_soporte/lista.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.crear')
        return super(TipoSoporteAdministrativoView, self).get_context_data(**kwargs)

class NuevoTipoSoporteAdministrativoView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     CreateView):
    model = TipoSoporte
    form_class = NuevoTipoSoporteForm
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/nuevo.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.crear"

class DeleteTipoSoporteAdministrativoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = TipoSoporte
    pk_url_kwarg = 'pk'
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/eliminar.html'
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
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/editar.html'
    permission_required = "permisos_sican.rh.rh_tipo_soporte.editar"

class FormadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/formadores/lista.html'
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
    template_name = 'rh/personal/formadores/nuevo.html'
    permission_required = "permisos_sican.rh.formadores.crear"

class UpdateFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Formador
    form_class = FormadorForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/formadores/'
    template_name = 'rh/personal/formadores/editar.html'
    permission_required = "permisos_sican.rh.formadores.editar"

class DeleteFormadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Formador
    pk_url_kwarg = 'pk'
    success_url = '/rh/formadores/'
    template_name = 'rh/personal/formadores/eliminar.html'
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
    template_name = 'rh/personal/formadores/soportes/lista.html'
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
    template_name = 'rh/personal/formadores/soportes/nuevo.html'
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
    template_name = 'rh/personal/formadores/soportes/editar.html'
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
    template_name = 'rh/personal/formadores/soportes/eliminar.html'
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
    template_name = 'rh/personal/acceso/lideres/lista.html'
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
    template_name = 'rh/personal/acceso/lideres/nuevo.html'
    permission_required = "permisos_sican.rh.lideres.crear"

class UpdateLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Lideres
    form_class = LideresForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/lideres/'
    template_name = 'rh/personal/acceso/lideres/editar.html'
    permission_required = "permisos_sican.rh.lideres.editar"

class DeleteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Lideres
    pk_url_kwarg = 'pk'
    success_url = '/rh/lideres/'
    template_name = 'rh/personal/acceso/lideres/eliminar.html'
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
    template_name = 'rh/personal/acceso/lideres/soportes/lista.html'
    permission_required = "permisos_sican.rh.lideres_soportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_lider'] = kwargs['pk']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.lideres_soportes.crear')
        return super(SoporteLiderView, self).get_context_data(**kwargs)


class SoporteNegociadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/negociadores/soportes/lista.html'
    permission_required = "permisos_sican.rh.negociador_soportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_negociador'] = kwargs['pk']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.negociadores_soportes.crear')
        return super(SoporteNegociadorView, self).get_context_data(**kwargs)



class NuevoSoporteLiderView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SoporteFormador
    form_class = NuevoSoporteLiderForm
    success_url = '../'
    template_name = 'rh/personal/acceso/lideres/soportes/nuevo.html'
    permission_required = "permisos_sican.rh.lideres_soportes.crear"

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name()
        return super(NuevoSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}



class NuevoSoporteNegociadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = SoporteNegociador
    form_class = NuevoSoporteNegociadorForm
    success_url = '../'
    template_name = 'rh/personal/acceso/negociadores/soportes/nuevo.html'
    permission_required = "permisos_sican.rh.negociadores_soportes.crear"

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name()
        return super(NuevoSoporteNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'negociador':self.kwargs['pk']}




class UpdateSoporteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SoporteLider
    form_class = NuevoSoporteLiderForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/soportes/editar.html'
    permission_required = "permisos_sican.rh.lideres_soportes.editar"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}


class UpdateSoporteNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SoporteNegociador
    form_class = NuevoSoporteNegociadorForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/negociadores/soportes/editar.html'
    permission_required = "permisos_sican.rh.negociadores_soportes.editar"

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'negociador':self.kwargs['pk']}


class DeleteSoporteLiderView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SoporteLider
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/soportes/eliminar.html'
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

class DeleteSoporteNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SoporteNegociador
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/negociadores/soportes/eliminar.html'
    permission_required = "permisos_sican.rh.negociadores_soportes.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteNegociadorView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class NegociadoresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/negociadores/lista.html'
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
    template_name = 'rh/personal/acceso/negociadores/nuevo.html'
    permission_required = "permisos_sican.rh.negociadores.crear"

class UpdateNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Negociador
    form_class = NegociadorForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/negociadores/'
    template_name = 'rh/personal/acceso/negociadores/editar.html'
    permission_required = "permisos_sican.rh.negociadores.editar"

class DeleteNegociadorView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Negociador
    pk_url_kwarg = 'pk'
    success_url = '/rh/negociadores/'
    template_name = 'rh/personal/acceso/negociadores/eliminar.html'
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

    def get_context_data(self, **kwargs):
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.requerimientosrhrespuesta.reportes')
        return super(ListaRequerimientosContratacionView, self).get_context_data(**kwargs)

class NuevoRequerimientoContratacionView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = RequerimientoPersonal
    form_class = RequerimientoPersonalRh
    form_class_2 = RequerimientoPersonalRhEspera
    form_class_3 = RequerimientoPersonalRhContratar
    form_class_4 = RequerimientoPersonalRhDeserta
    pk_url_kwarg = 'pk'
    success_url = '/rh/requerimientoscontratacion/'
    template_name = 'rh/requerimientosrh/editar.html'
    permission_required = "permisos_sican.rh.requerimientosrhrespuesta.editar"

    def get_form_class(self):
        obj = RequerimientoPersonal.objects.get(id = self.kwargs['pk'])

        if obj.remitido_respuesta == True and obj.remitido_contratacion == False and obj.contratar == False and obj.desierto == False and obj.contratado == False:
            return self.form_class_2
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == True and obj.desierto == False and obj.contratado == False:
            return self.form_class_3
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == False and obj.desierto == True and obj.contratado == False:
            return self.form_class_4
        elif obj.contratado == True:
            return self.form_class_3
        else:
            return self.form_class

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        return super(NuevoRequerimientoContratacionView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        obj = self.object

        if obj.remitido_respuesta == True and obj.remitido_contratacion == False and obj.contratar == False and obj.desierto == False and obj.contratado == False:
            pass
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == True and obj.desierto == False and obj.contratado == False:
            pass
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == False and obj.desierto == True and obj.contratado == False:
            pass
        elif obj.contratado == True:
            pass
        else:
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


class FormadoresConsolidadoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/interventoria_formadores/lista.html'
    permission_required = "permisos_sican.rh.interventoria_formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.masivo')
        return super(FormadoresConsolidadoView, self).get_context_data(**kwargs)