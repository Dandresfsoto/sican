from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
class InicioView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'informes/excel/lista.html'
    permission_required = "permisos_sican.informes.excel.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.informes.excel.crear')
        return super(InicioView, self).get_context_data(**kwargs)