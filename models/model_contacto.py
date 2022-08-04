# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Contacto

from models.db import conectar

def send_data_contact(name,email,contact):
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
            INSERT INTO contacto (nombre, email, mensaje)
            VALUES( '{name}', '{email}', '{contact}');
        """
        print(sentence)
        # Ejecuto la sentencia SQL
        cursor.execute(sentence)
        conn.commit()
    except Exception as error:
        # Si hay un error, lo imprimo y retorno None
        print(f"Error: {error}")
        return None
    finally:
        # Pase lo que pase, cierro la conexión
        conn.close()
    
    return cursor.lastrowid
# Fin de send_data_contact