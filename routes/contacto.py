# Acá van todas las rutas de la aplicación del endpoint contacto

from flask import jsonify, request, Blueprint

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_contacto = Blueprint("bp_contacto", __name__)


# Ruta Contacto
@bp_contacto.route("/contacto", methods=["GET"])
def index():
    return "Estamos en la Sección de Contacto."
# Fin Ruta Contacto

