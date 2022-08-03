from flask import redirect, render_template, request, Blueprint, url_for
from admin.forms import HabitacionForm, UsuarioForm, ComentarioForm, ReservaForm
from decorators import admin_required
from admin.controllers.usuario_controller import buscar_tipo_usuario, consultar_usuarios, guardar_usuario,  consultar_usuario
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
def usuarios_admin():
    tipo_usuario = 0 #este valor viene de la session
    usuarios = consultar_usuarios(tipo_usuario)

    data = {
        "titulo_head": "Usuarios",
        "usuarios": usuarios
    }

    return render_template("admin/usuarios.html", data=data)
#fin usuarios


@bp_admin.route('/admin/nuevo-usuario', methods=['get', 'post'])
@bp_admin.route('/admin/nuevo-usuario/<id_usuario>', methods=['get', 'post'])
def nuevo_usuario_admin(id_usuario=None):
    titulo_head = "Nuevo usuario"

    form = UsuarioForm(request.form)
    form.tipo_usuario.choices = buscar_tipo_usuario() #carga los tipos de usuario. funcion retorna un array de tupla
    
    #para llenar los inputs al modificar.
    if id_usuario != None:
            titulo_head = "Modificar usuario"
            #busco al usuario y luego almaceno sus datos en los inputs.
            #usuario = consultar_usuario(id_usuario)
            #form.nombres.data = usuario["Nombres"]
    
    if form.validate_on_submit():
        #result = guardar_usuario(id_usuario)
        print("submit")

    data = {
        "titulo_head": "Usuarios",
        "titulo_content": titulo_head,
        "form": form
    }

    return render_template("admin/nuevo-usuario.html", data=data)
#fin nuevo usuario


@bp_admin.route('/admin/habitaciones')
def habitaciones_admin():

    habitaciones = consultar_habitacion(None)

    data = {
        "titulo_head": "Habitaciones",
        "habitaciones": habitaciones
    }
    
    return render_template("admin/habitaciones.html", data=data)
#fin habitaciones


@bp_admin.route('/admin/nueva-habitacion', methods=['get', 'post'])
@bp_admin.route('/admin/nueva-habitacion/<id_habitacion>', methods=['get', 'post'])
def nueva_habitacion_admin(id_habitacion=None):
    form = HabitacionForm(request.form)
    data = {
        "titulo_head": "Habitaciones",
        "titulo_content": "Nueva habitación",
        "form": form
    }

    if request.method.lower() == 'get' and id_habitacion:
        habitacion = consultar_habitacion(id_habitacion)
        if len(habitacion) > 0:
            form.numero.data = habitacion[0]["Numero"]
            form.precio.data = habitacion[0]["Precio"]

    if form.validate_on_submit():
        numero = form.numero.data
        precio = form.precio.data

        result = guardar_habitacion(id_habitacion, numero, precio)

        if result:
            return redirect(url_for('.habitaciones_admin'))
    
    return render_template('admin/nueva-habitacion.html', data=data)
#fin nueva habitacion


@bp_admin.route('/admin/habitaciones/remove/<id_habitacion>')
def remover_habitacion_admin(id_habitacion):
    desactivar_habitacion(id_habitacion)

    return redirect(url_for('.habitaciones_admin'))
#fin reservas admin


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
