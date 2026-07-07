"""Helpers de navegacion reusables entre App y AdministrarFrame."""

import tkinter as tk

from src.constants.styles import Colors, Fonts


def crear_grid_botones(master, botones, columnas=4, bg=None):
    """Arma una grilla de botones de ancho igual.

    `botones` es una lista de (texto, comando_o_None); comando=None deja el
    boton deshabilitado. Devuelve el Frame contenedor (falta packearlo).
    """
    contenedor = tk.Frame(master, bg=bg or Colors.BG_SIDEBAR)

    for indice, (texto, comando) in enumerate(botones):
        fila, columna = divmod(indice, columnas)
        contenedor.grid_columnconfigure(columna, weight=1, uniform="grid_botones")
        tk.Button(
            contenedor,
            text=texto,
            font=Fonts.BUTTON,
            bg=Colors.BTN_PRIMARY,
            fg=Colors.TEXT_LIGHT,
            relief="flat",
            command=comando,
            state="normal" if comando else "disabled",
        ).grid(row=fila, column=columna, sticky="ew", padx=5, pady=(0, 5) if fila == 0 else 0)

    return contenedor
