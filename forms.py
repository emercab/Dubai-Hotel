from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class FormInicio(FlaskForm):
    nombre = StringField(
        "Usuario:", validators=[DataRequired(message="Este campo es obligatorio")]
    )
    password = PasswordField(
        "Password:", validators=[DataRequired(message="Ingrese su contraseña")]
    )
    recordar = BooleanField("Recordar usuario")
    enviar = SubmitField("Ingresar")
