from django.db import models

class Localidad(models.Model):
    nombre=models.CharField(max_length=20)
    codigo_postal=models.CharField(max_length=10, primary_key=True)

class Chofer(models.Model):
    legajo=models.CharField(max_length=10, primary_key=True)
    nombre=models.CharField(max_length=10)
    apellido=models.CharField(max_length=10)
    dni=models.CharField(max_length=15)
    fecha_nac=models.DateField()
    fecha_ingreso=models.DateField()


class Remito(models.Model):
    MEDIO_PAGO=[
        ('OR', 'Pago en Origen'),
        ('DES', 'Pago en Destino'),
        ('CC', 'Pago con Cuenta Corriente')
    ]
    nro_remito=models.CharField(max_length=20, primary_key=True)
    legajo_chofer=models.ForeignKey(Chofer, on_delete=models.RESTRICT)
    fecha_asignacion=models.DateField()
    valor_flete=models.FloatField(null=True)
    valor_contrareembolso=models.FloatField(null=True)
    medio_pago=models.CharField(max_length=20, choices=MEDIO_PAGO, null=True)
    #solicitud_transporte=models.OneToOneField(SolicitudTransporte, on_delete=models.RESTRICT, blank=True, null=True)
