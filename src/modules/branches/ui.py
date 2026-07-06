import tkinter as tk

from src.constants.styles import Colors, Fonts


class SucursalesFrame(tk.Frame):
    """Interfaz del módulo de sucursales."""

    def __init__(self, master):
        super().__init__(master, bg=Colors.BG_MAIN)
        tk.Label(
            self,
            text="Módulo Sucursales (en construcción)",
            font=Fonts.SUBTITLE,
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_DARK,
        ).pack(pady=40)
