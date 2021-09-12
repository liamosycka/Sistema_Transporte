from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import ClienteSerializer, SolicitudTransporteSerializer
from .models import SolicitudTransporte, Cliente

class ClienteViewSet (viewsets.ModelViewSet):
    """esto encapsula todas las operaciones CRUD básicas y con el router
    creamos automáticamente todos los endpoints requeridos"""
    serializer_class=ClienteSerializer
    queryset=Cliente.objects.all()

class SolicitudListView(generics.ListCreateAPIView):
    """es lo mismo que la clase SolicitudTransporteView"""
    queryset=SolicitudTransporte.objects.all()
    serializer_class=SolicitudTransporteSerializer

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