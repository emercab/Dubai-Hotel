from flask import redirect, render_template, request, Blueprint, session, url_for
from admin.forms import ComentarioForm, HabitacionForm, ReservaForm, UsuarioForm
from decorators import admin_required


bp_admin = Blueprint("bp_admin", __name__)

# @bp_admin.route("/admin", methods=["GET"])
# def admin():
    
#     return "Estamos en el Admin"

#session
#session['key_session']="value session" - crear session
#acceder_session = ['key_session']      - acceder a session
#session.pop('key_session', None)       - eliminar session
#session.clear()                        - eliminar todas las sessiones

@bp_admin.route('/admin')
@bp_admin.route('/admin/usuarios')
def usuarios_admin():
    data = {
        "titulo_head": "Usuarios"
    }
    
    return render_template("admin/usuarios.html", data=data)
#fin usuarios


@bp_admin.route('/admin/nuevo-usuario')
def nuevo_usuario_admin():
    form = UsuarioForm(request.form)
    form.tipo_usuario.choices = [form.tipo_usuario.choices[0], ("0", "Numero 1"), ("1", "Numero 2"), ("2", "Numero 3")]

    data = {
        "titulo_head": "Usuarios",
        "titulo_content": "Nuevo usuario",
        "form": form
    }
    
    return render_template("admin/nuevo-usuario.html", data=data)
#fin nuevo usuario


@bp_admin.route('/admin/habitaciones')
def habitaciones_admin():
    data = {
        "titulo_head": "Habitaciones"
    }
    
    return render_template("admin/habitaciones.html", data=data)
#fin habitaciones


@bp_admin.route('/admin/nueva-habitacion', methods=['get', 'post'])
def nueva_habitacion_admin():
    form = HabitacionForm(request.form)
    data = {
        "titulo_head": "Habitaciones",
        "titulo_content": "Nueva habitación",
        "form": form
    }

    if request.method.lower() == "post":
        if form.validate_on_submit():
            return redirect(url_for('bp_admin.habitaciones_admin'))
            #return render_template('admin/nueva-habitacion.html', data=data, message="ok")
    
    return render_template('admin/nueva-habitacion.html', data=data)
#fin nueva habitacion


@bp_admin.route('/admin/reservas')
def reservas_admin():
    data = {
        "titulo_head": "Reservas"
    }

    return render_template('admin/reservas.html', data=data)
#fin reservas admin


@bp_admin.route('/admin/nueva-reserva', methods=['get', 'post'])
def nueva_reserva_admin():
    form = ReservaForm(request.form)
    data = {
        "titulo_head": "Reservas",
        "titulo_content": "Nueva reserva",
        "form": form
    }

    return render_template('admin/nueva-reserva.html', data=data)
#fin nueva reserva admin


@bp_admin.route('/admin/comentarios')
def comentarios_admin():
    data = {
        "titulo_head": "Comentarios"
    }

    return render_template('admin/comentarios.html', data=data)
#fin comentarios admin


@bp_admin.route('/admin/nuevo-comentario', methods=['get', 'post'])
def nuevo_comentario_admin():
    form = ComentarioForm(request.form)
    data = {
        "titulo_head": "Comentarios",
        "titulo_content": "Nuevo comentario",
        "form": form
    }

    return render_template('admin/nuevo-comentario.html', data=data)
#fin nuevo comentario admin