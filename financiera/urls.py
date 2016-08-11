from django.conf.urls import url
from financiera.views import TransportesView, TransportesEstadoView, TransportesEliminarView

urlpatterns = [
    url(r'^transportes/$', TransportesView.as_view()),
    url(r'^transportes/estado/(?P<pk>\w+)/$', TransportesEstadoView.as_view()),
    url(r'^transportes/eliminar/(?P<pk>\w+)/$', TransportesEliminarView.as_view()),
]