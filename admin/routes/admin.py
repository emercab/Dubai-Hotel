from flask import flash, redirect, render_template, request, Blueprint, url_for, escape, session
from admin.forms import HabitacionForm, UsuarioForm, ComentarioForm, ReservaForm
from controllers.controller_micuenta import data_to_template
from decorators import is_administrativo, login_required, superadmin_required
from admin.controllers.usuario_controller import buscar_tipo_usuario, guardar_usuario,  consultar_usuario, cambiar_estado_usuario
from admin.controllers.habitacion_controller import consultar_habitacion, desactivar_habitacion, guardar_habitacion

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
@login_required
@is_administrativo
def usuarios_admin():
    tipo_usuario_admin = session["tipo_usuario"] #este valor viene de la session
    usuarios = consultar_usuario(tipo_usuario_admin)

    data = data_to_template("Usuarios")
    data["usuarios"] = usuarios

    return render_template("admin/usuarios.html", data=data)
#fin usuarios


@bp_admin.route('/admin/nuevo-usuario', methods=['get', 'post'])
@bp_admin.route('/admin/nuevo-usuario/<id_usuario>', methods=['get', 'post'])
@login_required
@is_administrativo
def nuevo_usuario_admin(id_usuario=None):
    titulo_content = "Nuevo usuario"
    form = UsuarioForm(request.form)
     #carga los tipos de usuario. funcion retorna un array de tupla
    form.tipo_usuario.choices = buscar_tipo_usuario(session["tipo_usuario"])

    if request.method.lower() == 'get' and id_usuario != None:
        #para llenar los inputs al modificar.
        titulo_content = "Modificar usuario"
        usuario = consultar_usuario(None, id_usuario)

        if len(usuario) > 0:
            form.nombres.data           = usuario["Nombres"]
            form.apellidos.data         = usuario["Apellidos"]
            form.cedula.data            = usuario["Cedula"]
            form.celular.data           = usuario["Celular"]
            form.email.data             = usuario["Email"]
            form.direccion.data         = usuario["Direccion"]
            form.usuario.data           = usuario["Username"]
            form.ciudad.data            = usuario["Ciudad"]
            form.tipo_usuario.process_data(usuario["TipoUsuarioId"])

            password = usuario["Password"]
            if type(password) == bytes:
                form.password.data      = usuario["Password"].decode('utf8')
            else:
                form.password.data      = usuario["Password"]

    if form.validate_on_submit():
        nombres         = form.nombres.data
        apellidos       = form.apellidos.data
        cedula          = form.cedula.data
        celular         = form.celular.data
        email           = form.email.data
        tipo_usuario    = form.tipo_usuario.data
        clave           = form.password.data
        direccion       = form.direccion.data
        usuario         = form.usuario.data
        ciudad          = form.ciudad.data

        response = guardar_usuario(id_usuario, usuario, nombres, apellidos, cedula, celular, email, tipo_usuario, clave, ciudad, direccion)

        if response["type"] == "ok":
            return redirect(url_for('.usuarios_admin'))
        else:
            flash(response["message"], "error")

    data = data_to_template("Usuarios")
    data["form"] = form
    data["titulo_content"] = titulo_content

    if (form.errors and len(form.errors) > 0):
        flash([error[0] for error in form.errors.values()], "error")

    return render_template("admin/nuevo-usuario.html", data=data)
#fin nuevo usuario


@bp_admin.route('/admin/estado-usuario/<id_usuario>')
@login_required
@is_administrativo
def estado_usuario_admin(id_usuario):
    estado = request.args["estado"] #obtenemos el estado de la url
    cambiar_estado_usuario(id_usuario, estado)

    return redirect(url_for('.usuarios_admin'))
#fin estado usuario


@bp_admin.route('/admin/habitaciones')
@login_required
@is_administrativo
def habitaciones_admin():
    habitaciones = consultar_habitacion(None)

    data = data_to_template("Habitaciones")
    data["habitaciones"] = habitaciones

    return render_template("admin/habitaciones.html", data=data)
#fin habitaciones


@bp_admin.route('/admin/nueva-habitacion', methods=['get', 'post'])
@bp_admin.route('/admin/nueva-habitacion/<id_habitacion>', methods=['get', 'post'])
@login_required
@is_administrativo
def nueva_habitacion_admin(id_habitacion=None):
    title_content = "Nueva habitación"
    form = HabitacionForm(request.form)
    
    if request.method.lower() == 'get' and id_habitacion:
        title_content= "Modificar habitación"
        habitacion = consultar_habitacion(id_habitacion)
        
        if len(habitacion) > 0:
            form.numero.data = escape(habitacion["Numero"])
            form.precio.data = escape(habitacion["Precio"])

    if form.validate_on_submit():
        numero = form.numero.data
        precio = form.precio.data

        result = guardar_habitacion(id_habitacion, numero, precio)

        if result:
            return redirect(url_for('.habitaciones_admin'))
    
    data = data_to_template("Habitaciones")
    data["titulo_content"] = title_content
    data["form"] = form

    return render_template('admin/nueva-habitacion.html', data=data)
#fin nueva habitacion


@bp_admin.route('/admin/habitaciones/estado-habitacion/<id_habitacion>')
@login_required
@is_administrativo
def estado_habitacion_admin(id_habitacion):
    estado = request.args["estado"]
    desactivar_habitacion(id_habitacion, estado)
    return redirect(url_for('.habitaciones_admin'))
#fin reservas admin


@bp_admin.route('/admin/reservas')
@login_required
@is_administrativo
@superadmin_required
def reservas_admin():
    data = data_to_template("Reservas")

    return render_template('admin/reservas.html', data=data)
#fin reservas admin


@bp_admin.route('/admin/nueva-reserva', methods=['get', 'post'])
@login_required
@is_administrativo
@superadmin_required
def nueva_reserva_admin():
    form = ReservaForm(request.form)

    data = data_to_template("Reservas")
    data["titulo_content"] = "Nueva reserva"
    data["form"] = form
    
    return render_template('admin/nueva-reserva.html', data=data)
#fin nueva reserva admin


@bp_admin.route('/admin/comentarios')
@login_required
@is_administrativo
@superadmin_required
def comentarios_admin():
    data = {
        "titulo_head": "Comentarios"
    }

    return render_template('admin/comentarios.html', data=data)
#fin comentarios admin


@login_required
@is_administrativo
@superadmin_required
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
