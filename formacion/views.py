from preinscripcion.models import DocentesPreinscritos
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from preinscripcion.forms import DocentesPreinscritosForm, DocentesPreinscritosUpdateForm
from docentes.models import DocentesMinEducacion



class ListaPreinscritosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/preinscritos/lista.html'
    permission_required = "permisos_sican.formacion.preinscritos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.informes')
        return super(ListaPreinscritosView, self).get_context_data(**kwargs)

class NuevoPreinscritoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosForm
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/nuevo.html'
    permission_required = "permisos_sican.formacion.preinscritos.crear"


    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(NuevoPreinscritoView,self).form_valid(form)

class UpdatePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosUpdateForm
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/editar.html'
    permission_required = "permisos_sican.formacion.preinscritos.editar"

    def get_initial(self):
        return {'departamento':self.object.departamento.id,'municipio':self.object.municipio.id}

    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(UpdatePreinscritoView,self).form_valid(form)

class DeletePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = DocentesPreinscritos
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/eliminar.html'
    permission_required = "permisos_sican.formacion.preinscritos.eliminar"

class ListaRevisionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/revision/lista.html'
    permission_required = "permisos_sican.formacion.revision.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.masivo')
        return super(ListaRevisionView, self).get_context_data(**kwargs)