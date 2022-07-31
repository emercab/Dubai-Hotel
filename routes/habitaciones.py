# Acá van todas las rutas de la aplicación del endpoint habitaciones
from flask import jsonify, request, Blueprint

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_habitaciones = Blueprint("bp_habitaciones", __name__)


@bp_habitaciones.route("/habitaciones", methods=["GET"])
def habitaciones():
    return "Estamos en Habitaciones."


@bp_habitaciones.route("/habitaciones/reservar", methods=["GET"])
def reservar():
    return "Estamos en Reservar."
    