from flask import Flask, render_template, session
from admin.routes.admin import bp_admin
from routes.habitaciones import bp_habitaciones
from routes.contacto import bp_contacto
from routes.micuenta import bp_micuenta
from routes.api import bp_api
import controllers.controller_micuenta as controller
from settings.config import Configuration

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

app.register_blueprint(bp_api)

# Cargamos la página principal (home)
@app.route("/", methods=["GET"])
def index():
    # Preparo datos a enviar a la vista
    data = controller.data_to_template("Home")
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host='localhost', port=5005, debug=True)
