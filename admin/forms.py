from multiprocessing import Value
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, TextAreaField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, NumberRange, Email
from datetime import date, timedelta

class UsuarioForm(FlaskForm):
    tipo_usuario = SelectField(
        "Tipo de usuario",
        choices=[("0", "Seleccionar una opción")],
        validators=[
            DataRequired(message="Seleccionar una opción")
        ],
        render_kw={
            "class": "form-control select-border"
        },
        id="selectTipoUsuario",
        name="selectTipoUsuario"
    )
    nombres = StringField(
        "Nombres",
        validators=[
            DataRequired(message="Ingrese sus nombres.")
        ],
        id="txtNombre",
        name="txtNombre",
        render_kw={
            "placeholder": "Ingrese sus nombres",
        }
    )
    apellidos = StringField(
        "Apellidos",
        validators=[
            DataRequired(message="Ingrese sus apellidos.")
        ],
        id="txtApellido",
        name="txtApellido",
        render_kw={
            "placeholder": "Ingrese sus apellidos",
        }
    )
    cedula = IntegerField(
        "Cédula",
        validators=[
            DataRequired(message="Ingrese su cédula.")
        ],
        id="txtCedula",
        name="txtCedula",
        render_kw={
            "placeholder": "Sin puntos ni espacios",
        }
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Ingrese su email."),
            Email(message="Ingrese un email válido.")
        ],
        id="txtEmail",
        name="txtEmail",
        render_kw={
            "placeholder": "Ingrese su correo electrónico",
        }
    )
    direccion = StringField(
        "Dirección",
        validators=[
            DataRequired(message="Ingrese su dirección.")
        ],
        id="txtDireccion",
        name="txtDireccion",
        render_kw={
            "placeholder": "Ingrese su dirección",
        }
    )
    celular = IntegerField(
        "Celular",
        validators=[
            DataRequired(message="Ingrese su número de celular.")
        ],
        id="txtCelular",
        name="txtCelular",
        render_kw={
            "placeholder": "Ingrese su celular",
        }
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="Ingrese su contraseña.")
        ],
        id="txtPassword",
        name="txtPassword",
        render_kw={
            "placeholder": "Ingrese su contraseña",
            "autocomplete": "off"
        }
    )

    btn_guardar = SubmitField("Guardar")
#fin usuario form


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
            DataRequired("Ingresar el número de la habitación.")
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
