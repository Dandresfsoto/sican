from django.conf.urls import url
from formadores.views import InicioView, VinculosView, LegalizacionView, LegalizacionCompletaView

urlpatterns = [
    url(r'^$', InicioView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/$', VinculosView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/legalizacion/$', LegalizacionView.as_view()),
    url(r'^(?P<cedula>[0-9]+)/legalizacion/completo/$', LegalizacionCompletaView.as_view()),
]