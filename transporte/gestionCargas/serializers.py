from rest_framework import serializers
from .models import Empresa, Particular, SolicitudTransporte
from .models import Remito
from .models import Chofer
from .models import Encargado
from .models import Cliente
from .models import Localidad
from .models import Viaje
from .models import EstadoRemito, TipoEstadoRemito
from .models import Bulto

class SolicitudTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model= SolicitudTransporte
        fields='__all__'
        
class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Remito
        fields='__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cliente
        fields='__all__'

class ParticularSerializer(serializers.ModelSerializer):
    class Meta:
        model= Particular
        fields='__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Empresa
        fields='__all__'

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model= Localidad
        fields='__all__'

class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model= Chofer
        fields='__all__'

class EncargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Encargado
        fields='__all__'

class BultoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bulto
        fields='__all__'

class EstadoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model= EstadoRemito
        fields='__all__'

class TipoEstadoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model= TipoEstadoRemito
        fields='__all__'

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Viaje
        fields='__all__'