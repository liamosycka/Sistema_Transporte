from datetime import date
import json
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

from .serializers import BultoSerializer, ClienteSerializer, EstadoRemitoSerializer, SolicitudTransporteSerializer, LocalidadSerializer
from .serializers import ParticularSerializer, EmpresaSerializer, ViajeSerializer, RemitoSerializer
from .serializers import ChoferSerializer, EncargadoSerializer, TipoEstadoRemitoSerializer
from .models import EstadoRemito, Particular, SolicitudTransporte, Cliente, Bulto, Localidad, Empresa, Viaje, Remito
from .models import Chofer, Encargado, TipoEstadoRemito

import re
from .views_validators import validate_crear_solicitud, validate_agregar_bultos, validate_remitos_chofer_estado
from .views_validators import validate_asociar_sol_remito, validate_viaje_fecha, validate_asoc_remito_viaje


def actualizar_estado_remito(remito, es_anterior, es_nuevo):
    fecha_in_estado=date.today()
    tipo_estado_anterior=TipoEstadoRemito.objects.get(pk=es_anterior)
    tipo_estado_nuevo=TipoEstadoRemito.objects.get(pk=es_nuevo)
    estado_anterior=EstadoRemito.objects.get(actual=True, tipo_estado=tipo_estado_anterior, remito=remito)
    estado_anterior.fecha_fin=date.today()
    estado_anterior.actual=False
    estado_anterior.save()
    estado_nuevo=EstadoRemito(fecha_inicio=fecha_in_estado, tipo_estado=tipo_estado_nuevo, actual=True, remito=remito)
    estado_nuevo.save()

class CrearSolicitudView(APIView):
    def post(self, request, id_cliente, opcion_dest_remit):
        print("en rama mainnn crear sol")
        try:
            body=request.data
            exito_validacion=validate_crear_solicitud(body, id_cliente, opcion_dest_remit)
            if exito_validacion is False:
                return Response("Datos inválidos, intente nuevamente")
            cliente=get_object_or_404(Cliente, pk=id_cliente)
            direccion=cliente.direccion
            nombre=cliente.nombre
            localidad=cliente.localidad.codigo_postal
            if opcion_dest_remit==0:
                #Soy remitente, los datos del cliente se llenan en origen y los del destinatario
                #se obtienen del body.
                direccion_origen=direccion
                localidad_origen=get_object_or_404(Localidad, pk=localidad)
                remitente=nombre
                direccion_destinatario=body['direccion']
                localidad_destinatario=get_object_or_404(Localidad, pk=body['localidad'])
                destintatario=body['nombre_2']
            else:
                #Soy Destinatario, los datos del cliente se llenan en destino y los del remitente
                #se obtienen del body.
                direccion_origen=body['direccion']
                localidad_origen=get_object_or_404(Localidad, pk=body['localidad'])
                remitente=body['nombre_2']
                direccion_destinatario=direccion
                localidad_destinatario=get_object_or_404(Localidad, pk=localidad)
                destintatario=nombre
            fecha=date.today()
            solicitud_anterior=SolicitudTransporte.objects.last()
            if solicitud_anterior is None:
                id_anterior="S0"
            else:
                id_anterior=solicitud_anterior.pk

            id_nuevo= "S"+str(int(id_anterior.split('S')[1])+1)
            solicitud=SolicitudTransporte(id=id_nuevo, fecha=fecha,direccion_origen=direccion_origen, \
                remitente=remitente,localidad_origen=localidad_origen,direccion_destinatario=direccion_destinatario,\
                destinatario=destintatario,localidad_destino=localidad_destinatario,cliente=cliente)
            solicitud.save()
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(solicitud.id)

class AgregarBultosView(APIView):
    def post(self, request, id_solicitud):
        """se obtienen los datos del body para crear el bulto
        y se utiliza el parámetro id_solicitud para asociarlos a la solicitud"""
        try:
            body=request.data
            exito_validacion=validate_agregar_bultos(body, id_solicitud)
            if exito_validacion is not True:
                return Response("Error en los datos de bultos")
            peso=body['peso']
            tipo=body['tipo']
            descripcion=body['descripcion']
            valor_flete=body['valor_flete']
            solicitud=get_object_or_404(SolicitudTransporte, pk=id_solicitud)
            bulto=Bulto(peso=peso, tipo=tipo, descripcion=descripcion, valor_flete=valor_flete, solicitud=solicitud)
            bulto.save()
        except ValueError as ve:
            return Response(f"{ve}", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(BultoSerializer(bulto).data)


class RemitosChoferEstado(APIView):
    def get(self, request):
        try:
            body=request.data
            exito_validacion=validate_remitos_chofer_estado(body)
            if(exito_validacion is False):
                return Response("Error en los datos")
            legajo=body['legajo']
            estado=body['estado']
            remitos_estado_chofer=[]
            #obtenemos los numeros de remitos de cada uno de los estados actuales y filtrados
            nrosR_estados_actuales=EstadoRemito.objects.filter(actual=True, tipo_estado=estado).values('remito')
            #esto nos devuelve los números de remito únicamente, con ellos debemos buscar el objeto remito
            #correspondiente para poder consultar el chofer
            for remito_estado in nrosR_estados_actuales:
                remito=Remito.objects.get(pk=remito_estado['remito'])
                if remito.legajo_chofer.legajo==legajo:
                    remitos_estado_chofer.append(remito.nro_remito)
        except ValueError as ve:
            return Response(f"{ve}", status=status.HTTP_400_BAD_REQUEST)
        return Response(remitos_estado_chofer)

class AsociarSolRemito(APIView):
    def put(self, request):
        try:
            body=request.data
            exito_validacion=validate_asociar_sol_remito(body)
            if exito_validacion is False:
                return Response("Error en los datos")
            nro_remito=body['remito']
            id_solicitud=body['sol']
            medio_pago=body['m_pago']
            valor_contra=body['contra']
            remito=get_object_or_404(Remito, pk=nro_remito)
            solicitud=get_object_or_404(SolicitudTransporte, pk=id_solicitud)
            #flete=CalcularValorFlete(remito)
            flete=0
            remito.medio_pago=medio_pago
            remito.valor_contrareembolso=valor_contra
            remito.valor_flete=flete
            remito.solicitud_transporte=solicitud
            remito.save()
            actualizar_estado_remito(remito, 'asignado', 'en_circulacion')
            
        except ValueError as ve:
            return Response(f"{ve}", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(RemitoSerializer(remito).data)

class ViajeFechaView(APIView):
    def get(self, request, fecha):
        exito_validacion=validate_viaje_fecha(fecha)
        if exito_validacion is False:
            return Response("Error en los datos")
        viajes=Viaje.objects.filter(fecha_salida=fecha)
        return Response(ViajeSerializer(viajes, many=True).data)

class RemitosParaViaje(APIView):
    def get(self, request, id_viaje):
        try:
            localidadesViaje=get_object_or_404(Viaje, pk=id_viaje).localidades.all()
            num_remitos_estados=EstadoRemito.objects.filter((Q(tipo_estado='en_circulacion')|\
                Q(tipo_estado='segunda_entrega')),actual=True).values('remito')
            remitos_viaje=[]
            for remito_estado in num_remitos_estados:
                remito=get_object_or_404(Remito, pk=remito_estado['remito'])
                if remito.solicitud_transporte.localidad_destino in localidadesViaje:
                    remitos_viaje.append(remito.nro_remito)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(remitos_viaje)

class AsociarRemitosAViaje(APIView):
    def put(self, request, id_viaje):
        try:
            body=request.data
            viaje=get_object_or_404(Viaje, pk=id_viaje)
            exito_validacion=validate_asoc_remito_viaje(body)
            if exito_validacion is False:
                return Response("Error en los datos")
            remitos=body['remitos']
            for nro_remito in remitos:
                remito=get_object_or_404(Remito, pk=nro_remito)
                viaje.remitos.add(remito)
                #actualizar estado del remito
                actualizar_estado_remito(remito, 'en_circulacion', 'en_viaje')
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(ViajeSerializer(viaje).data)

class CierreViaje(APIView):
    def get(self, request, id_viaje):
        try:
            viaje=get_object_or_404(Viaje, pk=id_viaje)
            remitos_viaje=viaje.remitos.all()
        
            monto_cierre=0
            
            for remito in remitos_viaje:
                #esto deberia ser un solo estado, ya que el remito puede tener uno solo actual
                #estado=EstadoRemito.objects.get(remito=remito, actual=True)
                estado=get_object_or_404(EstadoRemito, remito=remito, actual=True)
                if estado.tipo_estado.tipo_estado=='pagado':
                    monto_cierre+=remito.valor_contrareembolso
                    sol=remito.solicitud_transporte
                    bultos_sol=Bulto.objects.filter(solicitud=sol.id)
                    for bulto in bultos_sol:
                        monto_cierre+=bulto.valor_flete
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
            
        return Response(monto_cierre)


class AltaRemitoView(APIView):
    def post(self, request):
        patron_nro_remito=re.compile(r"R[0-9]{4}")
        body=request.data
        nro_remito=body['nro_remito']
        if re.fullmatch(patron_nro_remito, nro_remito):
            print("exito")
        else:
            print("no exito")
        fecha=date.today()
        legajo_chofer=body['legajo_chofer']
        chofer=Chofer.objects.get(pk=legajo_chofer)
        remito=Remito(nro_remito=nro_remito, fecha_asignacion=fecha, legajo_chofer=chofer)
        remito.save()
        #crear estado asignado y asignarle el remito nuevo
        #la fecha inicial del estado será la actual.
        fecha_in_estado=date.today()
        tipo_estado_ob=TipoEstadoRemito.objects.get(pk='asignado') #se obtiene la instancia del Tipo de Estado.
        estado=EstadoRemito(fecha_inicio=fecha_in_estado, tipo_estado=tipo_estado_ob, actual=True, remito=remito)
        estado.save()
        return Response(EstadoRemitoSerializer(estado).data)

class CambiarEstadoRemito(APIView):

    def put(self, request, nro_remito):

        body=request.data
        estado_nuevo_body=body['estado_nuevo']
        remito=Remito.objects.get(pk=nro_remito)
        fecha_in_estado=date.today()
        tipo_estado_anterior=TipoEstadoRemito.objects.get(pk='en_circulacion')
        tipo_estado_nuevo=TipoEstadoRemito.objects.get(pk=estado_nuevo_body)
        estado_anterior=EstadoRemito.objects.get(tipo_estado=tipo_estado_anterior, remito=remito)
        estado_anterior.fecha_fin=date.today()
        estado_anterior.actual=False
        estado_anterior.save()
        estado_nuevo=EstadoRemito(fecha_inicio=fecha_in_estado, tipo_estado=tipo_estado_nuevo, actual=True, remito=remito)
        estado_nuevo.save()

        return Response(EstadoRemitoSerializer(estado_nuevo).data)

class SolicitudTransporteView(APIView):
    def get(self, request, id_solicitud):
        solicitud=SolicitudTransporte.objects.get(pk=id_solicitud)
        return Response(SolicitudTransporteSerializer(solicitud).data)


class ParticularViewSet(viewsets.ModelViewSet):
    serializer_class=ParticularSerializer
    queryset=Particular.objects.all()

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class=EmpresaSerializer
    queryset=Empresa.objects.all()

class ChoferViewSet(viewsets.ModelViewSet):
    serializer_class=ChoferSerializer
    queryset=Chofer.objects.all()

class EncargadoViewSet(viewsets.ModelViewSet):
    serializer_class=EncargadoSerializer
    queryset=Encargado.objects.all()

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class=SolicitudTransporteSerializer
    queryset=SolicitudTransporte.objects.all()

class BultoViewSet(viewsets.ModelViewSet):
    serializer_class=BultoSerializer
    queryset=Bulto.objects.all()

class RemitoViewSet(viewsets.ModelViewSet):
    serializer_class=RemitoSerializer
    queryset=Remito.objects.all()

class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class=ViajeSerializer
    queryset=Viaje.objects.all()

class EstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=EstadoRemitoSerializer
    queryset=EstadoRemito.objects.all()

class TipoEstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=TipoEstadoRemitoSerializer
    queryset=TipoEstadoRemito.objects.all()

"""Fin Viewsets------------------------------------------------------------------------"""
class SolicitudListView(generics.ListCreateAPIView):
    """es lo mismo que la clase SolicitudTransporteView"""
    queryset=SolicitudTransporte.objects.all()
    serializer_class=SolicitudTransporteSerializer

class BultoView(generics.ListCreateAPIView):
    serializer_class=BultoSerializer
    def get_queryset(self):
        return Bulto.objects.filter(solicitud=self.kwargs['sol'])

class ParticularView(generics.ListCreateAPIView):
    serializer_class=ParticularSerializer
    def get_queryset(self):
        return Particular.objects.get(id_cliente=self.kwargs['id_cliente'])
        
class LocalidadListView(generics.ListCreateAPIView):
    queryset=Localidad.objects.all()
    serializer_class=LocalidadSerializer

class ClienteListView(generics.ListCreateAPIView):
    queryset=Cliente.objects.all()
    serializer_class=ClienteSerializer

class ParticularListView(generics.ListCreateAPIView):
    queryset=Particular.objects.all()
    serializer_class=ParticularSerializer


class SolicitudTransporteFecha(APIView):
    def get(self, request, fecha, op,format=None):
        """Si op=0 solicitud.fecha=fecha
        Si op=1 solicitud.fecha>=fecha
        Si op=2 solicitud.fecha<=fecha"""
        if(op==0):
            solicitud=SolicitudTransporte.objects.filter(fecha=fecha)
        elif(op==1):
            solicitud=SolicitudTransporte.objects.filter(fecha__gte=fecha)
        elif(op==2):
            solicitud=SolicitudTransporte.objects.filter(fecha__lte=fecha)
        serializer=SolicitudTransporteSerializer(solicitud, many=True)
        return Response(serializer.data)

'''class vista(APIView):
    def get(self,request,format=None):'''

"""
----------------------------------------------------------------------------------------"""
class LocalidadViewSet(viewsets.ModelViewSet):
    serializer_class=LocalidadSerializer
    queryset=Localidad.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    """esto encapsula todas las operaciones CRUD básicas y con el router
    creamos automáticamente todos los endpoints requeridos"""
    serializer_class=ClienteSerializer
    queryset=Cliente.objects.all()

class ParticularViewSet(viewsets.ModelViewSet):
    serializer_class=ParticularSerializer
    queryset=Particular.objects.all()

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class=EmpresaSerializer
    queryset=Empresa.objects.all()

class ChoferViewSet(viewsets.ModelViewSet):
    serializer_class=ChoferSerializer
    queryset=Chofer.objects.all()

class EncargadoViewSet(viewsets.ModelViewSet):
    serializer_class=EncargadoSerializer
    queryset=Encargado.objects.all()

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class=SolicitudTransporteSerializer
    queryset=SolicitudTransporte.objects.all()

class BultoViewSet(viewsets.ModelViewSet):
    serializer_class=BultoSerializer
    queryset=Bulto.objects.all()

class RemitoViewSet(viewsets.ModelViewSet):
    serializer_class=RemitoSerializer
    queryset=Remito.objects.all()

class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class=ViajeSerializer
    queryset=Viaje.objects.all()

class EstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=EstadoRemitoSerializer
    queryset=EstadoRemito.objects.all()

class TipoEstadoRemitoViewSet(viewsets.ModelViewSet):
    serializer_class=TipoEstadoRemitoSerializer
    queryset=TipoEstadoRemito.objects.all()

"""Fin Viewsets------------------------------------------------------------------------"""