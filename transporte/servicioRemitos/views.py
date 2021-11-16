from django.shortcuts import render
from .serializers import RemitoSerializer
from .models import Remito
from rest_framework import viewsets

class RemitoViewSet(viewsets.ModelViewSet):
    serializer_class=RemitoSerializer
    queryset=Remito.objects.all()
