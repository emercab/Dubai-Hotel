# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Habitaciones

from datetime import datetime
import sqlite3
from models.db import conectar


def get_rooms(fecha_inicio: str, fecha_final: str):
    try:
        # Me conecto a la DB
        conn = conectar()
        conn.row_factory = sqlite3.Row #disponible desde python>=3
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence_de_nico = """
            SELECT habitaciones.*, 'Habitación ' || IFNull(habitaciones.numero, '') as NumeroHabitacion FROM habitaciones
            LEFT JOIN (
                SELECT * FROM reservas
                WHERE fechaFinal >= ? AND fechaInicial <= ?
            ) as B
            ON B.habitacionId = habitaciones.id
            WHERE B.id IS NULL AND habitaciones.activo = 1
        """
        valores = (fecha_inicio, fecha_final)
        # Ejecuto la sentencia SQL
        cursor.execute(sentence_de_nico, valores)
        # Guardo el primer resultado de la consulta
        result = cursor.fetchall()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno None
        print(f"Error: {error}")
        return None
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return result
# Fin de get_rooms()


def get_precio(id):
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            SELECT precio
            FROM habitaciones
            WHERE
                activo=1 AND id=?; 
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, [id])
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
# Fin de get_precio()


def get_cliente_id(cedula):
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            SELECT id
            FROM usuarios
            WHERE
                activo=1 AND cedula=?; 
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, [cedula])
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
# Fin de get_cliente_id()


def save_reserva(data:dict):
    # Guarda los datos de la reserva en la DB.
    # Retorna True o False si tuvo éxito o no
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            INSERT INTO reservas (
                habitacionID, clienteID, fechaInicial,
                fechaFinal, total
            )
            VALUES (?, ?, ?, ?, ?);
        """
        valores = (
            data["habitacion"], data["cliente_id"], data["fecha_inicio"],
            data["fecha_final"], data["total"]
        )
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
# Fin de save_reserva()
