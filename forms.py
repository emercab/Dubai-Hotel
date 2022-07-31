# En este archivo irán todas las clases que van a representar
# todos los formularios del proyecto usando la librería WTForms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Formulario del Login
class LoginForm(FlaskForm):
    username = StringField(
        "Usuario, cédula o email:",
        validators=[
            DataRequired(message="Ingrese su Usuario, cédula o email.")
        ],
        id="username",
        name="txtUsername",
    )
    password = PasswordField(
        "Password:",
        validators=[
            DataRequired(message="Ingrese su contraseña.")
        ],
        id="password",
        name="txtPassword"
    )
    ingresar = SubmitField("Ingresar", None, None, id="miid")
