from flask_app.model.modelo_base import BaseModelo

class UsuarioAvanzado(BaseModelo):

    tabla_nombre = "usuarios"
    campos = ['id','nombre','email', 'contraseña', 'created_at','updated_at']

    def __init__(self, data):
        super().__init__(data)