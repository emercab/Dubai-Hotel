# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Habitaciones

from models.db import conectar


def get_rooms():
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            SELECT *
            FROM habitaciones
            WHERE
                activo=1 
                AND (1 = 1); 
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence)
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
        print(data["habitacion"])
        print(data["cliente_id"])
        print(data["fecha_inicio"])
        print(data["fecha_final"])
        print(data["total"])
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
