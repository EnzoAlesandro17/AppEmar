import tkinter as tk
from tkinter import messagebox, ttk

from src.constants.styles import Colors, Fonts
from src.exceptions import ValidationError
from src.modules.branches.logic import listar_sucursales
from src.modules.user.logic import ROLES, actualizar_usuario, crear_usuario

_SIN_SUCURSAL = "(sin sucursal)"


class UsuarioFormDialog(tk.Toplevel):
    """Alta/edición de un usuario. Si `usuario` viene con datos, edita; si no, crea."""

    def __init__(self, master, on_exito, usuario=None):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._on_exito = on_exito
        self._usuario = usuario
        self._es_edicion = usuario is not None

        self.title("Editar usuario" if self._es_edicion else "Nuevo usuario")
        self.transient(master)
        self.grab_set()

        contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        contenedor.pack(padx=20, pady=20)

        self._entries = {}
        campos = [
            ("name", "Nombre"),
            ("last_name", "Apellido"),
            ("dni", "DNI"),
            ("code", "Código"),
            ("username", "Usuario"),
            ("email", "Email"),
            ("birth_date", "Fecha nac. (AAAA-MM-DD)"),
            ("phone", "Teléfono"),
        ]

        fila = 0
        if not self._es_edicion:
            campos.insert(5, ("password", "Contraseña"))

        for clave, etiqueta in campos:
            tk.Label(
                contenedor, text=etiqueta, font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
            ).grid(row=fila, column=0, sticky="e", padx=5, pady=5)

            show = "*" if clave == "password" else ""
            entry = tk.Entry(contenedor, font=Fonts.BODY, show=show)
            if self._es_edicion and clave != "password":
                valor = usuario[clave]
                if valor is not None:
                    entry.insert(0, valor)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            self._entries[clave] = entry
            fila += 1

        tk.Label(
            contenedor, text="Rol", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        self._combo_role = ttk.Combobox(contenedor, values=ROLES, state="readonly", font=Fonts.BODY)
        self._combo_role.set(usuario["role"] if self._es_edicion else "Vendedor")
        self._combo_role.grid(row=fila, column=1, padx=5, pady=5)
        fila += 1

        self._sucursales = listar_sucursales()
        tk.Label(
            contenedor, text="Sucursal", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        self._combo_branch = ttk.Combobox(
            contenedor,
            values=[_SIN_SUCURSAL] + [s["name"] for s in self._sucursales],
            state="readonly",
            font=Fonts.BODY,
        )
        nombre_sucursal_actual = _SIN_SUCURSAL
        if self._es_edicion and usuario["branch_id"] is not None:
            sucursal_actual = next((s for s in self._sucursales if s["id"] == usuario["branch_id"]), None)
            if sucursal_actual is not None:
                nombre_sucursal_actual = sucursal_actual["name"]
        self._combo_branch.set(nombre_sucursal_actual)
        self._combo_branch.grid(row=fila, column=1, padx=5, pady=5)
        fila += 1

        tk.Button(
            contenedor,
            text="Guardar",
            font=Fonts.BUTTON,
            bg=Colors.BTN_SUCCESS,
            fg=Colors.TEXT_LIGHT,
            relief="flat",
            command=self._guardar,
        ).grid(row=fila, column=0, columnspan=2, pady=(15, 0), sticky="ew")

    def _valor(self, clave):
        return self._entries[clave].get().strip() or None

    def _branch_id_seleccionado(self):
        nombre = self._combo_branch.get()
        if nombre == _SIN_SUCURSAL:
            return None
        sucursal = next((s for s in self._sucursales if s["name"] == nombre), None)
        return sucursal["id"] if sucursal is not None else None

    def _guardar(self):
        branch_id = self._branch_id_seleccionado()
        try:
            if self._es_edicion:
                actualizar_usuario(
                    self._usuario["id"],
                    name=self._valor("name"),
                    last_name=self._valor("last_name"),
                    dni=self._valor("dni"),
                    code=self._valor("code"),
                    username=self._valor("username"),
                    email=self._valor("email"),
                    birth_date=self._valor("birth_date"),
                    phone=self._valor("phone"),
                    role=self._combo_role.get(),
                    branch_id=branch_id,
                    quitar_branch_id=branch_id is None,
                )
            else:
                crear_usuario(
                    name=self._valor("name"),
                    last_name=self._valor("last_name"),
                    dni=self._valor("dni"),
                    code=self._valor("code"),
                    username=self._valor("username"),
                    password=self._valor("password"),
                    email=self._valor("email"),
                    birth_date=self._valor("birth_date"),
                    phone=self._valor("phone"),
                    role=self._combo_role.get(),
                    branch_id=branch_id,
                )
        except ValidationError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        self._on_exito()
        self.destroy()
