from flask import jsonify, request, Blueprint

bp_habitaciones = Blueprint("bp_habitaciones", __name__)


@bp_habitaciones.route("/habitaciones", methods=["GET"])
def habitaciones():
    return "Estamos en Habitaciones."


@bp_habitaciones.route("/habitaciones/reservar", methods=["GET"])
def reservar():
    return "Estamos en Reservar."
    