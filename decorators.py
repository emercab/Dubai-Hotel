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


# admin_required
def admin_required(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #codigo del decorador
        if False:
            return redirect(url_for('index'))

        return function(*args, **kws)

    return decorator_function


# superadmin_required
def superadmin_required(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #codigo del decorador
        if False:
            return redirect(url_for('index'))

        return function(*args, **kws)

    return decorator_function
