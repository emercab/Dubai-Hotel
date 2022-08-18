# Acá van todas las rutas de la aplicación del endpoint mi-cuenta

from datetime import datetime
from flask import flash, redirect, render_template, request, Blueprint, url_for, session
from decorators import login_required, only_clientes
from forms.forms_micuenta import LoginForm, RegisterForm, ChangePassword,NuevaCalificacion
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
        username = escape(login_form.username.data).strip()
        password = escape(login_form.password.data).strip()
        
        # Llamo a la función del controller que revisa el login
        result_login = controller.check_login(username, password)
        
        # Reviso la respuesta del login obtenida por el controlador
        if result_login == 0:
            flash("Campo de usuario o contraseña incorrectos.")
        elif result_login == 2:
            flash("Contraseña incorrecta.")
        elif result_login == 1:
            if "tipo_usuario" in session and (session["tipo_usuario"] == 1 or session["tipo_usuario"] == 2):
                    return redirect('/admin')
            else:
                return redirect("/mi-cuenta")
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


# Ruta de Cambiar Contraseña
@bp_micuenta.route("/mi-cuenta/cambiar-password", methods=["GET", "POST"])
@login_required
def cambiar_password():
    change_password_form = ChangePassword(request.form)
    
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Cambiar Contraseña")
    data["form"] = change_password_form

    # Se verifica que el form haya pasado la validación
    if change_password_form.validate_on_submit():
        # Capturo las variables ingresadas por el usuario y 
        # por seguridad aplico escape a todo lo ingresado
        password = escape(change_password_form.password.data).strip()
        new_password = escape(change_password_form.new_password.data).strip()
        
        # Llamo a la función del controller que realiza el cambio de password
        result = controller.change_password(data["cedula"], password, new_password)
        
        # Reviso la respuesta obtenida por el controlador
        if not result["exito"]:
            flash(f"Error. {result['error']}")
        else:
            # Significa que se hizo el cambio de clave con éxito
            return redirect("/mi-cuenta")

    return render_template("cambiar-password.html", data=data)
# Fin Ruta Cambiar Contraseña


# Ruta de Mi Cuenta
@bp_micuenta.route("/mi-cuenta", methods=["GET"])
@login_required
@only_clientes
def mi_cuenta():
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Mi Cuenta")
    return render_template("mi-cuenta.html", data=data)
# Fin de Ruta de Mi Cuenta


# Ruta de Mis Reservas
@bp_micuenta.route("/mi-cuenta/reservas", methods=["GET"])
@login_required
@only_clientes
def reservas():
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Mis Reservas")
    userId = data["id"]
    misReservas= controller.consulta_miReserva(userId)
    data["mis_reservas"] = misReservas
    return render_template("mis-reservas.html", data=data)
# Fin Ruta de Mis Reservas


# Ruta Calificar Habitaciones
@bp_micuenta.route("/mi-cuenta/calificar-habitacion", methods=["GET"])
@login_required
@only_clientes
def calificar_habitacion():
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Calificar Habitaciones")
    comentarios=controller.comentarios(data["id"],None)
    data["comentarios"]=comentarios
    return render_template("calificar-habitacion.html", data=data)
# Fin Ruta Calificar Habitaciones


# Ruta Nueva Calificacion
@bp_micuenta.route("/mi-cuenta/calificar-habitacion/nueva-calificacion", methods=["get","post"])
@bp_micuenta.route("/mi-cuenta/calificar-habitacion/nueva-calificacion/<id_calificacion>", methods=["get","post"])
@login_required
@only_clientes
def nueva_calificacion(id_calificacion=None):
    # Preparo datos a enviar a la vista
    calificar_form = NuevaCalificacion(request.form)
    
    data = controller.data_to_template("Calificar Habitaciones")
    data["form"] = calificar_form
    comentarios=controller.comentarios(data["id"],id_calificacion)
    data["comentarios"]=comentarios
    if calificar_form.validate_on_submit():
        # Capturo las variables ingresadas por el usuario y 
        # por seguridad aplico escape a todo lo ingresado
        reservaId = comentarios[0]
        comentario = escape(calificar_form.comentario.data)
        calificacion = escape(calificar_form.calificacion.data)
        comentarioId = comentarios[3]
        habitacionId = comentarios[1]      

        # Llamo a la función del controller que realiza el cambio de password
        result = controller.create_comment(
            reservaId, comentario, calificacion, comentarioId, habitacionId
        )
        # Reviso la respuesta obtenida por el controlador
        if result:
            return redirect("/mi-cuenta/calificar-habitacion")
            
        else:
            # Significa que se hizo el cambio de clave con éxito
            flash(f"Error. {result}")
    return render_template("nueva-calificacion.html", data=data)
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
