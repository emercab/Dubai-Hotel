from models.model_micuenta import get_data_login


def buscar_cliente_reserva(valor_busqueda):
    usuario = get_data_login(valor_busqueda)
    
    if usuario == None or (usuario != None and len(usuario) <= 0):
        return {}

    diccionario = {}

    if usuario["TipoUsuarioId"] == 3:
        count = 0
        columns = usuario.keys()
        
        for item in usuario:
            if columns[count].lower() == "id" or columns[count].lower() == "nombres" or columns[count].lower() == "apellidos":
                diccionario[columns[count]] = item
            count += 1
    return diccionario