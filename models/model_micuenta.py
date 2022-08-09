# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Mi Cuenta

from models.db import conectar


def get_data_login(login_field:str):
    # Retorna los campos usados para login: username, cedula o email
    # y password registrado en DB del campo usado para hacer login que 
    # recibe. En caso de que no exista, retorna None
    
    try:
        # Me conecto a la DB
        conn = conectar()
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

