# En este archivo irán todas las clases que van a representar
# todos los formularios del proyecto usando la librería WTForms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email


# Formulario de Reservar
class ReservaForm(FlaskForm):
    nombres = StringField(
        "Nombres:",
        validators=[
            DataRequired(message="Ingrese sus nombres.")
        ],
        id="nombres",
        name="txtNombres",
        render_kw={
            "placeholder": "Ingrese sus nombres",
            "class": "controls",
        }
    )
    apellidos = StringField(
        "Apellidos:",
        validators=[
            DataRequired(message="Ingrese sus apellidos.")
        ],
        id="apellidos",
        name="txtApellidos",
        render_kw={
            "placeholder": "Ingrese sus apellidos",
            "class": "controls",
        }
    )
    cedula = IntegerField(
        "Cédula:",
        validators=[
            DataRequired(message="Ingrese su cédula.")
        ],
        id="cedula",
        name="txtCedula",
        render_kw={
            "placeholder": "Sin puntos ni espacios",
            "class": "controls",
        }
    )
    email = EmailField(
        "Email:",
        validators=[
            DataRequired(message="Ingrese su email."),
            Email(message="Ingrese un email válido.")
        ],
        id="email",
        name="txtEmail",
        render_kw={
            "placeholder": "Ingrese su correo electrónico",
            "class": "controls",
        }
    )
    direccion = StringField(
        "Dirección:",
        validators=[
            DataRequired(message="Ingrese su dirección.")
        ],
        id="direccion",
        name="txtDireccion",
        render_kw={
            "placeholder": "Ingrese su dirección",
            "class": "controls",
        }
    )
    ciudad = StringField(
        "Ciudad:",
        validators=[
            DataRequired(message="Ingrese su ciudad.")
        ],
        id="ciudad",
        name="txtCiudad",
        render_kw={
            "placeholder": "Ingrese su ciudad",
            "class": "controls",
        }
    )
    celular = IntegerField(
        "Celular:",
        validators=[
            DataRequired(message="Ingrese su número de celular.")
        ],
        id="celular",
        name="txtCelular",
        render_kw={
            "placeholder": "Ingrese su celular",
            "class": "controls",
        }
    )
    reservar = SubmitField(
        "Realizar Reserva",
        render_kw= {
            "class": "btn btn-secondary text-primary"
        }
    )
# Fin Formulario de Reservar
