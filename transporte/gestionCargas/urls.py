from django.urls import path
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, SolicitudListView, SolicitudTransporteFecha, SolicitudTransporteView

"""

router=DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
urlpatterns=router.urls
"""

"""
comentar lo de abajo para usar el router de cliente
"""
urlpatterns = [
    path('sols/',SolicitudTransporteView.as_view()),
    path('sols/<str:fecha>/<int:op>/', SolicitudTransporteFecha.as_view()),
    path('sols/list/',SolicitudListView.as_view())
]




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