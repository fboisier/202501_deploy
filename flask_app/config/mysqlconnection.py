import pymysql.cursors  # Utilizamos un cursos para interactuar con BD
import os

class MySQLConnection:  # Clase que permite generar instancia de conexión con BD

    def __init__(self):
        connection = pymysql.connect(
            host=os.getenv("HOST_BASEDATOS", "localhost"),
            user=os.getenv("USUARIO_BASEDATOS"),
            password=os.getenv("PASSWORD"),
            db=os.getenv("BASE_DATOS"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

        self.connection = connection  # Establecemos conexión con BD

    # El método que se encarga de la consulta

    def query_db(self, query, data=None):

        with self.connection.cursor() as cursor:

            try:

                query = cursor.mogrify(query, data)

                print("Running Query:", query)

                executable = cursor.execute(query, data)

                if query.lower().find("insert") >= 0:

                    # La consulta INSERT regresan el id del nuevo registro

                    self.connection.commit()

                    return cursor.lastrowid

                elif query.lower().find("select") >= 0:

                    # La consulta SELECT regresa una LISTA DE DICCIONARIOS con los datos

                    result = cursor.fetchall()

                    return result

                else:

                    # UPDATE y DELETE no regresan nada

                    self.connection.commit()
                    return True


            except Exception as e:

                # En caso de alguna falla, regresa FALSE

                print("Something went wrong", e)

                return False

            finally:

                # Cerramos conexión

                self.connection.close()


# connectToMySQL recibe el nombre de la base de datos y genera una instancia de MySQLConnection


def connectToMySQL():

    return MySQLConnection()
