from flask import jsonify, request, Blueprint

bp_admin = Blueprint("bp_admin", __name__, template_folder='./admin/templates')


@bp_admin.route("/admin", methods=["GET"])
def index():
    return "Estamos en el Admin"
