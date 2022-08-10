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
@bp_api.route('/api/calcular-total-reserva', methods=['get'])
def calcular_total_reserva():
    # Recojo los parámetros que recibe este endpoint
    params = request.args
    fecha1 = params["fecha1"]
    fecha2 = params["fecha2"]
    habitacion_id = params["habitacion_id"]
    total = controller_habitaciones.calcular_total_reserva(fecha1, fecha2, habitacion_id)
    return jsonify(total)
