from flask import Blueprint, jsonify, make_response, request, escape
from admin.controllers.reserva_controller import buscar_cliente_reserva
import controllers.controller_habitaciones as controller_habitaciones

bp_api = Blueprint("bp_api", __name__)


@bp_api.route('/api/clientes', methods=["post"])
def get_clientes_api():
    
    if not 'cliente' in request.json:
        return make_response({}, 400)

    valor_busqueda = escape(request.json['cliente']).strip()

    if valor_busqueda == None or valor_busqueda == '':
        return make_response({}, 400)

    resultado = buscar_cliente_reserva(valor_busqueda)

    return make_response(jsonify(resultado), 200)


# Retorna al frontend el precio de la reserva
@bp_api.route('/api/info-reserva', methods=['get', 'post'])
def info_reserva():
    # Recojo los parámetros que recibe este endpoint
    if request.method.lower() == 'get':
        params = request.args
        fecha1 = params["fecha1"]
        fecha2 = params["fecha2"]
        habitacion_id = params["habitacion_id"]
    else:   
        params = request.json
        fecha1 = params["fecha1"]
        fecha2 = params["fecha2"]
        habitacion_id = params["habitacion_id"]

    fecha1 = escape(fecha1)
    fecha2 = escape(fecha2)

    # Obtengo total a pagar y habitaciones disponibles para luego
    # retornarlos como respuesta
    total_a_pagar = controller_habitaciones.calcular_total_reserva(fecha1, fecha2, habitacion_id)
    rooms = controller_habitaciones.available_rooms(fecha1, fecha2)
    if rooms != None:
        # Significa que encontró habitaciones disponibles y armo la lista de
        # diccionarios que llenará el select de habitaciones disponibles en el template
        list_rooms = [{"value": r[0], "info": f"Habitación {r[1]}"} for r in rooms]
    else:
        list_rooms = [{"value": -1, "info": "No hay habitaciones disponibles en esas fechas"}]
    
    # Armo la respuesta
    data_reserva = {
        "total": total_a_pagar,
        "list_rooms": list_rooms
    }
    return jsonify(data_reserva)
