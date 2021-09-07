from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import SolicitudTransporteSerializer
from .models import SolicitudTransporte

class SolicitudTransporteView(APIView):
    serializer_class=SolicitudTransporteSerializer

    def get(self, request, format=None):
        solicitudes=SolicitudTransporte.objects.all()
        serializer=SolicitudTransporteSerializer(solicitudes, many=True)
        return Response(serializer.data)


