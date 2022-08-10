import sqlite3
from models.db import conectar


def create_reserva_admin(id_reserva, id_cliente, fecha_ingreso, fecha_salida, id_habitacion, total):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_reserva:
            query = """
                update Reservas
                    set HabitacionId = ?
                        FechaInicial = ?,
                        FechaFinal = ?,
                        Total = ?
                where Id = ?
            """
            datos = (id_habitacion, fecha_ingreso, fecha_salida, total, id_reserva)
        else:
            query = """
                insert into Habitaciones (HabitacionId, ClienteId, FechaInicial, FechaFinal, Total)
                values (?, ?, ?, ?, ?)
            """
            datos = (id_habitacion, id_cliente, fecha_ingreso, fecha_salida, total)

        cursor.execute(query, datos)
        conn.commit()

        #.lasrowid  -retorna el id del registro insertado
        last_id = id_reserva if id_reserva else cursor.lastrowid 
    except Exception as error:
        print(f'insert habitacion {error}')
        last_id = None
    finally:
        cursor.close()
        conn.close()

    return last_id


def select_reserva_admin(id_reserva=None):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if id_reserva:
            query = """
                select Row_Number() over (order by Reservas.Id desc) as Row, Reservas.Id, HabitacionId, ClienteId, FechaInicial, FechaFinal, Total,
                    IfNull(Nombres, '')|| ' ' ||IfNull(Apellidos, '') as NombreCompleto, Numero as NumeroHabitacion
                from Reservas
                    inner join Habitaciones on Habitaciones.Id = HabitacionId
                    inner join Usuarios on Usuarios.Id = ClienteId
                where Reservas.Id = ?
            """
            cursor.execute(query, [id_reserva])
            resultado = cursor.fetchone()
        else:
            query = """
                select Row_Number() over (order by Reservas.FechaInicial desc) as Row, Reservas.Id, HabitacionId, ClienteId, FechaInicial, FechaFinal, Total,
                    IfNull(Nombres, '')|| ' ' ||IfNull(Apellidos, '') as NombreCompleto, Numero as NumeroHabitacion
                from Reservas
                    inner join Habitaciones on Habitaciones.Id = HabitacionId
                    inner join Usuarios on Usuarios.Id = ClienteId
            """
            cursor.execute(query)
            resultado = cursor.fetchall()  
    except Exception as error:
        print(f'select_habitacion {error}')
        resultado = None
    finally:
        cursor.close()
        conn.close()

    return resultado

