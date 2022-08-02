# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from flask import flash, render_template, request, Blueprint
from forms import LoginForm, RegisterForm
import controllers.controller_micuenta as controller

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_micuenta = Blueprint("bp_micuenta", __name__)


# Ruta del Login
@bp_micuenta.route("/mi-cuenta/login", methods=["GET", "POST"])
def login():
    # Creo un objeto de tipo formulario que le pasaré al template y
    # que se inicializa con los parámetros recibidos en la vista
    login_form = LoginForm(request.form)
    
    data = {
        "titulo": "Ingrese al Sistema",
        "form": login_form,
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        result_login = controller.check_login(username, password)
        print(f"Login: {result_login}")
        if result_login == 0:
            flash("Campo de usuario o contraseña incorrectos.")
        elif result_login == 2:
            flash("Contraseña incorrecta.")
        elif result_login == 1:
            flash("Login correcto.")
        # Diccionario que prepara todo lo que se le enviará al template
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
