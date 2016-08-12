from django.conf.urls import url
from informes.views import InicioView

urlpatterns = [
    url(r'^excel/$', InicioView.as_view()),
]