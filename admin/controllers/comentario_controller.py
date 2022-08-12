from admin.models.comentario_model import select_comentario, create_comentario,delete_comentario


def consultar_comentario(id_comentario):
    comentarios = select_comentario(id_comentario)

    if len(comentarios) > 0:
        return comentarios
    
    return []

def guardar_comentario(id_comentario,comentario,calificacion):

    nuevo_comentario = create_comentario(id_comentario,comentario,calificacion)

    return nuevo_comentario

def eliminar_comentario(id_comentario):

    delete_comentario(id_comentario)
