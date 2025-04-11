from flask_app.config.mysqlconnection import connectToMySQL


class BaseModelo:

    tabla_nombre = ""
    campos = []

    def __init__(self, data):
        for campo in self.campos:
            setattr(self, campo, data[campo])

    @classmethod
    def get_all(cls):
        campos_join = ", ".join(cls.campos)
        query = f"SELECT {campos_join} FROM {cls.tabla_nombre};"
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            instancia_nueva = cls(dato)
            instancias.append(instancia_nueva)
        return instancias
    
    @classmethod
    def get(cls, id):
        campos_join = ", ".join(cls.campos)
        query = f"SELECT {campos_join} FROM {cls.tabla_nombre} WHERE id = %(id)s;"
        data = {
            'id': id
        }
        resultados = connectToMySQL().query_db(query, data)
        instancia_nueva = cls(resultados[0])
        return instancia_nueva


    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM {cls.tabla_nombre} WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connectToMySQL().query_db(query, data)
        return True

    def update(self):
        campos_para_set = ", ".join([f"{campo} = %({campo})s" for campo in self.campos if campo != 'id'])
        campos_para_set += ", updated_at = NOW()"
        
        query = f"""
            UPDATE {self.tabla_nombre}
            SET {campos_para_set}
            WHERE id = %(id)s;
        """
        
        data = {campo: getattr(self, campo) for campo in self.campos}
        return connectToMySQL().query_db(query, data)