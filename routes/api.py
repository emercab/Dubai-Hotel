from flask import Blueprint, jsonify, request
import controllers.controller_habitaciones as controller_habitaciones

bp_api = Blueprint("bp_api", __name__)


@bp_api.route('/api/clientes', methods=["post"])
def clientes_api():
    #print(request.get_json())
    print(len(request.json) > 0)

    return request.json['input1']


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
