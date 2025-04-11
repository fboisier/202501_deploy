from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.comunas import Comuna

class Direccion:

    def __init__(self, data):
        # nativas
        self.id = data["id"]
        self.calle = data["calle"]
        self.numero = data["numero"]
        self.comuna_id = data["comuna_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # generadas
        self.comuna = None

    @classmethod
    def get_all(cls):
        query = "SELECT id, calle, numero, comuna_id, created_at, updated_at FROM direcciones;"
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            direccion_instancia = cls(dato)
            comuna_instancia = Comuna.get(direccion_instancia.comuna_id)
            direccion_instancia.comuna = comuna_instancia
            instancias.append(direccion_instancia)
        return instancias
    
    @classmethod
    def get_all_with_comuna(cls):
        query = """
        SELECT
            direcciones.id, direcciones.calle, direcciones.numero, direcciones.comuna_id, direcciones.created_at, direcciones.updated_at,
            comunas.id, comunas.nombre, comunas.pais_id, comunas.created_at, comunas.updated_at
        FROM direcciones JOIN comunas ON comunas.id = direcciones.comuna_id
        """
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            direccion_instancia = cls(dato)
            
            dato_comuna = {
                'id': dato['comunas.id'],
                'nombre': dato['nombre'],
                'pais_id': dato['pais_id'],
                'created_at': dato['comunas.created_at'],
                'updated_at': dato['comunas.updated_at'],
            }

            comuna_instancia = Comuna(dato_comuna)
            direccion_instancia.comuna = comuna_instancia
            instancias.append(direccion_instancia)
        return instancias
    
    @classmethod
    def get(cls, id):
        query = f"SELECT id, calle, numero, comuna_id, created_at, updated_at FROM direcciones WHERE id = %(id)s;"
        data = {
            'id': id
        }
        resultados = connectToMySQL().query_db(query, data)
        direccion_instancia = cls(resultados[0])
        comuna_instancia = Comuna.get(direccion_instancia.comuna_id)
        direccion_instancia.comuna = comuna_instancia
        return direccion_instancia

    @classmethod
    def save(cls, datos):
        query = "INSERT INTO direcciones (calle, numero, comuna_id, created_at, updated_at) VALUES (%(calle)s, %(numero)s, %(comuna_id)s, NOW(), NOW());"
        return connectToMySQL().query_db(query, datos)
    
    def update(self):
        query = """
                UPDATE direcciones
                    SET
                        calle = %(calle)s,
                        numero = %(numero)s,
                        comuna_id = %(comuna_id)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;
                """
        
        datos = {
            'id': self.id,
            'calle': self.calle,
            'numero': self.numero,
            'comuna_id': self.comuna_id
        }
        return connectToMySQL().query_db(query, datos)
    
    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM direcciones WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connectToMySQL().query_db(query, data)
        return True
