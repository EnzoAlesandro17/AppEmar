import tkinter as tk
from tkinter import ttk

from src.constants.styles import Colors, Fonts, Sizes


class ListadoFrame(tk.Frame):
    """Base para las pantallas de listado del módulo Administrar: título +
    Treeview + fila de botones de acción abajo a la derecha, en el mismo
    lugar fijo en todas las pantallas.

    Las subclases definen:
    - TITULO, COLUMNAS, ENCABEZADOS.
    - _definir_botones(): lista de dicts {clave, texto, command, color=None},
      en el orden visual izquierda -> derecha (se empaquetan de derecha a
      izquierda, así que la lista va en orden de lectura normal).
    - refrescar(): usa limpiar_filas()/insertar_fila() para llenar el
      Treeview, y termina llamando actualizar_botones().
    - actualizar_botones() (opcional): habilita/deshabilita self.boton(clave)
      según selección/permisos. Si no se sobreescribe, los botones quedan
      siempre deshabilitados (pantallas todavía sin lógica real).
    """

    TITULO = ""
    COLUMNAS = ()
    ENCABEZADOS = {}

    def __init__(self, master):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._botones = {}
        self._items_por_id = {}
        self._crear_layout()
        self.refrescar()

    def _crear_layout(self):
        header = tk.Frame(self, bg=Colors.BG_MAIN)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(
            header, text=self.TITULO, font=Fonts.SUBTITLE, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
        ).pack(side="left")

        # Los botones se empaquetan ANTES que el Treeview y con side="bottom"
        # para reservar su lugar fijo: si el Treeview (que se expande) se
        # empaqueta primero, se come todo el espacio y los botones quedan
        # fuera de la ventana en resoluciones más chicas.
        acciones = tk.Frame(self, bg=Colors.BG_MAIN)
        acciones.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self._tree = ttk.Treeview(self, columns=self.COLUMNAS, show="headings", selectmode="browse")
        for columna in self.COLUMNAS:
            self._tree.heading(columna, text=self.ENCABEZADOS[columna])
            self._tree.column(columna, width=110)
        self._tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._tree.bind("<<TreeviewSelect>>", lambda _evento: self.actualizar_botones())

        for definicion in self._definir_botones():
            boton = tk.Button(
                acciones,
                text=definicion["texto"],
                font=Fonts.BUTTON,
                bg=definicion.get("color", Colors.BTN_PRIMARY),
                fg=Colors.TEXT_LIGHT,
                relief="flat",
                width=Sizes.BOTON_ACCION,
                command=definicion.get("command"),
                state="disabled",
            )
            boton.pack(side="right", padx=(5, 0))
            self._botones[definicion["clave"]] = boton

    def _definir_botones(self):
        return []

    def boton(self, clave):
        return self._botones[clave]

    def actualizar_botones(self):
        """Las subclases sobreescriben esto para habilitar/deshabilitar según
        selección/permisos. Por defecto no hace nada: los botones quedan
        siempre deshabilitados.
        """

    def id_seleccionado(self):
        seleccion = self._tree.selection()
        if not seleccion:
            return None
        return self._items_por_id.get(seleccion[0])

    def limpiar_filas(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._items_por_id = {}

    def insertar_fila(self, id_negocio, valores):
        item = self._tree.insert("", "end", values=valores)
        self._items_por_id[item] = id_negocio
        return item

    def refrescar(self):
        raise NotImplementedError
