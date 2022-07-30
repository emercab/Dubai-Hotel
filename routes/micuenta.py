from flask import jsonify, request, Blueprint

bp_micuenta = Blueprint("bp_micuenta", __name__)


@bp_micuenta.route("/mi-cuenta", methods=["GET"])
def index():
    return "Estamos en Mi Cuenta."
    