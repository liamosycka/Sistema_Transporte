from django.db import models
from django.db.models.deletion import RESTRICT

class Localidad(models.Model):
    nombre=models.CharField(max_length=20)
    codigo_postal=models.CharField(max_length=10, primary_key=True)

class Encargado(models.Model):
    legajo=models.CharField(max_length=10, primary_key=True)
    nombre=models.CharField(max_length=10)
    apellido=models.CharField(max_length=10)
    dni=models.CharField(max_length=15)
    tipo_doc=models.CharField(max_length=5)
    fecha_ingreso=models.DateField()

class Chofer(models.Model):
    legajo=models.CharField(max_length=10, primary_key=True)
    nombre=models.CharField(max_length=10)
    apellido=models.CharField(max_length=10)
    dni=models.CharField(max_length=15)
    tipo_doc=models.CharField(max_length=5)
    fecha_ingreso=models.DateField()

class Cliente(models.Model):
    id=models.CharField(max_length=10, primary_key=True)
    nombre=models.CharField(max_length=10)
    apellido=models.CharField(max_length=10)
    dni=models.CharField(max_length=15)
    tipo_doc=models.CharField(max_length=5)
    localidad=models.ForeignKey(Localidad, on_delete=models.RESTRICT)

class EstadoRemito(models.Model):
    id=models.AutoField(primary_key=True)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tipo_estado=models.CharField(max_length=20)

class SolicitudTransporte(models.Model):
    id_solicitud=models.CharField(max_length=3, primary_key=True)
    fecha=models.DateTimeField()
    direccion_origen=models.CharField(max_length=20)
    destinatario=models.CharField(max_length=20)
    direccion_destinatario=models.CharField(max_length=20)
    cliente=models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    localidad_destino=models.ForeignKey(Localidad, on_delete=models.RESTRICT)

class Bulto(models.Model):
    id=models.BigAutoField(primary_key=True)
    peso=models.FloatField()
    tipo=models.CharField(max_length=10)
    descripcion=models.CharField(max_length=20)
    valor_flete=models.FloatField()
    solicitud=models.ForeignKey(SolicitudTransporte, on_delete=models.RESTRICT )

class Remito(models.Model):
    nro_remito=models.CharField(max_length=20, primary_key=True)
    legajo_chofer=models.ForeignKey(Chofer, on_delete=models.RESTRICT)
    fecha_asignacion=models.DateField()
    valor_flete=models.FloatField()
    valor_contrareembolso=models.FloatField()
    estado_actual=models.ManyToManyField(EstadoRemito)
    solicitud_transporte=models.CharField(max_length=10)

class Viaje(models.Model):
    id_viaje=models.CharField(max_length=4)
    fecha_salida=models.DateField()
    fecha_confeccion=models.DateField()
    monto_inicial=models.FloatField
    legajo_chofer=models.ForeignKey(Chofer, on_delete=models.RESTRICT)
    remitos=models.ManyToManyField(Remito)
    localidades=models.ManyToManyField(Localidad)
    patente=models.CharField(max_length=10)
    


