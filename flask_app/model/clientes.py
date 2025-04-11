from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.direcciones import Direccion
from flask_app.model.tipos_clientes import TipoCliente
from flask_app.model.productos import Producto
from flask import flash
import re

DNI_VALIDADOR_REGEX = re.compile(r"^[0-9]{3,}-[0-9]{5,}$")

class Cliente:

    def __init__(self, data):
        # nativas
        self.id = data["id"]
        self.dni = data["dni"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.direccion_id = data["direccion_id"]
        self.tipo_cliente_id = data["tipo_cliente_id"]
        self.eliminado = data["eliminado"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # generadas
        self.direccion = None
        self.tipo_cliente = None
        self.productos = []

    @staticmethod
    def validar(data):

        esta_todo_ok = True

        if len(data["dni"]) < 3:
            flash("El DNI tiene menos de 3 caracteres", "error")
            esta_todo_ok = False
        
        if not DNI_VALIDADOR_REGEX.match(data["dni"]):
            flash("Debe contener exactamente un guión (-) Mínimo 3 caracteres antes del guión Mínimo 5 caracteres después del guión Debe tener al menos un número antes y después del guión", 
                "error"
            )
            esta_todo_ok = False

        if "-" not in data["dni"]:
            flash("El DNI debe contener al menos un guión (-)", "error")
            esta_todo_ok = False
    
        if len(data["nombre"]) < 3:
            flash("El nombre tiene menos de 3 caracteres", "error")
            esta_todo_ok = False

        if len(data["apellido"]) < 3:
            flash("El apellido tiene menos de 3 caracteres", "error")
            esta_todo_ok = False
        
        if not data["direccion_id"]:
            flash("Debes seleccionar una dirección", "error")
            esta_todo_ok = False

        if not data["tipo_cliente_id"]:
            flash("Debes seleccionar un tipo de cliente", "error")
            esta_todo_ok = False

        return esta_todo_ok

    @classmethod
    def get_all(cls):
        query = "SELECT id, dni, nombre, apellido, direccion_id, tipo_cliente_id, eliminado, created_at, updated_at FROM clientes WHERE eliminado = 0;"
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            cliente_instancia = cls(dato)
            cliente_instancia.direccion = Direccion.get(cliente_instancia.direccion_id)
            cliente_instancia.tipo_cliente = TipoCliente.get(cliente_instancia.tipo_cliente_id)
            instancias.append(cliente_instancia)
        return instancias
    
    @classmethod
    def get_all_with_relations(cls):
        query = """
        SELECT
            clientes.id, clientes.dni, clientes.nombre, clientes.apellido, clientes.direccion_id, 
            clientes.tipo_cliente_id, clientes.eliminado, clientes.created_at, clientes.updated_at,
            direcciones.id, direcciones.calle, direcciones.numero, direcciones.comuna_id, direcciones.created_at, direcciones.updated_at,
            tipos_clientes.id, tipos_clientes.nombre, tipos_clientes.created_at, tipos_clientes.updated_at
        FROM clientes 
        JOIN direcciones ON direcciones.id = clientes.direccion_id
        JOIN tipos_clientes ON tipos_clientes.id = clientes.tipo_cliente_id
        WHERE clientes.eliminado = 0
        """
        resultados = connectToMySQL().query_db(query)

        instancias = []
        for dato in resultados:
            cliente_instancia = cls(dato)
            
            dato_direccion = {
                'id': dato['direcciones.id'],
                'calle': dato['calle'],
                'numero': dato['numero'],
                'comuna_id': dato['comuna_id'],
                'created_at': dato['direcciones.created_at'],
                'updated_at': dato['direcciones.updated_at'],
            }
            
            dato_tipo_cliente = {
                'id': dato['tipos_clientes.id'],
                'nombre': dato['tipos_clientes.nombre'],
                'created_at': dato['tipos_clientes.created_at'],
                'updated_at': dato['tipos_clientes.updated_at'],
            }

            cliente_instancia.direccion = Direccion(dato_direccion)
            cliente_instancia.tipo_cliente = TipoCliente(dato_tipo_cliente)
            instancias.append(cliente_instancia)
        return instancias
    
    @classmethod
    def get(cls, id):
        query = """
        SELECT 
            clientes.id, dni, clientes.nombre, apellido, direccion_id, tipo_cliente_id, eliminado, clientes.created_at, clientes.updated_at,
            productos.id, productos.nombre, productos.created_at, productos.updated_at
        FROM
            clientes
                LEFT JOIN
            clientes_has_productos ON clientes.id = clientes_has_productos.cliente_id
                LEFT JOIN
            productos ON clientes_has_productos.producto_id = productos.id
        WHERE
            clientes.id = %(id)s AND eliminado = 0;
        """
        data = {
            'id': id
        }
        resultados = connectToMySQL().query_db(query, data)
        
        if resultados:
            instancia_cliente = cls(resultados[0])

            for resultado in resultados:
                datos_producto={
                    'id': resultado['productos.id'],
                    'nombre': resultado['productos.nombre'],
                    'created_at': resultado['productos.created_at'],
                    'updated_at': resultado['productos.updated_at'],
                }
                instancia_producto = Producto(datos_producto)
                instancia_cliente.productos.append(instancia_producto)

            return instancia_cliente
        return None

    @classmethod
    def save(cls, datos):
        query = """
        INSERT INTO clientes (dni, nombre, apellido, direccion_id, tipo_cliente_id, eliminado, created_at, updated_at) 
        VALUES (%(dni)s, %(nombre)s, %(apellido)s, %(direccion_id)s, %(tipo_cliente_id)s, 0, NOW(), NOW());
        """
        return connectToMySQL().query_db(query, datos)
    
    def update(self):
        query = """
                UPDATE clientes
                    SET
                        dni = %(dni)s,
                        nombre = %(nombre)s,
                        apellido = %(apellido)s,
                        direccion_id = %(direccion_id)s,
                        tipo_cliente_id = %(tipo_cliente_id)s,
                        updated_at = NOW()
                    WHERE id = %(id)s AND eliminado = 0;
                """
        
        datos = {
            'id': self.id,
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'direccion_id': self.direccion_id,
            'tipo_cliente_id': self.tipo_cliente_id
        }
        return connectToMySQL().query_db(query, datos)
    
    @classmethod
    def delete(cls, id):
        # Soft delete - actualiza el campo eliminado a 1 en lugar de eliminar el registro
        query = "UPDATE clientes SET eliminado = 1, updated_at = NOW() WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connectToMySQL().query_db(query, data)
        return True


    def save_producto(self, producto_id):
        query = """
        INSERT INTO clientes_has_productos (cliente_id, producto_id) VALUES (%(cliente_id)s, %(producto_id)s);
        """
        datos = {
            'cliente_id': self.id,
            'producto_id': producto_id
        }
        return connectToMySQL().query_db(query, datos)