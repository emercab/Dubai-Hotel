from flask import jsonify, request, Blueprint
from admin.decorators import hola_decorator

bp_admin = Blueprint("bp_admin", __name__, template_folder='./admin/templates')


@bp_admin.route("/admin", methods=["GET"])
@hola_decorator
def admin():
    
    return "Estamos en el Admin"
