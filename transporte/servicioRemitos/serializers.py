from rest_framework import serializers
from .models import Remito, Chofer, Localidad

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model= Localidad
        fields='__all__'

class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model= Chofer
        fields='__all__'

class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Remito
        fields='__all__'