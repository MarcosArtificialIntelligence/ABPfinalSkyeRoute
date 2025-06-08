import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("Conexión a la base de datos MySQL exitosa")
    except Error as err:
        print(f"Error al conectar a la base de datos: '{err}'")
    return connection

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        # print("Operación realizada con éxito.") # Puedes comentar esto para menos salida
        return True
    except Error as err:
        print(f"Error al ejecutar la consulta: '{err}'")
        return False
    finally:
        cursor.close()

def read_query(connection, query, data=None):
    cursor = connection.cursor(buffered=True)
    result = None
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error al leer la consulta: '{err}'")
        return None
    finally:
        cursor.close()