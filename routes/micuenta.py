# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from flask import jsonify, render_template, request, Blueprint
from forms import LoginForm

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_micuenta = Blueprint("bp_micuenta", __name__)

# Ruta del Login
@bp_micuenta.route("/mi-cuenta/login", methods=["GET", "POST"])
def login():
    # Creo un objeto de tipo formulario que le pasaré al template y
    # que se inicializa con los parámetros recibidos en la vista
    login_form = LoginForm(request.form)
    
    # Diccionario que prepara todo lo que se le enviará al template
    data = {
        "titulo": "Ingrese al Sistema",
        "form": login_form,
    }
    return render_template("login.html", data=data)


# Ruta del formulario de registro
@bp_micuenta.route("/mi-cuenta/register", methods=["GET"])
def register():
    return "Register."


@bp_micuenta.route("/mi-cuenta", methods=["GET"])
def mi_cuenta():
    return "Estamos en Mi Cuenta."


@bp_micuenta.route("/mi-cuenta/reservas", methods=["GET"])
def reservas():
    return "Estamos en Mis Reservas."


@bp_micuenta.route("/mi-cuenta/calificar-habitacion", methods=["GET"])
def calificar_habitacion():
    return "Estamos en Calificar Habitación."


@bp_micuenta.route("/mi-cuenta/logout", methods=["GET"])
def logout():
    return "Cerrar sesión."
