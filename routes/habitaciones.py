# Acá van todas las rutas de la aplicación del endpoint habitaciones

from flask import render_template, request, Blueprint, redirect, flash
from forms.forms_habitaciones import ReservaForm
from flask_bcrypt import Bcrypt
import controllers.controller_habitaciones as controller
import controllers.controller_micuenta as controller_micuenta
from datetime import datetime, timedelta
from markupsafe import escape

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_habitaciones = Blueprint("bp_habitaciones", __name__)

my_bcrypt = Bcrypt()


# Ruta Habitaciones
@bp_habitaciones.route("/habitaciones", methods=["GET"])
def habitaciones():
    # Preparo datos a enviar a la vista
    data = controller_micuenta.data_to_template("Habitaciones")
    return render_template("habitaciones.html", data=data)
# Fin Ruta Habitaciones


# Ruta Reservar
@bp_habitaciones.route("/habitaciones/reservar", methods=["GET", "POST"])
def reservar():
    # Inicializo el form y le paso las habitaciones al select
    reserva_form = ReservaForm(request.form)

    # Obtengo las habitaciones disponibles por defecto entre hoy y una semana más
    if request.method.lower() == 'get':    
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        tomorrow = datetime.strftime(datetime.today() + timedelta(days=1), "%Y-%m-%d")
        reserva_form.fecha_inicio.render_kw["min"] = today
        reserva_form.fecha_final.render_kw["min"] = tomorrow
    else:
        today = reserva_form.fecha_inicio.data
        tomorrow = reserva_form.fecha_final.data
    rooms = controller.available_rooms(today, tomorrow)
    
    print(today, tomorrow)
    #Valido que haya habitaciones
    if len(rooms) > 0:
        options = [(r[0], f"Habitación {r[1]}") for r in rooms]
    else:
        options = (-1, "No hay habitaciones disponibles")
    reserva_form.list_habitaciones.choices = options

    # Preparo datos a enviar a la vista
    data = controller_micuenta.data_to_template("Habitaciones")

    # Agrego el formulario al diccionario de data que se enviará al template
    data["form"] = reserva_form
    data["today"] = today
    data["tomorrow"] = tomorrow

    # Se verifica que el form haya pasado la validación
    if reserva_form.validate_on_submit():
        # Capturo info ingresada por el usuario en un diccionario
        # y por seguridad aplico escape a todo lo ingresado, borro espacios
        # en blanco y convierto a mayúsculas nombres y apellidos.
        data_reserva = {
            "nombres": escape(reserva_form.nombres.data).strip().upper(),
            "apellidos": escape(reserva_form.apellidos.data).strip().upper(),
            "cedula": escape(reserva_form.cedula.data).strip(),
            "email": escape(reserva_form.email.data).strip().lower(),
            "direccion": escape(reserva_form.direccion.data).strip().capitalize(),
            "ciudad": escape(reserva_form.ciudad.data).strip().capitalize(),
            "celular": escape(reserva_form.celular.data).strip(),
            # Creo el hash del password a partir de la cédula
            "password": my_bcrypt.generate_password_hash(
                escape(reserva_form.cedula.data).strip()
            ).decode("utf-8"),
            "tipo_usuario": 3, # Cliente
            "fecha_registro": datetime.today(),
            "activo": 1,
            "fecha_inicio": datetime.strptime(
                escape(reserva_form.fecha_inicio.data), "%Y-%m-%d"
            ),
            "fecha_final": datetime.strptime( 
                escape(reserva_form.fecha_final.data), "%Y-%m-%d"
            ),
            "habitacion": reserva_form.list_habitaciones.data,
        }
        # Llamo a la función del controller que hace la reserva y 
        # registra al usuario en caso de no estarlo
        result_reserva = controller.reservar(data_reserva)
        
        # Reviso la respuesta del controlador para ver si la eserva fue exitosa
        if result_reserva["reserva_exitosa"]:
            # Significa que se creó el registro con éxito.
            return redirect("/mi-cuenta/reservas")
        else:
            flash("Error. " + result_reserva["error"])

    return render_template("reserva.html", data=data)
# Fin Ruta Reservar


