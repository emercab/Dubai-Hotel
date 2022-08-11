# En este archivo irán todas las clases que van a representar
# todos los formularios del proyecto usando la librería WTForms

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


# Formulario del Login
class ContactForm(FlaskForm):
    name = StringField(
        "Nombre:",
        validators=[
            DataRequired(message="Ingrese su nombre.")
        ],
        id="name",
        name="nombre_contacto",
        render_kw= {
            "autocomplete": "off",
            "placeholder" : "Nombre completo",
            "class": "input",
        }
    )
    email = EmailField(
        "Email:",
        validators=[
            DataRequired(message="Ingrese su email."),
            Email(message="Ingrese un email válido.")
        ],
        id="email",
        name="correo_persona",
        render_kw={
            "placeholder": "Correo electrónico",
            "class": "input",
        }
    )
    comentario = TextAreaField(
        "comentario",
        validators=[
            DataRequired(message="Ingrese su comentario.")
        ],
        id="contacto",
        name="msg_contacto",
        render_kw={
            "autocomplete": "off",
            "placeholder": "Cuentanos tu problema",
            "class": "textarea"
        }
    )
    enviar = SubmitField(
        "Enviar",
        id="btnEnviar",
        render_kw= {
            "class": "btn btn-secondary text-primary"
        }
    )
    
# Fin Formulario de contacto