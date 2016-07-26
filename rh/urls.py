from django.conf.urls import url
from rh.views import AdministrativoView, NuevoAdministrativoView, CargosView, NuevoCargoView, DeleteCargoView,UpdateCargoView
from rh.views import DeleteAdministrativoView, UpdateAdministrativoView, SoporteAdministrativoView, NuevoSoporteAdministrativoView
from rh.views import UpdateSoporteAdministrativoView, DeleteSoporteAdministrativoView
from rh.views import TipoSoporteAdministrativoView, NuevoTipoSoporteAdministrativoView, UpdateTipoSoporteAdministrativoView, DeleteTipoSoporteAdministrativoView
from rh.views import FormadoresView, NuevoFormadorView,UpdateFormadorView, DeleteFormadorView
from rh.views import SoporteFormadorView, NuevoSoporteFormadorView, UpdateSoporteFormadorView, DeleteSoporteFormadorView

urlpatterns = [
    url(r'^administrativos/$', AdministrativoView.as_view()),
    url(r'^administrativos/nuevo/$', NuevoAdministrativoView.as_view()),
    url(r'^administrativos/editar/(?P<pk>[0-9]+)/$', UpdateAdministrativoView.as_view()),
    url(r'^administrativos/eliminar/(?P<pk>[0-9]+)/$', DeleteAdministrativoView.as_view()),


    url(r'^administrativos/soportes/(?P<pk>[0-9]+)/$', SoporteAdministrativoView.as_view()),
    url(r'^administrativos/soportes/(?P<pk>[0-9]+)/nuevo/$', NuevoSoporteAdministrativoView.as_view()),
    url(r'^administrativos/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', UpdateSoporteAdministrativoView.as_view()),
    url(r'^administrativos/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', DeleteSoporteAdministrativoView.as_view()),


    url(r'^cargos/$', CargosView.as_view()),
    url(r'^cargos/nuevo/$', NuevoCargoView.as_view()),
    url(r'^cargos/editar/(?P<pk>[0-9]+)/$', UpdateCargoView.as_view()),
    url(r'^cargos/eliminar/(?P<pk>[0-9]+)/$', DeleteCargoView.as_view()),

    url(r'^tipo_soporte/$', TipoSoporteAdministrativoView.as_view()),
    url(r'^tipo_soporte/nuevo/$', NuevoTipoSoporteAdministrativoView.as_view()),
    url(r'^tipo_soporte/editar/(?P<pk>[0-9]+)/$', UpdateTipoSoporteAdministrativoView.as_view()),
    url(r'^tipo_soporte/eliminar/(?P<pk>[0-9]+)/$', DeleteTipoSoporteAdministrativoView.as_view()),

    url(r'^formadores/$', FormadoresView.as_view()),
    url(r'^formadores/nuevo/$', NuevoFormadorView.as_view()),
    url(r'^formadores/editar/(?P<pk>[0-9]+)/$', UpdateFormadorView.as_view()),
    url(r'^formadores/eliminar/(?P<pk>[0-9]+)/$', DeleteFormadorView.as_view()),

    url(r'^formadores/soportes/(?P<pk>[0-9]+)/$', SoporteFormadorView.as_view()),
    url(r'^formadores/soportes/(?P<pk>[0-9]+)/nuevo/$', NuevoSoporteFormadorView.as_view()),
    url(r'^formadores/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', UpdateSoporteFormadorView.as_view()),
    url(r'^formadores/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', DeleteSoporteFormadorView.as_view()),
]