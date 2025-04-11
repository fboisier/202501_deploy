import os
from flask_app import app
from flask_app.controllers import usuarios 
from flask_app.controllers import autentificacion 
from flask_app.controllers import paises
from flask_app.controllers import comunas
from flask_app.controllers import direcciones
from flask_app.controllers import tipos_clientes
from flask_app.controllers import clientes
from flask_app.controllers import productos


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"), port=os.getenv("PUERTO"))
