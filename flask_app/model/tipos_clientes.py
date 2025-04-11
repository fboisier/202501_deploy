from flask_app.config.mysqlconnection import connectToMySQL

class TipoCliente:

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data["nombre"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT id, nombre, created_at, updated_at FROM tipos_clientes;"
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            instancia_nueva = cls(dato)
            instancias.append(instancia_nueva)
        return instancias
    
    @classmethod
    def get(cls, id):
        query = "SELECT id, nombre, created_at, updated_at FROM tipos_clientes WHERE id = %(id)s;"
        data = {
            'id': id
        }
        resultados = connectToMySQL().query_db(query, data)
        instancia_nueva = cls(resultados[0])
        return instancia_nueva

    @classmethod
    def save(cls, datos):
        query = "INSERT INTO tipos_clientes (nombre, created_at, updated_at) VALUES (%(nombre)s, NOW(), NOW());"
        return connectToMySQL().query_db(query, datos)
    
    def update(self):
        query = """
                UPDATE tipos_clientes
                    SET
                        nombre = %(nombre)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;
                """
        
        datos = {
            'id': self.id,
            'nombre': self.nombre
        }
        return connectToMySQL().query_db(query, datos)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM tipos_clientes WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connectToMySQL().query_db(query, data)
        return True
