from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SolicitudTransporteSerializer
from .models import SolicitudTransporte

class SolicitudTransporteView(APIView):
    #serializer_class=SolicitudTransporteSerializer
   
    def get(self, request, format=None):
        solicitudes=SolicitudTransporte.objects.all()
        serializer=SolicitudTransporteSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=SolicitudTransporteSerializer(data=request.data)
        if serializer.is_valid():
            print("correcto: ")
            print(serializer)
            print("tipo: ",type(serializer))
            if (serializer.save()):
                print("insertó")
            else:
                print("no insertó")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("incorrecto")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


