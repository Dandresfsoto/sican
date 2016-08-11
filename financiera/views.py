from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from formadores.models import SolicitudTransporte
from formadores.forms import SolicitudTransporteForm
from financiera.tasks import construir_pdf
import locale
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")


# Create your views here.
class TransportesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'financiera/transportes/lista.html'
    permission_required = "permisos_sican.financiera.transportes.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.financiera.transportes.crear')
        return super(TransportesView, self).get_context_data(**kwargs)

class TransportesEstadoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SolicitudTransporte
    form_class = SolicitudTransporteForm
    pk_url_kwarg = 'pk'
    success_url = '/financiera/transportes/'
    template_name = 'financiera/transportes/estado.html'
    permission_required = "permisos_sican.financiera.transportes.editar"

    def form_valid(self, form):
        self.object.terminada = False
        self.object.valor_aprobado = 0

        valores = self.object.desplazamientos.all().values_list('valor',flat=True)
        valor_aprobado = 0

        for valor in valores:
            valor_aprobado += valor

        if form.cleaned_data['estado'] == 'aprobado':
            construir_pdf.delay(self.object.id)
            send_mail_templated.delay('email/desplazamiento.tpl',
                                      {
                                          'url_base':'http://sican.asoandes.org/',
                                          'fullname':self.object.formador.get_full_name(),
                                          'nombre_solicitud': self.object.nombre,
                                          'fecha_solicitud': self.object.creacion.strftime('%d/%m/%Y'),
                                          'valor_solicitado': locale.currency(self.object.valor,grouping=True),
                                          'valor_aprobado': locale.currency(valor_aprobado,grouping=True),
                                          'observacion': form.cleaned_data['observacion']
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])

            self.object.valor_aprobado = valor_aprobado
        if form.cleaned_data['estado'] == 'consignado':
            self.object.terminada = True
            self.object.valor_aprobado = valor_aprobado


        if form.cleaned_data['estado'] == 'rechazado':
            self.object.valor_aprobado = 0
        if form.cleaned_data['estado'] == 'revision':
            self.object.valor_aprobado = 0

        self.object.save()
        form.save()
        return super(TransportesEstadoView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['valor_solicitado'] = locale.currency(self.object.valor,grouping=True)
        kwargs['archivo_url'] = self.object.get_archivo_url()
        kwargs['archivo_filename'] = self.object.archivo_filename()
        return super(TransportesEstadoView,self).get_context_data(**kwargs)


class TransportesEliminarView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = SolicitudTransporte
    pk_url_kwarg = 'pk'
    success_url = '/financiera/transportes/'
    template_name = 'financiera/transportes/eliminar.html'
    permission_required = "permisos_sican.financiera.transportes.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['valor_solicitado'] = locale.currency(self.object.valor,grouping=True)
        if self.object.valor_aprobado != None:
            kwargs['valor_aprobado'] = locale.currency(self.object.valor_aprobado,grouping=True)
        kwargs['archivo_url'] = self.object.get_archivo_url()
        kwargs['archivo_filename'] = self.object.archivo_filename()
        return super(TransportesEliminarView,self).get_context_data(**kwargs)