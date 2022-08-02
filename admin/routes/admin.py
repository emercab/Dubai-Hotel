from flask import jsonify, request, Blueprint
from decorators import admin_required

bp_admin = Blueprint("bp_admin", __name__, template_folder='./admin/templates')


@bp_admin.route("/admin", methods=["GET"])
@admin_required
def admin():
    
    return "Estamos en el Admin"
