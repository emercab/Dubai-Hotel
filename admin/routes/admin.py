from flask import redirect, render_template, request, Blueprint, url_for
from admin.forms import HabitacionForm, UsuarioForm
from decorators import admin_required


bp_admin = Blueprint("bp_admin", __name__)

# @bp_admin.route("/admin", methods=["GET"])
# def admin():
    
#     return "Estamos en el Admin"

@bp_admin.route('/admin')
@bp_admin.route('/admin/usuarios')
def usuarios_admin():
    data = {
        "titulo_head": "Usuarios"
    }
    
    return render_template("admin/usuarios.html", data=data)


@bp_admin.route('/admin/nuevo-usuario')
def nuevo_usuario_admin():
    form = UsuarioForm(request.form)
    data = {
        "titulo_head": "Usuarios",
        "titulo_content": "Nuevo usuario",
        "form": form
    }
    
    return render_template("admin/nuevo-usuario.html", data=data)


@bp_admin.route('/admin/habitaciones')
def habitaciones_admin():
    data = {
        "titulo_head": "Habitaciones"
    }
    
    return render_template("admin/habitaciones.html", data=data)

@bp_admin.route('/admin/nueva-habitacion', methods=['get', 'post'])
def nueva_habitacion_admin(message=None):
    form = HabitacionForm(request.form)
    data = {
        "titulo_head": "Habitaciones",
        "titulo_content": "Nueva habitación",
        "form": form
    }

    if request.method.lower() == "post":
        if form.validate_on_submit():
            return redirect(url_for('bp_admin.habitaciones_admin', message="ok"))
            #return render_template('admin/nueva-habitacion.html', data=data, message="ok")
    
    return render_template('admin/nueva-habitacion.html', data=data, message=message)