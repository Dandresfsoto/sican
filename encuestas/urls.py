from django.conf.urls import url
from encuestas.views import InicioView, EncuestaView, CompletoView
from encuestas.views import ResultadosPercepcionInicialView
from encuestas.views import RespuestasPercepcionInicialView

urlpatterns = [
    url(r'^percepcioninicial/$', InicioView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/$', EncuestaView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/completo/$', CompletoView.as_view()),

    url(r'^resultados/percepcioninicial/$', ResultadosPercepcionInicialView.as_view()),
    url(r'^respuestas/percepcioninicial/$', RespuestasPercepcionInicialView.as_view()),
]