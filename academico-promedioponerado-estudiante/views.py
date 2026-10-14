from abc import ABC, abstractmethod
import os

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass


class EstudianteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "estudiantes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Estudiante.desde_diccionario(d) for d in self.gestor.leer()]
        self.matriculas_controller = None
        self.materias_controller = None

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def carnets_registrados(self, excepto_id=None):
        return {e.carnet.strip().upper() for e in self.lista if e.id != excepto_id and e.carnet}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {e.email for e in self.lista if e.id != id_actual}:
                return "Ese email ya está registrado"
        if "carnet" in datos:
            car = str(datos["carnet"]).strip().upper()
            if car in self.carnets_registrados(id_actual):
                return f"El carnet '{car}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_e):
        for e in self.lista:
            if e.id == id_e: return e
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [e for e in self.lista if t in e.nombre.lower() or t in e.apellido.lower() or t in e.carnet.lower()]

    # NUEVO MÉTODO SOLICITADO: Cálculo de promedio ponderado por créditos
    def calcular_promedio_estudiante(self, estudiante_id):
        if not self.matriculas_controller or not self.materias_controller:
            return 0.0

        # Filtramos las matrículas de este estudiante que tengan nota registrada
        matriculas_est = [
            m for m in self.matriculas_controller.leer() 
            if m.estudiante_id == estudiante_id and m.nota > 0.0
        ]

        if not matriculas_est:
            return 0.0

        suma_ponderada = 0.0
        total_creditos = 0

        for mat in matriculas_est:
            materia = self.materias_controller.obtener(mat.materia_id)
            if materia:
                suma_ponderada += (mat.nota * materia.creditos)
                total_creditos += materia.creditos

        if total_creditos == 0:
            return 0.0

        return round(suma_ponderada / total_creditos, 2)

    def siguiente(self):
        return max([e.id for e in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        estudiante = Estudiante(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["carnet"]).strip().upper(), str(datos.get("carrera", "")).strip().title()
        )
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante registrado: {estudiante.etiqueta()}"

    def actualizar(self, id_e, datos):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        error = self.validar(datos, id_e)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "carrera"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "carnet": val = val.upper()
            setattr(e, k, val)
        self.guardar()
        return True, f"Estudiante {id_e} actualizado"

    def eliminar(self, id_e):
        e = self.obtener(id_e)
        if not e: return False, "No existe"

        if self.matriculas_controller:
            tiene_matriculas = any(mat.estudiante_id == id_e for mat in self.matriculas_controller.leer())
            if tiene_matriculas:
                return False, "No se puede eliminar al estudiante porque tiene matrículas vigentes asociadas."

        self.lista.remove(e)
        self.guardar()
        return True, "Estudiante eliminado con éxito."


class MateriaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "materias.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Materia.desde_diccionario(d) for d in self.gestor.leer()]
        self.matriculas_controller = None

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {m.codigo.strip().upper() for m in self.lista if m.id != excepto_id and m.codigo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_m):
        for m in self.lista:
            if m.id == id_m: return m
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [m for m in self.lista if t in m.nombre.lower() or t in m.codigo.lower()]

    def siguiente(self):
        return max([m.id for m in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        materia = Materia(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["codigo"]).strip().upper(), int(datos["creditos"]),
            int(datos.get("cupos", 30))
        )
        self.lista.append(materia)
        self.guardar()
        return True, f"Materia registrada: {materia.etiqueta()}"

    def actualizar(self, id_m, datos):
        m = self.obtener(id_m)
        if not m: return False, "No existe"
        error = self.validar(datos, id_m)
        if error: return False, error
        if "nombre" in datos: m.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos: m.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos and str(datos["creditos"]).strip() != "": m.creditos = int(datos["creditos"])
        if "cupos" in datos and str(datos["cupos"]).strip() != "": m.cupos = int(datos["cupos"])
        self.guardar()
        return True, "Materia actualizada"

    def eliminar(self, id_m):
        m = self.obtener(id_m)
        if not m: return False, "No existe"

        if self.matriculas_controller:
            matriculas_conservadas = [
                mat for mat in self.matriculas_controller.leer() if mat.materia_id != id_m
            ]
            self.matriculas_controller.lista = matriculas_conservadas
            self.matriculas_controller.guardar()

        self.lista.remove(m)
        self.guardar()
        return True, "Materia y sus matrículas asociadas eliminadas en cascada."


class MatriculaController(CrudBase):
    def __init__(self, estudiantes, materias, archivo=None):
        self.estudiantes = estudiantes
        self.materias = materias
        ruta = archivo or os.path.join(DATA_DIR, "matriculas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Matricula.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([mat.a_diccionario() for mat in self.lista])

    def validar(self, datos):
        try:
            est_id = int(datos.get("estudiante_id", 0))
            mat_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        
        if not self.estudiantes.obtener(est_id): return "No existe el estudiante"
        materia = self.materias.obtener(mat_id)
        if not materia: return "No existe la materia"

        if not materia.hay_cupo():
            return f"Error: La materia {materia.nombre} no tiene cupos disponibles."

        for m in self.lista:
            if m.estudiante_id == est_id and m.materia_id == mat_id:
                return "El estudiante ya está matriculado en esta materia."

        return None

    def leer(self): return self.lista
    def obtener(self, id_mat):
        for mat in self.lista:
            if mat.id == id_mat: return mat
        return None

    def buscar(self, t):
        return [mat for mat in self.lista if t.strip() in mat.periodo]

    def siguiente(self):
        return max([mat.id for mat in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        
        estudiante = self.estudiantes.obtener(int(datos["estudiante_id"]))
        materia = self.materias.obtener(int(datos["materia_id"]))

        matricula = Matricula(
            self.siguiente(), estudiante.id, materia.id,
            str(datos.get("periodo", "2026-1")).strip(),
            float(datos.get("nota", 0.0))
        )

        materia.ocupar_cupo()
        self.materias.guardar()

        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula #{matricula.id} registrada con éxito."

    def actualizar(self, id_mat, datos):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"
        if "nota" in datos:
            if not Materia.es_nota_valida(datos["nota"]):
                return False, "Nota inválida (debe ser entre 0 y 20)"
            mat.nota = float(datos["nota"])
            self.guardar()
            return True, "Nota registrada con éxito"
        return False, "Solo se permite actualizar la nota"

    def eliminar(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"

        materia = self.materias.obtener(mat.materia_id)
        if materia:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(mat)
        self.guardar()
        return True, "Matrícula eliminada y cupo devuelto."