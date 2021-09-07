from django.contrib import admin
from .models import Cliente
from .models import Chofer
from .models import Localidad
from .models import Encargado
from .models import Remito
from .models import SolicitudTransporte
from .models import EstadoRemito
from .models import Viaje
from .models import Bulto


admin.site.register(Cliente)
admin.site.register(Chofer)
admin.site.register(Localidad)
admin.site.register(Remito)
admin.site.register(SolicitudTransporte)
admin.site.register(EstadoRemito)
admin.site.register(Viaje)
admin.site.register(Bulto)
