from django.conf.urls import url
from financiera.views import TransportesView, TransportesEstadoView, TransportesEliminarView
from financiera.views import TransportesCreateView, TransportesUpdateView
from financiera.views import DiplomadosListView, DiplomadoCreateView,DiplomadoUpdateView
from financiera.views import NivelesListView, NivelesCreateView, NivelesUpdateView
from financiera.views import SesionesListView, SesionesCreateView, SesionesUpdateView

urlpatterns = [
    url(r'^transportes/$', TransportesView.as_view()),
    url(r'^transportes/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/nuevo/$', TransportesCreateView.as_view()),
    url(r'^transportes/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),
    url(r'^transportes/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),

    url(r'^diplomados/$', DiplomadosListView.as_view()),
    url(r'^diplomados/nuevo/$', DiplomadoCreateView.as_view()),
    url(r'^diplomados/editar/(?P<pk>\w+)/$', DiplomadoUpdateView.as_view()),

    url(r'^niveles/$', NivelesListView.as_view()),
    url(r'^niveles/nuevo/$', NivelesCreateView.as_view()),
    url(r'^niveles/editar/(?P<pk>\w+)/$', NivelesUpdateView.as_view()),

    url(r'^sesiones/$', SesionesListView.as_view()),
    url(r'^sesiones/nuevo/$', SesionesCreateView.as_view()),
    url(r'^sesiones/editar/(?P<pk>\w+)/$', SesionesUpdateView.as_view()),
]