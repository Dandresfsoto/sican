from django.conf.urls import url
from preinscripcion.views import ConsultaView, RegistroView, UpdateRegistroView, PreregistroView, DiplomaView, Completo, DiplomaReingresoView

urlpatterns = [
    url(r'^$', ConsultaView.as_view()),
    url(r'^registro/(?P<cedula>[0-9]+)/$', RegistroView.as_view()),
    url(r'^modificar/(?P<cedula>[0-9]+)/$', UpdateRegistroView.as_view()),
    url(r'^preregistro/(?P<cedula>[0-9]+)/$', PreregistroView.as_view()),
    url(r'^diploma/(?P<cedula>[0-9]+)/$', DiplomaView.as_view()),
    url(r'^diploma_reingreso/(?P<cedula>[0-9]+)/$', DiplomaReingresoView.as_view()),
    url(r'^completo/$', Completo.as_view()),
]