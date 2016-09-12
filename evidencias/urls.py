from django.conf.urls import url
from evidencias.views import DiplomadosListView

urlpatterns = [
    url(r'^general/$', DiplomadosListView.as_view()),
]