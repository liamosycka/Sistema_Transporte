from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from .models import EstadoRemito, Localidad, Cliente, SolicitudTransporte, Remito, Chofer, TipoEstadoRemito, Viaje
from .models import Bulto
import json

def setUpAltaSolicitud(self):
    Localidad.objects.create(nombre="Prueba", codigo_postal="100")
    Localidad.objects.create(nombre="Prueba2", codigo_postal="101")
    localidad = Localidad.objects.get(pk="100")
    Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
                           localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest",
                           tipo_cliente="P")
    cliente = Cliente.objects.get(pk="C1")
    SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test", direccion_origen="Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
                                       cliente=cliente, localidad_destino=localidad)
    solicitud = SolicitudTransporte.objects.get(pk="S1")
    
def setUpAsociarSolRemito(self):
    Localidad.objects.create(nombre="Prueba", codigo_postal="100")
    localidad = Localidad.objects.get(pk="100")
    Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
                           localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest",
                           tipo_cliente="P")
    cliente = Cliente.objects.get(pk="C1")
    SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test", direccion_origen="Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
                                       cliente=cliente, localidad_destino=localidad)
    Chofer.objects.create(legajo="CH1", nombre="Test", apellido="Test", dni="40000000", fecha_nac="1980-10-10",
                          fecha_ingreso="2018-10-10")
    chofer = Chofer.objects.get(pk="CH1")
    Remito.objects.create(
        nro_remito="R0001", legajo_chofer=chofer, fecha_asignacion="2020-10-10")
    remito = Remito.objects.get(pk="R0001")
    TipoEstadoRemito.objects.create(tipo_estado='asignado')
    TipoEstadoRemito.objects.create(tipo_estado='en_circulacion')
    tipoEstado = TipoEstadoRemito.objects.get(tipo_estado='asignado')
    EstadoRemito.objects.create(
        fecha_inicio="2021-11-20", tipo_estado=tipoEstado, actual=True, remito=remito)

def setUpAsociarRemitosViaje(self):
    Chofer.objects.create(legajo="CH1", nombre="Test", apellido="Test", dni="40000000", fecha_nac="1980-10-10",
                          fecha_ingreso="2018-10-10")
    chofer = Chofer.objects.get(pk="CH1")
    Localidad.objects.create(nombre="Prueba", codigo_postal="100")
    localidad = Localidad.objects.get(pk="100")
    viaje = Viaje.objects.create(
        fecha_salida="2020-11-10", fecha_confeccion="2020-11-05", legajo_chofer=chofer)
    viaje.localidades.add(localidad)
    Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
                           localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest",
                           tipo_cliente="P")
    cliente = Cliente.objects.get(pk="C1")
    SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test", direccion_origen="Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
                                       cliente=cliente, localidad_destino=localidad)
    solicitud = SolicitudTransporte.objects.get(pk="S1")
    Remito.objects.create(
        nro_remito="R0001", legajo_chofer=chofer, fecha_asignacion="2020-10-10",
        solicitud_transporte=solicitud)
    remito = Remito.objects.get(pk="R0001")
    TipoEstadoRemito.objects.create(tipo_estado='en_circulacion')
    tipoEstado = TipoEstadoRemito.objects.get(tipo_estado='en_circulacion')
    TipoEstadoRemito.objects.create(tipo_estado='en_viaje')
    EstadoRemito.objects.create(
        fecha_inicio="2021-11-20", tipo_estado=tipoEstado, actual=True, remito=remito)

def setUpCierreViaje(self):
    Chofer.objects.create(legajo="CH1", nombre="Test", apellido="Test", dni="40000000", fecha_nac="1980-10-10",
                          fecha_ingreso="2018-10-10")
    chofer = Chofer.objects.get(pk="CH1")
    Localidad.objects.create(nombre="Prueba", codigo_postal="100")
    localidad = Localidad.objects.get(pk="100")
    viaje = Viaje.objects.create(
        fecha_salida="2020-11-10", fecha_confeccion="2020-11-05", legajo_chofer=chofer)
    viaje.localidades.add(localidad)
    Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
                           localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest",
                           tipo_cliente="P")
    cliente = Cliente.objects.get(pk="C1")
    SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test", direccion_origen="Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
                                       cliente=cliente, localidad_destino=localidad)
    solicitud = SolicitudTransporte.objects.get(pk="S1")
    Bulto.objects.create(peso=5, tipo='CH', descripcion='Caja', valor_flete=500,solicitud=solicitud)
    Bulto.objects.create(peso=5, tipo='CH', descripcion='Caja', valor_flete=500,solicitud=solicitud)
    Bulto.objects.create(peso=5, tipo='CH', descripcion='Caja', valor_flete=500,solicitud=solicitud)
    Bulto.objects.create(peso=5, tipo='CH', descripcion='Caja', valor_flete=500,solicitud=solicitud)
    
    Remito.objects.create(
        nro_remito="R0001", legajo_chofer=chofer, fecha_asignacion="2020-10-10",
        solicitud_transporte=solicitud, valor_flete=0, valor_contrareembolso=2000)
    remito = Remito.objects.get(pk="R0001")
    TipoEstadoRemito.objects.create(tipo_estado='pagado')
    tipoEstado = TipoEstadoRemito.objects.get(tipo_estado='pagado')
    EstadoRemito.objects.create(
        fecha_inicio="2021-11-20", tipo_estado=tipoEstado, actual=True, remito=remito)
    viaje.remitos.add(remito)

class AltaSolicitud(TestCase):
    def test_camino1(self):
        # camino de exito
        setUpAltaSolicitud(self)
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        data_sol = {"idCliente": "C1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": "100",
                    "nombre_2": "Nombre"}
        ruta_post_sol = "http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(
            **data_sol)
        response = self.client.post(ruta_post_sol, data_sol)
        solicitud_creada = SolicitudTransporte.objects.get(pk="S1")
        data_bulto = {"peso": 20, "tipo": 'M', "descripcion": "test descrip",
                      "valor_flete": 100, "solicitud": solicitud_creada}
        ruta_post_bul = f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        response = self.client.post(ruta_post_bul, data_bulto)

        assert response.status_code == 201

    def test_camino2(self):
        # falla porque no hay ninguna localidad cargada
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        #print("camino2: ",response.data)
        assert response.status_code == 200
        self.assertEqual(response.content, b'[]')

    def test_camino3(self):
        # Falla con datos de solicitud inválidos
        # el id cliente y la localidad las chequea bien, hay que revisar la opcion (permite ingresar otra cosa
        # que no sea 0 o 1)
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        localidad = response.data[0]['codigo_postal']
        data_sol = {"idCliente": "CC1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": localidad,
                    "nombre_2": "Nombre"}
        ruta_post_sol = "http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(
            **data_sol)
        response = self.client.post(ruta_post_sol, data_sol)
        assert response.status_code == 400

    def test_camino4(self):
        setUpAltaSolicitud(self)
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        localidad = response.data[0]['codigo_postal']
        data_sol = {"idCliente": "C1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": localidad,
                    "nombre_2": "Nombre"}
        ruta_post_sol = "http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(
            **data_sol)
        response = self.client.post(ruta_post_sol, data_sol)
        solicitud_creada = SolicitudTransporte.objects.get(pk="S1")
        data_bulto = {"peso": 20, "tipo": 'LL', "descripcion": "test descrip",
                      "valor_flete": 100, "solicitud": solicitud_creada}
        ruta_post_bul = f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        response = self.client.post(ruta_post_bul, data_bulto)
        assert response.status_code == 400

    def test_camino5(self):
        # falla cuando se envia un segundo bulto con datos erróneos
        setUpAltaSolicitud(self)
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        localidad = response.data[0]['codigo_postal']
        data_sol = {"idCliente": "C1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": localidad,
                    "nombre_2": "Nombre"}
        ruta_post_sol = "http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(
            **data_sol)
        response = self.client.post(ruta_post_sol, data_sol)
        solicitud_creada = SolicitudTransporte.objects.get(pk="S1")
        data_bulto = {"peso": 20, "tipo": 'M', "descripcion": "test descrip",
                      "valor_flete": 100, "solicitud": solicitud_creada}
        ruta_post_bul = f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        self.client.post(ruta_post_bul, data_bulto)
        data_bulto2 = {"peso": 20, "tipo": 'L', "descripcion": "test descrip",
                       "valor_flete": 100, "solicitud": solicitud_creada}
        ruta_post_bul = f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        response = self.client.post(ruta_post_bul, data_bulto2)
        assert response.status_code == 400


class AsociarSolicitudRemito(TestCase):
    def test_camino1(self):
        # camino de exito
        setUpAsociarSolRemito(self)
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/solicitudes/S1/")
        solicitud = response.data
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/remitos/chofer-estado/CH1/asignado/")
        remito = response.data[0]
        datos_asoc = {"remito": remito,
                "sol": solicitud['id'], "m_pago": "DES", "contra": 150}
        response = self.client.put(
            "http://127.0.0.1:8000/gestionCargas/remitos/asoc-sol-remito/", json.dumps(datos_asoc), content_type="application/json")
        assert response.status_code == 202

    def test_camino2(self):
        # falla cuando no hay ninguna solicitud
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/solicitudes/29/")
        assert response.status_code == 404

    def test_camino3(self):
        setUpAsociarSolRemito(self)
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/solicitudes/S1/")
        solicitud = response.data
        # EstadoRemito.objects.get(id=1).delete()
        # es extraño... porq no puedo acceder al ID 1 pero si al 2..
        EstadoRemito.objects.all().delete()
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/remitos/chofer-estado/CH1/asignado/")
        self.assertEqual(response.content, b'[]')

    def test_camino4(self):
        setUpAsociarSolRemito(self)
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/solicitudes/S1/")
        solicitud = response.data
        response = self.client.get(
            "http://127.0.0.1:8000/gestionCargas/remitos/chofer-estado/CH1/asignado/")
        remito = response.data[0]
        datos_asoc = {"remito": remito,
                "sol": solicitud['id'], "m_pago": "EEE", "contra": 150}
        response = self.client.put(
            "http://127.0.0.1:8000/gestionCargas/remitos/asoc-sol-remito/",  json.dumps(datos_asoc), content_type="application/json")
        assert response.status_code == 400


class AsociarRemitosAViaje(TestCase):
    
    def test_camino1(self):
        setUpAsociarRemitosViaje(self)
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        id_viaje=response.data[0]['id']
        response=self.client.get(f"http://127.0.0.1:8000/gestionCargas/remitos/viaje/{id_viaje}/")
        remitos={'remitos':response.data}
        response=self.client.put(f"http://127.0.0.1:8000/gestionCargas/viajes/asoc-remitos-viaje/{id_viaje}/",json.dumps(remitos), content_type="application/json")
        #print("Response: ",response.data)
        self.assertNotEqual(response.content, b'[]')

    def test_camino2(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-14-10/")
        assert response.status_code==400

    def test_camino3(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        response=self.client.get(f"http://127.0.0.1:8000/gestionCargas/remitos/viaje/A/")
        assert response.status_code==404

    def test_camino4(self):
        setUpAsociarRemitosViaje(self)
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        id_viaje=response.data[0]['id']
        response=self.client.get(f"http://127.0.0.1:8000/gestionCargas/remitos/viaje/{id_viaje}/")
        remitos={'remitos':['REM0001']}
        response=self.client.put(f"http://127.0.0.1:8000/gestionCargas/viajes/asoc-remitos-viaje/{id_viaje}/",json.dumps(remitos), content_type="application/json")
        assert response.status_code==400

class CierreViaje(TestCase):
    def test_camino1(self):
        setUpCierreViaje(self)
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        id_viaje=response.data[0]['id']
        response=self.client.get(f"http://127.0.0.1:8000/gestionCargas/viajes/cierre/{id_viaje}/")
        print("Valor Cierre: ",response.data)
        self.assertNotEqual(response.content, b'[]')

    def test_camino2(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-13-10/")
        assert response.status_code==400

    def test_camino3(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        response=self.client.get(f"http://127.0.0.1:8000/gestionCargas/remitos/viaje/A/")
        assert response.status_code==404
        

"""
class AltaSolicitud_Camino1(TestCase):
    #Camino de exito
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        Localidad.objects.create(nombre="Prueba2", codigo_postal="101")
        localidad=Localidad.objects.get(pk="100")
        Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
        localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest", 
        tipo_cliente="P")
        cliente=Cliente.objects.get(pk="C1")
        SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test",direccion_origen=
        "Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
        cliente=cliente, localidad_destino=localidad)
        solicitud=SolicitudTransporte.objects.get(pk="S1")
        
    def test_getLocalidades(self):
        #test get localidades
        response = self.client.get('http://127.0.0.1:8000/gestionCargas/localidades/')
        #print("content", response.content)
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')
    
    def test_post_solicitud(self):
        #test post nueva solicitud (datos validos)
        data_sol={"idCliente":"C1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": "100",
        "nombre_2": "Nombre"}
        ruta_post_sol="http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(**data_sol)
        #print("ruta: ",ruta_post_sol)
        response=self.client.post(ruta_post_sol, data_sol)
        #print("respuesta post: ", response.content.decode())
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')
        solicitud_creada=SolicitudTransporte.objects.get(pk="S1")
        #print("Sol creada: ", solicitud_creada)
    
    def test_post_bulto(self):
        solicitud=SolicitudTransporte.objects.get(pk="S1")
        data_bulto={"peso":20, "tipo": 'M', "descripcion": "test descrip", "valor_flete":100, "solicitud":solicitud}
        ruta_post_bul=f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        response=self.client.post(ruta_post_bul, data_bulto)
        assert response.status_code == 201
"""
"""
class AltaSolicitud_Camino2(TestCase):
    #Falla porque no hay ninguna localidad cargada en el sistema
    def test_get_localidades(self):
        response = self.client.get('http://127.0.0.1:8000/gestionCargas/localidades/')
        assert response.status_code == 200
        self.assertEqual(response.content, b'[]')
"""

"""
class AltaSolicitud_Camino3(TestCase):
    # Falla con datos de solicitud inválidos
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")

    def test_get_localidades(self):
        response = self.client.get(
            'http://127.0.0.1:8000/gestionCargas/localidades/')
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')

    def test_post_solicitud(self):
        # test post nueva solicitud (datos validos)
        # el id cliente y la localidad las chequea bien, hay que revisar la opcion (permite ingresar otra cosa
        # que no sea 0 o 1)
        data_sol = {"idCliente": "C1", "opcion_dest_remit": 5, "direccion": "Calle 200", "localidad": "100",
                    "nombre_2": "Nombre"}
        ruta_post_sol = "http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(
            **data_sol)
        response = self.client.post(ruta_post_sol, data_sol)
        assert response.status_code == 400
"""

"""
class AltaSolicitud_Camino4(TestCase):
    #Falla con datos de bultos inválidos
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        localidad=Localidad.objects.get(pk="100")
        Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
        localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest", 
        tipo_cliente="P")
        cliente=Cliente.objects.get(pk="C1")
        SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test",direccion_origen=
        "Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
        cliente=cliente, localidad_destino=localidad)

    def test_post_solicitud(self):
        data_sol={"idCliente":"C1", "opcion_dest_remit": 0, "direccion": "Calle 200", "localidad": "100",
        "nombre_2": "Nombre"}
        ruta_post_sol="http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(**data_sol)
        response=self.client.post(ruta_post_sol, data_sol)
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')

    def test_post_bulto(self):
        solicitud=SolicitudTransporte.objects.get(pk="S1")
        data_bulto={"peso":20, "tipo": 'Error', "descripcion": "test descrip", "valor_flete":100, "solicitud":solicitud}
        ruta_post_bul=f"http://127.0.0.1:8000/gestionCargas/solicitudes/bultos/S1/"
        response=self.client.post(ruta_post_bul, data_bulto)
        assert response.status_code == 400
"""
"""
class AsociarSolicitudRemito_Camino1(TestCase):
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        localidad=Localidad.objects.get(pk="100")
        Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
        localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest", 
        tipo_cliente="P")
        cliente=Cliente.objects.get(pk="C1")
        SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test",direccion_origen=
        "Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
        cliente=cliente, localidad_destino=localidad)
        Chofer.objects.create(legajo="CH1", nombre="Test", apellido="Test", dni="40000000", fecha_nac="1980-10-10",
        fecha_ingreso="2018-10-10")
        chofer=Chofer.objects.get(pk="CH1")
        Remito.objects.create(nro_remito="R0001", legajo_chofer=chofer, fecha_asignacion="2020-10-10")

    def test_get_solicitud(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/solicitudes/S1/")
        assert response.status_code == 200
        #self.assertNotEqual(response.content, b'[]')
    #Este test falla
    def test_get_remitos_chofer_estado(self):
        data_chofer_estado={"legajo":"CH1", "estado":"asignado"}
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/remitos/chofer-estado/", data_chofer_estado)
        assert response.status_code == 200
        self.assertEqual(response.content, b'[]')

    def test_put_asociar_sol_remito(self):
        data={"remito":"R0001", "sol":"S1", "m_pago":"DES", "contra":150}
        response=self.client.put("http://127.0.0.1:8000/gestionCargas/remitos/asoc-sol-remito", data)
        assert response.status_code == 202
"""
"""
class AsociarSolicitudRemito_Camino2(TestCase):
    def test_get_solicitud(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/solicitudes/29/")
        assert response.status_code == 404
"""
"""
class AsociarSolicitudRemito_Camino3(TestCase):
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        localidad=Localidad.objects.get(pk="100")
        Cliente.objects.create(id="C1", nombre="NombreTest", apellido="ApellidoTest",
        localidad=localidad, direccion="DirTest", email="emailTest", telefono="telTest", 
        tipo_cliente="P")
        cliente=Cliente.objects.get(pk="C1")
        SolicitudTransporte.objects.create(id="S1", fecha="2021-10-10", remitente="Test",direccion_origen=
        "Calle 30", localidad_origen=localidad, destinatario="Test", direccion_destinatario="Calle 20",
        cliente=cliente, localidad_destino=localidad)

    def test_get_solicitud(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/solicitudes/S1/")
        assert response.status_code == 200
"""
"""
class AsociarSolicitudRemito_Camino4(TestCase):
    def test_put_asociar_sol_remito(self):
        data={"remito":"AA", "sol":"S1", "m_pago":"DES", "contra":150}
        response=self.client.put("http://127.0.0.1:8000/gestionCargas/remitos/asoc-sol-remito", data)
        assert response.status_code == 202
"""
"""
class AsociarRemitosAViaje_Camino1(TestCase):
    def setUp(self):
        Chofer.objects.create(legajo="CH1", nombre="Test", apellido="Test", dni="40000000", fecha_nac="1980-10-10",
        fecha_ingreso="2018-10-10")
        chofer=Chofer.objects.get(pk="CH1")
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
        localidad=Localidad.objects.get(pk="100")
        #conjunto=[]
        #conjunto.append(localidad)
        #conjunto.append(localidad)
        viaje=Viaje.objects.create(fecha_salida="2020-11-10", fecha_confeccion="2020-11-05", legajo_chofer=chofer)
        viaje.localidades.add(localidad)

    def test_get_viajes_fecha(self):
        response=self.client.get("http://127.0.0.1:8000/gestionCargas/viajes/2020-11-10/")
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')

"""
