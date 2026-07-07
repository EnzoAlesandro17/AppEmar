import tkinter as tk
from tkinter import messagebox, ttk

from src import session
from src.constants.styles import Colors, Fonts
from src.modules.user.logic import borrar_usuario, listar_usuarios, obtener_por_id
from src.modules.user.password_dialog import CambiarContrasenaDialog
from src.modules.user.user_form_dialog import UsuarioFormDialog
from src.permissions import puede_cambiar_contrasenas, puede_gestionar_usuarios

_COLUMNAS = ("code", "name", "last_name", "dni", "username", "role")
_ENCABEZADOS = {
    "code": "Código",
    "name": "Nombre",
    "last_name": "Apellido",
    "dni": "DNI",
    "username": "Usuario",
    "role": "Rol",
}


class UsuariosFrame(tk.Frame):
    """Interfaz del módulo de usuarios: listado + alta/edición/baja/cambio de contraseña."""

    def __init__(self, master):
        super().__init__(master, bg=Colors.BG_MAIN)
        usuario_logueado = session.usuario_actual
        self._rol_actual = usuario_logueado["role"] if usuario_logueado else None
        self._usuarios_por_item = {}

        self._btn_editar = None
        self._btn_eliminar = None
        self._btn_password = None

        self._crear_layout()
        self._refrescar()

    def _crear_layout(self):
        header = tk.Frame(self, bg=Colors.BG_MAIN)
        header.pack(fill="x", padx=10, pady=10)

        tk.Label(
            header, text="Usuarios", font=Fonts.SUBTITLE, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).pack(side="left")

        if puede_gestionar_usuarios(self._rol_actual):
            tk.Button(
                header,
                text="Nuevo usuario",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                command=self._nuevo,
            ).pack(side="right")

        self._tree = ttk.Treeview(self, columns=_COLUMNAS, show="headings", selectmode="browse")
        for columna in _COLUMNAS:
            self._tree.heading(columna, text=_ENCABEZADOS[columna])
            self._tree.column(columna, width=110)
        self._tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._tree.bind("<<TreeviewSelect>>", lambda _evento: self._actualizar_botones())

        acciones = tk.Frame(self, bg=Colors.BG_MAIN)
        acciones.pack(fill="x", padx=10, pady=(0, 10))

        if puede_gestionar_usuarios(self._rol_actual):
            self._btn_editar = tk.Button(
                acciones,
                text="Editar",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                command=self._editar,
                state="disabled",
            )
            self._btn_editar.pack(side="left", padx=(0, 5))

            self._btn_eliminar = tk.Button(
                acciones,
                text="Eliminar",
                font=Fonts.BUTTON,
                bg=Colors.BTN_DANGER,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                command=self._eliminar,
                state="disabled",
            )
            self._btn_eliminar.pack(side="left", padx=(0, 5))

        if puede_cambiar_contrasenas(self._rol_actual):
            self._btn_password = tk.Button(
                acciones,
                text="Cambiar contraseña",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                command=self._cambiar_password,
                state="disabled",
            )
            self._btn_password.pack(side="left")

    def _actualizar_botones(self):
        estado = "normal" if self._tree.selection() else "disabled"
        for boton in (self._btn_editar, self._btn_eliminar, self._btn_password):
            if boton is not None:
                boton.configure(state=estado)

    def _refrescar(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._usuarios_por_item = {}

        for usuario in listar_usuarios():
            item = self._tree.insert(
                "",
                "end",
                values=(
                    usuario["code"] or "",
                    usuario["name"],
                    usuario["last_name"],
                    usuario["dni"],
                    usuario["username"] or "",
                    usuario["role"],
                ),
            )
            self._usuarios_por_item[item] = usuario["id"]

        self._actualizar_botones()

    def _id_seleccionado(self):
        seleccion = self._tree.selection()
        if not seleccion:
            return None
        return self._usuarios_por_item.get(seleccion[0])

    def _nuevo(self):
        UsuarioFormDialog(self, on_exito=self._refrescar)

    def _editar(self):
        id_usuario = self._id_seleccionado()
        if id_usuario is None:
            return
        usuario = obtener_por_id(id_usuario)
        UsuarioFormDialog(self, on_exito=self._refrescar, usuario=usuario)

    def _eliminar(self):
        id_usuario = self._id_seleccionado()
        if id_usuario is None:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            borrar_usuario(id_usuario)
            self._refrescar()

    def _cambiar_password(self):
        id_usuario = self._id_seleccionado()
        if id_usuario is None:
            return
        CambiarContrasenaDialog(self, on_exito=self._refrescar, id_usuario=id_usuario)
