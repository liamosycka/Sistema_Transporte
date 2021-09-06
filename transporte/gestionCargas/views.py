from rest_framework.serializers import Serializer
from django.shortcuts import render
from rest_framework import generics
from .serializers import SolicitudTransporteSerializer
from .models import SolicitudTransporte

class SolicitudTransporteView(generics.CreateAPIView):
    queryset=SolicitudTransporte.objects.all()
    serializer_class=SolicitudTransporteSerializer

