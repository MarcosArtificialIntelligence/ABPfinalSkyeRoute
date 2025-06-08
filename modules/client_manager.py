from modules.db_manager import execute_query, read_query

def agregar_cliente(connection):
    print("\n--- AGREGAR NUEVO CLIENTE ---")
    razon_social = input("Ingrese razón social: ")
    cuit = input("Ingrese CUIT: ")
    correo_electronico = input("Ingrese correo electrónico: ")

    query = "INSERT INTO clientes (razon_social, cuit, correo_electronico) VALUES (%s, %s, %s)"
    data = (razon_social, cuit, correo_electronico)
    execute_query(connection, query, data)

def listar_clientes(connection):
    query = "SELECT id_cliente, razon_social, cuit, correo_electronico FROM clientes ORDER BY id_cliente"
    clientes = read_query(connection, query)
    if clientes:
        print("\n--- LISTADO DE CLIENTES ---")
        print("{:<5} {:<30} {:<20} {:<30}".format("ID", "Razón Social", "CUIT", "Email"))
        print("-" * 85)
        for cliente in clientes:
            print("{:<5} {:<30} {:<20} {:<30}".format(cliente[0], cliente[1], cliente[2], cliente[3]))
        print("--------------------------")
    else:
        print("No hay clientes registrados.")
    return clientes

def modificar_cliente(connection):
    print("\n--- MODIFICAR CLIENTE ---")
    listar_clientes(connection)
    if not read_query(connection, "SELECT id_cliente FROM clientes"):
        return

    try:
        id_cliente = int(input("Ingrese el ID del cliente a modificar: "))
    except ValueError:
        print("ID inválido. Por favor, ingrese un número.")
        return

    check_query = "SELECT razon_social, cuit, correo_electronico FROM clientes WHERE id_cliente = %s"
    current_data = read_query(connection, check_query, (id_cliente,))
    if not current_data:
        print(f"No se encontró un cliente con ID {id_cliente}.")
        return
    current_razon_social, current_cuit, current_email = current_data[0]

    nueva_razon_social = input(f"Ingrese nueva razón social (actual: {current_razon_social}): ") or current_razon_social
    nuevo_cuit = input(f"Ingrese nuevo CUIT (actual: {current_cuit}): ") or current_cuit
    nuevo_correo_electronico = input(f"Ingrese nuevo correo electrónico (actual: {current_email}): ") or current_email

    query = """
    UPDATE clientes
    SET razon_social = %s, cuit = %s, correo_electronico = %s
    WHERE id_cliente = %s
    """
    data = (nueva_razon_social, nuevo_cuit, nuevo_correo_electronico, id_cliente)
    execute_query(connection, query, data)


def eliminar_cliente(connection):
    print("\n--- ELIMINAR CLIENTE ---")
    listar_clientes(connection)
    if not read_query(connection, "SELECT id_cliente FROM clientes"):
        return

    try:
        id_cliente = int(input("Ingrese el ID del cliente a eliminar: "))
    except ValueError:
        print("ID inválido. Por favor, ingrese un número.")
        return

    check_query = "SELECT id_cliente FROM clientes WHERE id_cliente = %s"
    if not read_query(connection, check_query, (id_cliente,)):
        print(f"No se encontró un cliente con ID {id_cliente}.")
        return

    check_sales_query = "SELECT COUNT(*) FROM ventas WHERE id_cliente = %s"
    sales_count = read_query(connection, check_sales_query, (id_cliente,))[0][0]
    if sales_count > 0:
        print(f"Error: El cliente con ID {id_cliente} tiene {sales_count} venta(s) asociada(s) y no puede ser eliminado.")
        print("Primero debe eliminar las ventas relacionadas con este cliente.")
        return

    query = "DELETE FROM clientes WHERE id_cliente = %s"
    data = (id_cliente,)
    execute_query(connection, query, data)

def menu_clientes(connection):
    while True:
        print("\n===== GESTIÓN DE CLIENTES =====")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Modificar cliente")
        print("4. Eliminar cliente")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_cliente(connection)
        elif opcion == '2':
            listar_clientes(connection)
        elif opcion == '3':
            modificar_cliente(connection)
        elif opcion == '4':
            eliminar_cliente(connection)
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Intente de nuevo.")