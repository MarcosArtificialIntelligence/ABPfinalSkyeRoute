# Main.py

from modules.db_manager import create_db_connection
from modules.client_manager import menu_clientes
from modules.destination_manager import menu_destinos
from modules.sales_manager import menu_ventas

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---

DB_HOST = "HOST DEL PROFESOR" # Coloque su IP o localhost
DB_USER = "root"
DB_PASSWORD = "CONTRASEÑA DEL MYSQL DEL PROFESOR" # Coloque su contraseña
DB_NAME = "skyeroute_ARRUTI" # o el nombre de la base de datos creada por los profes con script en la carpeta base de datos

# --- MENÚ PRINCIPAL DEL PROGRAMA ---
def main_menu():
    conn = create_db_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    if not conn:
        print("No se pudo establecer conexión con la base de datos. Saliendo del programa.")
        return

    while True:
        print("\n========== MENÚ PRINCIPAL SKYE ROUTE ==========")
        print("1. Gestión de Clientes")
        print("2. Gestión de Destinos")
        print("3. Gestión de Ventas")
        print("4. Salir")

        opcion_principal = input("Seleccione una opción: ")

        if opcion_principal == '1':
            menu_clientes(conn)
        elif opcion_principal == '2':
            menu_destinos(conn)
        elif opcion_principal == '3':
            menu_ventas(conn)
        elif opcion_principal == '4':
            print("Gracias por usar Skye Route. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

    conn.close()
    print("Conexión a la base de datos cerrada.")

# --- PUNTO DE INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    main_menu()