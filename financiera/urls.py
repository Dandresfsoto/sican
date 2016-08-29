from django.conf.urls import url
from financiera.views import TransportesView, TransportesEstadoView, TransportesEliminarView
from financiera.views import TransportesCreateView, TransportesUpdateView
from financiera.views import TransportesAprobadasFinancieraView, TransportesAprobadasLideresView, TransportesRechazadasView, TransportesPendientesView
from financiera.views import TransportesConsignadasFinancieraView
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


    url(r'^cronograma/$', SemanasListView.as_view()),
]