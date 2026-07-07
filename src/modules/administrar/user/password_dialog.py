import tkinter as tk
from tkinter import messagebox

from src.constants.styles import Colors, Fonts
from src.exceptions import ValidationError
from src.modules.administrar.user.logic import actualizar_usuario


class CambiarContrasenaDialog(tk.Toplevel):
    """Cambia la contraseña de un usuario puntual."""

    def __init__(self, master, on_exito, id_usuario):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._on_exito = on_exito
        self._id_usuario = id_usuario

        self.title("Cambiar contraseña")
        self.transient(master)
        self.grab_set()

        contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        contenedor.pack(padx=20, pady=20)

        tk.Label(
            contenedor, text="Nueva contraseña", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self._entry_nueva = tk.Entry(contenedor, font=Fonts.BODY, show="*")
        self._entry_nueva.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            contenedor, text="Confirmar", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self._entry_confirmar = tk.Entry(contenedor, font=Fonts.BODY, show="*")
        self._entry_confirmar.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            contenedor,
            text="Guardar",
            font=Fonts.BUTTON,
            bg=Colors.BTN_SUCCESS,
            fg=Colors.TEXT_LIGHT,
            relief="flat",
            command=self._guardar,
        ).grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="ew")

    def _guardar(self):
        nueva = self._entry_nueva.get()
        confirmar = self._entry_confirmar.get()

        if not nueva or nueva != confirmar:
            messagebox.showerror("Error de validación", "Las contraseñas no coinciden.")
            return

        try:
            actualizar_usuario(self._id_usuario, password=nueva)
        except ValidationError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        self._on_exito()
        self.destroy()
