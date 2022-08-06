import sqlite3
from models.db import conectar


def select_tipo_usuario(tipo_usuario_session):
    try:
        conn = conectar()  
        cursor = conn.cursor()

        if tipo_usuario_session:
            if tipo_usuario_session == 1:
                query = "select Id, Descripcion from TipoUsuario"
            else:
                query = "select Id, Descripcion from TipoUsuario where Id = 3 or Descripcion like '%cliente%'"
            cursor.execute(query)

            return cursor.fetchall()
    except Exception as e:
        print(f'select_tipo_usuario {e}')
        return None
    finally:
        cursor.close()
        conn.close()
    return None


#consulta solo un usuario
def select_usuario(id_usuario, tipo_usuario_session=None):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if id_usuario:
            query = """
                select Usuarios.Id, Username, Nombres, Apellidos, Cedula, Ciudad, Direccion, Celular, TipoUsuarioId, Email, Password,
                    FechaRegistro, Activo
                from Usuarios
                where Id = ?
            """

            cursor.execute(query, [id_usuario])

            return cursor.fetchone() #retona una sola tupla
    except Exception as e:
        print(f'select_tipo_usuario {e}')
        return None
    finally:
        cursor.close()
        conn.close()
    return None
#fin select usuarios


#consulta todos los usuarios
def select_usuarios(tipo_usuario_session):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if tipo_usuario_session:
            if tipo_usuario_session == 1: #si es superadmin
                query = """
                    select Usuarios.Id, Username, Nombres, Apellidos, Cedula, Ciudad, Direccion, Celular, TipoUsuarioId, Email, Password,
                        FechaRegistro, Activo, Descripcion as NombreTipoUsuario, Row_Number() over (order by TipoUsuario.Id) as Row
                    from Usuarios
                        inner join TipoUsuario on TipoUsuario.Id = TipoUsuarioId
                    order by Activo desc, TipoUsuario.Id asc, Usuarios.Id
                """
            else:
                query = """
                    select Usuarios.Id, Username, Nombres, Apellidos, Cedula, Ciudad, Direccion, Celular, TipoUsuarioId, Email, Password, 
                        FechaRegistro, Activo, Descripcion as NombreTipoUsuario, Row_Number() over (order by TipoUsuario.Id) as Row
                    from Usuarios
                        inner join TipoUsuario on TipoUsuario.Id = TipoUsuarioId
                    where TipoUsuario.Id = 3 or Descripcion like '%cliente%'
                    order by Activo desc, TipoUsuario.Id asc, Usuarios.Id
                """
            cursor.execute(query)

            return cursor.fetchall()
    except Exception as e:
        print(f'select_tipo_usuarios {e}')
        return None
    finally:
        cursor.close()
        conn.close()
    return None
#fin select usuarios


def create_usuario(id_usuario, usuario, nombres, apellidos, cedula, celular, email, tipo_usuario, clave_encryp, ciudad, direccion):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_usuario != None:
            query = """
                update Usuarios
                    set Username = ?,
                        Nombres = ?,
                        Apellidos = ?,
                        Cedula = ?,
                        Ciudad = ?,
                        Direccion = ?,
                        Celular = ?,
                        TipoUsuarioId = ?,
                        Email = ?,
                        Password = ?
                where Id = ?
            """
            datos = (usuario, nombres, apellidos, cedula, ciudad, direccion, celular, tipo_usuario, email, clave_encryp, id_usuario)
        else:
            query = """
                insert into Usuarios (username, nombres, apellidos, cedula, ciudad, direccion, celular, tipoUsuarioId, email, 
                    password, fechaRegistro, activo)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, DateTime('now'), 1)
            """
            datos = (usuario, nombres, apellidos, cedula, ciudad, direccion, celular, tipo_usuario, email, clave_encryp)

        cursor.execute(query, datos)
        conn.commit()

        last_id = id_usuario if id_usuario else cursor.lastrowid 
    except Exception as error:
        print(f'insert usuarios {error}')
        return None
    finally:
        cursor.close()
        conn.close()

    return last_id
#fin create habtiacion


def update_estado_usuario(id_usuario, estado):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if id_usuario != None:
            query = """
                update Usuarios
                    set Activo = ?
                where Id = ?
            """
            datos = (estado, id_usuario)

            cursor.execute(query, datos)
            conn.commit()
            return 1
    except Exception as error:
        print(f'estado usuario. {error}')
        return None
    finally:
        cursor.close()
        conn.close()
    return None


def select_existe_usuario(id_usuario, username, cedula, email):
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sentence = """
            select Id, Username, Cedula, Email
            from Usuarios
            where Id <> ? and (Username = ? or Cedula = ? or Email = ?)
        """

        id_usuario = 0 if id_usuario == None else id_usuario

        print((id_usuario, username, cedula, email))

        cursor.execute(sentence, (id_usuario, username, cedula, email))
        result = cursor.fetchone()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno None
        print(f"Error: {error}")
        return None
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return result