from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import BultoSerializer, ClienteSerializer, EstadoRemitoSerializer, SolicitudTransporteSerializer, LocalidadSerializer
from .serializers import ParticularSerializer, EmpresaSerializer, ViajeSerializer, RemitoSerializer
from .serializers import ChoferSerializer, EncargadoSerializer, TipoEstadoRemitoSerializer
from .models import EstadoRemito, Particular, SolicitudTransporte, Cliente, Bulto, Localidad, Empresa, Viaje, Remito
from .models import Chofer, Encargado, TipoEstadoRemito

"""Viewsets: Usar Router (descomentar en urls.py)
----------------------------------------------------------------------------------------"""
class LocalidadViewSet(viewsets.ModelViewSet):
    serializer_class=LocalidadSerializer
    queryset=Localidad.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    """esto encapsula todas las operaciones CRUD básicas y con el router
    creamos automáticamente todos los endpoints requeridos"""
    serializer_class=ClienteSerializer
    queryset=Cliente.objects.all()

class ParticularViewSet(viewsets.ModelViewSet):
    serializer_class=ParticularSerializer
    queryset=Particular.objects.all()

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class=EmpresaSerializer
    queryset=Empresa.objects.all()

class ChoferViewSet(viewsets.ModelViewSet):
    serializer_class=ChoferSerializer
    queryset=Chofer.objects.all()

class EncargadoViewSet(viewsets.ModelViewSet):
    serializer_class=EncargadoSerializer
    queryset=Encargado.objects.all()

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class=SolicitudTransporteSerializer
    queryset=SolicitudTransporte.objects.all()

class BultoViewSet(viewsets.ModelViewSet):
    serializer_class=BultoSerializer
    queryset=Bulto.objects.all()

class RemitoViewSet(viewsets.ModelViewSet):
    serializer_class=RemitoSerializer
    queryset=Remito.objects.all()

class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class=ViajeSerializer
    queryset=Viaje.objects.all()

class EstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=EstadoRemitoSerializer
    queryset=EstadoRemito.objects.all()

class TipoEstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=TipoEstadoRemitoSerializer
    queryset=TipoEstadoRemito.objects.all()

"""Fin Viewsets------------------------------------------------------------------------"""
class SolicitudListView(generics.ListCreateAPIView):
    """es lo mismo que la clase SolicitudTransporteView"""
    queryset=SolicitudTransporte.objects.all()
    serializer_class=SolicitudTransporteSerializer

class BultoView(generics.ListCreateAPIView):
    serializer_class=BultoSerializer
    def get_queryset(self):
        return Bulto.objects.filter(solicitud=self.kwargs['sol'])

class ParticularView(generics.ListCreateAPIView):
    serializer_class=ParticularSerializer
    def get_queryset(self):
        return Particular.objects.get(id_cliente=self.kwargs['id_cliente'])
        
class LocalidadListView(generics.ListCreateAPIView):
    queryset=Localidad.objects.all()
    serializer_class=LocalidadSerializer

class ClienteListView(generics.ListCreateAPIView):
    queryset=Cliente.objects.all()
    serializer_class=ClienteSerializer

class ParticularListView(generics.ListCreateAPIView):
    queryset=Particular.objects.all()
    serializer_class=ParticularSerializer

class SolicitudTransporteView(APIView):

    def get(self, request,format=None):
        solicitudes=SolicitudTransporte.objects.all()
        serializer=SolicitudTransporteSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=SolicitudTransporteSerializer(data=request.data)
        if serializer.is_valid():
            if (serializer.save()):
                print("insertó")
            else:
                print("no insertó")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudTransporteFecha(APIView):
    def get(self, request, fecha, op,format=None):
        """Si op=0 solicitud.fecha=fecha
        Si op=1 solicitud.fecha>=fecha
        Si op=2 solicitud.fecha<=fecha"""
        if(op==0):
            solicitud=SolicitudTransporte.objects.filter(fecha=fecha)
        elif(op==1):
            solicitud=SolicitudTransporte.objects.filter(fecha__gte=fecha)
        elif(op==2):
            solicitud=SolicitudTransporte.objects.filter(fecha__lte=fecha)
        serializer=SolicitudTransporteSerializer(solicitud, many=True)
        return Response(serializer.data)