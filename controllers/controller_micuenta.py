# Acá van todas las clases y métodos que controlarán y harán la lógica
# de las operaciones sobre las rutas de Mi Cuenta. Desde acá se enviará las
# respuestas a las rutass

from flask import session
from flask_bcrypt import check_password_hash
import models.model_micuenta as model


def check_login(username, password):
    # Recibe un username y un password y revisa que se haga un login
    # válido. Retorna 1 si el login es correcto, 2 si el username existe
    # en DB pero el password es incorrecto y 0 si tanto username y
    # password no existen en la DB
    
    # Pido al modelo los datos de login del usuario
    data = model.get_data_login(username)
    
    # Reviso la respuesta de la consulta
    if data != None:
        # Significa que encontró al usuario en la DB
        # Ahora, reviso si la clave ingresada coincide con la del usuario
        user_password = data[3]
        if check_password_hash(user_password, password):
            # Significa que la clave ingresada coincide con la del usuario
            # y el login es correcto

            # Creo las variables de sesión con los datos del usuario
            # obtenidos de la DB
            session["username"] = data[0]
            session["cedula"] = data[1]
            session["email"] = data[2]
            session["nombres"] = data[4]
            session["apellidos"] = data[5]
            session["tipo_usuario"] = data[6]
            session["user_login"] = True
            return 1
        else:
            # Significa que la clave ingresada no coincide con la del usuario
            return 2
    else:
        # Significa que no encontró al usuario en la DB
        return 0
# Fin de check_login()


def destroy_session():
    # Destruye todas las variables de sesión creadas tras el login exitoso
    session.pop("username", None)
    session.pop("cedula", None)
    session.pop("email", None)
    session.pop("nombres", None)
    session.pop("apellidos", None)
    session.pop("tipo_usuario", None)
    session.pop("user_login", None)
# Fin de destroy_session()


def get_nombre_corto(nombre):
    # Recibe los nombres de un usuario y retorna solamente el primero

    if nombre.find(" ") != -1:
        return nombre[0:nombre.find(" ")]
    else:
        return nombre.capitalize()
# Fin de get_nombre_corto()


def crear_username(nombres, apellidos):
    # Crea un nombre de usuario único a partir de los nombres y apellidos y lo retorna
    
    # Variables para separar nombres y apellidos
    nombre1 = ""
    nombre2 = ""
    apellido1 = ""

    #Verifico si vienen dos nombres para separarlos
    if nombres.find(" ") == -1:
        # Significa que viene un solo nombre
        nombre1 = nombres
    else:
        # Significa que hay dos nombres y los separo
        nombre1 = nombres[0:nombres.find(" ")]
        nombre2 = nombres[nombres.find(" ") + 1:]

    #Verifico si vienen dos apellidos para separarlos
    if apellidos.find(" ") == -1:
        # Significa que viene un solo nombre
        apellido1 = apellidos
    else:
        # Significa que hay dos nombres y los separo
        apellido1 = apellidos[0:apellidos.find(" ")]

    # Armo username inicial a partir de primera letra mayúscula
    # del nombre1, más primera letra minúscula del nombre 2 (si lo hay),
    # más el apellido1 en minúsculas
    if nombre2 == "":
        username = nombre1[0].upper() + apellido1.lower()
    else:
        username = nombre1[0].upper() + nombre2[0].lower() + apellido1.lower()
    
    # Ahora verifico que no exista otro mismo username en la DB y en caso
    # afirmativo se le añade un número consecutivo
    n = 1
    base = username
    while model.ya_existe(username, "username", "usuarios"):
        username = base + str(n)
        n += 1
    
    return username
# Fin de crear_username


def register_user(data_user:dict):
    # Registra los datos del usuario recibidos en el diccionario data_user
    # y los registra en la DB. Retorna un diccionario con un indicador de
    # registro exitoso (True o False) y un mensaje de error (si lo hubo)

    # Inicializo los valores que retornaré
    respuesta = {
        "registro_exitoso": False,
        "error": "",
    }

    # Antes de registrar la info del usuario se debe validar que no exista
    # un registro duplicado en los campos claves para el login:
    # username, cedula y email

    if model.ya_existe(data_user["cedula"], "cedula", "usuarios"):
        respuesta["error"] = "Ya existe un usuario con la cédula ingresada."
    elif model.ya_existe(data_user["email"], "email", "usuarios"):
        respuesta["error"] = "Ya existe un usuario con el email ingresado."
    else:
        # Significa que no hay registros duplicados y se puede guardar la info        
        respuesta["registro_exitoso"] = model.save_data_user(data_user)
    
    return respuesta
