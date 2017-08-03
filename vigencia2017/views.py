from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from vigencia2017.models import DaneSEDE, TipoContrato, ValorEntregableVigencia2017
from vigencia2017.forms import DaneSEDEForm, GruposForm, TipoContratoForm, ValorEntregableVigencia2017Form
from formadores.models import Contrato, Grupos
from productos.models import Entregable
from productos.models import Diplomado

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
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.crear"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        return super(NuevoGrupoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk']}










class ListadoValorContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/valor_contratos/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear')
        return super(ListadoValorContratosView, self).get_context_data(**kwargs)



class NuevoValorContratoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = TipoContrato
    form_class = TipoContratoForm
    success_url = '../'
    template_name = 'vigencia2017/valor_contratos/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"



class ValorProductosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):

    form_class = ValorEntregableVigencia2017Form
    success_url = '../../../'
    template_name = 'vigencia2017/valor_contratos/valor_diplomado.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"

    def get_context_data(self, **kwargs):
        kwargs['contrato'] = TipoContrato.objects.get(id = self.kwargs['id_contrato']).nombre
        kwargs['diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        return super(ValorProductosView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['id_contrato'],'id_diplomado':self.kwargs['id_diplomado']}

    def form_valid(self, form):

        entregables = Entregable.objects.filter(sesion__nivel__diplomado__id=self.kwargs['id_diplomado']).order_by('numero')
        tipo_contrato = TipoContrato.objects.get(id = self.kwargs['id_contrato'])

        for entregable in entregables:
            valor, created = ValorEntregableVigencia2017.objects.get_or_create(entregable = entregable,tipo_contrato = tipo_contrato)
            valor.valor = form.cleaned_data[str(entregable.id)]
            valor.save()

        return super(ValorProductosView, self).form_valid(form)