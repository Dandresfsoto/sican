from django.conf.urls import url
from rest.views import UserList, UserChatList, UserDetail, UserPermissionList, AdministrativosRh,CargosRh
from rest.views import AdministrativosRhSoportes, AdminUserList, GroupUserList, AdminUserPermissionList

urlpatterns = [
    url(r'usuarios/chat_list/$', UserList.as_view()),
    url(r'usuarios/chat_list/(?P<id>\w+)/$', UserDetail.as_view()),
    url(r'usuarios/chat_last/$', UserChatList.as_view()),
    url(r'usuarios/permisos/$', UserPermissionList.as_view()),

    url(r'administrativos/rh/$', AdministrativosRh.as_view()),
    url(r'administrativos/rh/soportes/(?P<id_administrativo>\w+)/$', AdministrativosRhSoportes.as_view()),

    url(r'adminuser/usuarios/$', AdminUserList.as_view()),
    url(r'adminuser/grupos/$', GroupUserList.as_view()),

    url(r'cargos/rh/$', CargosRh.as_view()),

    url(r'adminuser/permisos/$', AdminUserPermissionList.as_view()),
]