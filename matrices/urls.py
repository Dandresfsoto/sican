from django.conf.urls import url
from matrices.views import ListadoMatricesView, NuevoBeneficiarioView, UpdateBeneficiarioView, DeleteBeneficiarioView

urlpatterns = [
    url(r'^cargamasiva/$', ListadoMatricesView.as_view()),
    url(r'^diplomados/(?P<diplomado>\w+)/$', ListadoMatricesView.as_view()),
    url(r'^diplomados/(?P<diplomado>\w+)/nuevo/$', NuevoBeneficiarioView.as_view()),
    url(r'^diplomados/(?P<diplomado>\w+)/editar/(?P<pk>\w+)/$', UpdateBeneficiarioView.as_view()),
    url(r'^diplomados/(?P<diplomado>\w+)/eliminar/(?P<pk>\w+)/$', DeleteBeneficiarioView.as_view()),
]