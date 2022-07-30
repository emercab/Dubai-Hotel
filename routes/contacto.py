from flask import jsonify, request, Blueprint

bp_contacto = Blueprint("bp_contacto", __name__)


@bp_contacto.route("/contacto", methods=["GET"])
def index():
    return "Estamos en Contacto."
