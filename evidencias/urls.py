from django.conf.urls import url
from evidencias.views import DiplomadosListView, FormadoresListView, NivelesListView, SesionesListView, EntregablesListView

urlpatterns = [
    url(r'^general/$', DiplomadosListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/$', FormadoresListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/$', NivelesListView.as_view()),

    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/$', SesionesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/$', EntregablesListView.as_view()),
]