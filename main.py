from flask import Flask, render_template, session
from admin.routes.admin import bp_admin
from routes.habitaciones import bp_habitaciones
from routes.contacto import bp_contacto
from routes.micuenta import bp_micuenta
from settings.config import Configuration
import controllers.controller_micuenta as controller

app = Flask(__name__)
# Cargo las opciones de configuración de la app
app.config.from_object(Configuration)


# Me vinculo con el route de los endpoints de /admin
app.register_blueprint(bp_admin)

# Me vinculo con el route de los endpoints de /habitaciones
app.register_blueprint(bp_habitaciones)

# Me vinculo con el route de los endpoints de /contacto
app.register_blueprint(bp_contacto)

# Me vinculo con el route de los endpoints de /mi-cuenta
app.register_blueprint(bp_micuenta)


# Cargamos la página principal (home)
@app.route("/", methods=["GET"])
def index():
    # Inicializo variables con valores por default para pasar al template.
    # Si el usuario hizo login cambio sus valores por los que están
    # almacenados en las variables de sesión.
    user_login = False
    nombre = ""
    # Reviso si el usuario ha hecho login para enviar variables de sesión
    if "user_login" in session:
        # Significa que existe una variable de sesión user_login
        # creada cuando el usuario hizo login. Guardo dicha variable
        # en otra variable del mismo nombre que le pasaré al template
        user_login = True
        nombre = controller.get_nombre_corto(session["nombres"])
    
    # Preparo datos a enviar al template
    data = {
        "titulo_head": "Home",
        "user_login": user_login,
        "nombre": nombre,
    }
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host='localhost', port=5005, debug=True)
