from django.conf.urls import url
from rh.views import AdministrativoView, NuevoAdministrativoView, CargosView, NuevoCargoView, DeleteCargoView,UpdateCargoView
from rh.views import DeleteAdministrativoView, UpdateAdministrativoView

urlpatterns = [
    url(r'^administrativos/$', AdministrativoView.as_view()),
    url(r'^administrativos/nuevo/$', NuevoAdministrativoView.as_view()),
    url(r'^administrativos/editar/(?P<pk>[0-9]+)/$', UpdateAdministrativoView.as_view()),
    url(r'^administrativos/eliminar/(?P<pk>[0-9]+)/$', DeleteAdministrativoView.as_view()),

    url(r'^cargos/$', CargosView.as_view()),
    url(r'^cargos/nuevo/$', NuevoCargoView.as_view()),
    url(r'^cargos/editar/(?P<pk>[0-9]+)/$', UpdateCargoView.as_view()),
    url(r'^cargos/eliminar/(?P<pk>[0-9]+)/$', DeleteCargoView.as_view()),
]