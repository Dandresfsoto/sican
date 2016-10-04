from django.conf.urls import url
from evidencias.views import DiplomadosListView, FormadoresListView, NivelesListView, SesionesListView, EntregablesListView, SoportesListView
from evidencias.views import NuevoSoporteView, UpdateSoporteView, DeleteSoporteView, EvidenciasListView
from evidencias.views import RedsListView, NuevoRedView

urlpatterns = [
    url(r'^general/$', DiplomadosListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/$', FormadoresListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/$', NivelesListView.as_view()),

    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/$', SesionesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/$', EntregablesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/$', SoportesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/nuevo/$', NuevoSoporteView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', UpdateSoporteView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', DeleteSoporteView.as_view()),

    url(r'^codigos/$', EvidenciasListView.as_view()),

    url(r'^reds/$', RedsListView.as_view()),
    url(r'^reds/nuevo/$', NuevoRedView.as_view()),
]