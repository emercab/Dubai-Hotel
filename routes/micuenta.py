# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from datetime import datetime
from flask import flash, redirect, render_template, request, Blueprint, url_for
from forms import LoginForm, RegisterForm
from markupsafe import escape
from flask_bcrypt import Bcrypt
import controllers.controller_micuenta as controller


# Creo el objeto my_bcrypt para crear y comparar los hash de passwords
my_bcrypt = Bcrypt()

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

    # Se verifica que el form haya pasado la validación
    if login_form.validate_on_submit():
        # Capturo las variables ingresadas por el usuario y 
        # por seguridad aplico escape a todo lo ingresado
        username = escape(login_form.username.data)
        password = escape(login_form.password.data)
        
        # Llamo a la función del controller que revisa el login
        result_login = controller.check_login(username, password)
        
        # Reviso la respuesta del login obtenida por el controlador
        if result_login == 0:
            flash("Campo de usuario o contraseña incorrectos.")
        elif result_login == 2:
            flash("Contraseña incorrecta.")
        elif result_login == 1:
            return redirect("/")
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

    # Se verifica que el form haya pasado la validación
    if register_form.validate_on_submit():
        # Capturo las variables ingresadas por el usuario en un diccionario
        # y por seguridad aplico escape a todo lo ingresado, borro espacios
        # en blanco y convierto la primera letra a mayúsculas en nombres y apellidos,
        # También envío los demás valores por defecto
        print("Passed")
        data_user = {
            "nombres": escape(register_form.nombres.data).strip().upper(),
            "apellidos": escape(register_form.apellidos.data).strip().upper(),
            "cedula": escape(register_form.cedula.data).strip(),
            "email": escape(register_form.email.data).strip().lower(),
            "direccion": escape(register_form.direccion.data).strip().capitalize(),
            "ciudad": escape(register_form.ciudad.data).strip().capitalize(),
            "celular": escape(register_form.celular.data).strip(),
            # Creo el hash del password
            "password": my_bcrypt.generate_password_hash(
                escape(register_form.password.data).strip()
            ).decode("utf-8"),
            # Creo el username desde la función del controlador
            # y le mando nombres y apellidos
            "username": controller.crear_username(
                escape(register_form.nombres.data).strip().upper(),
                escape(register_form.apellidos.data).strip().upper(),
            ),
            "tipo_usuario": 3, # Cliente
            "fecha_registro": datetime.today(),
            "activo": True,
        }
        # Llamo a la función del controller que registra al usuario
        result_register = controller.register_user(data_user)
        
        # Reviso la respuesta del controlador para ver si el registro fue exitoso
        if result_register["registro_exitoso"]:
            # Significa que se creó el registro con éxito.
            return redirect("/mi-cuenta/login")
        else:
            flash("Error. " + result_register["error"])
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
    # Llamo a la función del controlador que destruye todas las
    # variables de sesión
    controller.destroy_session()
    return redirect(url_for("index"))
# Fin Ruta de Cerrar Sesión
