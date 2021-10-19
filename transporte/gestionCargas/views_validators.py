import re
import datetime

from rest_framework.response import Response
"""Expresiones Regulares"""
patron_id_cliente=re.compile(r"C[0-9]{1,}")
patron_dir=re.compile(r"[A-Za-z]+ [0-9]+")
patron_nombre=re.compile(r"[A-Za-z]+")
patron_id_sol=re.compile(r"S[0-9]{1,}")
patron_legajo=re.compile(r"CH[0-9]{1,}")
patron_remito=re.compile(r"R[0-9]{1,}")
"""Fin ER"""

def validate_crear_solicitud(body, id_cliente, opcion):
    dir_body=body['direccion']
    nombre=body['nombre_2']
    exito=False
    if re.fullmatch(patron_dir, dir_body) and re.fullmatch(patron_id_cliente, id_cliente) \
        and opcion in (0,1) and re.fullmatch(patron_nombre, nombre):
        exito=True
    return exito

def validate_agregar_bultos(body, id_solicitud):
    tipos_validos=('CH', 'M', 'G')
    tipo_bulto=body['tipo']
    exito=False
    if re.fullmatch(patron_id_sol, id_solicitud) and tipo_bulto in tipos_validos:
        exito=True
    return exito


def validate_remitos_chofer_estado(body):
    legajo=body['legajo']
    estado=body['estado']
    estados_validos=['asignado', 'en_circulacion', 'en_viaje', 'rendido', 'segunda_entrega',\
        'pendiente', 'pagado']
    exito=False
    if re.fullmatch(patron_legajo, legajo) and estado in estados_validos:
        exito=True
    return exito

def validate_asociar_sol_remito(body):
    medios_validos=['OR', 'DES', 'CC']
    nro_remito=body['remito']
    id_solicitud=body['sol']
    medio_pago=body['m_pago']
    exito=False
    if re.fullmatch(patron_remito, nro_remito) and re.fullmatch(patron_id_sol, id_solicitud)\
        and medio_pago in medios_validos:
        exito=True
    return exito

def validate_viaje_fecha(fecha):
    format="%Y-%m-%d"
    exito=True
    try:
        datetime.datetime.strptime(fecha, format)
    except ValueError:
        exito=False
    return exito
    
def validate_asoc_remito_viaje(body):
    remitos=body['remitos']
    exito=True
    index=0
    while exito is True and index < len(remitos):
        if re.fullmatch(patron_remito, remitos[index]) is None:
            exito=False
        index+=1
    
    return exito
