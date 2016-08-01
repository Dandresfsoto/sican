from django.shortcuts import render
from django.views.generic import FormView, CreateView
from preinscripcion.forms import Consulta, Registro
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
            redirect = '/preinscripcion/registro/&cedula='+str(cedula)

        elif docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/preinscripcion/registro/&cedula='+str(cedula)

        elif docentic.count() == 1 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/preinscripcion/registro/&cedula='+str(cedula)

        elif preinscritos.count() == 1:
            redirect = '/preinscripcion/registro/&cedula='+str(cedula)

        return HttpResponseRedirect(redirect)

class RegistroView(CreateView):
    model = DocentesPreinscritos
    template_name = 'preinscripcion/registro.html'
    form_class = Registro
    success_url = '/preinscripcion/'