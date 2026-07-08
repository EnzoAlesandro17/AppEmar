import tkinter as tk
from tkinter import messagebox

from src.constants.styles import Colors, Fonts
from src.exceptions import ValidationError
from src.modules.administrar.products.logic import actualizar_producto, crear_producto


class ProductoFormDialog(tk.Toplevel):
    """Alta/edición de un producto. Si `producto` viene con datos, edita; si no, crea."""

    def __init__(self, master, on_exito, producto=None):
        super().__init__(master, bg=Colors.BG_MAIN)
        self._on_exito = on_exito
        self._producto = producto
        self._es_edicion = producto is not None

        self.title("Editar producto" if self._es_edicion else "Nuevo producto")
        self.transient(master)
        self.grab_set()

        contenedor = tk.Frame(self, bg=Colors.BG_MAIN)
        contenedor.pack(padx=20, pady=20)

        self._entries = {}
        campos = [
            ("code", "Código"),
            ("name", "Nombre"),
            ("category", "Categoría"),
            ("brand", "Marca"),
            ("description", "Descripción"),
            ("stock", "Stock (vacío = sin stock)"),
            ("wholesale_price", "Precio mayorista"),
            ("retail_price", "Precio minorista"),
        ]

        for fila, (clave, etiqueta) in enumerate(campos):
            tk.Label(
                contenedor, text=etiqueta, font=Fonts.BODY, bg=Colors.BG_MAIN, fg=Colors.TEXT_DARK
            ).grid(row=fila, column=0, sticky="e", padx=5, pady=5)

            entry = tk.Entry(contenedor, font=Fonts.BODY)
            if self._es_edicion:
                valor = producto[clave]
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

    def _texto(self, clave):
        return self._entries[clave].get().strip() or None

    def _guardar(self):
        try:
            stock_texto = self._texto("stock")
            stock = int(stock_texto) if stock_texto is not None else None

            precio_mayorista_texto = self._texto("wholesale_price")
            wholesale_price = float(precio_mayorista_texto) if precio_mayorista_texto is not None else None

            precio_minorista_texto = self._texto("retail_price")
            retail_price = float(precio_minorista_texto) if precio_minorista_texto is not None else None
        except ValueError:
            messagebox.showerror("Error de validación", "Stock y precios deben ser números.")
            return

        try:
            if self._es_edicion:
                actualizar_producto(
                    self._producto["id"],
                    code=self._texto("code"),
                    name=self._texto("name"),
                    category=self._texto("category"),
                    brand=self._texto("brand"),
                    description=self._texto("description"),
                    stock=stock,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                )
            else:
                crear_producto(
                    code=self._texto("code"),
                    name=self._texto("name"),
                    category=self._texto("category"),
                    brand=self._texto("brand"),
                    description=self._texto("description"),
                    stock=stock,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                )
        except ValidationError as error:
            messagebox.showerror("Error de validación", str(error))
            return

        self._on_exito()
        self.destroy()
