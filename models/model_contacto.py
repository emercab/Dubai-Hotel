# Acá irán todas las clases y métodos que van a acceder a la DB cuando se
# requiera en las rutas de Contacto

from models.db import conectar

def send_data_contact(name,email,contact):
    # Guarda mensaje de contacto en la DB. En caso de no tener éxito retorna None
    
    try:
        # Me conecto a la DB
        conn = conectar()
        # Creo el cursor que me permitirá operar en la DB
        cursor = conn.cursor()
        # Creo la sentencia SQL
        sentence = """
            INSERT INTO contacto (nombre, email, mensaje)
            VALUES(?, ?, ?);
        """
        valores = [name, email, contact]
        # Ejecuto la sentencia SQL
        cursor.execute(sentence, valores)
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