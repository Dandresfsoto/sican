from django.conf.urls import url
from formacion.views import ListaPreinscritosView, NuevoPreinscritoView, UpdatePreinscritoView,DeletePreinscritoView
from formacion.views import ListaRevisionView
from formacion.views import ListaTransportesView, ListaTransportesAprobadasView, ListaTransportesRechazadasView, ListaTransportesPendientesView
from formacion.views import TransporteFormView, TransporteFormUpdateView

urlpatterns = [
    url(r'^preinscritos/$', ListaPreinscritosView.as_view()),
    url(r'^preinscritos/nuevo/$', NuevoPreinscritoView.as_view()),
    url(r'^preinscritos/editar/(?P<pk>[0-9]+)/$', UpdatePreinscritoView.as_view()),
    url(r'^preinscritos/eliminar/(?P<pk>[0-9]+)/$', DeletePreinscritoView.as_view()),

    url(r'^revision/$', ListaRevisionView.as_view()),

    url(r'^transportes/$', ListaTransportesView.as_view()),
    url(r'^transportes/aprobadas/(?P<id>[0-9]+)/$', ListaTransportesAprobadasView.as_view()),
    url(r'^transportes/rechazadas/(?P<id>[0-9]+)/$', ListaTransportesRechazadasView.as_view()),

    url(r'^transportes/pendientes/(?P<id>[0-9]+)/$', ListaTransportesPendientesView.as_view()),
    url(r'^transportes/pendientes/(?P<id>[0-9]+)/estado/(?P<id_solicitud>[0-9]+)/$', TransporteFormView.as_view()),
    url(r'^transportes/pendientes/(?P<id>[0-9]+)/editar/(?P<id_solicitud>[0-9]+)/$', TransporteFormUpdateView.as_view()),
]