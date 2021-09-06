from django.urls import path
from .views import SolicitudTransporteView

urlpatterns = [
    path('home', SolicitudTransporteView.as_view())
]