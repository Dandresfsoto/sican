from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from formadores.forms import ConsultaFormador, LegalizacionForm
from django.shortcuts import HttpResponseRedirect
from formadores.models import TipoSoporte
from formadores.models import Formador, Soporte
from django.shortcuts import HttpResponseRedirect
from formadores.tables import SolicitudTable
from formadores.models import SolicitudTransporte, Desplazamiento
from formadores.forms import NuevaSolicitudTransportes, SubirSoporteForm
from departamentos.models import Departamento
from municipios.models import Municipio
import datetime

# Create your views here.
class InicioView(FormView):
    form_class = ConsultaFormador
    template_name = 'formadores/inicio.html'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        return HttpResponseRedirect('/formadores/'+str(cedula))

class VinculosView(TemplateView):
    template_name = 'formadores/vinculos/vinculos.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])

        try:
            contrato = Soporte.objects.filter(formador=formador,oculto=False).get(tipo__id=10)
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.cargo.nombre
        kwargs['link_contrato'] = link

        dic = {
            '1':{
                'Formador Tipo 1':'Diplomados R1.pdf',
                'Formador Tipo 2':'Diplomados R1.pdf',
                'Formador Tipo 3':'Diplomados R1.pdf',
                'Formador Tipo 4':'Escuela Tic R1.pdf',
            },
            '2':{
                'Formador Tipo 1':'Diplomados R2.pdf',
                'Formador Tipo 2':'Diplomados R2.pdf',
                'Formador Tipo 3':'Diplomados R2.pdf',
                'Formador Tipo 4':'Escuela Tic R2.pdf',
            },
        }

        kwargs['carta'] = '/static/documentos/'+dic[str(formador.region.all()[0].numero)][formador.cargo.nombre]
        kwargs['cargo'] = formador.cargo.nombre

        return super(VinculosView,self).get_context_data(**kwargs)

class LegalizacionView(UpdateView):
    template_name = "formadores/legalizacion.html"
    success_url = "completo/"
    form_class = LegalizacionForm
    dic = {
            'rut':6,
            'cedula':2,
            'policia':4,
            'procuraduria':5,
            'contraloria':11,
            'certificacion':9,
            'seguridad_social':8
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        for key, value in self.dic.iteritems():
            try:
                Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=value)
            except:
                nuevo = Soporte(formador=self.object,fecha=datetime.datetime.now(),tipo=TipoSoporte.objects.get(id=value))
                nuevo.save()
            else:
                pass
        return self.render_to_response(self.get_context_data())



    def get_object(self, queryset=None):
        return Formador.objects.get(cedula=self.kwargs['cedula'])


    def form_valid(self, form):
        soportes = Soporte.objects.filter(formador=self.object,oculto=False)
        self.object.celular_personal = form.cleaned_data['celular_personal']
        self.object.correo_personal = form.cleaned_data['correo_personal']
        self.object.numero_cuenta = form.cleaned_data['numero_cuenta']
        self.object.profesion = form.cleaned_data['profesion']
        self.object.tipo_cuenta = form.cleaned_data['tipo_cuenta']
        self.object.banco = form.cleaned_data['banco']
        self.object.save()

        rut = soportes.get(tipo__id=self.dic['rut'])
        rut.archivo = form.cleaned_data['rut']
        rut.save()


        cedula = soportes.get(tipo__id=self.dic['cedula'])
        cedula.archivo = form.cleaned_data['fotocopia_cedula']
        cedula.save()

        policia = soportes.get(tipo__id=self.dic['policia'])
        policia.archivo = form.cleaned_data['antecedentes_judiciales']
        policia.save()

        procuraduria = soportes.get(tipo__id=self.dic['procuraduria'])
        procuraduria.archivo = form.cleaned_data['antecedentes_procuraduria']
        procuraduria.save()

        contraloria = soportes.get(tipo__id=self.dic['contraloria'])
        contraloria.archivo = form.cleaned_data['antecedentes_contraloria']
        contraloria.save()

        certificacion = soportes.get(tipo__id=self.dic['certificacion'])
        certificacion.archivo = form.cleaned_data['certificacion']
        certificacion.save()

        seguridad_social = soportes.get(tipo__id=self.dic['seguridad_social'])
        seguridad_social.archivo = form.cleaned_data['seguridad_social']
        seguridad_social.save()


        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        return {'cedula':self.object.cedula}

class LegalizacionCompletaView(TemplateView):
    template_name = 'formadores/legalizacion_completa.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        try:
            contrato = Soporte.objects.filter(formador=formador).get(nombre="Contrato")
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.cargo.nombre
        kwargs['link_contrato'] = link
        return super(LegalizacionCompletaView,self).get_context_data(**kwargs)

class TransportesView(TemplateView):
    template_name = 'formadores/transportes/tabla.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.cargo.nombre
        query = SolicitudTransporte.objects.filter(formador=formador)
        kwargs['table'] = SolicitudTable(query)
        return super(TransportesView,self).get_context_data(**kwargs)

class NuevaSolicitudTransportesView(FormView):
    template_name = "formadores/transportes/nuevo.html"
    form_class = NuevaSolicitudTransportes
    success_url = '../'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.cargo.nombre
        return super(NuevaSolicitudTransportesView,self).get_context_data(**kwargs)

    def form_valid(self, form):



        desplazamientos = [
            {
                'fecha':form.cleaned_data['fecha_1'],
                'd_origen':form.cleaned_data['departamento_origen_1'],
                'm_origen':form.cleaned_data['municipio_origen_1'],
                'd_destino':form.cleaned_data['departamento_destino_1'],
                'm_destino':form.cleaned_data['municipio_destino_1'],
                'valor':float(form.cleaned_data['valor_1'].replace(',','')) if form.cleaned_data['valor_1'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_1']
            },
            {
                'fecha':form.cleaned_data['fecha_2'],
                'd_origen':form.cleaned_data['departamento_origen_2'],
                'm_origen':form.cleaned_data['municipio_origen_2'],
                'd_destino':form.cleaned_data['departamento_destino_2'],
                'm_destino':form.cleaned_data['municipio_destino_2'],
                'valor':float(form.cleaned_data['valor_2'].replace(',','')) if form.cleaned_data['valor_2'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_2']
            },
            {
                'fecha':form.cleaned_data['fecha_3'],
                'd_origen':form.cleaned_data['departamento_origen_3'],
                'm_origen':form.cleaned_data['municipio_origen_3'],
                'd_destino':form.cleaned_data['departamento_destino_3'],
                'm_destino':form.cleaned_data['municipio_destino_3'],
                'valor':float(form.cleaned_data['valor_3'].replace(',','')) if form.cleaned_data['valor_3'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_3']
            },
            {
                'fecha':form.cleaned_data['fecha_4'],
                'd_origen':form.cleaned_data['departamento_origen_4'],
                'm_origen':form.cleaned_data['municipio_origen_4'],
                'd_destino':form.cleaned_data['departamento_destino_4'],
                'm_destino':form.cleaned_data['municipio_destino_4'],
                'valor':float(form.cleaned_data['valor_4'].replace(',','')) if form.cleaned_data['valor_4'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_4']
            },
            {
                'fecha':form.cleaned_data['fecha_5'],
                'd_origen':form.cleaned_data['departamento_origen_5'],
                'm_origen':form.cleaned_data['municipio_origen_5'],
                'd_destino':form.cleaned_data['departamento_destino_5'],
                'm_destino':form.cleaned_data['municipio_destino_5'],
                'valor':float(form.cleaned_data['valor_5'].replace(',','')) if form.cleaned_data['valor_5'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_5']
            },
            {
                'fecha':form.cleaned_data['fecha_6'],
                'd_origen':form.cleaned_data['departamento_origen_6'],
                'm_origen':form.cleaned_data['municipio_origen_6'],
                'd_destino':form.cleaned_data['departamento_destino_6'],
                'm_destino':form.cleaned_data['municipio_destino_6'],
                'valor':float(form.cleaned_data['valor_6'].replace(',','')) if form.cleaned_data['valor_6'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_6']
            },
            {
                'fecha':form.cleaned_data['fecha_7'],
                'd_origen':form.cleaned_data['departamento_origen_7'],
                'm_origen':form.cleaned_data['municipio_origen_7'],
                'd_destino':form.cleaned_data['departamento_destino_7'],
                'm_destino':form.cleaned_data['municipio_destino_7'],
                'valor':float(form.cleaned_data['valor_7'].replace(',','')) if form.cleaned_data['valor_7'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_7']
            },
            {
                'fecha':form.cleaned_data['fecha_8'],
                'd_origen':form.cleaned_data['departamento_origen_8'],
                'm_origen':form.cleaned_data['municipio_origen_8'],
                'd_destino':form.cleaned_data['departamento_destino_8'],
                'm_destino':form.cleaned_data['municipio_destino_8'],
                'valor':float(form.cleaned_data['valor_8'].replace(',','')) if form.cleaned_data['valor_8'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_8']
            },
            {
                'fecha':form.cleaned_data['fecha_9'],
                'd_origen':form.cleaned_data['departamento_origen_9'],
                'm_origen':form.cleaned_data['municipio_origen_9'],
                'd_destino':form.cleaned_data['departamento_destino_9'],
                'm_destino':form.cleaned_data['municipio_destino_9'],
                'valor':float(form.cleaned_data['valor_9'].replace(',','')) if form.cleaned_data['valor_9'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_9']
            },
            {
                'fecha':form.cleaned_data['fecha_10'],
                'd_origen':form.cleaned_data['departamento_origen_10'],
                'm_origen':form.cleaned_data['municipio_origen_10'],
                'd_destino':form.cleaned_data['departamento_destino_10'],
                'm_destino':form.cleaned_data['municipio_destino_10'],
                'valor':float(form.cleaned_data['valor_10'].replace(',','')) if form.cleaned_data['valor_10'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_10']
            },
        ]

        desplazamientos_obj = []

        valor = 0

        for desplazamiento in desplazamientos:
            if desplazamiento['valor'] != None:
                if desplazamiento['fecha'] != '':
                    if desplazamiento['d_origen'] != '':
                        if desplazamiento['m_origen'] != '':
                            if desplazamiento['d_destino'] != '':
                                if desplazamiento['m_destino'] != '':
                                    if desplazamiento['motivo'] != '':
                                        valor += desplazamiento['valor']
                                        desplazamientos_obj.append(Desplazamiento.objects.create(
                                            departamento_origen=Departamento.objects.get(id=desplazamiento['d_origen']),
                                            municipio_origen=Municipio.objects.get(id=desplazamiento['m_origen']),
                                            departamento_destino=Departamento.objects.get(id=desplazamiento['d_destino']),
                                            municipio_destino=Municipio.objects.get(id=desplazamiento['m_destino']),
                                            valor=desplazamiento['valor'],
                                            fecha = desplazamiento['fecha'],
                                            motivo = desplazamiento['motivo']
                                        ))

        solicitud = SolicitudTransporte.objects.create(
            formador = Formador.objects.get(cedula=self.kwargs['cedula']),
            nombre = form.cleaned_data['nombre'],
            valor = valor
        )

        for desplazamiento_obj in desplazamientos_obj:
            solicitud.desplazamientos.add(desplazamiento_obj)

        solicitud.save()



        return super(NuevaSolicitudTransportesView,self).form_valid(form)

class SubirSoporteTransportesView(UpdateView):
    template_name = "formadores/transportes/subir_soporte.html"
    model = SolicitudTransporte
    success_url = "../../"
    pk_url_kwarg = 'id_soporte'
    form_class = SubirSoporteForm