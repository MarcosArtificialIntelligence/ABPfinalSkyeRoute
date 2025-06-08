from modules.db_manager import execute_query, read_query

def registrar_destino(connection):
    print("\n--- REGISTRAR NUEVO DESTINO ---")
    ciudad = input("Ingrese la ciudad del destino: ")
    pais = input("Ingrese el país del destino: ")
    try:
        costo_base = float(input("Ingrese el costo base del destino: "))
    except ValueError:
        print("Costo base inválido. Por favor, ingrese un número.")
        return

    query = "INSERT INTO destinos (ciudad, pais, costo_base) VALUES (%s, %s, %s)"
    data = (ciudad, pais, costo_base)
    execute_query(connection, query, data)
    print(f"Destino '{ciudad}, {pais}' registrado.")

def listar_destinos(connection):
    query = "SELECT id_destino, ciudad, pais, costo_base FROM destinos ORDER BY id_destino"
    destinos = read_query(connection, query)
    if destinos:
        print("\n--- LISTADO DE DESTINOS ---")
        print("{:<5} {:<25} {:<20} {:<15}".format("ID", "Ciudad", "País", "Costo Base"))
        print("-" * 65)
        for destino in destinos:
            print("{:<5} {:<25} {:<20} {:<15.2f}".format(destino[0], destino[1], destino[2], destino[3]))
        print("--------------------------")
    else:
        print("No hay destinos disponibles.")
    return destinos

def modificar_destino(connection):
    print("\n--- MODIFICAR DESTINO ---")
    listar_destinos(connection)
    if not read_query(connection, "SELECT id_destino FROM destinos"):
        return

    try:
        id_destino = int(input("Ingrese el ID del destino a modificar: "))
    except ValueError:
        print("ID inválido. Por favor, ingrese un número.")
        return

    check_query = "SELECT ciudad, pais, costo_base FROM destinos WHERE id_destino = %s"
    current_data = read_query(connection, check_query, (id_destino,))
    if not current_data:
        print(f"No se encontró un destino con ID {id_destino}.")
        return
    current_ciudad, current_pais, current_costo_base = current_data[0]

    nueva_ciudad = input(f"Ingrese nueva ciudad (actual: {current_ciudad}): ") or current_ciudad
    nuevo_pais = input(f"Ingrese nuevo país (actual: {current_pais}): ") or current_pais

    while True:
        try:
            nuevo_costo_str = input(f"Ingrese nuevo costo base (actual: {current_costo_base:.2f}): ")
            nuevo_costo_base = float(nuevo_costo_str) if nuevo_costo_str else current_costo_base
            break
        except ValueError:
            print("Costo base inválido. Por favor, ingrese un número.")


    query = """
    UPDATE destinos
    SET ciudad = %s, pais = %s, costo_base = %s
    WHERE id_destino = %s
    """
    data = (nueva_ciudad, nuevo_pais, nuevo_costo_base, id_destino)
    execute_query(connection, query, data)
    print(f"Destino con ID {id_destino} modificado.")

def eliminar_destino(connection):
    print("\n--- ELIMINAR DESTINO ---")
    listar_destinos(connection)
    if not read_query(connection, "SELECT id_destino FROM destinos"):
        return

    try:
        id_destino = int(input("Ingrese el ID del destino a eliminar: "))
    except ValueError:
        print("ID inválido. Por favor, ingrese un número.")
        return

    check_query = "SELECT id_destino FROM destinos WHERE id_destino = %s"
    if not read_query(connection, check_query, (id_destino,)):
        print(f"No se encontró un destino con ID {id_destino}.")
        return

    check_sales_query = "SELECT COUNT(*) FROM ventas WHERE id_destino = %s"
    sales_count = read_query(connection, check_sales_query, (id_destino,))[0][0]
    if sales_count > 0:
        print(f"Error: El destino con ID {id_destino} tiene {sales_count} venta(s) asociada(s) y no puede ser eliminado.")
        print("Primero debe eliminar las ventas relacionadas con este destino.")
        return

    query = "DELETE FROM destinos WHERE id_destino = %s"
    data = (id_destino,)
    execute_query(connection, query, data)
    print(f"Destino con ID {id_destino} eliminado.")

def menu_destinos(connection):
    while True:
        print("\n===== GESTIÓN DE DESTINOS =====")
        print("1. Registrar destino")
        print("2. Listar destinos")
        print("3. Modificar destino")
        print("4. Eliminar destino")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_destino(connection)
        elif opcion == '2':
            listar_destinos(connection)
        elif opcion == '3':
            modificar_destino(connection)
        elif opcion == '4':
            eliminar_destino(connection)
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Intente de nuevo.")