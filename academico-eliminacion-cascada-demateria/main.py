from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

# 1. Inicialización limpia de controladores
estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)

# 2. ENLACE CRUZADO SEGURO (Evita errores circulares para la cascada)
materias.matriculas_controller = matriculas


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
# FUNCIONES DE ESTUDIANTES
# =====================================================================
def crear_estudiante():
    imprimir_titulo("REGISTRAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet (ej. EST-001): "),
        "carrera": input("Carrera: ")
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()

def listar_estudiantes():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "No hay estudiantes registrados.")
    pausa()

def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido o carnet: ")
    mostrar_lista(estudiantes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    e = estudiantes.obtener(pedir_entero("Id: "))
    if not e: imprimir_error("No encontrado")
    else: mostrar_detalle(e)
    pausa()

def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    e = estudiantes.obtener(id_e)
    if not e:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(e, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_e, cambios))
    pausa()

def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este estudiante?"):
        mostrar_resultado(*estudiantes.eliminar(id_e))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE MATERIAS
# =====================================================================
def crear_materia():
    imprimir_titulo("REGISTRAR MATERIA")
    datos = {
        "nombre": input("Nombre de la materia: "),
        "codigo": input("Código (ej. MAT-101): "),
        "creditos": input("Créditos: "),
        "cupos": input("Cupos [30 por defecto]: ") or 30
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()

def listar_materias():
    imprimir_titulo("CATÁLOGO DE MATERIAS")
    mostrar_lista(materias.leer(), "No hay materias registradas.")
    pausa()

def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    m = materias.obtener(pedir_entero("Id: "))
    if not m: imprimir_error("No encontrado")
    else: mostrar_detalle(m)
    pausa()

def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_m = pedir_entero("Id: ")
    m = materias.obtener(id_m)
    if not m:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(m, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_m, cambios))
    pausa()

def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA (CASCADA)")
    id_m = pedir_entero("Id de la materia a eliminar: ")
    if id_m and confirmar("⚠ ¡Atención! Al eliminar esta materia se borrarán también todas sus matrículas en cascada. ¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_m))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE MATRÍCULAS
# =====================================================================
def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRÍCULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    est_id = pedir_entero("\nId del estudiante: ")
    mat_id = pedir_entero("Id de la materia: ")
    periodo = input("Periodo académico (ej. 2026-1): ")

    datos = {
        "estudiante_id": est_id,
        "materia_id": mat_id,
        "periodo": periodo
    }
    mostrar_resultado(*matriculas.crear(datos))
    pausa()

def listar_matriculas():
    imprimir_titulo("LISTA DE MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "No hay matrículas registradas.")
    pausa()

def calificar_matricula():
    imprimir_titulo("REGISTRAR / ACTUALIZAR NOTA")
    id_mat = pedir_entero("Id de la matrícula: ")
    nota = input("Ingrese la nota (0 a 20): ")
    mostrar_resultado(*matriculas.actualizar(id_mat, {"nota": nota}))
    pausa()

def cancelar_matricula():
    imprimir_titulo("CANCELAR MATRÍCULA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat and confirmar("¿Confirma cancelar esta matrícula y liberar cupo?"):
        mostrar_resultado(*matriculas.eliminar(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚS Y MAIN
# =====================================================================
MENU_ESTUDIANTES = {
    "1": ("Registrar", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por ID", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Registrar", crear_materia),
    "2": ("Ver catálogo", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por ID", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar (Cascada)", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),
    "2": ("Ver matrículas", listar_matriculas),
    "3": ("Calificar (Nota)", calificar_matricula),
    "4": ("Cancelar matrícula", cancelar_matricula),
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
        imprimir_titulo("SISTEMA ACADÉMICO UNIVERSITARIO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2": ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3": ejecutar_menu("MATRICULAS", MENU_MATRICULAS)
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