# Acá van todas las rutas de la aplicación del endpoint habitaciones

from flask import render_template, request, Blueprint
from forms.forms_habitaciones import ReservaForm
import controllers.controller_micuenta as controller_micuenta

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_habitaciones = Blueprint("bp_habitaciones", __name__)


# Ruta Habitaciones
@bp_habitaciones.route("/habitaciones", methods=["GET"])
def habitaciones():
    # Preparo datos a enviar a la vista
    data = controller_micuenta.data_to_template("Habitaciones")
    return render_template("habitaciones.html", data=data)
# Fin Ruta Habitaciones


# Ruta Reservar
@bp_habitaciones.route("/habitaciones/reservar", methods=["GET"])
def reservar():
    reserva_form = ReservaForm(request.form)

    # Preparo datos a enviar a la vista
    data = controller_micuenta.data_to_template("Habitaciones")

    # Agrego el formulario al diccionario de data que se enviará al template
    data["form"] = reserva_form

    return render_template("reserva.html", data=data)
# Fin Ruta Reservar


