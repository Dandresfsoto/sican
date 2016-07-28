from django.conf.urls import url
from bases.views import DepartamentoListView, NuevoDepartamentoView, UpdateDepartamentoView, DeleteDepartamentoView
from bases.views import MunicipioListView, NuevoMunicipioView,UpdateMunicipioView, DeleteMunicipioView

urlpatterns = [
    url(r'^departamentos/$', DepartamentoListView.as_view()),
    url(r'^departamentos/nuevo/$', NuevoDepartamentoView.as_view()),
    url(r'^departamentos/editar/(?P<pk>[0-9]+)/$', UpdateDepartamentoView.as_view()),
    url(r'^departamentos/eliminar/(?P<pk>[0-9]+)/$', DeleteDepartamentoView.as_view()),

    url(r'^municipios/$', MunicipioListView.as_view()),
    url(r'^municipios/nuevo/$', NuevoMunicipioView.as_view()),
    url(r'^municipios/editar/(?P<pk>[0-9]+)/$', UpdateMunicipioView.as_view()),
    url(r'^municipios/eliminar/(?P<pk>[0-9]+)/$', DeleteMunicipioView.as_view()),
]