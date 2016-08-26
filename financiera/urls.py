from django.conf.urls import url
from financiera.views import TransportesView, TransportesEstadoView, TransportesEliminarView
from financiera.views import TransportesCreateView, TransportesUpdateView
from financiera.views import DiplomadosListView, DiplomadoCreateView,DiplomadoUpdateView
from financiera.views import NivelesListView, NivelesCreateView, NivelesUpdateView
from financiera.views import SesionesListView, SesionesCreateView, SesionesUpdateView
from financiera.views import TransportesAprobadasFinancieraView, TransportesAprobadasLideresView, TransportesRechazadasView, TransportesPendientesView
from financiera.views import TransportesConsignadasFinancieraView
from financiera.views import EntregablesListView, EntregablesCreateView, EntregablesUpdateView
from financiera.views import SemanasListView

urlpatterns = [
    url(r'^transportes/$', TransportesView.as_view()),

    url(r'^transportes/consignadas/(?P<id_formador>\w+)/$', TransportesConsignadasFinancieraView.as_view()),
    url(r'^transportes/consignadas/(?P<id_formador>\w+)/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/consignadas/(?P<id_formador>\w+)/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),
    url(r'^transportes/consignadas/(?P<id_formador>\w+)/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),


    url(r'^transportes/aprobadasfinanciera/(?P<id_formador>\w+)/$', TransportesAprobadasFinancieraView.as_view()),
    url(r'^transportes/aprobadasfinanciera/(?P<id_formador>\w+)/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/aprobadasfinanciera/(?P<id_formador>\w+)/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),
    url(r'^transportes/aprobadasfinanciera/(?P<id_formador>\w+)/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),


    url(r'^transportes/aprobadaslideres/(?P<id_formador>\w+)/$', TransportesAprobadasLideresView.as_view()),
    url(r'^transportes/aprobadaslideres/(?P<id_formador>\w+)/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/aprobadaslideres/(?P<id_formador>\w+)/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),
    url(r'^transportes/aprobadaslideres/(?P<id_formador>\w+)/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),


    url(r'^transportes/rechazadas/(?P<id_formador>\w+)/$', TransportesRechazadasView.as_view()),
    url(r'^transportes/rechazadas/(?P<id_formador>\w+)/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/rechazadas/(?P<id_formador>\w+)/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),
    url(r'^transportes/rechazadas/(?P<id_formador>\w+)/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),


    url(r'^transportes/pendientes/(?P<id_formador>\w+)/$', TransportesPendientesView.as_view()),
    url(r'^transportes/pendientes/(?P<id_formador>\w+)/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/pendientes/(?P<id_formador>\w+)/editar/(?P<pk>\w+)/$', TransportesUpdateView.as_view()),
    url(r'^transportes/pendientes/(?P<id_formador>\w+)/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),



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

    url(r'^entregables/$', EntregablesListView.as_view()),
    url(r'^entregables/nuevo/$', EntregablesCreateView.as_view()),
    url(r'^entregables/editar/(?P<pk>\w+)/$', EntregablesUpdateView.as_view()),

    url(r'^cronograma/$', SemanasListView.as_view()),
]