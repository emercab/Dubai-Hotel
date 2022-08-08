# Acá van todas las clases y métodos que controlarán y harán la lógica
# de las operaciones sobre las rutas de Mi Cuenta. Desde acá se enviará las
# respuestas a las rutass

from flask import session
from flask_bcrypt import check_password_hash, generate_password_hash
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
            session["user_login"] = True
            session["username"] = data[0]
            session["cedula"] = data[1]
            session["email"] = data[2]
            session["nombres"] = data[4]
            session["apellidos"] = data[5]
            session["tipo_usuario"] = data[6]
            session["ciudad"] = data[7]
            session["direccion"] = data[8]
            session["celular"] = data[9]
            session["id"] = data[10]
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
    session.pop("user_login", None)
    session.pop("nombres", None)
    session.pop("apellidos", None)
    session.pop("tipo_usuario", None)
    session.pop("ciudad", None)
    session.pop("direccion", None)
    session.pop("celular", None)
    session.pop("id", None)
# Fin de destroy_session()


def get_nombre_corto(nombre):
    # Recibe los nombres de un usuario y retorna solamente el primero

    if nombre.find(" ") != -1:
        return nombre[0:nombre.find(" ")]
    else:
        return nombre.capitalize()
# Fin de get_nombre_corto()


def data_to_template(title:str):
    # Inicializo variables con valores por default para pasar al template.
    # Si el usuario hizo login cambio sus valores por los que están
    # almacenados en las variables de sesión.
    user_login = False
    nombre = ""
    tipo_usuario = 0
    nombres = ""
    apellidos = ""
    email = ""
    cedula = ""
    ciudad = ""
    direccion = ""
    celular = ""
    id = ""
    # Reviso si el usuario ha hecho login para enviar variables de sesión
    if "user_login" in session:
        # Significa que existe una variable de sesión user_login
        # creada cuando el usuario hizo login. Guardo dicha variable
        # y demás variables de sesión que le pasaré al template
        user_login = True
        nombre = get_nombre_corto(session["nombres"]).capitalize()
        tipo_usuario = session["tipo_usuario"]
        nombres = session["nombres"]
        apellidos = session["apellidos"]
        email = session["email"]
        cedula = session["cedula"]
        ciudad = session["ciudad"]
        direccion = session["direccion"]
        celular = session["celular"]
        id = session["id"]
    
    # Preparo datos a enviar al template
    data = {
        "titulo_head": title,
        "user_login": user_login,
        "nombre": nombre,
        "tipo_usuario": tipo_usuario,
        "nombres": nombres,
        "apellidos": apellidos,
        "email": email,
        "cedula": cedula,
        "ciudad": ciudad,
        "direccion": direccion,
        "celular": celular,
        "id": id,
    }

    return data
# End of data_to_template()


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
# Fin de register_user()


def change_password(cedula, password, new_password):
    # Cambia el password del usuario

    # Inicializo los valores que retornaré
    respuesta = {
        "exito": False,
        "error": "",
    }

    data_user = model.get_data_login(cedula)
    if data_user == None:
        respuesta["error"] = "No se pudo obtener datos del usuario."
        return respuesta
    else:
        # Comparo password enviado con el guardado
        user_password = data_user[3]
        if not check_password_hash(user_password, password):
            # Significa que el password actual no coincide con el del usuario,
            # por tanto se anula el cambio de clave y se envía el mensaje de error.
            respuesta["error"] = "La contraseña actual es incorrecta."
        else:
            # Significa que la contraseña actual es correcta y se hace el
            # cambio de contraseña, mando id del usuario y nuevo password
            new_password_hash = generate_password_hash(new_password)
            respuesta["exito"] = model.update_password(data_user[10], new_password_hash)
            if not respuesta["exito"]:
                respuesta["error"] = "No se pudo actualizar la nueva contraseña."  
        return respuesta
# Fin de change_password()

