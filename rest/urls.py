from django.conf.urls import url
from rest.views import UserList, UserChatList, UserDetail, UserPermissionList, AdministrativosRh,CargosRh
from rest.views import AdministrativosRhSoportes, AdminUserList, GroupUserList, AdminUserPermissionList, TipoSoporteRh
from rest.views import FormadoresRh, FormadoresRhSoportes
from rest.views import DepartamentosList, MunicipiosList, SecretariasList, RadicadosList
from rest.views import MunicipiosChainedList, RadicadosChainedList
from rest.views import SolicitudesTransporteList, InformesExcelList, ReportesView,PreinscritosList, ResultadosPercepcionInicial

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

    url(r'tipo_soporte/rh/$', TipoSoporteRh.as_view()),

    url(r'formadores/rh/$', FormadoresRh.as_view()),
    url(r'formadores/rh/soportes/(?P<id_formador>\w+)/$', FormadoresRhSoportes.as_view()),

    url(r'bases/departamentos/$', DepartamentosList.as_view()),
    url(r'bases/municipios/$', MunicipiosList.as_view()),
    url(r'bases/secretarias/$', SecretariasList.as_view()),
    url(r'bases/radicados/$', RadicadosList.as_view()),
    url(r'chained/municipios/$', MunicipiosChainedList.as_view()),
    url(r'chained/radicados/$', RadicadosChainedList.as_view()),

    url(r'financiera/transportes/$', SolicitudesTransporteList.as_view()),
    url(r'informes/excel/$', InformesExcelList.as_view()),
    url(r'reportes/$', ReportesView.as_view()),
    url(r'formacion/preinscritos/$', PreinscritosList.as_view()),

    url(r'encuestas/percepcioninicial/$', ResultadosPercepcionInicial.as_view()),
]