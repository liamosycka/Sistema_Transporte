from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RemitoViewSet, HistorialEstadosRemitoView, ChoferViewSet, EstadoRemitoViewSet, TipoEstadoRemitoViewSet, ViajeViewSet
from .views import BultoViewSet, ParticularViewSet, SolicitudViewSet, ClienteViewSet, LocalidadViewSet
from .views import RemitoCompletoView, ViajeViewSet, ViajesRemitoView
from django.urls.conf import include

router = DefaultRouter()
router.register(r'localidades', LocalidadViewSet, basename='localidades')
router.register(r'remitos', RemitoViewSet, basename='remitos')
router.register(r'choferes', ChoferViewSet, basename='choferes')
router.register(r'solicitudes', SolicitudViewSet, basename='solicitudes')
router.register(r'bultos', BultoViewSet, basename='bultos')
router.register(r'estados_remitos', EstadoRemitoViewSet,
                basename='estados_remitos')
router.register(r'tipos_estados', TipoEstadoRemitoViewSet,
                basename='tipos_estados')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'viajes', ViajeViewSet, basename='viajes')

urlpatterns = [
    path('remito/estado/<str:nro_remito>/', HistorialEstadosRemitoView.as_view()),
    path('remito/completo/<str:nro_remito>/', RemitoCompletoView.as_view()),
    path('remito/viaje/<str:nro_remito>/', ViajesRemitoView.as_view()),
    path('api/', include(router.urls)),
]