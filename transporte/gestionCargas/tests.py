from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from .models import Localidad, Cliente, SolicitudTransporte, Remito, Chofer, Viaje

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

class AltaSolicitud_Camino3(TestCase):
    #Falla con datos de solicitud inválidos
    def setUp(self):
        Localidad.objects.create(nombre="Prueba", codigo_postal="100")
    
    def test_get_localidades(self):
        response = self.client.get('http://127.0.0.1:8000/gestionCargas/localidades/')
        assert response.status_code == 200
        self.assertNotEqual(response.content, b'[]')
    
    def test_post_solicitud(self):
        #test post nueva solicitud (datos validos)
        # el id cliente y la localidad las chequea bien, hay que revisar la opcion (permite ingresar otra cosa 
        # que no sea 0 o 1)
        data_sol={"idCliente":"C1", "opcion_dest_remit": 5, "direccion": "Calle 200", "localidad": "100",
        "nombre_2": "Nombre"}
        ruta_post_sol="http://127.0.0.1:8000/gestionCargas/solicitudes/alta/{idCliente}/{opcion_dest_remit}/".format(**data_sol)
        response=self.client.post(ruta_post_sol, data_sol)
        assert response.status_code == 400

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