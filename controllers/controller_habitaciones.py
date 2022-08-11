# Acá van todas las clases y métodos que controlarán y harán la lógica
# de las operaciones sobre las rutas de Habitaciones. Desde acá se enviará las
# respuestas a las rutas

from datetime import datetime
import models.model_habitaciones as model
import controllers.controller_micuenta as controller_micuenta
from flask import session


def available_rooms(fecha_inicio:datetime, fecha_final:datetime):
    result = model.get_rooms(fecha_inicio, fecha_final)
    if result == None:
        return {}
    else:
        return result
# Fin de get_available_rooms()


def total_reserva(fecha_inicial:datetime, fecha_final:datetime, precio:int):
    # Calcula y retorna el total de la reserva
    return (fecha_final - fecha_inicial).days * precio
# Fin de total_reserva


def calcular_total_reserva(fecha_inicial:str, fecha_final:str, habitacion_id:int):
    # Calcula el total de reserva a partir de las fechas y la id de la habitacion
    # Esta funcion es llamada por la api
    precio = model.get_precio(habitacion_id)
    if precio != None:
        # Significa que obtuvo elprecio dela habitación con éxito y calcula
        #  el total a pagar de la reserva
        total = total_reserva(
            datetime.strptime(fecha_inicial, "%Y-%m-%d"),
            datetime.strptime(fecha_final, "%Y-%m-%d"),
            precio[0]
        )
        return total
    else:
        return 0
# Fin de calcular_total_reserva()


def reservar(data):
    # Registra la reserva en la DB y en caso de que el cliente no esté
    # registrado, lo registra.

    # Inicializo los valores que retornaré
    respuesta = {
        "reserva_exitosa": False,
        "error": "",
    }

    # Calculo el total a pagar de la reserva
    precio = model.get_precio(data["habitacion"])
    if precio != None:
        total = total_reserva(data["fecha_inicio"], data["fecha_final"], precio[0])
        data["total"] = total
    else:
        total = 0 # No se pudo calcular
        respuesta["error"] = "No se pudo calcular el total de la reserva."
        return respuesta
    
    # Preparo los datos a guardar de la reserva
    data_reserva = {
        "habitacion": data["habitacion"],
        "fecha_inicio": data["fecha_inicio"],
        "fecha_final": data["fecha_final"],
        "total": total,
    }

    # Determino si el cliente hizo login
    if not "user_login" in session:
        # Significa que el cliente no se ha logueado y reviso si
        # ya está registrado buscando su cédula en la DB
        if model.get_cliente_id(data["cedula"]) == None:
            # Significa que el cliente no está registrado y procedo a hacerlo
        
            # Agrego el username a los datos que se van a registrar
            data["username"] = controller_micuenta.crear_username(
                data["nombres"], data["apellidos"]
            )
            # Registro al cliente
            result_register = controller_micuenta.register_user(data)
            if not result_register["registro_exitoso"]:
                # Significa que no se guardó al usuario correctamente, entonces
                # se termina el proceso y se muestra el mensaje de error recibido
                respuesta["error"] = result_register["error"]
                return respuesta
        
        # Significa que el cliente está registrado pero no hizo login
    
    # Significa que el cliente está logueado    
    # Busco el id del cliente y lo agrego a los datos de la reserva
    cliente_id = model.get_cliente_id(data["cedula"])
    if cliente_id == None:
        respuesta["error":] = "No se pudo obtener la id del cliente."
        return respuesta
    data_reserva["cliente_id"] = cliente_id[0]
    
    # Mando los datos de la reserva al modelo para que los guarde
    respuesta["reserva_exitosa"] = model.save_reserva(data_reserva)
    if not respuesta["reserva_exitosa"]:
        respuesta["error"] = "No se pudo guardar la reserva."
    return respuesta
