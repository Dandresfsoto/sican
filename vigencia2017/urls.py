from django.conf.urls import url
from vigencia2017 import views

urlpatterns = [
    url(r'^codigosdane/$', views.ListadoCodigosDaneView.as_view()),
    url(r'^codigosdane/nuevo/$', views.NuevoCodigoDaneView.as_view()),
    url(r'^codigosdane/editar/(?P<pk>[0-9]+)/$', views.UpdateCodigoDaneView.as_view()),

    url(r'^grupos/$', views.ListadoGruposFormacionView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/$', views.ListadoGruposFormadorView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/nuevo/$', views.NuevoGrupoFormadorView.as_view()),

    url(r'^valor_contratos/$', views.ListadoValorContratosView.as_view()),
    url(r'^valor_contratos/nuevo/$', views.NuevoValorContratoView.as_view()),

    url(r'^valor_contratos/(?P<id_contrato>[0-9]+)/diplomado/(?P<id_diplomado>[0-9]+)/$', views.ValorProductosView.as_view()),
]