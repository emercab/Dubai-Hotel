from admin.models.reserva_modal import create_reserva_admin, select_reserva_admin
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


def guardar_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, id_habitacion):
    total = 0#calcular_total()

    result = create_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, id_habitacion, total)

    if result:
        return { 
            "type": "ok",
            "response": result
        }
    
    return { 
        "type": "err",
        "message": "No se pudo crear la reserva."
    }
    

def consultar_reserva_admin(id_reserva):
    reservas = select_reserva_admin(id_reserva)

    return reservas
