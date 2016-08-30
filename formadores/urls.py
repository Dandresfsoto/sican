from django.conf.urls import url
from formadores.views import InicioView, VinculosView, LegalizacionView, LegalizacionCompletaView, TransportesView
from formadores.views import NuevaSolicitudTransportesView, SubirSoporteTransportesView, OtroSiView, OtroSiCompletoView
from formadores.views import EntregablesView

urlpatterns = [
    url(r'^$', InicioView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/$', VinculosView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/otrosi/$', OtroSiView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/otrosi/completo/$', OtroSiCompletoView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/legalizacion/$', LegalizacionView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/legalizacion/completo/$', LegalizacionCompletaView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/transportes/$', TransportesView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/transportes/nueva/$', NuevaSolicitudTransportesView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/transportes/soporte/(?P<id_soporte>[0-9]+)/$', SubirSoporteTransportesView.as_view()),

    url(r'^(?P<cedula>[0-9]+)/entregables/$', EntregablesView.as_view()),
]