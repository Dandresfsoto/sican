from django.conf.urls import url
from formacion.views import ListaPreinscritosView, NuevoPreinscritoView, UpdatePreinscritoView,DeletePreinscritoView
urlpatterns = [
    url(r'^preinscritos/$', ListaPreinscritosView.as_view()),
    url(r'^preinscritos/nuevo/$', NuevoPreinscritoView.as_view()),
    url(r'^preinscritos/editar/(?P<pk>[0-9]+)/$', UpdatePreinscritoView.as_view()),
    url(r'^preinscritos/eliminar/(?P<pk>[0-9]+)/$', DeletePreinscritoView.as_view()),
]