from venv import create
from flask_bcrypt import generate_password_hash, check_password_hash
from admin.models.usuario_model import create_usuario, select_tipo_usuario, select_usuario, select_usuarios, update_estado_usuario

def buscar_tipo_usuario(tipo_usuario_admin):
    tipo_usuario = select_tipo_usuario(tipo_usuario_admin)

    return tipo_usuario


#hay que tener en cuenta si es admin ve solo los clientes.
def consultar_usuario(tipo_usuario_admin, id_usuario=None):
    
    if id_usuario:
        usuarios = select_usuario(id_usuario) #retorna solo una tupla o none
    else:
        usuarios = select_usuarios(tipo_usuario_admin)

    if usuarios:
        return usuarios
    return []

#retorna bool
def guardar_usuario(id_usuario, usuario, nombres, apellidos, cedula, celular, email, tipo_usuario, clave, ciudad, direccion):
    #pw_hash = bcrypt.generate_password_hash('hunter2')
    #bcrypt.check_password_hash(pw_hash, 'hunter2')

    #podemos hacer validaciones si los campos estan vacios

    clave_encryp = generate_password_hash(clave)

    nuevo_id = create_usuario(id_usuario, usuario, nombres, apellidos, cedula, celular, email, tipo_usuario, clave_encryp, ciudad, direccion)

    return nuevo_id


def cambiar_estado_usuario(id_usuario, estado):
    update_estado_usuario(id_usuario, estado)

