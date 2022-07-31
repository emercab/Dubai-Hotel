from functools import wraps
from flask import redirect, url_for


#admin_required
def hola_decorator(function):
    @wraps(function)
    def decorator_function(*args, **kws):
        #codigo del decorador
        if False:
            return redirect(url_for('index'))

        return function(*args, **kws)

    return decorator_function