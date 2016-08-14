from django.conf.urls import url
from encuestas.views import InicioView, EncuestaView, CompletoView

urlpatterns = [
    url(r'^percepcioninicial/$', InicioView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/$', EncuestaView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/completo/$', CompletoView.as_view()),
]