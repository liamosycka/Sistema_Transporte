from django.shortcuts import get_object_or_404, render

from .serializers import RemitoSerializer, ChoferSerializer, ViajeSerializer
from .models import Remito, Chofer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BultoSerializer, ClienteSerializer, EstadoRemitoSerializer, SolicitudTransporteSerializer, LocalidadSerializer
from .serializers import ParticularSerializer, RemitoSerializer
from .serializers import ChoferSerializer, TipoEstadoRemitoSerializer, RemitoCompletoSerializer
from .models import EstadoRemito, Particular, SolicitudTransporte, Cliente, Bulto, Localidad,Remito
from .models import Chofer, TipoEstadoRemito, Viaje
from collections import namedtuple


class RemitoViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=RemitoSerializer
    queryset=Remito.objects.all()

class ChoferViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=ChoferSerializer
    queryset=Chofer.objects.all()

class RemitoCompletoView(APIView):
    swagger_schema = None
    def get(self, request, nro_remito):
        remito=get_object_or_404(Remito, pk=nro_remito)
        solicitud=remito.solicitud_transporte
        bultos=Bulto.objects.filter(solicitud=solicitud.pk)
        chofer=get_object_or_404(Chofer, pk=remito.legajo_chofer.legajo)
        RemitoCompleto=namedtuple('RemitoCompleto', ('remito', 'solicitud', 'bultos', 'chofer'))
        respuesta=RemitoCompleto(remito=remito, solicitud=solicitud, bultos=bultos, chofer=chofer)
        serializer=RemitoCompletoSerializer(respuesta)
        return Response(serializer.data)

class HistorialEstadosRemitoView(APIView):
    swagger_schema = None
    def get(self, request, nro_remito):
        remito=get_object_or_404(Remito, pk=nro_remito)
        historial_estados=EstadoRemito.objects.filter(remito=nro_remito)
        return Response(EstadoRemitoSerializer(historial_estados, many=True).data)

class ViajesRemitoView(APIView):
    swagger_schema = None
    def get(self, request, nro_remito):
        remito=get_object_or_404(Remito, pk=nro_remito)
        viajes=Viaje.objects.filter(remitos=nro_remito)
        return Response(ViajeSerializer(viajes, many=True).data)


class LocalidadViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=LocalidadSerializer
    queryset=Localidad.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    """esto encapsula todas las operaciones CRUD básicas y con el router
    creamos automáticamente todos los endpoints requeridos"""
    serializer_class=ClienteSerializer
    queryset=Cliente.objects.all()

class ParticularViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=ParticularSerializer
    queryset=Particular.objects.all()

class ChoferViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=ChoferSerializer
    queryset=Chofer.objects.all()

class SolicitudViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=SolicitudTransporteSerializer
    queryset=SolicitudTransporte.objects.all()

class BultoViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=BultoSerializer
    queryset=Bulto.objects.all()


class EstadoRemitoViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=EstadoRemitoSerializer
    queryset=EstadoRemito.objects.all()

class TipoEstadoRemitoViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=TipoEstadoRemitoSerializer
    queryset=TipoEstadoRemito.objects.all()

class ViajeViewSet(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class=ViajeSerializer
    queryset=Viaje.objects.all()