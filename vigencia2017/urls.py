from django.conf.urls import url
from vigencia2017 import views

urlpatterns = [
    url(r'^codigosdane/$', views.ListadoCodigosDaneView.as_view()),
    url(r'^codigosdane/nuevo/$', views.NuevoCodigoDaneView.as_view()),
    url(r'^codigosdane/editar/(?P<pk>[0-9]+)/$', views.UpdateCodigoDaneView.as_view()),

    url(r'^grupos/$', views.ListadoGruposFormacionView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/$', views.ListadoGruposFormadorView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/nuevo/$', views.NuevoGrupoFormadorView.as_view()),
]