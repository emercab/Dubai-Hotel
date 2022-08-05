

def buscar_tipo_usuario():
    tipo_usuario = [
        ('', 'Seleccionar una opción'),
        (1, 'valor 1'),
        (2, 'valor 2'),
        (3, 'valor 3')
    ]

    return tipo_usuario


#hay que tener en cuenta si es admin ve solo los clientes.
def consultar_usuarios(tipo_usuario_admin):
    return []


def consultar_usuario(id_usuario):
    pass


#retorna bool
def guardar_usuario(id_usuario, nombres, apellidos, cedula, celular, email, tipo_usuario, clave, direccion):
    pass


def desactivar_usuario(id_usuario):
    pass

