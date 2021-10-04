from datetime import date
import json
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import BultoSerializer, ClienteSerializer, EstadoRemitoSerializer, SolicitudTransporteSerializer, LocalidadSerializer
from .serializers import ParticularSerializer, EmpresaSerializer, ViajeSerializer, RemitoSerializer
from .serializers import ChoferSerializer, EncargadoSerializer, TipoEstadoRemitoSerializer
from .models import EstadoRemito, Particular, SolicitudTransporte, Cliente, Bulto, Localidad, Empresa, Viaje, Remito
from .models import Chofer, Encargado, TipoEstadoRemito

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

class CrearSolicitudView(APIView):
    def post(self, request, id_cliente, opcion_dest_remit):
        cliente=Cliente.objects.get(pk=id_cliente)
        direccion=cliente.direccion
        nombre=cliente.nombre
        localidad=cliente.localidad.codigo_postal
        body=request.data
        if opcion_dest_remit==0:
            #Soy remitente
            direccion_origen=direccion
            print("antes del loc orign")
            localidad_origen=Localidad.objects.get(pk='8300')
            print("dsps del loc origen: ", localidad_origen)
            remitente=nombre
            direccion_destinatario=body['direccion']
            localidad_destinatario=Localidad.objects.filter(pk=body['localidad']).get()
            destintatario=body['nombre_2']
        else:
            #Soy Destinatario
            direccion_origen=body['direccion']
            localidad_origen=Localidad.objects.filter(pk=body['localidad']).get()
            remitente=body['nombre_2']
            direccion_destinatario=direccion
            localidad_destinatario=Localidad.objects.get(pk=localidad)
            destintatario=nombre
        fecha=date.today()
        solicitud=SolicitudTransporte(fecha=fecha,direccion_origen=direccion_origen,remitente=remitente,localidad_origen=localidad_origen,direccion_destinatario=direccion_destinatario,destinatario=destintatario,localidad_destino=localidad_destinatario,cliente=cliente)
        solicitud.save()
        id_solicitud=SolicitudTransporte.objects.last().pk
        return Response(id_solicitud)

class AgregarBultosView(APIView):
    def post(self, request, id_solicitud):
        body=request.data
        peso=body['peso']
        tipo=body['tipo']
        descripcion=body['descripcion']
        valor_flete=body['valor_flete']
        solicitud=SolicitudTransporte.objects.get(pk=id_solicitud)
        bulto=Bulto(peso=peso, tipo=tipo, descripcion=descripcion, valor_flete=valor_flete, solicitud=solicitud)
        bulto.save()
        return Response(BultoSerializer(bulto).data)

class AltaRemitoView(APIView):
    def post(self, request):
        body=request.data
        nro_remito=body['nro_remito']
        fecha=date.today()
        valor_flete=body['flete']
        valor_contra=body['contra']
        legajo_chofer=body['legajo_chofer']
        chofer=Chofer.objects.get(pk=legajo_chofer)
        remito=Remito(nro_remito=nro_remito, fecha_asignacion=fecha, valor_flete=valor_flete, valor_contrareembolso=valor_contra, legajo_chofer=chofer)
        remito.save()

        #crear estado asignado
        fecha_in_estado=date.today()
        tipo_estado_ob=TipoEstadoRemito.objects.get(pk='asignado')
        nuevo_remito_nro=Remito.objects.last().pk
        nuevo_remito=Remito.objects.get(pk=nuevo_remito_nro)
        estado=EstadoRemito(fecha_inicio=fecha_in_estado, tipo_estado=tipo_estado_ob, actual=True, remito=nuevo_remito)
        estado.save()
        return Response(EstadoRemitoSerializer(estado).data)

class RemitosChoferEstado(APIView):
    def get(self, request):
        body=request.data
        legajo=body['legajo']
        estado=body['estado']
        remitos=Remito.objects.filter(legajo_chofer=legajo)
        remitos_estado=[]
        for remito in remitos:
            remitos_estado+=EstadoRemito.objects.filter(tipo_estado=estado, remito=remito).values('remito')

        return Response(remitos_estado)

class AsociarSolRemito(APIView):
    def put(self, request):
        body=request.data
        nro_remito=body['remito']
        id_solicitud=body['sol']
        medio_pago=body['m_pago']
        valor_contra=body['contra']
        remito=Remito.objects.get(pk=nro_remito)
        solicitud=SolicitudTransporte.objects.get(pk=id_solicitud)
        #flete=CalcularValorFlete(remito)
        flete=1200
        remito.medio_pago=medio_pago
        remito.valor_contrareembolso=valor_contra
        remito.valor_flete=flete
        remito.solicitud_transporte=solicitud
        remito.save()

        #actualizar estado del remito
        fecha_in_estado=date.today()
        tipo_estado_anterior=TipoEstadoRemito.objects.get(pk='asignado')
        tipo_estado_nuevo=TipoEstadoRemito.objects.get(pk='en_circulacion')
        estado_anterior=EstadoRemito.objects.get(tipo_estado=tipo_estado_anterior, remito=remito)
        estado_anterior.fecha_fin=date.today()
        estado_anterior.actual=False
        estado_anterior.save()
        estado_nuevo=EstadoRemito(fecha_inicio=fecha_in_estado, tipo_estado=tipo_estado_nuevo, actual=True, remito=remito)
        estado_nuevo.save()

        return Response(RemitoSerializer(remito).data)

class ViajeFechaView(APIView):
    def get(self, request, fecha):
        viajes=Viaje.objects.filter(fecha_salida=fecha)
        return Response(ViajeSerializer(viajes, many=True).data)

class RemitosParaViaje(APIView):
    def get(self, request, id_viaje):
        localidadesViaje=Viaje.objects.get(pk=id_viaje).localidades.all()
        print(localidadesViaje)
        num_remitos_estados=EstadoRemito.objects.filter(Q(tipo_estado='en_circulacion')|Q(tipo_estado='segunda_entrega'))
        remitos=[]
        for num_remito in num_remitos_estados:
            remitos.append(num_remito.remito)
        print("Remitos: ", remitos)
        remitos_viaje=[]
        for remito in remitos:
            if remito.solicitud_transporte.localidad_destino in localidadesViaje:
                print("está en las loc del viaje")
                remitos_viaje.append(remito.nro_remito)
        print("remitos viaje: ", remitos_viaje)
        #falta ver como devolver únicamente el nro_remito
        #return Response(RemitoSerializer(remitos_viaje, many=True).data)
        return Response(remitos_viaje)

class AsociarRemitosAViaje(APIView):
    def put(self, request, id_viaje):
        body=request.data
        viaje=Viaje.objects.get(pk=id_viaje)
        remitos=body['remitos']
        remitos_obj=[]
        for nro_remito in remitos:
            print("hola: ",nro_remito)
            remitos_obj.append(Remito.objects.get(pk=nro_remito))

        for remito_obj in remitos_obj:
            viaje.remitos.add(remito_obj)

        #print("el viaje quedo: ",viaje.remitos.all())

        return Response(ViajeSerializer(viaje).data)

class CierreViaje(APIView):
    def get(self, request, id_viaje):
        viaje=Viaje.objects.get(pk=id_viaje)
        remitos_viaje=viaje.remitos.all()
        print("remitos en viaje: ", remitos_viaje)
        #se filtran remitos en estado pagado o pendiente por un solo motivo
        remitos_filtro=[]
        
        for remito in remitos_viaje:
            print("remito en for: ", remito)
            estado=EstadoRemito.objects.get(remito=remito, actual=True)
            if estado.tipo_estado.tipo_estado=='pagado':
                if remito.nro_remito==estado.remito.nro_remito:
                    remitos_filtro.append(remito)

        monto_cierre=0
        for remito in remitos_filtro:
            monto_cierre+=remito.valor_contrareembolso
            sol=remito.solicitud_transporte
            print("sol: ", sol)
            bultos_sol=Bulto.objects.filter(solicitud=sol.id)
            print("bultos: ", bultos_sol)
            for bulto in bultos_sol:
                print("bulto flete: ", bulto.valor_flete)
                monto_cierre+=bulto.valor_flete

        return Response(monto_cierre)

class CambiarEstadoRemito(APIView):

    def put(self, request, nro_remito):

        body=request.data
        estado_nuevo_body=body['estado_nuevo']
        remito=Remito.objects.get(pk=nro_remito)
        fecha_in_estado=date.today()
        tipo_estado_anterior=TipoEstadoRemito.objects.get(pk='en_circulacion')
        print("paso")
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