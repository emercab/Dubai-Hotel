# Acá van todas las rutas de la aplicación del endpoint habitaciones

from dataclasses import dataclass
from flask import jsonify, render_template, request, Blueprint, session
import controllers.controller_micuenta as controller

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_habitaciones = Blueprint("bp_habitaciones", __name__)


# Ruta Habitaciones
@bp_habitaciones.route("/habitaciones", methods=["GET"])
def habitaciones():
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
    diccionario = {
        "titulo_head": "Habitaciones",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("habitaciones.html", data=diccionario)
# Fin Ruta Habitaciones


# Ruta Reservar
@bp_habitaciones.route("/habitaciones/reservar", methods=["GET"])
def reservar():
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
        "titulo_head": "Habitaciones",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("reserva.html", data=data)
# Fin Ruta Reservar


