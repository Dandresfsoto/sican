from django.conf.urls import url
from rest.views import UserList, UserChatList, UserDetail, UserPermissionList, AdministrativosRh,CargosRh
from rest.views import AdministrativosRhSoportes, AdminUserList, GroupUserList, AdminUserPermissionList, TipoSoporteRh
from rest.views import FormadoresRh, FormadoresRhSoportes
from rest.views import DepartamentosList, MunicipiosList, SecretariasList, RadicadosList
from rest.views import MunicipiosChainedList, RadicadosChainedList
from rest.views import SolicitudesTransporteList, InformesExcelList, ReportesView,PreinscritosList, ResultadosPercepcionInicial
from rest.views import DiplomadosList, NivelesList, SesionesList, SolicitudesTransporteFormacionList, SolicitudesTransporteFormadorList
from rest.views import SolicitudesTransporteFormadorFinancieraList, EntregablesList
from rest.views import FormadoresCronogramasList, FormadoresCronogramasFilterList, SecretariasChainedList
from rest.views import SemanasList, LideresRh, LideresRhSoportes
from rest.views import SemanasFormacionList, FormadoresFinancieraCronogramasList
from rest.views import ResultadosPercepcionInicialList, RadicadosRetomaList, RetomaList
from rest.views import MatricesDiplomadosList, AutocompleteRadicados, GruposChainedList
from rest.views import FormadoresGrupos, FormadoresGruposLista, ContratosValorList, EntregablesValorList, FormadoresRevision
from rest.views import FormadoresRevisionFormador, CortesList, NegociadoresRh
from rest.views import RequerimientosContratacion, AutocompleteMunicipios, RequerimientosContratacionRespuesta
from rest.views import CargaMasivaMatrices, FormadoresListEvidencias, NivelesListEvidencias, SesionesListEvidencias, EntregablesListEvidencias
from rest.views import SoportesListEvidencias,Cedulas2BeneficiariosId
from rest.views import DelegacionRequerimientos, EvidenciasCodigos
from rest.views import RedList, CargaMasivaEvidenciasList, DiplomadosEvidenciasList, FormadoresConsolidadoRh,CertificadosEscuelaTic

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


    url(r'lideres/rh/$', LideresRh.as_view()),
    url(r'lideres/rh/soportes/(?P<id_lider>\w+)/$', LideresRhSoportes.as_view()),

    url(r'negociadores/rh/$', NegociadoresRh.as_view()),


    url(r'bases/departamentos/$', DepartamentosList.as_view()),
    url(r'bases/municipios/$', MunicipiosList.as_view()),
    url(r'bases/secretarias/$', SecretariasList.as_view()),
    url(r'bases/radicados/$', RadicadosList.as_view()),
    url(r'chained/municipios/$', MunicipiosChainedList.as_view()),
    url(r'chained/radicados/$', RadicadosChainedList.as_view()),
    url(r'chained/secretarias/$', SecretariasChainedList.as_view()),
    url(r'chained/grupos/$', GruposChainedList.as_view()),

    url(r'financiera/transportes/$', SolicitudesTransporteList.as_view()),
    url(r'financiera/transportes/(?P<id_formador>\w+)/$', SolicitudesTransporteFormadorFinancieraList.as_view()),


    url(r'informes/excel/$', InformesExcelList.as_view()),
    url(r'reportes/$', ReportesView.as_view()),
    url(r'formacion/preinscritos/$', PreinscritosList.as_view()),

    url(r'encuestas/percepcioninicial/$', ResultadosPercepcionInicial.as_view()),
    url(r'encuestas/percepcioninicialresultados/$', ResultadosPercepcionInicialList.as_view()),


    url(r'financiera/diplomados/$', DiplomadosList.as_view()),
    url(r'financiera/niveles/$', NivelesList.as_view()),
    url(r'financiera/sesiones/$', SesionesList.as_view()),
    url(r'financiera/entregables/$', EntregablesList.as_view()),

    url(r'formacion/transportes/$', SolicitudesTransporteFormacionList.as_view()),
    url(r'formacion/transportes/(?P<id_formador>\w+)/$', SolicitudesTransporteFormadorList.as_view()),

    url(r'formacion/cronogramas/(?P<id_semana>\w+)/$', FormadoresCronogramasList.as_view()),
    url(r'formacion/cronogramas/(?P<id_formador>\w+)/(?P<id_semana>\w+)/$', FormadoresCronogramasFilterList.as_view()),

    url(r'financiera/cronogramas/$', SemanasList.as_view()),
    url(r'financiera/cronogramas/(?P<id_semana>\w+)/$', FormadoresFinancieraCronogramasList.as_view()),

    url(r'formacion/semanas/$', SemanasFormacionList.as_view()),
    url(r'acceso/radicadosretoma/$', RadicadosRetomaList.as_view()),

    url(r'acceso/retoma/$', RetomaList.as_view()),

    url(r'matrices/diplomados/(?P<diplomado>\w+)/$', MatricesDiplomadosList.as_view()),
    url(r'autocomplete/radicados/$', AutocompleteRadicados.as_view()),
    url(r'autocomplete/municipios/$', AutocompleteMunicipios.as_view()),


    url(r'formacion/grupos/$', FormadoresGrupos.as_view()),
    url(r'formacion/grupos/(?P<id_formador>\w+)/$', FormadoresGruposLista.as_view()),

    url(r'financiera/contratos/$', ContratosValorList.as_view()),
    url(r'financiera/entregablesvalor/(?P<id_contrato>\w+)/$', EntregablesValorList.as_view()),

    url(r'formadores/revision/$', FormadoresRevision.as_view()),
    url(r'formadores/revision/(?P<id_formador>\w+)/$', FormadoresRevisionFormador.as_view()),

    url(r'financiera/cortes/$', CortesList.as_view()),

    url(r'formacion/requerimientoscontratacion/$', RequerimientosContratacion.as_view()),
    url(r'formacion/requerimientoscontratacionrespuesta/$', RequerimientosContratacionRespuesta.as_view()),

    url(r'cargamasiva/matrices/$', CargaMasivaMatrices.as_view()),

    url(r'evidencias/diplomados/$', DiplomadosEvidenciasList.as_view()),
    url(r'evidencias/formadores/(?P<id_diplomado>\w+)/$', FormadoresListEvidencias.as_view()),
    url(r'evidencias/niveles/(?P<id_diplomado>\w+)/$', NivelesListEvidencias.as_view()),
    url(r'evidencias/sesiones/(?P<id_nivel>\w+)/$', SesionesListEvidencias.as_view()),
    url(r'evidencias/entregables/(?P<id_sesion>\w+)/$', EntregablesListEvidencias.as_view()),
    url(r'evidencias/soportes/(?P<id_entregable>\w+)/(?P<id_formador>\w+)/$', SoportesListEvidencias.as_view()),
    url(r'cedulas/id/',Cedulas2BeneficiariosId.as_view()),

    url(r'requerimientos/delegacion/$', DelegacionRequerimientos.as_view()),

    url(r'evidencias/codigos/',EvidenciasCodigos.as_view()),
    url(r'reds/lista/',RedList.as_view()),

    url(r'cargamasivaevidencias/lista/',CargaMasivaEvidenciasList.as_view()),

    url(r'rh/consolidadoformadores/',FormadoresConsolidadoRh.as_view()),

    url(r'diplomas/escuelatic/',CertificadosEscuelaTic.as_view()),
]