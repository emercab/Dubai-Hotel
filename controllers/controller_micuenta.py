# Acá van todas las clases y métodos que controlarán y harán la lógica
# de las operaciones sobre las rutas de Mi Cuenta. Desde acá se enviará las
# respuestas a las rutass

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
        print(user_password + " - " + password)
        if check_password_hash(user_password, password):
            # Significa que la clave ingresada coincide con la del usuario
            return 1
        else:
            # Significa que la clave ingresada no coincide con la del usuario
            return 2
    else:
        # Significa que no encontró al usuario en la DB
        return 0
# Fin de check_login()


