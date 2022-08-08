# Acá van todas las clases y métodos que controlarán y harán la lógica
# de las operaciones sobre las rutas de Contacto. Desde acá se enviará las
# respuestas a las rutas

import models.model_contacto as model


def send_contacto(name,email,contact):
    data = model.send_data_contact(name,email,contact)

    if data != None:
        print('Solicitud de contacto creada')
    else:
        print('Hubo un error')
    return data