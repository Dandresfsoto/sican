from django.conf.urls import url
from matrices.views import ListadoMatricesView, NuevoBeneficiarioView, UpdateBeneficiarioView, DeleteBeneficiarioView

urlpatterns = [
    url(r'^(?P<diplomado>\w+)/$', ListadoMatricesView.as_view()),
    url(r'^(?P<diplomado>\w+)/nuevo/$', NuevoBeneficiarioView.as_view()),
    url(r'^(?P<diplomado>\w+)/editar/(?P<pk>\w+)/$', UpdateBeneficiarioView.as_view()),
    url(r'^(?P<diplomado>\w+)/eliminar/(?P<pk>\w+)/$', DeleteBeneficiarioView.as_view()),
]