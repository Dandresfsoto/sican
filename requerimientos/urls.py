from django.conf.urls import url
from requerimientos.views import RequerimientosListView, NuevoRequerimientoView

urlpatterns = [
    url(r'^delegacion/$', RequerimientosListView.as_view()),
    url(r'^delegacion/nuevo/$', NuevoRequerimientoView.as_view()),
    #url(r'^administrativos/editar/(?P<pk>[0-9]+)/$', UpdateAdministrativoView.as_view()),
    #url(r'^administrativos/eliminar/(?P<pk>[0-9]+)/$', DeleteAdministrativoView.as_view()),
]