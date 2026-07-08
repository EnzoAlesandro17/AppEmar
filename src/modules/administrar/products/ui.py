from tkinter import messagebox

from src import session
from src.constants.styles import Colors
from src.modules.administrar.listado_frame import ListadoFrame
from src.modules.administrar.products.logic import borrar_producto, listar_productos, obtener_por_id
from src.modules.administrar.products.product_form_dialog import ProductoFormDialog
from src.permissions import puede_gestionar_registros


class ProductosFrame(ListadoFrame):
    """Interfaz del módulo de productos: listado + alta/edición/baja."""

    TITULO = "Productos"
    COLUMNAS = ("code", "name", "category", "brand", "stock", "wholesale_price", "retail_price")
    ENCABEZADOS = {
        "code": "Código",
        "name": "Nombre",
        "category": "Categoría",
        "brand": "Marca",
        "stock": "Stock",
        "wholesale_price": "P. mayorista",
        "retail_price": "P. minorista",
    }

    def __init__(self, master):
        usuario_logueado = session.usuario_actual
        self._rol_actual = usuario_logueado["role"] if usuario_logueado else None
        super().__init__(master)

    def _definir_botones(self):
        return [
            {"clave": "eliminar", "texto": "Eliminar", "command": self._eliminar, "color": Colors.BTN_DANGER},
            {"clave": "editar", "texto": "Editar", "command": self._editar},
            {"clave": "nuevo", "texto": "Nuevo producto", "command": self._nuevo},
        ]

    def actualizar_botones(self):
        id_producto = self.id_seleccionado()
        gestion_ok = puede_gestionar_registros(self._rol_actual)
        estado_gestion = "normal" if gestion_ok and id_producto is not None else "disabled"

        self.boton("nuevo").configure(state="normal" if gestion_ok else "disabled")
        self.boton("editar").configure(state=estado_gestion)
        self.boton("eliminar").configure(state=estado_gestion)

    def refrescar(self):
        self.limpiar_filas()
        for producto in listar_productos():
            self.insertar_fila(
                producto["id"],
                (
                    producto["code"],
                    producto["name"],
                    producto["category"],
                    producto["brand"],
                    producto["stock"] if producto["stock"] is not None else "",
                    producto["wholesale_price"],
                    producto["retail_price"],
                ),
            )

        self.actualizar_botones()

    def _nuevo(self):
        ProductoFormDialog(self, on_exito=self.refrescar)

    def _editar(self):
        id_producto = self.id_seleccionado()
        if id_producto is None:
            return
        producto = obtener_por_id(id_producto)
        ProductoFormDialog(self, on_exito=self.refrescar, producto=producto)

    def _eliminar(self):
        id_producto = self.id_seleccionado()
        if id_producto is None:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            borrar_producto(id_producto)
            self.refrescar()
