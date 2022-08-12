# En este archivo irán todas las clases que van a representar
# todos los formularios del proyecto usando la librería WTForms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SubmitField,DecimalField
from wtforms.validators import DataRequired, Email, EqualTo


# Formulario del Login
class LoginForm(FlaskForm):
    username = StringField(
        "Usuario, cédula o email:",
        validators=[
            DataRequired(message="Ingrese su Usuario, cédula o email.")
        ],
        id="username",
        name="txtUsername",
        render_kw= {
            "autocomplete": "off",
            "placeholder": "Usuario, cédula o email."
        }
    )
    password = PasswordField(
        "Contraseña:",
        validators=[
            DataRequired(message="Ingrese su contraseña.")
        ],
        id="password",
        name="txtPassword",
        render_kw={
            "autocomplete": "off",
            "placeholder": "Ingrese su clave...",
            "class": "form-control",
        }
    )    
    ingresar = SubmitField(
        "Ingresar",
        render_kw= {
            "class": "btn btn-secondary text-primary"
        }
    )
# Fin Formulario del Login


# Formulario de Registro
class RegisterForm(FlaskForm):
    nombres = StringField(
        "Nombres:",
        validators=[
            DataRequired(message="Ingrese sus nombres.")
        ],
        id="nombres",
        name="txtNombres",
        render_kw={
            "placeholder": "Ingrese sus nombres",
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
        }
    )
    password = PasswordField(
        "Contraseña:",
        validators=[
            DataRequired(message="Ingrese su contraseña."),
            EqualTo("confirm_password", message="Las contraseñas ingresadas no coinciden.")
        ],
        id="password",
        name="txtPassword",
        render_kw={
            "placeholder": "Ingrese su contraseña",
            "autocomplete": "off"
        }
    )
    confirm_password = PasswordField(
        "Confirme su Contraseña:",
        validators=[
            DataRequired(message="Debe confirmar su contraseña."),
        ],
        id="confirm_password",
        name="txtConfirmPassword",
        render_kw={
            "placeholder": "Repita su contraseña",
            "autocomplete": "off"
        }
    )
    registrar = SubmitField(
        "Registrarme",
        render_kw= {
            "class": "btn btn-secondary text-primary"
        }
    )
# Fin Formulario de Registro


class ChangePassword(FlaskForm):
    password = PasswordField(
        "Contraseña Actual:",
        validators=[
            DataRequired(message="Ingrese su contraseña actual.")
        ],
        id="password",
        name="txtPassword",
        render_kw={
            "autocomplete": "off",
            "placeholder": "Ingrese su contraseña actual",
        }
    )
    new_password = PasswordField(
        "Nueva Contraseña:",
        validators=[
            DataRequired(message="Ingrese su nueva contraseña."),
            EqualTo("new_password2", message="Las contraseñas nuevas no coinciden."),
        ],
        id="new_password",
        name="txtNewPassword",
        render_kw={
            "autocomplete": "off",
            "placeholder": "Ingrese su nueva contraseña",
        }
    )
    new_password2 = PasswordField(
        "Confirmar Nueva Contraseña:",
        validators=[
            DataRequired(message="Repita su nueva contraseña.")
        ],
        id="new_password2",
        name="txtNewPassword2",
        render_kw={
            "autocomplete": "off",
            "placeholder": "Repita su nueva contraseña",
        }
    )
    btn_cambiar_password = SubmitField(
        "Cambiar Contraseña",
        render_kw= {
            "class": "btn btn-primary text-secondary"
        }
    )

class NuevaCalificacion(FlaskForm):
    habitacion = StringField(
        "Habitación",
        render_kw={
            "readonly": "",
            "class": "form-control"
        }
    )

    calificacion = DecimalField(
        "Calificación",
        validators=[
            DataRequired("Ingresar calificación.")
        ],
        render_kw={
            "class": "form-control"
        },
        places=1
    )

    comentario = StringField(
        "Comentario",
        validators=[
            DataRequired("Ingresar comentario.")
        ],
        render_kw={
            "class": "form-control"
        }
    )

    btn_enviar_comentario = SubmitField(
        "Enviar Comentario",
        render_kw= {
            "class": "btn btn-primary text-secondary"
        }
    )

