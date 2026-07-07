import tkinter as tk
from tkinter import messagebox, ttk

from src import session
from src.constants.styles import Colors, Fonts
from src.modules.branches.logic import listar_sucursales
from src.modules.user.logic import borrar_usuario, listar_usuarios, obtener_por_id
from src.modules.user.password_dialog import CambiarContrasenaDialog
from src.modules.user.user_form_dialog import UsuarioFormDialog
from src.permissions import (
    puede_cambiar_alguna_password,
    puede_cambiar_password,
    puede_gestionar_usuarios,
)

_ANCHO_BOTON_ACCION = 18

_COLUMNAS = ("code", "name", "last_name", "dni", "username", "role", "branch")
_ENCABEZADOS = {
    "code": "Código",
    "name": "Nombre",
    "last_name": "Apellido",
    "dni": "DNI",
    "username": "Usuario",
    "role": "Rol",
    "branch": "Sucursal",
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

        # Los botones de acción se empaquetan ANTES que el Treeview y con
        # side="bottom", para reservar su lugar fijo abajo a la derecha.
        # Si el Treeview (que se expande) se empaqueta primero, se come
        # todo el espacio disponible y los botones quedan fuera de la
        # ventana en resoluciones más chicas.
        acciones = tk.Frame(self, bg=Colors.BG_MAIN)
        acciones.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self._tree = ttk.Treeview(self, columns=_COLUMNAS, show="headings", selectmode="browse")
        for columna in _COLUMNAS:
            self._tree.heading(columna, text=_ENCABEZADOS[columna])
            self._tree.column(columna, width=110)
        self._tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._tree.bind("<<TreeviewSelect>>", lambda _evento: self._actualizar_botones())

        if puede_cambiar_alguna_password(self._rol_actual):
            self._btn_password = tk.Button(
                acciones,
                text="Cambiar contraseña",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                width=_ANCHO_BOTON_ACCION,
                command=self._cambiar_password,
                state="disabled",
            )
            self._btn_password.pack(side="right", padx=(5, 0))

        if puede_gestionar_usuarios(self._rol_actual):
            self._btn_eliminar = tk.Button(
                acciones,
                text="Eliminar",
                font=Fonts.BUTTON,
                bg=Colors.BTN_DANGER,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                width=_ANCHO_BOTON_ACCION,
                command=self._eliminar,
                state="disabled",
            )
            self._btn_eliminar.pack(side="right", padx=(5, 0))

            self._btn_editar = tk.Button(
                acciones,
                text="Editar",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                width=_ANCHO_BOTON_ACCION,
                command=self._editar,
                state="disabled",
            )
            self._btn_editar.pack(side="right", padx=(5, 0))

            tk.Button(
                acciones,
                text="Nuevo usuario",
                font=Fonts.BUTTON,
                bg=Colors.BTN_PRIMARY,
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                width=_ANCHO_BOTON_ACCION,
                command=self._nuevo,
            ).pack(side="right", padx=(5, 0))

    def _actualizar_botones(self):
        id_usuario = self._id_seleccionado()
        estado_gestion = "normal" if id_usuario is not None else "disabled"
        for boton in (self._btn_editar, self._btn_eliminar):
            if boton is not None:
                boton.configure(state=estado_gestion)

        if self._btn_password is not None:
            self._btn_password.configure(state=self._estado_password(id_usuario))

    def _estado_password(self, id_usuario):
        if id_usuario is None:
            return "disabled"
        objetivo = obtener_por_id(id_usuario)
        usuario_logueado = session.usuario_actual
        es_uno_mismo = usuario_logueado is not None and usuario_logueado["id"] == id_usuario
        puede = puede_cambiar_password(self._rol_actual, objetivo["role"], es_uno_mismo)
        return "normal" if puede else "disabled"

    def _refrescar(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._usuarios_por_item = {}

        nombres_sucursal = {s["id"]: s["name"] for s in listar_sucursales()}

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
                    nombres_sucursal.get(usuario["branch_id"], ""),
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
