from django.conf.urls import url
from .views import UserListView, UpdateUserView, NewUserView, GroupListView,NewGroupView, UpdateGrupoView,DeleteGrupoView

urlpatterns = [
    url(r'^usuarios/$', UserListView.as_view()),
    url(r'^usuarios/nuevo/$', NewUserView.as_view()),
    url(r'^usuarios/editar/(?P<pk>[0-9]+)/$', UpdateUserView.as_view()),

    url(r'^grupos/$', GroupListView.as_view()),
    url(r'^grupos/nuevo/$', NewGroupView.as_view()),
    url(r'^grupos/editar/(?P<pk>[0-9]+)/$', UpdateGrupoView.as_view()),
    url(r'^grupos/eliminar/(?P<pk>[0-9]+)/$', DeleteGrupoView.as_view()),
]