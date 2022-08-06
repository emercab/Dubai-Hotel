# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from datetime import datetime
from flask import flash, redirect, render_template, request, Blueprint, url_for
from decorators import login_required, only_clientes
from forms import LoginForm, RegisterForm
from markupsafe import escape
from flask_bcrypt import Bcrypt
import controllers.controller_micuenta as controller

# Menú para admins
# Mostrar errores del form


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

    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Ingrese al Sistema")
    
    # Agrego el formulario al diccionario de data que se enviará al template
    data["form"] = login_form

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
    
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Registro de usuario")
    
    # Agrego el formulario al diccionario de data que se enviará al template
    data["form"] = register_form

    # Se verifica que el form haya pasado la validación
    if register_form.validate_on_submit():
        # Capturo las variables ingresadas por el usuario en un diccionario
        # y por seguridad aplico escape a todo lo ingresado, borro espacios
        # en blanco y convierto a mayúsculas nombres y apellidos.
        # También envío los demás valores por defecto
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
            "activo": 1,
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
@login_required
@only_clientes
def mi_cuenta():
    user_login = False
    nombre = ""
    # Reviso si el usuario ha hecho login para enviar variables de sesión
    if "user_login" in session:
        # Significa que existe una variable de sesión user_login
        # creada cuando el usuario hizo login. Guardo dicha variable
        # en otra variable del mismo nombre que le pasaré al template
        user_login = True
        nombre = controller.get_nombre_corto(session["nombres"])
    
    # Preparo datos a enviar al template
    data = {
        "titulo_head": "Mi Cuenta",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("mi-cuenta.html", data=data)
# Fin de Ruta de Mi Cuenta


# Ruta de Mis Reservas
@bp_micuenta.route("/mi-cuenta/reservas", methods=["GET"])
@login_required
@only_clientes
def reservas():
    user_login = False
    nombre = ""
    # Reviso si el usuario ha hecho login para enviar variables de sesión
    if "user_login" in session:
        # Significa que existe una variable de sesión user_login
        # creada cuando el usuario hizo login. Guardo dicha variable
        # en otra variable del mismo nombre que le pasaré al template
        user_login = True
        nombre = controller.get_nombre_corto(session["nombres"])
    
    # Preparo datos a enviar al template
    data = {
        "titulo_head": "Home",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("mis-reservas.html", data=data)
# Fin Ruta de Mis Reservas


# Ruta Calificar Habitaciones
@bp_micuenta.route("/mi-cuenta/calificar-habitacion", methods=["GET"])
@login_required
@only_clientes
def calificar_habitacion():
    user_login = False
    nombre = ""
    # Reviso si el usuario ha hecho login para enviar variables de sesión
    if "user_login" in session:
        # Significa que existe una variable de sesión user_login
        # creada cuando el usuario hizo login. Guardo dicha variable
        # en otra variable del mismo nombre que le pasaré al template
        user_login = True
        nombre = controller.get_nombre_corto(session["nombres"])
    
    # Preparo datos a enviar al template
    data = {
        "titulo_head": "Home",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("calificar-habitacion.html", data=data)
# Fin Ruta Calificar Habitaciones


# Ruta de Cerrar Sesión
@bp_micuenta.route("/mi-cuenta/logout", methods=["GET"])
@login_required
def logout():
    # Llamo a la función del controlador que destruye todas las
    # variables de sesión
    controller.destroy_session()
    return redirect(url_for("index"))
# Fin Ruta de Cerrar Sesión
