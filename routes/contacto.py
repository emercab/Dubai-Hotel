# Acá van todas las rutas de la aplicación del endpoint contacto

from flask import jsonify, request, Blueprint,render_template, redirect,url_for
from forms_contacto import contacto
import controllers.controller_contacto as controller

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_contacto = Blueprint("bp_contacto", __name__)


# Ruta Contacto
@bp_contacto.route("/contacto", methods=["GET","POST"])
def index():

    contacto_form = contacto(request.form)

    data = {
        "titulo_head": "Contacto",
        "user_login": False,
        "form": contacto_form,
    }
    if contacto_form.validate_on_submit():
        name=contacto_form.name.data
        email=contacto_form.email.data
        comentario=contacto_form.comentario.data
        result=controller.send_contacto(name,email,comentario)

        if result:
            return redirect(('contacto'))

    return render_template('contacto.html',data=data)
# Fin Ruta Contacto



