# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from flask import jsonify, render_template, request, Blueprint
from forms import LoginForm, RegisterForm

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
# Fin de la ruta del Login


# Ruta del formulario de registro
@bp_micuenta.route("/mi-cuenta/register", methods=["GET", "POST"])
def register():
    # Creo un objeto de tipo formulario que le pasaré al template y
    # que se inicializa con los parámetros recibidos en la vista
    register_form = RegisterForm(request.form)
    
    # Diccionario que prepara todo lo que se le enviará al template
    data = {
        "titulo": "Ingrese al Sistema",
        "form": register_form,
    }
    return render_template("register.html", data=data)
# Fin de Ruta del formulario de registro


# Ruta de Mi Cuenta
@bp_micuenta.route("/mi-cuenta", methods=["GET"])
def mi_cuenta():
    return "Estamos en Mi Cuenta."
# Fin de Ruta de Mi Cuenta


# Ruta de Mis Reservas
@bp_micuenta.route("/mi-cuenta/reservas", methods=["GET"])
def reservas():
    return "Estamos en Mis Reservas."
# Fin Ruta de Mis Reservas


# Ruta Calificar Habitaciones
@bp_micuenta.route("/mi-cuenta/calificar-habitacion", methods=["GET"])
def calificar_habitacion():
    return "Estamos en Calificar Habitación."
# Fin Ruta Calificar Habitaciones


# Ruta de Cerrar Sesión
@bp_micuenta.route("/mi-cuenta/logout", methods=["GET"])
def logout():
    return "Cerrar sesión."
# Fin Ruta de Cerrar Sesión
