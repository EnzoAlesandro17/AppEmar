import tkinter as tk

from src import session
from src.constants.settings import Settings
from src.constants.styles import Colors, Fonts
from src.modules.branches.db import crear_tabla as crear_tabla_branches
from src.modules.branches.ui import SucursalesFrame
from src.modules.clients.db import crear_tabla as crear_tabla_clients
from src.modules.clients.ui import ClientesFrame
from src.modules.products.db import crear_tabla as crear_tabla_products
from src.modules.products.ui import ProductosFrame
from src.modules.user.db import crear_tabla as crear_tabla_users
from src.modules.user.login_ui import LoginFrame
from src.modules.user.ui import UsuariosFrame


def inicializar_db():
    """Crea todas las tablas del proyecto si todavía no existen."""
    crear_tabla_users()
    crear_tabla_clients()
    crear_tabla_products()
    crear_tabla_branches()


class App(tk.Tk):
    """Ventana principal: sidebar de navegación + área de contenido intercambiable.

    Para sumar un módulo nuevo alcanza con agregarlo a MODULOS: la clase debe
    ser un tk.Frame que reciba el contenedor como único argumento.
    """

    MODULOS = {
        "Clientes": ClientesFrame,
        "Productos": ProductosFrame,
        "Usuarios": UsuariosFrame,
        "Sucursales": SucursalesFrame,
    }

    def __init__(self):
        super().__init__()
        self.title(Settings.APP_NAME)
        self.geometry(Settings.WINDOW_SIZE)
        self.minsize(Settings.MIN_WIDTH, Settings.MIN_HEIGHT)
        self.configure(bg=Colors.BG_MAIN)

        self._frame_actual = None
        self._mostrar_login()

    def _mostrar_login(self):
        self._frame_actual = LoginFrame(self, on_exito=self._on_login_exitoso)
        self._frame_actual.pack(fill="both", expand=True)

    def _on_login_exitoso(self, usuario):
        self._frame_actual.destroy()
        self._frame_actual = None
        self._crear_layout()
        self.mostrar_modulo(next(iter(self.MODULOS)))

    def _crear_layout(self):
        sidebar = tk.Frame(self, bg=Colors.BG_SIDEBAR, width=180)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text=Settings.APP_NAME,
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_LIGHT,
            font=Fonts.TITLE,
            wraplength=160,
            justify="left",
        ).pack(pady=20, padx=10)

        usuario = session.usuario_actual
        tk.Label(
            sidebar,
            text=f"Hola, {usuario['name']} ({usuario['role']})",
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_LIGHT,
            font=Fonts.BODY,
            wraplength=160,
            justify="left",
        ).pack(pady=(0, 20), padx=10)

        for nombre in self.MODULOS:
            tk.Button(
                sidebar,
                text=nombre,
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                command=lambda n=nombre: self.mostrar_modulo(n),
            ).pack(fill="x", padx=10, pady=5)

        self.contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        self.contenedor.pack(side="right", fill="both", expand=True)

    def mostrar_modulo(self, nombre):
        if self._frame_actual is not None:
            self._frame_actual.destroy()

        clase_frame = self.MODULOS[nombre]
        self._frame_actual = clase_frame(self.contenedor)
        self._frame_actual.pack(fill="both", expand=True)


if __name__ == "__main__":
    inicializar_db()
    app = App()
    app.mainloop()
