import tkinter as tk
from tkinter import ttk

from src.constants.styles import Colors, Fonts
from src.modules.branches.logic import listar_sucursales

_COLUMNAS = ("code", "name", "country", "city", "address", "phone")
_ENCABEZADOS = {
    "code": "Código",
    "name": "Nombre",
    "country": "País",
    "city": "Ciudad",
    "address": "Dirección",
    "phone": "Teléfono",
}


class SucursalesFrame(tk.Frame):
    """Listado de sucursales, de solo lectura: el alta/edición se gestiona fuera de la app por ahora."""

    def __init__(self, master):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._crear_layout()
        self._refrescar()

    def _crear_layout(self):
        tk.Label(
            self, text="Sucursales", font=Fonts.SUBTITLE, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).pack(anchor="w", padx=10, pady=10)

        # Fila reservada en el mismo lugar fijo que van a ocupar los botones
        # de acción en Usuarios, para el día que Sucursales tenga alta/edición.
        # Se empaqueta ANTES que el Treeview (que se expande) para que su
        # lugar quede reservado siempre, sin importar la altura de ventana.
        acciones = tk.Frame(self, bg=Colors.BG_MAIN, height=40)
        acciones.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        acciones.pack_propagate(False)

        self._tree = ttk.Treeview(self, columns=_COLUMNAS, show="headings", selectmode="browse")
        for columna in _COLUMNAS:
            self._tree.heading(columna, text=_ENCABEZADOS[columna])
            self._tree.column(columna, width=110)
        self._tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _refrescar(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

        for sucursal in listar_sucursales():
            self._tree.insert(
                "",
                "end",
                values=(
                    sucursal["code"] or "",
                    sucursal["name"],
                    sucursal["country"] or "",
                    sucursal["city"] or "",
                    sucursal["address"] or "",
                    sucursal["phone"] or "",
                ),
            )
