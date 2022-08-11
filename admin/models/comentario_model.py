import sqlite3
from models.db import conectar

def create_comentario(id_comentario, comentario,calificacion):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_comentario:
            query = """
                update comentarios
                    set comentario = ?,
                        calificacion = ?
                where id = ?
            """
            datos = (comentario, str(calificacion),id_comentario)
            query2 = """
            UPDATE habitaciones
            SET calificacion = (SELECT SUM(comentarios.calificacion)/COUNT(comentarios.calificacion) FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            GROUP BY reservas.habitacionId
            HAVING reservas.habitacionId=(SELECT reservas.habitacionId FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            WHERE comentarios.id = ?))
            WHERE id = (SELECT reservas.habitacionId FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            WHERE comentarios.id = ?)
            """
            datos2 = (id_comentario,id_comentario)
            
        else:
            None

        cursor.execute(query, datos)
        cursor.execute(query2, datos2)
        conn.commit()


        #.lasrowid  -retorna el id del registro insertado
        last_id = id_comentario if id_comentario else cursor.lastrowid 
    except Exception as error:
        print(f'insert comentarios {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return last_id

def select_comentario(id_comentario=None):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if id_comentario:
            sql_sentence = """
            SELECT comentarios.id,
                    usuarios.nombres || ' ' || usuarios.apellidos as cliente, 
                    habitaciones.numero, comentarios.comentario, comentarios.calificacion, comentarios.fecha 
            FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            INNER JOIN usuarios on usuarios.id= reservas.clienteID
            INNER JOIN habitaciones on habitaciones.id = reservas.habitacionId
            WHERE comentarios.id=?;
            """
            cursor.execute(sql_sentence, [id_comentario])
            resultado = cursor.fetchone()
        else:
            sql_sentence = """
            SELECT comentarios.id,
                    usuarios.nombres || ' ' || usuarios.apellidos as cliente, 
                    habitaciones.numero, comentarios.comentario, comentarios.calificacion, comentarios.fecha 
            FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            INNER JOIN usuarios on usuarios.id= reservas.clienteID
            INNER JOIN habitaciones on habitaciones.id = reservas.habitacionId;
            """
            cursor.execute(sql_sentence)
            resultado = cursor.fetchall()  
    except Exception as error:
        print(f'select_comentario {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return resultado
#fin consultar comentario

def delete_comentario(id_comentario):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_comentario:
            query = """
                DELETE FROM comentarios
                WHERE id=?;
            """
            datos = (id_comentario,)
            query2 = """
            UPDATE habitaciones
            SET calificacion = (SELECT SUM(comentarios.calificacion)/COUNT(comentarios.calificacion) FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            GROUP BY reservas.habitacionId
            HAVING reservas.habitacionId=(SELECT reservas.habitacionId FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            WHERE comentarios.id = ?))
            WHERE id = (SELECT reservas.habitacionId FROM comentarios
            INNER JOIN reservas ON reservas.id= comentarios.reservaId
            WHERE comentarios.id = ?)
            """
            datos2 = (id_comentario,datos)
            
        else:
            None

        cursor.execute(query, datos)
        #cursor.execute(query2, datos2)
        conn.commit()


        #.lasrowid  -retorna el id del registro insertado
    except Exception as error:
        print(f'insert comentarios {error}')
        return None
    finally:
        cursor.close()
        conn.close()