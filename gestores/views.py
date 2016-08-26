from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from formadores.forms import ConsultaFormador, LegalizacionForm

from django.shortcuts import HttpResponseRedirect

# Create your views here.
class InicioView(FormView):
    form_class = ConsultaFormador
    template_name = 'formadores/inicio.html'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        return HttpResponseRedirect('/formadores/'+str(cedula))