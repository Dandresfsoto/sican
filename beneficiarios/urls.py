from django.conf.urls import url
from beneficiarios import views

urlpatterns = [
    url(r'^$', views.ListaBeneficiariosView.as_view()),
    url(r'^nuevo_grupo/$', views.NuevoGrupoView.as_view()),
    url(r'^grupo/(?P<id_grupo>\w+)/editar/$', views.UpdateGrupoView.as_view()),
    url(r'^grupo/(?P<id_grupo>\w+)/lista/$', views.ListaBeneficiariosGrupoView.as_view()),
]