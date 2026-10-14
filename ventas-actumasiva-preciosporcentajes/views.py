from abc import ABC, abstractmethod
import os

from models import Cliente, Producto, Factura
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


class ClienteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "clientes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Cliente.desde_diccionario(d) for d in self.gestor.leer()]
        self.facturas_controller = None

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def rucs_registrados(self, excepto_id=None):
        return {c.ruc.strip() for c in self.lista if c.id != excepto_id and c.ruc}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "ruc"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"
        if "ruc" in datos:
            ruc = str(datos["ruc"]).strip()
            if ruc in self.rucs_registrados(id_actual):
                return f"El RUC/CI '{ruc}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.ruc.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        cliente = Cliente(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["ruc"]).strip(), str(datos.get("direccion", "")).strip()
        )
        self.lista.append(cliente)
        self.guardar()
        return True, f"Cliente registrado: {cliente.etiqueta()}"

    def actualizar(self, id_c, datos):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        error = self.validar(datos, id_c)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(c, k, val)
        self.guardar()
        return True, f"Cliente {id_c} actualizado"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"

        if self.facturas_controller:
            tiene_facturas = any(f.cliente_id == id_c for f in self.facturas_controller.leer())
            if tiene_facturas:
                return False, "No se puede eliminar al cliente porque registra facturas emitidas en el sistema."

        self.lista.remove(c)
        self.guardar()
        return True, "Cliente eliminado con éxito."


class ProductoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "productos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Producto.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def skus_registrados(self, excepto_id=None):
        return {p.sku.strip().upper() for p in self.lista if p.id != excepto_id and p.sku}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "sku", "precio", "stock"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "sku" in datos:
            sku = str(datos["sku"]).strip().upper()
            if sku in self.skus_registrados(id_actual): return f"El SKU '{sku}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.nombre.lower() or t in p.sku.lower()]

    def actualizar_precios_masivo(self, porcentaje):
        try:
            porc = float(porcentaje)
            if not self.lista:
                return False, "No hay productos en el catálogo para actualizar."
            
            for p in self.lista:
                nuevo_precio = p.precio * (1 + (porc / 100.0))
                p.precio = round(max(0.0, nuevo_precio), 2)
            
            self.guardar()
            return True, f"Precios actualizados exitosamente en todo el catálogo aplicando un {porc}%."
        except (TypeError, ValueError):
            return False, "Porcentaje inválido ingresado."

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        producto = Producto(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["sku"]).strip().upper(), float(datos["precio"]),
            int(datos["stock"])
        )
        self.lista.append(producto)
        self.guardar()
        return True, f"Producto registrado: {producto.etiqueta()}"

    def actualizar(self, id_p, datos):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        if "nombre" in datos: p.nombre = str(datos["nombre"]).strip().title()
        if "sku" in datos: p.sku = str(datos["sku"]).strip().upper()
        if "precio" in datos and str(datos["precio"]).strip() != "": p.precio = float(datos["precio"])
        if "stock" in datos and str(datos["stock"]).strip() != "": p.stock = int(datos["stock"])
        self.guardar()
        return True, "Producto actualizado"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Producto eliminado"


class FacturaController(CrudBase):
    def __init__(self, clientes, productos, archivo=None):
        self.clientes = clientes
        self.productos = productos
        ruta = archivo or os.path.join(DATA_DIR, "facturas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Factura.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([f.a_diccionario() for f in self.lista])

    def validar(self, datos):
        try:
            cli_id = int(datos.get("cliente_id", 0))
            prod_id = int(datos.get("producto_id", 0))
            cant = int(datos.get("cantidad", 0))
        except (TypeError, ValueError):
            return "IDs o cantidad inválidos"
        
        if not self.clientes.obtener(cli_id): return "No existe el cliente"
        producto = self.productos.obtener(prod_id)
        if not producto: return "No existe el producto"

        if cant <= 0: return "La cantidad debe ser mayor a 0."

        if not producto.hay_stock(cant):
            return f"Stock insuficiente. Stock actual: {producto.stock} unidades."

        return None

    def leer(self): return self.lista
    def obtener(self, id_f):
        for f in self.lista:
            if f.id == id_f: return f
        return None

    def buscar(self, t):
        return [f for f in self.lista if t.strip() in f.fecha]

    def siguiente(self):
        return max([f.id for f in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        
        producto = self.productos.obtener(int(datos["producto_id"]))
        cant = int(datos["cantidad"])
        total_pagar = producto.precio * cant

        factura = Factura(
            self.siguiente(), int(datos["cliente_id"]), producto.id,
            cant, total_pagar
        )

        producto.descontar_stock(cant)
        self.productos.guardar()

        self.lista.append(factura)
        self.guardar()
        return True, f"Factura #{factura.id} emitida con éxito. Total: ${total_pagar:.2f}"

    def actualizar(self, id_f, datos): return False, "Las facturas no se modifican"

    def eliminar(self, id_f):
        f = self.obtener(id_f)
        if not f: return False, "No existe"

        producto = self.productos.obtener(f.producto_id)
        if producto:
            producto.devolver_stock(f.cantidad)
            self.productos.guardar()

        self.lista.remove(f)
        self.guardar()
        return True, "Factura anulada y stock devuelto al inventario."