from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
from forms import RegisterForm

class UsuarioForm(RegisterForm):
    tipoUsuario = SelectField(
        "Tipo de usuario",
        choices=[("0", "Seleccionar una opción")],
        render_kw={
            "class": "form-control select-border"
        }
    )


class ReservaForm(FlaskForm):
    pass


class HabitacionForm(FlaskForm):
    nombre = StringField(
        "Número",
        validators=[
            DataRequired("Ingresar el nombre de la habitación.")
        ],
        id="txtNombre",
        name="txtNombre",
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
        render_kw={
            "class": "form-control"
        }
    )
