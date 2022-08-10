from unittest import result
from admin.models.habitacion_model import create_habitacion, update_estado_habitacion, select_habitacion
import re


def is_number(number):
    if re.findall("\d", number) > 0:
        return True

    return False


def consultar_habitacion(id_habitacion):
    habitaciones = select_habitacion(id_habitacion) #recive un array de tuplas

    if len(habitaciones) > 0:
        return habitaciones

    return []

def guardar_habitacion(id_habitacion, numero, precio):
    #se pueden agregar validaciones aqui. por ahora solo un crud simple

    nuevo_id = create_habitacion(id_habitacion, numero, precio)
    return nuevo_id


def desactivar_habitacion(id_habitacion, estado):
    
    return update_estado_habitacion(id_habitacion, estado)

def ver_precio_habitacion():
    habitaciones = select_habitacion() 
    precio_habitacion = None

    if habitaciones and len(habitaciones) > 0:
        precio_habitacion = habitaciones[0]["Precio"]
    return precio_habitacion
    