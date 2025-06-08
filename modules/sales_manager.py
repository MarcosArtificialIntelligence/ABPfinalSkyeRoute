import datetime
from modules.db_manager import execute_query, read_query
# Importar listar_clientes y listar_destinos para usarlos en registrar_venta
from modules.client_manager import listar_clientes
from modules.destination_manager import listar_destinos


def registrar_venta(connection):
    print("\n--- REGISTRAR NUEVA VENTA ---")

    clientes = listar_clientes(connection)
    if not clientes:
        print("No hay clientes registrados. Registre uno primero.")
        return

    cliente_existe = False
    id_cliente = None
    while not cliente_existe:
        try:
            id_cliente = int(input("Ingrese el ID del cliente para la venta: "))
            check_query = "SELECT id_cliente FROM clientes WHERE id_cliente = %s"
            if read_query(connection, check_query, (id_cliente,)):
                cliente_existe = True
            else:
                print(f"Cliente con ID {id_cliente} no encontrado. Intente de nuevo.")
        except ValueError:
            print("ID inválido. Por favor, ingrese un número.")

    destinos = listar_destinos(connection)
    if not destinos:
        print("No hay destinos disponibles. Registre uno primero.")
        return

    destino_existe = False
    id_destino = None
    while not destino_existe:
        try:
            id_destino = int(input("Ingrese el ID del destino para la venta: "))
            check_query = "SELECT id_destino, costo_base FROM destinos WHERE id_destino = %s"
            destino_data = read_query(connection, check_query, (id_destino,))
            if destino_data:
                id_destino, costo_base_destino = destino_data[0]
                destino_existe = True
            else:
                print(f"Destino con ID {id_destino} no encontrado. Intente de nuevo.")
        except ValueError:
            print("ID inválido. Por favor, ingrese un número.")

    costo_venta = costo_base_destino

    query = "INSERT INTO ventas (id_cliente, id_destino, costo_venta) VALUES (%s, %s, %s)"
    data = (id_cliente, id_destino, costo_venta)
    execute_query(connection, query, data)
    print(f"Venta registrada para el cliente ID {id_cliente} y destino ID {id_destino} por un costo de ${costo_venta:.2f}.")


def listar_ventas(connection):
    query = """
    SELECT
        v.id_venta,
        c.razon_social,
        d.ciudad,
        d.pais,
        v.fecha_venta,
        v.costo_venta,
        v.estado_venta,
        v.fecha_anulacion
    FROM
        ventas v
    JOIN
        clientes c ON v.id_cliente = c.id_cliente
    JOIN
        destinos d ON v.id_destino = d.id_destino
    ORDER BY
        v.id_venta DESC;
    """
    ventas = read_query(connection, query)
    if ventas:
        print("\n--- LISTADO DE VENTAS ---")
        print("{:<5} {:<25} {:<20} {:<15} {:<20} {:<15} {:<12} {:<20}".format(
            "ID", "Cliente", "Ciudad", "País", "Fecha Venta", "Costo", "Estado", "Fecha Anulación"
        ))
        print("-" * 155)
        for venta in ventas:
            id_v, cliente_rs, ciudad_d, pais_d, fecha_v, costo_v, estado_v, fecha_a = venta

            fecha_venta_str = fecha_v.strftime("%Y-%m-%d %H:%M") if fecha_v else "N/A"
            fecha_anulacion_str = fecha_a.strftime("%Y-%m-%d %H:%M") if fecha_a else "N/A"

            print("{:<5} {:<25} {:<20} {:<15} {:<20} {:<15.2f} {:<12} {:<20}".format(
                id_v, cliente_rs, ciudad_d, pais_d, fecha_venta_str, costo_v, estado_v, fecha_anulacion_str
            ))
        print("--------------------------")
    else:
        print("No hay ventas registradas.")
    return ventas

def anular_venta(connection):
    print("\n--- ANULAR VENTA (Botón de Arrepentimiento) ---")
    listar_ventas(connection)
    if not read_query(connection, "SELECT id_venta FROM ventas"):
        return

    try:
        id_venta = int(input("Ingrese el ID de la venta a anular: "))
    except ValueError:
        print("ID inválido. Por favor, ingrese un número.")
        return

    check_query = "SELECT estado_venta, fecha_venta FROM ventas WHERE id_venta = %s"
    venta_data = read_query(connection, check_query, (id_venta,))

    if not venta_data:
        print(f"No se encontró una venta con ID {id_venta}.")
        return

    estado_actual, fecha_venta = venta_data[0]

    if estado_actual == 'Anulada':
        print(f"La venta con ID {id_venta} ya está anulada.")
        return

    tiempo_transcurrido = datetime.datetime.now() - fecha_venta

    DIAS_ARREPENTIMIENTO = 60
    SEGUNDOS_MAXIMOS = DIAS_ARREPENTIMIENTO * 24 * 60 * 60 

    if tiempo_transcurrido.total_seconds() > SEGUNDOS_MAXIMOS:
        print(f"No se puede anular la venta con ID {id_venta}.")
        print(f"Ha pasado más de {DIAS_ARREPENTIMIENTO} días desde su registro.")
        return

    query = """
    UPDATE ventas
    SET estado_venta = 'Anulada', fecha_anulacion = %s
    WHERE id_venta = %s
    """
    fecha_anulacion = datetime.datetime.now()
    data = (fecha_anulacion, id_venta)

    if execute_query(connection, query, data):
        print(f"Venta con ID {id_venta} anulada exitosamente. Fecha de anulación: {fecha_anulacion.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Error al anular la venta con ID {id_venta}.")

def menu_ventas(connection):
    while True:
        print("\n===== GESTIÓN DE VENTAS =====")
        print("1. Registrar venta")
        print("2. Listar ventas")
        print("3. Anular venta (Botón de Arrepentimiento)")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_venta(connection)
        elif opcion == '2':
            listar_ventas(connection)
        elif opcion == '3':
            anular_venta(connection)
        elif opcion == '4':
            break
        else:
            print("Opción inválida. Intente de nuevo.")