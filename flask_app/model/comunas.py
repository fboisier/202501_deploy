from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.paises import Pais

class Comuna:

    def __init__(self, data):
        # nativas
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.pais_id = data["pais_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # generadas
        self.pais = None

    @classmethod
    def get_all(cls):
        query = "SELECT id, nombre, pais_id, created_at, updated_at FROM comunas;"
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            print("DATO:", dato)
            comuna_instancia = cls(dato)
            pais_instancia = Pais.get(comuna_instancia.pais_id)
            comuna_instancia.pais = pais_instancia
            instancias.append(comuna_instancia)
        return instancias
    
    @classmethod
    def get_all_with_country(cls):
        query = """
        SELECT
            comunas.id, comunas.nombre, comunas.pais_id, comunas.created_at, comunas.updated_at,
            paises.id, paises.nombre, paises.created_at, paises.updated_at
        FROM comunas JOIN paises ON paises.id = comunas.pais_id
        """
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            print("DATO:", dato)
            comuna_instancia = cls(dato)
            
            dato_pais = {
                'id': dato['paises.id'],
                'nombre': dato['paises.nombre'],
                'created_at': dato['paises.created_at'],
                'updated_at': dato['paises.updated_at'],
            }

            pais_instancia = Pais(dato_pais)
            comuna_instancia.pais = pais_instancia
            instancias.append(comuna_instancia)
        return instancias
    
    @classmethod
    def get(cls, id):
        query = f"SELECT id, nombre, pais_id, created_at, updated_at FROM comunas WHERE id = %(id)s;"
        data = {
            'id': id
        }
        resultados = connectToMySQL().query_db(query, data)
        instancia_nueva = cls(resultados[0])
        return instancia_nueva

    @classmethod
    def save(cls, datos):
        query = "INSERT INTO comunas (nombre, pais_id, created_at, updated_at) VALUES (%(nombre)s, %(pais_id)s, NOW(), NOW());"
        return connectToMySQL().query_db(query, datos)
    
    def update(self):
        query = """
                UPDATE comunas
                    SET
                        nombre = %(nombre)s,
                        pais_id = %(pais_id)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;
                """
        
        datos = {
            'id': self.id,
            'nombre': self.nombre,
            'pais_id': self.pais_id
        }
        return connectToMySQL().query_db(query, datos)
    
    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM comunas WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connectToMySQL().query_db(query, data)
        return True
