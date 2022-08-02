from multiprocessing import Value
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from forms import RegisterForm
from datetime import date, timedelta

class UsuarioForm(RegisterForm):
    tipo_usuario = SelectField(
        "Tipo de usuario",
        choices=[("0", "Seleccionar una opción")],
        render_kw={
            "class": "form-control select-border"
        },
        id="selectTipoUsuario",
        name="selectTipoUsuario"
    )


class ReservaForm(FlaskForm):
    cliente = SelectField(
        "Cliente", 
        validators=[ DataRequired("Seleccionar a un cliente.") ],
        choices = [(0, "Seleccione un cliente")],
        render_kw = {
            "class": "form-control select-border"
        },
        id="selectCliente",
        name="selectCliente"
    )

    habitacion = SelectField(
        "Habitación",
        validators=[ DataRequired("Seleccionar una habitación.") ],
        choices = [(0, "Seleccione un habitación")],
        render_kw = {
            "class": "form-control select-border"
        },
        id="selectHabitacion",
        name="selectHabitacion"
    )

    hoy = date.today()

    fecha_ingreso = DateField(
        "Fecha de ingreso",
        validators=[ DataRequired("Seleccionar fecha de ingreso.") ],
        render_kw = {
            "class": "form-control",
            "value": hoy,
            "min": hoy
        },
        id="txtFechaIngreso",
        name="txtFechaIngreso"
    )

    tomorrow = hoy + timedelta(days=1)

    fecha_salida = DateField(
        "Fecha de salida",
        validators=[ DataRequired("Seleccionar fecha de salida.") ],
        render_kw = {
            "class": "form-control",
            "value": tomorrow,
            "min": tomorrow
        },
        id="txtFechaSalida",
        name="txtFechaSalida"
    )

    precio = IntegerField(
        "Precio",
        render_kw={
            "class": "form-control",
            "readonly": ""
        }
    )


class ComentarioForm(FlaskForm):
    cliente = StringField(
        "Cliente",
        render_kw={
            "readonly": "",
            "class": "form-control"
        }
    )

    habitacion = StringField(
        "Habitación",
        render_kw={
            "readonly": "",
            "class": "form-control"
        }
    )

    comentario = TextAreaField(
        "Comentario",
        validators=[DataRequired("Debe ingresar un comentario.")],
        render_kw = {
            "class": "form-control",
            "rows": "4"
        }
    )


class HabitacionForm(FlaskForm):
    numero = StringField(
        "Número",
        validators=[
            DataRequired("Ingresar número de la habitación.")
        ],
        id="txtNumero",
        name="txtNumero",
        render_kw={
            "class": "form-control"
        }
    )

    precio = IntegerField(
        "Precio",
        validators=[
            DataRequired("Ingresar el precio para la habitación."),
            NumberRange(min=0, message="El precio no puede ser menor a 0.")
        ],
        id="txtPrecio",
        name="txtPrecio",
        render_kw={
            "class": "form-control"
        }
    )
