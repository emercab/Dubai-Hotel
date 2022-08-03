from unittest import result
from admin.models.habitacion_model import create_habitacion, remove_habitacion, select_habitacion
import re


def is_number(number):
    if re.findall("\d", number) > 0:
        return True

    return False


def consultar_habitacion(id_habitacion):
    habitaciones = select_habitacion(id_habitacion) #recive un array de tuplas

    print(habitaciones)

    return habitaciones

def guardar_habitacion(id_habitacion, numero, precio):
    #se pueden agregar validaciones aqui. por ahora solo un crud simple

    nuevo_id = create_habitacion(id_habitacion, numero, precio)
    return nuevo_id


def desactivar_habitacion(id_habitacion):
    return remove_habitacion(id_habitacion)

