from datetime import date, timedelta
from flask import flash, redirect, render_template, request, Blueprint, url_for, escape, session, g
from admin.controllers.reserva_controller import consultar_reserva_admin, guardar_reserva_admin, obtener_habitaciones_reserva, validar_fecha_reserva
from admin.forms import HabitacionForm, UsuarioForm, ComentarioForm, ReservaForm
from controllers.controller_micuenta import data_to_template
from decorators import is_administrativo, login_required, superadmin_required
from admin.controllers.usuario_controller import buscar_tipo_usuario, guardar_usuario,  consultar_usuario, cambiar_estado_usuario
from admin.controllers.habitacion_controller import consultar_habitacion, desactivar_habitacion, guardar_habitacion, ver_precio_habitacion
from admin.controllers.comentario_controller import consultar_comentario,guardar_comentario, eliminar_comentario

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
    
    if request.method.lower() == 'get':
        if id_habitacion:
            title_content= "Modificar habitación"
            habitacion = consultar_habitacion(id_habitacion)
            
            if len(habitacion) > 0:
                form.numero.data = escape(habitacion["Numero"])
                form.precio.data = escape(habitacion["Precio"])
        else:
            precio_habitacion = ver_precio_habitacion()
            if precio_habitacion:
                form.precio.data = precio_habitacion

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


@bp_admin.route('/admin/estado-habitacion/<id_habitacion>')
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
    reservas = consultar_reserva_admin(None)
    data["reservas"] = reservas

    return render_template('admin/reservas.html', data=data)
#fin reservas admin


@bp_admin.route('/admin/nueva-reserva', methods=['get', 'post'])
@bp_admin.route('/admin/nueva-reserva/<id_reserva>', methods=['get', 'post'])
@login_required
@is_administrativo
@superadmin_required
def nueva_reserva_admin(id_reserva=None):
    form = ReservaForm(request.form)
    data = data_to_template("Reservas")
    data["titulo_content"] = "Nueva reserva"

    if request.method.lower() == "get":
        fecha_ingreso   = date.today()
        fecha_salida    = fecha_ingreso + timedelta(days=1)
        form.fecha_ingreso.render_kw = {
            "min":   fecha_ingreso,
            "value": fecha_ingreso,
            "class": "form-control date-field",
            "data-type": "llegada"
        }
        form.fecha_salida.render_kw = {
            "min": fecha_salida,
            "value": fecha_salida,
            "class": "form-control date-field",
            "data-type": "salida"
        }

        session.pop("numero_habitacion", None)
        session.pop("valor_habitacion", None)
        session.pop("total_reserva", None)

        if id_reserva:
            data["titulo_content"] = "Modificar reserva"
            reserva = consultar_reserva_admin(id_reserva)

            if reserva and len(reserva) > 0:
                form.fecha_ingreso.render_kw["value"]           = reserva["FechaInicial"]
                form.fecha_ingreso.render_kw["min"]             = validar_fecha_reserva(fecha_ingreso, reserva["FechaInicial"])
                form.fecha_salida.render_kw["value"]            = reserva["FechaFinal"]
                form.fecha_salida.render_kw["min"]              = validar_fecha_reserva(fecha_salida, reserva["FechaFinal"])
                form.reserva_hidden.data                        = reserva["ClienteId"]
                form.cliente.data                               = reserva["NombreCompleto"]
                form.busqueda_cliente.data                      = reserva["Username"]
                form.busqueda_cliente.render_kw["readonly"]     = "readonly"
                form.precio.data                                = reserva["Total"]

                session["numero_habitacion"]                    = reserva["Numero"]
                session["valor_habitacion"]                     = reserva["HabitacionId"]
                session["total_reserva"]                        = reserva["Total"]
    else:
        fecha_ingreso   = form.fecha_ingreso.data
        fecha_salida    = form.fecha_salida.data

    habitaciones = obtener_habitaciones_reserva(fecha_ingreso, fecha_salida)
    form.habitacion.choices = habitaciones

    if form.validate_on_submit():
        id_cliente              = escape(form.reserva_hidden.data)
        fecha_ingreso           = escape(form.fecha_ingreso.data)
        fecha_salida            = escape(form.fecha_salida.data)
        id_habitacion           = escape(form.habitacion.data)
        id_habitacion_actual    = None

        if "valor_habitacion" in session:
            id_habitacion_actual = session["valor_habitacion"]

        response = guardar_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, id_habitacion, id_habitacion_actual)
        
        if response["type"] == "ok":
            return redirect(url_for('.reservas_admin'))
        else:
            flash(response["message"], "error")
    
    if (form.errors and len(form.errors) > 0):
        flash([error[0] for error in form.errors.values()], "error")

    data["form"] = form

    return render_template('admin/nueva-reserva.html', data=data)
#fin nueva reserva admin


@bp_admin.route('/admin/comentarios')
@login_required
@is_administrativo
@superadmin_required
def comentarios_admin():
    comentarios = consultar_comentario(None)

    data = data_to_template("Comentarios")
    data["comentarios"] = comentarios

    return render_template('admin/comentarios.html', data=data)
#fin comentarios admin


@login_required
@is_administrativo
@superadmin_required
@bp_admin.route('/admin/nuevo-comentario', methods=['get', 'post'])
@bp_admin.route('/admin/nuevo-comentario/<id_comentario>', methods=['get', 'post'])
def nuevo_comentario_admin(id_comentario=None):
    title_content = "Nuevo comentario"
    form = ComentarioForm(request.form)

    if request.method.lower() == 'get' and id_comentario:
        title_content= "Modificar comentario"
        comentario = consultar_comentario(id_comentario)
        
        if len(comentario) > 0:
            form.cliente.data = escape(comentario["cliente"])
            form.habitacion.data = (escape(comentario["numero"]))
            form.calificacion.data = float(escape(comentario["calificacion"]))
            form.comentario.data = escape(comentario["comentario"])
    
    if form.validate_on_submit():
        comentario = form.comentario.data
        calificacion = form.calificacion.data
        result = guardar_comentario(id_comentario, comentario,calificacion)

        if result:
            return redirect(url_for('.comentarios_admin'))


    data = data_to_template("Comentarios")
    data["titulo_content"] = title_content
    data["form"] = form

    return render_template('admin/nuevo-comentario.html', data=data)
#fin nuevo comentario admin



@login_required
@is_administrativo
@superadmin_required
@bp_admin.route('/admin/desactivar-comentario/<id_comentario>', methods=['get', 'post'])
def desactivar_comentario_admin(id_comentario=None):
    title_content = "Desactivar comentario"
    form = ComentarioForm(request.form)
    
    eliminar_comentario(id_comentario)

    return redirect(url_for('.comentarios_admin'))