import tkinter as tk
from tkinter import messagebox

from src.constants.styles import Colors, Fonts
from src.exceptions import ValidationError
from src.modules.administrar.clients.logic import actualizar_cliente, crear_cliente


class ClienteFormDialog(tk.Toplevel):
    """Alta/edición de un cliente. Si `cliente` viene con datos, edita; si no, crea."""

    def __init__(self, master, on_exito, cliente=None):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._on_exito = on_exito
        self._cliente = cliente
        self._es_edicion = cliente is not None

        self.title("Editar cliente" if self._es_edicion else "Nuevo cliente")
        self.transient(master)
        self.grab_set()

        contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        contenedor.pack(padx=20, pady=20)

        self._entries = {}
        campos = [
            ("name", "Nombre"),
            ("last_name", "Apellido"),
            ("dni_cuit", "DNI/CUIT"),
            ("phone", "Teléfono"),
            ("email", "Email"),
        ]

        for fila, (clave, etiqueta) in enumerate(campos):
            tk.Label(
                contenedor, text=etiqueta, font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
            ).grid(row=fila, column=0, sticky="e", padx=5, pady=5)

            entry = tk.Entry(contenedor, font=Fonts.BODY)
            if self._es_edicion:
                valor = cliente[clave]
                if valor is not None:
                    entry.insert(0, valor)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            self._entries[clave] = entry

        tk.Button(
            contenedor,
            text="Guardar",
            font=Fonts.BUTTON,
            bg=Colors.BTN_SUCCESS,
            fg=Colors.TEXT_LIGHT,
            relief="flat",
            command=self._guardar,
        ).grid(row=len(campos), column=0, columnspan=2, pady=(15, 0), sticky="ew")

    def _valor(self, clave):
        return self._entries[clave].get().strip() or None

    def _guardar(self):
        try:
            if self._es_edicion:
                actualizar_cliente(
                    self._cliente["id"],
                    name=self._valor("name"),
                    last_name=self._valor("last_name"),
                    dni_cuit=self._valor("dni_cuit"),
                    phone=self._valor("phone"),
                    email=self._valor("email"),
                )
            else:
                crear_cliente(
                    name=self._valor("name"),
                    last_name=self._valor("last_name"),
                    dni_cuit=self._valor("dni_cuit"),
                    phone=self._valor("phone"),
                    email=self._valor("email"),
                )
        except ValidationError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        self._on_exito()
        self.destroy()
