from tkinter import messagebox

from src import session
from src.constants.styles import Colors
from src.modules.administrar.clients.client_form_dialog import ClienteFormDialog
from src.modules.administrar.clients.logic import borrar_cliente, listar_clientes, obtener_por_id
from src.modules.administrar.listado_frame import ListadoFrame
from src.permissions import puede_gestionar_registros


class ClientesFrame(ListadoFrame):
    """Interfaz del módulo de clientes: listado + alta/edición/baja."""

    TITULO = "Clientes"
    COLUMNAS = ("name", "last_name", "dni_cuit", "phone", "email")
    ENCABEZADOS = {
        "name": "Nombre",
        "last_name": "Apellido",
        "dni_cuit": "DNI/CUIT",
        "phone": "Teléfono",
        "email": "Email",
    }

    def __init__(self, master):
        usuario_logueado = session.usuario_actual
        self._rol_actual = usuario_logueado["role"] if usuario_logueado else None
        super().__init__(master)

    def _definir_botones(self):
        return [
            {"clave": "eliminar", "texto": "Eliminar", "command": self._eliminar, "color": Colors.BTN_DANGER},
            {"clave": "editar", "texto": "Editar", "command": self._editar},
            {"clave": "nuevo", "texto": "Nuevo cliente", "command": self._nuevo},
        ]

    def actualizar_botones(self):
        id_cliente = self.id_seleccionado()
        gestion_ok = puede_gestionar_registros(self._rol_actual)
        estado_gestion = "normal" if gestion_ok and id_cliente is not None else "disabled"

        self.boton("nuevo").configure(state="normal" if gestion_ok else "disabled")
        self.boton("editar").configure(state=estado_gestion)
        self.boton("eliminar").configure(state=estado_gestion)

    def refrescar(self):
        self.limpiar_filas()
        for cliente in listar_clientes():
            self.insertar_fila(
                cliente["id"],
                (
                    cliente["name"],
                    cliente["last_name"],
                    cliente["dni_cuit"],
                    cliente["phone"] or "",
                    cliente["email"] or "",
                ),
            )

        self.actualizar_botones()

    def _nuevo(self):
        ClienteFormDialog(self, on_exito=self.refrescar)

    def _editar(self):
        id_cliente = self.id_seleccionado()
        if id_cliente is None:
            return
        cliente = obtener_por_id(id_cliente)
        ClienteFormDialog(self, on_exito=self.refrescar, cliente=cliente)

    def _eliminar(self):
        id_cliente = self.id_seleccionado()
        if id_cliente is None:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            borrar_cliente(id_cliente)
            self.refrescar()
