# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Mi Cuenta

from models.db import conectar


def get_data_login(login_field):
    # Retorna los campos usados para login: username, cedula o email
    # y password registrado en DB del campo usado para hacer login que 
    # recibe. En caso de que no exista, retorna None
    
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = f"""
            SELECT username, cedula, email, password, nombres, apellidos, tipoUsuarioId
            FROM usuarios
            WHERE username='{login_field}' or cedula='{login_field}' or email='{login_field}' 
        """
        # Ejecuto la sentencia SQL
        cursor.execute(sentence)
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

