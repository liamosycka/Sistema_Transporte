from django.urls import path
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, SolicitudListView, SolicitudTransporteFecha, SolicitudTransporteView, BultoView
from .views import ClienteListView, LocalidadListView, ParticularListView

from .views import LocalidadViewSet, ParticularViewSet, EmpresaViewSet, ChoferViewSet, EncargadoViewSet
from .views import SolicitudViewSet, BultoViewSet, RemitoViewSet, ViajeViewSet, EstadoRemitoViewSet
from .views import TipoEstadoRemitoViewSet
"""

"""
router=DefaultRouter()
router.register(r'localidades', LocalidadViewSet, basename='localidades')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'particulares', ParticularViewSet, basename='particulares')
router.register(r'empresas', EmpresaViewSet, basename='empresas')
router.register(r'choferes', ChoferViewSet, basename='choferes')
router.register(r'encargados', EncargadoViewSet, basename='encargados')
router.register(r'solicitudes', SolicitudViewSet, basename='solicitudes')
router.register(r'bultos', BultoViewSet, basename='bultos')
router.register(r'remitos', RemitoViewSet, basename='remitos')
router.register(r'estados_remitos', EstadoRemitoViewSet, basename='estados_remitos')
router.register(r'tipos_estados', TipoEstadoRemitoViewSet, basename='tipos_estados')
router.register(r'viajes', ViajeViewSet, basename='viajes')
urlpatterns=router.urls

"""
comentar lo de abajo para usar el router de cliente
urlpatterns = [
    path('sols/',SolicitudTransporteView.as_view()),
    path('sols/<str:fecha>/<int:op>/', SolicitudTransporteFecha.as_view()),
    path('sols/list/',SolicitudListView.as_view()),
    path('bultos/<str:sol>/',BultoView.as_view() ),
    path('localidades/',LocalidadListView.as_view() ),
    path('clientes/',ClienteListView.as_view() ),
    path('particulares/<int:id_cliente>',ParticularListView.as_view() ),

]
"""




"""
Explicacion URLS:
definimos el url:
path('home/', some_view)
La url:
/home/?fecha=2021-09-09&destinatario=asd se dirigirá al some_view, ya que DJANGO 
coloca los params dentro de un dicc llamado query_params, que será asi: 
<QueryDict: {'fecha': ['2021-09-09'], 'destinatario': ['Pedro']}>
entonces fecha estará ahi dentro, para accederlo desde some_view
podemos hacer request.query_params['fecha']
la view solo tiene que tener esto:
def get(self, request)
------------------------------------
La manera que Django recomienda enviar params por el GET es asi:
/home/2021-09-09/Pedro
definiendo una ruta: 
path('home/<str:fecha>/<str:destinatario>)
y definiendo una vista:
def get(self, request, fecha, destinatario)
y accediendo los params solo por los atributos

"""