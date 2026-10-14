from datetime import date


class ModeloBase:
    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return f"registro {self.id}"

    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Cliente(Persona):
    def __init__(self, id_registro, nombre, apellido, email, ruc="", direccion=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc = ruc
        self.direccion = direccion

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc"] = self.ruc
        datos["direccion"] = self.direccion
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · RUC/CI: {self.ruc}"


class Producto(ModeloBase):
    def __init__(self, id_registro, nombre, sku, precio=0.0, stock=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.sku = str(sku).upper()
        self.precio = float(precio)
        self.stock = int(stock)

    def hay_stock(self, cantidad):
        return self.stock >= cantidad

    def descontar_stock(self, cantidad):
        self.stock -= cantidad

    def devolver_stock(self, cantidad):
        self.stock += cantidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["sku"] = self.sku
        datos["precio"] = self.precio
        datos["stock"] = self.stock
        return datos

    def etiqueta(self):
        alerta = " ⚠ POCO STOCK" if self.stock <= 5 else ""
        return f"{self.nombre} (SKU: {self.sku}) · ${self.precio:.2f} · Stock: {self.stock}{alerta}"


class Factura(ModeloBase):
    def __init__(self, id_registro, cliente_id, producto_id, cantidad, total_pagar=0.0, fecha=""):
        super().__init__(id_registro)
        self.cliente_id = int(cliente_id)
        self.producto_id = int(producto_id)
        self.cantidad = int(cantidad)
        self.total_pagar = float(total_pagar) if total_pagar != "" else 0.0
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cliente_id"] = self.cliente_id
        datos["producto_id"] = self.producto_id
        datos["cantidad"] = self.cantidad
        datos["total_pagar"] = self.total_pagar
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return f"Factura #{self.id} · Cliente ID {self.cliente_id} · Prod ID {self.producto_id} · Cant: {self.cantidad} · Total: ${self.total_pagar:.2f}"