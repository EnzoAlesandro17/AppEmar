import tkinter as tk

from src import session
from src.constants.settings import Settings
from src.constants.styles import Colors, Fonts
from src.modules.administrar.branches.db import crear_tabla as crear_tabla_branches
from src.modules.administrar.clients.db import crear_tabla as crear_tabla_clients
from src.modules.administrar.products.db import crear_tabla as crear_tabla_products
from src.modules.administrar.ui import AdministrarFrame
from src.modules.administrar.user.db import crear_tabla as crear_tabla_users
from src.modules.administrar.user.login_ui import LoginFrame
from src.ui_nav import crear_grid_botones


def inicializar_db():
    """Crea todas las tablas del proyecto si todavía no existen."""
    crear_tabla_branches()
    crear_tabla_users()
    crear_tabla_clients()
    crear_tabla_products()


class App(tk.Tk):
    """Ventana principal: barra de secciones arriba + área de contenido intercambiable.

    Hoy solo "Administrar" está activo; el resto de la grilla queda
    deshabilitado, reservado para futuras secciones (ventas, etc.).
    """

    def __init__(self):
        super().__init__()
        self.title(Settings.APP_NAME)
        self._centrar_ventana(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.resizable(False, False)
        # Sin esto, Tk recalcula el tamaño de la ventana al tamaño "pedido"
        # por el contenido cada vez que se cambia de frame (login, módulos),
        # ignorando el geometry fijo de arriba.
        self.pack_propagate(False)
        self.configure(bg=Colors.BG_MAIN)

        self._frame_actual = None
        self._mostrar_login()

    def _centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _mostrar_login(self):
        self._frame_actual = LoginFrame(self, on_exito=self._on_login_exitoso)
        self._frame_actual.pack(fill="both", expand=True)

    def _on_login_exitoso(self, usuario):
        self._frame_actual.destroy()
        self._frame_actual = None
        self._crear_layout()
        self._abrir_administrar()

    def _crear_layout(self):
        barra = tk.Frame(self, bg=Colors.BG_SIDEBAR)
        barra.pack(side="top", fill="x")

        usuario = session.usuario_actual
        tk.Label(
            barra,
            text=f"{Settings.APP_NAME} — Hola, {usuario['name']} ({usuario['role']})",
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_LIGHT,
            font=Fonts.TITLE,
        ).pack(side="top", anchor="w", padx=10, pady=(10, 5))

        # 8 lugares fijos (2 filas de 4): solo "Administrar" está activo hoy,
        # el resto queda reservado para futuras secciones (ventas, etc.).
        secciones = [("Administrar", self._abrir_administrar)]
        secciones += [(str(n), None) for n in range(2, 9)]
        grilla = crear_grid_botones(barra, secciones)
        grilla.pack(side="top", fill="x", padx=10, pady=(0, 10))

        self.contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        self.contenedor.pack(side="top", fill="both", expand=True)

    def _abrir_administrar(self):
        if self._frame_actual is not None:
            self._frame_actual.destroy()
        self._frame_actual = AdministrarFrame(self.contenedor)
        self._frame_actual.pack(fill="both", expand=True)


if __name__ == "__main__":
    inicializar_db()
    app = App()
    app.mainloop()
