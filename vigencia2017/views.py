from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from vigencia2017.models import DaneSEDE
from vigencia2017.forms import DaneSEDEForm, GruposForm
from formadores.models import Contrato, Grupos

# Create your views here.
class ListadoCodigosDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/dane/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.informes')
        return super(ListadoCodigosDaneView, self).get_context_data(**kwargs)


class NuevoCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../'
    template_name = 'vigencia2017/dane/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.crear"


class UpdateCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../../'
    template_name = 'vigencia2017/dane/editar.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.editar"


    def get_context_data(self, **kwargs):
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        return super(UpdateCodigoDaneView, self).get_context_data(**kwargs)









class ListadoGruposFormacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"




class ListadoGruposFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_formador.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        kwargs['id_contrato'] = self.kwargs['pk']
        return super(ListadoGruposFormadorView, self).get_context_data(**kwargs)


class NuevoGrupoFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = Grupos
    form_class = GruposForm
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.crear"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        return super(NuevoGrupoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk']}