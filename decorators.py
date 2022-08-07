# En este archivo van a quedar todas las funciones decoradoras
# que se van a usar en todo el proyecto. Serán 3 principalmente:
#   - login_required: comprobará que un usuario haya hecho login
#   - admin_required: comprobará que se tenga el rol de admninistrador
#   - superadmin_required: comprobará que se tenga el rol de super admnin.

from functools import wraps
from flask import redirect, url_for, session


# login_required
def login_required(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #codigo del decorador
        if "user_login" in session:
            return function(*args, **kws)
        return redirect(url_for('index'))
    return decorator_function


#valida si la persona es admin o superadmin
def is_administrativo(function):
    @wraps(function)
    def decorator(*args, **kws):
        if "tipo_usuario" in session and session["tipo_usuario"] == 1 or session["tipo_usuario"] == 2:
            return function(*args, **kws)

        #si no es un admin o super admin, retorna al index
        return redirect(url_for('index'))
    return decorator


# superadmin_required. se llama siempre del @is_administrativo
# solo el superadmin puede acceder a ciertas rutas.
def superadmin_required(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #si es superadmin
        if session["tipo_usuario"] == 1:
            return function(*args, **kws)

        return redirect('/admin') 
    return decorator_function


# only_clientes
def only_clientes(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #codigo del decorador
        if "tipo_usuario" in session and session["tipo_usuario"] == 3:
            return function(*args, **kws)
        return redirect(url_for('index'))
    return decorator_function
