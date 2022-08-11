from datetime import date, datetime
from admin.models.reserva_modal import create_reserva_admin, select_reserva_admin
from controllers.controller_habitaciones import available_rooms, calcular_total_reserva
from models.model_micuenta import get_data_login


def buscar_cliente_reserva(valor_busqueda):
    usuario = get_data_login(valor_busqueda)
    
    if usuario == None or (usuario != None and len(usuario) <= 0):
        return {}

    diccionario = {}

    if usuario["TipoUsuarioId"] == 3:
        count = 0
        columns = usuario.keys()
        
        for item in usuario:
            if columns[count].lower() == "id" or columns[count].lower() == "nombres" or columns[count].lower() == "apellidos":
                diccionario[columns[count]] = item
            count += 1
    return diccionario
#fin buscar cliente


def guardar_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, id_habitacion, id_habitacion_actual):
    habitacion_seleccionada = id_habitacion_actual

    if id_habitacion and (int(id_habitacion) > 0):
        habitacion_seleccionada = id_habitacion

    total = calcular_total_reserva(fecha_ingreso, fecha_salida, habitacion_seleccionada)
    result = create_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, habitacion_seleccionada, total)

    if result:
        return { 
            "type": "ok",
            "response": result
        }
    
    return { 
        "type": "err",
        "message": "No se pudo crear la reserva."
    }
    

def obtener_habitaciones_reserva(fecha_ingreso, fecha_salida):
    habitaciones = available_rooms(fecha_ingreso, fecha_salida)

    format_habitaciones  = [(0, "Seleccionar una habitación")]

    if habitaciones and len(habitaciones) > 0:
        for habitacion in habitaciones:
            format_habitaciones.append((habitacion["id"], habitacion["NumeroHabitacion"]))

    return format_habitaciones


def validar_fecha_reserva(fecha_hoy, fecha_guardada):
    fecha_db        = datetime.strptime(str(fecha_guardada), '%Y-%m-%d')
    fecha_today     = datetime.strptime(str(fecha_hoy), '%Y-%m-%d')

    if fecha_db < fecha_today:
        return date.strftime(fecha_db, '%Y-%m-%d')
    
    return date.strftime(fecha_today, '%Y-%m-%d')


def consultar_reserva_admin(id_reserva):
    reservas = select_reserva_admin(id_reserva)

    return reservas
