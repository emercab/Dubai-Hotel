from flask import Blueprint, jsonify, make_response, request, escape
from admin.controllers.reserva_controller import buscar_cliente_reserva

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
