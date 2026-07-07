import tkinter as tk
from tkinter import messagebox

from src import session
from src.constants.settings import Settings
from src.constants.styles import Colors, Fonts
from src.exceptions import ValidationError
from src.modules.user.logic import iniciar_sesion


class LoginFrame(tk.Frame):
    """Pantalla de login. Al autenticar OK llama a on_exito(usuario)."""

    def __init__(self, master, on_exito):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._on_exito = on_exito
        self._intentos_fallidos = 0

        contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            contenedor,
            text=Settings.APP_NAME,
            font=Fonts.TITLE,
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_DARK,
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(contenedor, text="Usuario", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self._entry_usuario = tk.Entry(contenedor, font=Fonts.BODY)
        self._entry_usuario.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(contenedor, text="Contraseña", font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK).grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self._entry_password = tk.Entry(contenedor, font=Fonts.BODY, show="*")
        self._entry_password.grid(row=2, column=1, padx=5, pady=5)

        self._boton_ingresar = tk.Button(
            contenedor,
            text="Ingresar",
            font=Fonts.BUTTON,
            bg=Colors.BTN_PRIMARY,
            fg=Colors.TEXT_LIGHT,
            relief="flat",
            command=self._intentar_login,
        )
        self._boton_ingresar.grid(row=3, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        self._entry_usuario.bind("<Return>", lambda _evento: self._intentar_login())
        self._entry_password.bind("<Return>", lambda _evento: self._intentar_login())
        self._entry_usuario.focus_set()

    def _intentar_login(self):
        username = self._entry_usuario.get().strip()
        password = self._entry_password.get()

        try:
            usuario = iniciar_sesion(username, password)
        except ValidationError as error:
            self._registrar_intento_fallido(error)
            return

        session.iniciar(usuario)
        self._on_exito(usuario)

    def _registrar_intento_fallido(self, error):
        self._intentos_fallidos += 1
        self._entry_password.delete(0, tk.END)

        if self._intentos_fallidos >= Settings.MAX_LOGIN_ATTEMPTS:
            self._entry_usuario.configure(state="disabled")
            self._entry_password.configure(state="disabled")
            self._boton_ingresar.configure(state="disabled")
            messagebox.showerror(
                "Acceso bloqueado",
                "Demasiados intentos fallidos. Cerrá y volvé a abrir la aplicación.",
            )
            return

        messagebox.showerror("Error de acceso", str(error))
