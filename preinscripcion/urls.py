from django.conf.urls import url
from preinscripcion.views import ConsultaView, RegistroView

urlpatterns = [
    url(r'^$', ConsultaView.as_view()),
    url(r'^registro/', RegistroView.as_view()),
]