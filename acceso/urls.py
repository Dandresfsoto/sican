from django.conf.urls import url
from acceso.views import ListaRadicadosRetomaView, NuevoRadicadosRetomaView, UpdateRadicadosRetomaView, DeleteRadicadosRetomaView

urlpatterns = [
    url(r'^radicadosretoma/$', ListaRadicadosRetomaView.as_view()),
    url(r'^radicadosretoma/nuevo/$', NuevoRadicadosRetomaView.as_view()),
    url(r'^radicadosretoma/editar/(?P<pk>[0-9]+)/$', UpdateRadicadosRetomaView.as_view()),
    url(r'^radicadosretoma/eliminar/(?P<pk>[0-9]+)/$', DeleteRadicadosRetomaView.as_view()),
]