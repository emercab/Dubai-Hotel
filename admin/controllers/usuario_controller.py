import flask_bcrypt
from admin.models.usuario_model import create_usuario, select_tipo_usuario, select_usuario, select_usuarios, update_estado_usuario, select_existe_usuario
from flask import escape


def buscar_tipo_usuario(tipo_usuario_admin):
    tipo_usuario = select_tipo_usuario(tipo_usuario_admin)

    return tipo_usuario


#hay que tener en cuenta si es admin ve solo los clientes.
def consultar_usuario(tipo_usuario_admin, id_usuario=None):
    
    if id_usuario and len(id_usuario) > 0:
        usuarios = select_usuario(id_usuario) #retorna solo una tupla o none
    else:
        usuarios = select_usuarios(tipo_usuario_admin)

    if usuarios and len(usuarios) > 0:
        return usuarios

    return []

#retorna id del usuario creado/modificado
def guardar_usuario(id_usuario, username, nombres, apellidos, cedula, celular, email, tipo_usuario, clave, ciudad, direccion):
    username    = escape(username).strip()
    nombres     = escape(nombres).strip().upper()
    apellidos   = escape(apellidos).strip().upper()
    cedula      = escape(cedula).strip()
    celular     = escape(celular).strip()
    email       = escape(email).strip().lower()
    ciudad      = escape(ciudad).strip().capitalize()
    direccion   = escape(direccion).strip().capitalize()
    clave       = escape(clave).strip()
    clave_encryp = flask_bcrypt.generate_password_hash(clave).decode("utf8")

    #validar si el usuario ya existe
    usuario_registrado = select_existe_usuario(id_usuario, username, cedula, email)
    
    print(usuario_registrado)

    if usuario_registrado and len(usuario_registrado) > 0:
        if usuario_registrado["Email"].lower() == email:
            return {
                "type": "err",
                "message": ["Ya existe un usuario con el mismo email."]
            }

        if usuario_registrado["Cedula"].lower() == cedula:
            return {
                "type": "err",
                "message": ["Ya existe un usuario con el mismo número de cédula."]
            }

        if usuario_registrado["Username"].lower().strip() == username.lower():
            return {
                "type": "err",
                "message": ["Ya existe un usuario con el mismo nombre de usuario."]
            }
    
    if id_usuario != None and int(id_usuario) > 0:
        usuario_db = consultar_usuario(None, id_usuario)

        if len(usuario_db) > 0:
            clave_db = usuario_db["Password"]

            if type(clave_db) == bytes:
                clave_db = clave_db.decode("utf8")

            if clave == clave_db:
                clave_encryp = clave
    nuevo_id = create_usuario(id_usuario, username, nombres, apellidos, cedula, celular, email, tipo_usuario, clave_encryp, ciudad, direccion)

    return {
        "type": "ok",
        "response": nuevo_id
    }


def cambiar_estado_usuario(id_usuario, estado):
    update_estado_usuario(id_usuario, estado)

