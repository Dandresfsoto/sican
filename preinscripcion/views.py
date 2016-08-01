from django.shortcuts import render
from django.views.generic import FormView, CreateView, UpdateView, TemplateView
from preinscripcion.forms import Consulta, Registro, UpdateRegistroForm, PregistroForm
from docentes.models import DocentesDocentic, DocentesMinEducacion
from preinscripcion.models import DocentesPreinscritos
from django.shortcuts import HttpResponseRedirect
from preinscripcion.models import DocentesPreinscritos
# Create your views here.

class ConsultaView(FormView):
    template_name = 'preinscripcion/consulta.html'
    form_class = Consulta
    success_url = '/preinscripcion/'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        docentic = DocentesDocentic.objects.filter(cedula=cedula)
        mineducacion = DocentesMinEducacion.objects.filter(cedula=cedula)
        preinscritos = DocentesPreinscritos.objects.filter(cedula=cedula)

        if docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 1:
            redirect = '/preinscripcion/registro/'+str(cedula)

        elif docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/preinscripcion/preregistro/'+str(cedula)

        elif docentic.count() == 1 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/diploma/'+str(cedula)

        elif preinscritos.count() == 1:
            redirect = '/preinscripcion/modificar/'+str(cedula)

        return HttpResponseRedirect(redirect)

class RegistroView(CreateView):
    model = DocentesPreinscritos
    template_name = 'preinscripcion/registro.html'
    form_class = Registro
    success_url = '/preinscripcion/'

class PreregistroView(CreateView):
    model = DocentesPreinscritos
    template_name = 'preinscripcion/registro.html'
    form_class = PregistroForm
    success_url = '/preinscripcion/'

class UpdateRegistroView(UpdateView):
    model = DocentesPreinscritos
    template_name = 'preinscripcion/update.html'
    form_class = UpdateRegistroForm
    success_url = '/preinscripcion/'

    def get_object(self, queryset=None):
        return self.model.objects.get(cedula=self.kwargs['cedula'])

class DiplomaView(TemplateView):
    template_name = 'preinscripcion/diploma.html'

    def get_context_data(self, **kwargs):
        docente = DocentesDocentic.objects.get(cedula=kwargs['cedula'])
        kwargs['nombre_docente'] = docente.nombres + " " + docente.apellidos
        kwargs['cedula_docente'] = docente.cedula
        return super(DiplomaView, self).get_context_data(**kwargs)

class Completo(TemplateView):
    template_name = 'preinscripcion/completo.html'