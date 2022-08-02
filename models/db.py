import sqlite3
from sqlite3 import Error

DATABASE = './models/db_dubai_hotel.db'


# Función que servirá a los modelos para conectarse con la DB, 
# retorna un objeto de tipo conexión o None en caso de que haya error
def conectar():
    try:
        con = sqlite3.connect(DATABASE)
    except Error:
        print(f"Error: {Error}")
        return None
    return con
