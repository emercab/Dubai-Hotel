# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Mi Cuenta

import sqlite3
from models.db import conectar
import datetime


def get_data_login(login_field:str):
    # Retorna los campos usados para login: username, cedula o email
    # y password registrado en DB del campo usado para hacer login que 
    # recibe. En caso de que no exista, retorna None
    
    try:
        # Me conecto a la DB
        conn = conectar()
        conn.row_factory = sqlite3.Row
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            SELECT username, cedula, email, password, nombres, apellidos, tipoUsuarioId,
                ciudad, direccion, celular, id
            FROM usuarios
            WHERE
                activo=1 
                AND (username=? OR cedula=? OR email=?); 
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, [login_field, login_field, login_field])
        # Guardo el primer resultado de la consulta
        result = cursor.fetchone()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno None
        print(f"Error: {error}")
        return None
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return result
# Fin de get_data_login()


def ya_existe(valor, campo, tabla):
    # Verifica si el valor que recibe ya existe en la tabla,
    # retorna True en ese caso o False al contrario

    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = f"""
            SELECT * FROM {tabla} WHERE {campo}='{valor}'
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence)
        # Guardo el primer resultado de la consulta
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
    except Exception as error:
        # Si hay un error, lo imprimo y retorno  indicando
        # que no se pudo hacer la revisión
        print(f"Error: {error}")
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()    
# Fin de ya_existe()


def save_data_user(data):
    # Guarda en la DB la información del usuario recién registrado

    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            INSERT INTO usuarios (
                username, nombres, apellidos, cedula,
                ciudad, direccion, celular,
                tipoUsuarioID, email,
                password, fechaRegistro, activo
            )
            VALUES (
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?, ?, ?
            );
        """
        valores = [
            data["username"], data["nombres"], data["apellidos"], data["cedula"],
            data["ciudad"], data["direccion"], data["celular"],
            data["tipo_usuario"], data["email"],
            data["password"], data["fecha_registro"], data["activo"]
        ]
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, valores)
        # Confirmo y envío los cambios a la tabla
        conn.commit()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno False indicando
        # que no se pudo hacer la inserción
        print(f"Error: {error}")
        return False
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return True
# Fin de save_data_user()


def update_password(user_id, new_password_hash):
    # Actualiza el password del usuario, retorna True o False si tuvo éxito
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            UPDATE usuarios SET password=? WHERE id=?
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, [new_password_hash, user_id])
        conn.commit()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno False
        print(f"Error: {error}")
        return False
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return True
# Fin de update_password()


def select_reservas(user_id):
    # Actualiza el password del usuario, retorna True o False si tuvo éxito
    try:
        # Me conecto a la DB
        conn = conectar()
        conn.row_factory=sqlite3.Row
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
           SELECT reservas.fechaInicial, reservas.fechaFinal, habitaciones.numero, habitaciones.calificacion FROM reservas INNER JOIN habitaciones ON reservas.habitacionId = habitaciones.id
           WHERE clienteID =?
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, [user_id])
        result = cursor.fetchall()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno False
        print(f"Error: {error}")
        return None
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return result


def select_comentario(usuario, id_comentario=None):
    try:
        # Me conecto a la DB
        conn = conectar()
        conn.row_factory = sqlite3.Row
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        if id_comentario:
            datos=(str(usuario),str(id_comentario))
            # Creo la sentencia SQL
            sentence = """
                SELECT reservas.id, reservas.habitacionId, habitaciones.numero, comentarios.id 
                AS comentarioId, comentarios.comentario, comentarios.calificacion 
                FROM usuarios 
                LEFT JOIN reservas ON usuarios.id=reservas.clienteID 
                LEFT JOIN habitaciones ON habitaciones.id=reservas.habitacionId 
                LEFT JOIN comentarios ON reservas.id=comentarios.reservaId 
                WHERE usuarios.id=? AND reservas.habitacionId=? 
            """
            # Ejecuto la sentencia SQL
            cursor.execute(sentence, datos)
            resultado=cursor.fetchone()  
        else:
            datos=(str(usuario))
            sentence = """
                SELECT reservas.id, reservas.habitacionId, habitaciones.numero, comentarios.id 
                AS comentarioId, comentarios.comentario, comentarios.calificacion 
                FROM usuarios 
                LEFT JOIN reservas ON usuarios.id=reservas.clienteID 
                LEFT JOIN habitaciones ON habitaciones.id=reservas.habitacionId 
                LEFT JOIN comentarios ON reservas.id=comentarios.reservaId 
                WHERE usuarios.id=? 
            """
            # Ejecuto la sentencia SQL
            cursor.execute(sentence, [str(usuario)])
            resultado=cursor.fetchall()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno False
        print(f"Error: {error}")
        return False
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    return resultado


def create_comment(reservaId, comentario, calificacion,comentarioId,habitacionId):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if comentarioId:
            query = """
                UPDATE comentarios 
                SET comentario = ?,
                    calificacion = ?
                WHERE id =?;
            """
            datos = (comentario, str(calificacion), str(comentarioId))
        else:
            query = """
                INSERT INTO comentarios (reservaId,comentario,calificacion,fecha) 
                VALUES( ?,	? ,?, ?);
            """
            datos = (str(reservaId), comentario,str(calificacion),datetime.datetime.now())
        
        cursor.execute(query, datos)
        conn.commit()

        #.lasrowid  -retorna el id del registro insertado
        last_id = comentarioId if comentarioId else cursor.lastrowid 
    except Exception as error:
        print(f'insert habitacion {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return last_id


def update_calificacion(habitacion_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE habitaciones 
        SET calificacion =(
            SELECT SUM(comentarios.calificacion)/COUNT(comentarios.calificacion) 
            AS calificacion FROM habitaciones 
            INNER JOIN reservas ON habitaciones.id = reservas.habitacionId 
            INNER JOIN comentarios ON reservas.id = comentarios.reservaId 
            GROUP BY habitaciones.id 
            HAVING habitaciones.id=?) 
        WHERE habitaciones.id=?;
        """
        datos = (str(habitacion_id), str(habitacion_id))
        cursor.execute(query, datos)
        conn.commit()
    except Exception as error:
        print(f'insert habitacion {error}')
        return False
    finally:
        cursor.close()
        conn.close()
    
    return True
