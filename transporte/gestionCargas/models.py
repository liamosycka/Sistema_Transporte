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
    fecha_nac=models.DateField()
    fecha_ingreso=models.DateField()

class Chofer(models.Model):
    legajo=models.CharField(max_length=10, primary_key=True)
    nombre=models.CharField(max_length=10)
    apellido=models.CharField(max_length=10)
    dni=models.CharField(max_length=15)
    fecha_nac=models.DateField()
    fecha_ingreso=models.DateField()

class Cliente(models.Model):
    TIPOS_CLIENTE=[
        ('P', 'Cliente Particular'),
        ('E', 'Cliente Empresa'),
    ]
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    localidad=models.ForeignKey(Localidad, on_delete=models.RESTRICT)
    direccion=models.CharField(max_length=20)
    email=models.EmailField()
    telefono=models.CharField(max_length=20)
    tipo_cliente=models.CharField(max_length=20, choices=TIPOS_CLIENTE)

class Particular(models.Model):
    dni=models.CharField(max_length=20, primary_key=True)
    nombre=models.CharField(max_length=20)
    apellido=models.CharField(max_length=20)
    fecha_nac=models.DateField()
    id_cliente=models.OneToOneField(Cliente, on_delete=models.RESTRICT)

class Empresa(models.Model):
    cuit=models.CharField(max_length=20, primary_key=True)
    nombre=models.CharField(max_length=20)
    id_cliente=models.OneToOneField(Cliente, on_delete=models.RESTRICT)

class TipoEstadoRemito(models.Model):
    id=models.AutoField(primary_key=True)
    TIPO_ESTADO_CHOICES=[
        ('asignado', 'Estado Asignado'),
        ('en_circulacion', 'Estado en Circulación'),
        ('en_viaje', 'Estado en Viaje'),
        ('rendido', 'Estado Rendido'),
        ('segunda_entrega', 'Estado Segunda Entrega'),
        ('pendiente', 'Estado Pendiente'),
        ('pagado', 'Estado Pagado'),
    ]
    tipo_estado=models.CharField(max_length=20, choices=TIPO_ESTADO_CHOICES, default='asignado')


class SolicitudTransporte(models.Model):
    id=models.AutoField(primary_key=True)
    fecha=models.DateField()
    remitente=models.CharField(max_length=20)
    direccion_origen=models.CharField(max_length=20)
    localidad_origen=models.ForeignKey(Localidad, on_delete=models.RESTRICT, related_name='localidades_origen')
    destinatario=models.CharField(max_length=20)
    direccion_destinatario=models.CharField(max_length=20)
    cliente=models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    localidad_destino=models.ForeignKey(Localidad, on_delete=models.RESTRICT, related_name='localidades_destino')

class Bulto(models.Model):
    TIPO_BULTO_CHOICES=[
        ('CH', 'Bulto chico (hasta 10kg)'),
        ('M', 'Bulto mediano (entre 10kg y 25kg)'),
        ('G', 'Bulto grande (más de 25kg)'),
    ]
    id=models.AutoField(primary_key=True)
    peso=models.FloatField()
    tipo=models.CharField(max_length=10, choices=TIPO_BULTO_CHOICES)
    descripcion=models.CharField(max_length=20)
    valor_flete=models.FloatField()
    solicitud=models.ForeignKey(SolicitudTransporte, on_delete=models.RESTRICT)

class HistorialEstados(models.Model):
    id=models.AutoField(primary_key=True)




class Remito(models.Model):
    MEDIO_PAGO=[
        ('OR', 'Pago en Origen'),
        ('DES', 'Pago en Destino'),
        ('CC', 'Pago con Cuenta Corriente')
    ]
    nro_remito=models.CharField(max_length=20, primary_key=True)
    legajo_chofer=models.ForeignKey(Chofer, on_delete=models.RESTRICT)
    fecha_asignacion=models.DateField()
    valor_flete=models.FloatField()
    valor_contrareembolso=models.FloatField()
    medio_pago=models.CharField(max_length=20, choices=MEDIO_PAGO)
    solicitud_transporte=models.OneToOneField(SolicitudTransporte, on_delete=models.RESTRICT, blank=True)

    #estado_actual=models.OneToOneField(EstadoRemito)
    #historial=models.OneToOneField(HistorialEstados)

class EstadoRemito(models.Model):
    id=models.AutoField(primary_key=True)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField(blank=True)
    tipo_estado=models.ForeignKey(TipoEstadoRemito, on_delete=models.RESTRICT)
    actual=models.BooleanField()
    remito=models.ForeignKey(Remito, on_delete=models.RESTRICT)
    #historial=models.ForeignKey(HistorialEstados, on_delete=models.RESTRICT)

class Viaje(models.Model):
    id=models.AutoField(primary_key=True)
    fecha_salida=models.DateField()
    fecha_confeccion=models.DateField()
    legajo_chofer=models.ForeignKey(Chofer, on_delete=models.RESTRICT)
    remitos=models.ManyToManyField(Remito, blank=True)
    localidades=models.ManyToManyField(Localidad)