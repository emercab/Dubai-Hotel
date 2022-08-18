import sqlite3
from models.db import conectar


def create_habitacion(id_habitacion, numero, precio):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_habitacion:
            query = """
                update Habitaciones
                    set Numero = ?,
                        Precio = ?
                where Id = ?
            """
            datos = (numero, precio, id_habitacion)
        else:
            query = """
                insert into Habitaciones (Numero, Precio, Calificacion, Activo)
                values (?, ?, Null, 1)
            """
            datos = (numero, precio)

        cursor.execute(query, datos)
        conn.commit()

        actualizar_precio_habitacion(precio, conn)

        #.lasrowid  -retorna el id del registro insertado
        last_id = id_habitacion if id_habitacion else cursor.lastrowid 
    except Exception as error:
        print(f'insert habitacion {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return last_id
#fin create habtiacion


def select_habitacion(id_habitacion=None):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if id_habitacion:
            cursor.execute("select Row_Number() over (order by Id) as Row, Id, Numero, Precio, IfNull(Calificacion, '') as Calificacion, Activo from Habitaciones where Id = ?", [id_habitacion])
            resultado = cursor.fetchone()
        else:
            cursor.execute("select Row_Number() over (order by Activo desc) as Row, Id, Numero, Precio, IfNull(Calificacion, '') as Calificacion, Activo from Habitaciones")
            resultado = cursor.fetchall()  
    except Exception as error:
        print(f'select_habitacion {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return resultado
#fin consultar habitacion


def update_estado_habitacion(id_habitacion, estado):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_habitacion:
            query = """
                update Habitaciones
                    set Activo = ?
                where Id = ?
            """
        
        cursor.execute(query, (estado, id_habitacion))
        conn.commit()
    except Exception as error:
        print(f'insert habitacion {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return 1
#fin remover habitacion

#actualiza el precio para todas las habitaciones
def actualizar_precio_habitacion(precio, connection):
    try:
        if connection == None:
            connection = conectar()

        cursor = connection.cursor()

        query = """
            update Habitaciones
                set Precio = ?
        """

        cursor.execute(query, [precio])
        connection.commit()
    except Exception as error:
        raise error
    finally:
        cursor.close()
        connection.close()