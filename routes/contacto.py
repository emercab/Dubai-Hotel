# Acá van todas las rutas de la aplicación del endpoint contacto

from flask import request, Blueprint,render_template, redirect
from forms.forms_contacto import ContactForm
import controllers.controller_contacto as controller
import controllers.controller_micuenta as controller_micuenta

# Objeto de la clase Blueprint que vincula el main con este módulo
bp_contacto = Blueprint("bp_contacto", __name__)


# Ruta Contacto# Preparo datos a enviar a la vist
@bp_contacto.route("/contacto", methods=["GET","POST"])
def contacto():
    contacto_form = ContactForm(request.form)
    
    # Preparo datos a enviar a la vista
    data = controller_micuenta.data_to_template("Contacto")
    
    # Agrego el formulario al diccionario de data que se enviará al template
    data["form"] = contacto_form

    if contacto_form.validate_on_submit():
        name = contacto_form.name.data
        email = contacto_form.email.data
        comentario = contacto_form.comentario.data
        result = controller.send_contacto(name, email, comentario)

        if result:
            return redirect('/contacto')

    return render_template('contacto.html', data=data)
# Fin Ruta Contacto

