import tkinter as tk

from src.constants.styles import Colors
from src.modules.administrar.branches.ui import SucursalesFrame
from src.modules.administrar.clients.ui import ClientesFrame
from src.modules.administrar.products.ui import ProductosFrame
from src.modules.administrar.user.ui import UsuariosFrame
from src.ui_nav import crear_grid_botones


class AdministrarFrame(tk.Frame):
    """Sección "Administrar": sub-barra de navegación + área de contenido
    intercambiable entre los módulos de datos maestros (clientes, productos,
    usuarios, sucursales).
    """

    MODULOS = {
        "Clientes": ClientesFrame,
        "Productos": ProductosFrame,
        "Usuarios": UsuariosFrame,
        "Sucursales": SucursalesFrame,
    }

    def __init__(self, master):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._frame_actual = None
        self._crear_layout()
        self.mostrar_modulo(next(iter(self.MODULOS)))

    def _crear_layout(self):
        botones = [(nombre, lambda n=nombre: self.mostrar_modulo(n)) for nombre in self.MODULOS]
        barra = crear_grid_botones(self, botones)
        barra.pack(side="top", fill="x", padx=10, pady=10)

        self.contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        self.contenedor.pack(side="top", fill="both", expand=True)

    def mostrar_modulo(self, nombre):
        if self._frame_actual is not None:
            self._frame_actual.destroy()

        clase_frame = self.MODULOS[nombre]
        self._frame_actual = clase_frame(self.contenedor)
        self._frame_actual.pack(fill="both", expand=True)
