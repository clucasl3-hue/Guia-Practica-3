from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ClienteController, ProductoController, FacturaController

# 1. Inicialización de controladores
clientes = ClienteController()
productos = ProductoController()
facturas = FacturaController(clientes, productos)

# 2. Enlace seguro para validar integridad
clientes.facturas_controller = facturas


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito: imprimir_exito(mensaje)
    else: imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for obj in objetos:
        print(f"  {obj}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# FUNCIONES DE CLIENTES
# =====================================================================
def crear_cliente():
    imprimir_titulo("REGISTRAR CLIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "ruc": input("RUC / Cédula: "),
        "direccion": input("Dirección: ")
    }
    mostrar_resultado(*clientes.crear(datos))
    pausa()

def listar_clientes():
    imprimir_titulo("LISTA DE CLIENTES")
    mostrar_lista(clientes.leer(), "No hay clientes registrados.")
    pausa()

def buscar_cliente():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, apellido o RUC: ")
    mostrar_lista(clientes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_cliente():
    imprimir_titulo("VER CLIENTE POR ID")
    c = clientes.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_cliente():
    imprimir_titulo("ACTUALIZAR CLIENTE")
    id_c = pedir_entero("Id: ")
    c = clientes.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "ruc", "direccion"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*clientes.actualizar(id_c, cambios))
    pausa()

def eliminar_cliente():
    imprimir_titulo("ELIMINAR CLIENTE (Protegido)")
    id_c = pedir_entero("Id del cliente a eliminar: ")
    if id_c and confirmar("¿Confirma intentar eliminar este cliente?"):
        mostrar_resultado(*clientes.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE PRODUCTOS
# =====================================================================
def crear_producto():
    imprimir_titulo("REGISTRAR PRODUCTO")
    datos = {
        "nombre": input("Nombre del producto: "),
        "sku": input("SKU (ej. PROD-01): "),
        "precio": input("Precio unitario ($): "),
        "stock": input("Stock inicial: ")
    }
    mostrar_resultado(*productos.crear(datos))
    pausa()

def listar_productos():
    imprimir_titulo("CATÁLOGO DE PRODUCTOS")
    mostrar_lista(productos.leer(), "No hay productos registrados.")
    pausa()

def buscar_producto():
    imprimir_titulo("BUSCAR PRODUCTO")
    termino = input("Nombre o SKU: ")
    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_producto():
    imprimir_titulo("VER PRODUCTO POR ID")
    p = productos.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_producto():
    imprimir_titulo("ACTUALIZAR PRODUCTO")
    id_p = pedir_entero("Id: ")
    p = productos.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "sku", "precio", "stock"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*productos.actualizar(id_p, cambios))
    pausa()

def eliminar_producto():
    imprimir_titulo("ELIMINAR PRODUCTO")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este producto?"):
        mostrar_resultado(*productos.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE FACTURAS
# =====================================================================
def registrar_factura():
    imprimir_titulo("EMITIR FACTURA DE VENTA")
    imprimir_info("Clientes:")
    mostrar_lista(clientes.leer())
    imprimir_info("Productos:")
    mostrar_lista(productos.leer())

    cli_id = pedir_entero("\nId del cliente: ")
    prod_id = pedir_entero("Id del producto: ")
    cant = pedir_entero("Cantidad a comprar: ")

    datos = {
        "cliente_id": cli_id,
        "producto_id": prod_id,
        "cantidad": cant
    }
    mostrar_resultado(*facturas.crear(datos))
    pausa()

def listar_facturas():
    imprimir_titulo("LISTA DE FACTURAS")
    mostrar_lista(facturas.leer(), "No hay facturas registradas.")
    pausa()

def anular_factura():
    imprimir_titulo("ANULAR FACTURA")
    id_f = pedir_entero("Id de la factura: ")
    if id_f and confirmar("¿Confirma anular esta factura y devolver stock?"):
        mostrar_resultado(*facturas.eliminar(id_f))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚS Y MAIN
# =====================================================================
MENU_CLIENTES = {
    "1": ("Registrar", crear_cliente),
    "2": ("Ver todos", listar_clientes),
    "3": ("Buscar", buscar_cliente),
    "4": ("Ver por ID", ver_cliente),
    "5": ("Actualizar", actualizar_cliente),
    "6": ("Eliminar (Protegido)", eliminar_cliente),
    "0": ("Volver", None),
}

MENU_PRODUCTOS = {
    "1": ("Registrar", crear_producto),
    "2": ("Ver catálogo", listar_productos),
    "3": ("Buscar", buscar_producto),
    "4": ("Ver por ID", ver_producto),
    "5": ("Actualizar", actualizar_producto),
    "6": ("Eliminar", eliminar_producto),
    "0": ("Volver", None),
}

MENU_FACTURAS = {
    "1": ("Emitir factura", registrar_factura),
    "2": ("Ver facturas", listar_facturas),
    "3": ("Anular factura", anular_factura),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _, funcion = opciones[tecla]
        if funcion is None: break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA DE FACTURACIÓN Y VENTAS")
        print("  1. Clientes")
        print("  2. Productos")
        print("  3. Facturas")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("CLIENTES", MENU_CLIENTES)
        elif tecla == "2": ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)
        elif tecla == "3": ejecutar_menu("FACTURAS", MENU_FACTURAS)
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")