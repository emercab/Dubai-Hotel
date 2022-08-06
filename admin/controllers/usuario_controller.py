import flask_bcrypt
from admin.models.usuario_model import create_usuario, select_tipo_usuario, select_usuario, select_usuarios, update_estado_usuario

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
    #podemos hacer validaciones si los campos estan vacios

    clave_encryp = flask_bcrypt.generate_password_hash(clave)

    if id_usuario != None and int(id_usuario) > 0:
        usuario_db = consultar_usuario(None, id_usuario)

        if len(usuario_db) > 0 and clave == usuario_db["Password"].decode("utf8"):
                clave_encryp = clave

    nuevo_id = create_usuario(id_usuario, username, nombres, apellidos, cedula, celular, email, tipo_usuario, clave_encryp, ciudad, direccion)

    return nuevo_id


def cambiar_estado_usuario(id_usuario, estado):
    update_estado_usuario(id_usuario, estado)

