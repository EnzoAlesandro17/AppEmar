import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import xlwings as xw
import os

class AppCaja:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingreso a CAJA")
        
        # Obtener la ruta al escritorio
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

        # Nombre de archivo
        mes_anio = datetime.now().strftime("%y%m")
        nombre_archivo = f"CAJA3ROSARIO{mes_anio}.xlsx"

        # Ruta completa
        self.archivo = os.path.join(escritorio, nombre_archivo)
        
        # Variables de la UI
        self.campos = [
            "FECHA", "DETALLE", "FAC.", "INGRESO", "SALIDA", "Cant", 
            "OPERACIÓN", "TIPO/MODELO", "DEST", "MODO", "Nº", "Movim.", "OBSERVACIONES"
        ]
        self.vars = {k: tk.StringVar() for k in self.campos}
        
        # Predeterminados
        self.vars["FECHA"].set(datetime.now().strftime("%Y-%m-%d"))
        self.vars["Cant"].set("1")

        self.plantillas = {
            "venta equipo": {"DETALLE": "venta de equipo", "OPERACIÓN": "venta", "Cant": "1"},
            "pago flete": {"DETALLE": "flete", "SALIDA": "1500", "OPERACIÓN": "gasto"}
        }

        self.wb = None
        self.cargar_datos()
        self.crear_ui()

    def leer_col(self, hoja, col, inicio=1, limite_vacias=2):
        datos, vacias, fila = [], 0, inicio
        while vacias < limite_vacias:
            valor = hoja.range(f"{col}{fila}").value
            if valor is None or str(valor).strip() == "":
                vacias += 1
            else:
                vacias = 0
                # Evitar el .0 en números enteros de Excel
                if isinstance(valor, float) and valor.is_integer():
                    datos.append(str(int(valor)))
                else:
                    datos.append(str(valor))
            fila += 1
        return datos

    def cargar_datos(self):
        if not os.path.exists(self.archivo):
            messagebox.showerror("Error", f"No se encontró el archivo: {self.archivo}\nDebe estar creado en el Escritorio.")
            self.root.destroy()
            return

        try:
            # Se conecta al Excel abierto o lo abre si no lo está
            self.wb = xw.Book(self.archivo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al Excel:\n{e}")
            self.root.destroy()
            return

        val = self.wb.sheets["Val"]
        eq = self.wb.sheets["Equipos"]
        mov = self.wb.sheets["Movimiento"]

        # Carga en memoria especificando 20 vacías para Movimiento
        self.listas = {
            "OPERACIÓN": self.leer_col(val, 'A'),
            "TIPO/MODELO": self.leer_col(val, 'C') + self.leer_col(eq, 'A', 4),
            "DEST": self.leer_col(val, 'B'),
            "MODO": self.leer_col(val, 'D') + self.leer_col(val, 'E'),
            "Movim.": self.leer_col(mov, 'A', limite_vacias=20)
        }

    def crear_ui(self):
        if not self.wb: return

        # Configurar tamaño y centrar ventana
        ancho, alto = 971, 600
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Frame principal para separar la UI de la barra de estado
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar las columnas para que se expandan parejo
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)

        # --- Fila 0: Gestión de Plantillas ---
        ttk.Label(main_frame, text="PLANTILLA RÁPIDA:", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.var_plantilla = tk.StringVar()
        combo_plantillas = ttk.Combobox(main_frame, textvariable=self.var_plantilla, values=list(self.plantillas.keys()), state="readonly")
        combo_plantillas.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ttk.Button(main_frame, text="Cargar Plantilla", command=self.cargar_plantilla).grid(row=0, column=2, padx=10, sticky="w")

        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, columnspan=4, sticky="ew", pady=15)

        # --- Filas siguientes: Campos en 2 columnas ---
        fila = 2
        columna = 0
        for campo in self.campos:
            ttk.Label(main_frame, text=campo).grid(row=fila, column=columna, padx=10, pady=5, sticky="w")
            
            if campo in self.listas:
                widget = ttk.Combobox(main_frame, textvariable=self.vars[campo], values=self.listas[campo], state="normal")
                widget.bind("<KeyRelease>", lambda event, c=campo, w=widget: self.filtrar_combo(event, c, w))
            else:
                widget = ttk.Entry(main_frame, textvariable=self.vars[campo])
            
            widget.grid(row=fila, column=columna+1, padx=10, pady=5, sticky="ew")
            
            # Lógica para alternar entre 2 columnas (0 y 2)
            columna += 2
            if columna > 2:
                columna = 0
                fila += 1

        # Botón guardar
        ttk.Button(main_frame, text="Guardar Asiento", command=self.guardar).grid(row=fila+1, column=0, columnspan=4, pady=25)

        # --- Barra de Estado ---
        self.status_bar = ttk.Label(self.root, text=" Listo", relief=tk.SUNKEN, anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def cargar_plantilla(self):
        seleccion = self.var_plantilla.get()
        if seleccion in self.plantillas:
            datos = self.plantillas[seleccion]
            
            # Limpiar campos primero (opcional, para no mezclar datos viejos)
            for k in self.vars:
                if k not in ["FECHA", "Cant"]:
                    self.vars[k].set("")
            
            # Cargar los valores de la plantilla
            for campo, valor in datos.items():
                if campo in self.vars:
                    self.vars[campo].set(valor)
            
            self.status_bar.config(text=f" Plantilla '{seleccion}' cargada con éxito.")

    def filtrar_combo(self, event, campo, widget):
        # Ignorar teclas que no sean de escritura (navegación)
        if event.keysym in ["Up", "Down", "Left", "Right", "Return", "Escape", "Shift_L", "Shift_R", "BackSpace"]:
            return

        texto_ingresado = widget.get().lower()
        
        # Filtrar o restaurar lista
        if not texto_ingresado:
            widget['values'] = self.listas[campo]
        else:
            filtrados = [x for x in self.listas[campo] if texto_ingresado in x.lower()]
            widget['values'] = filtrados

    def guardar(self):
        ingreso = self.vars["INGRESO"].get().strip()
        salida = self.vars["SALIDA"].get().strip()

        if ingreso and salida:
            messagebox.showerror("Error", "Si hay un valor en INGRESO, no puede haber uno en SALIDA y viceversa.")
            return

        hoja_caja = self.wb.sheets["CAJA"]
        
        # Buscar la última fila de abajo hacia arriba en la columna A
        fila_destino = hoja_caja.range('A1048576').end('up').row + 1
        
        # Si la celda A1 está completamente vacía, end('up') devuelve 1, corregimos a fila 1
        if fila_destino == 2 and hoja_caja.range('A1').value is None:
            fila_destino = 1

        # Escribir datos directamente en las celdas
        for col, clave in enumerate(self.campos, start=1):
            hoja_caja.cells(fila_destino, col).value = self.vars[clave].get()
        
        # Escribir datos directamente en las celdas en minúscula
        for col, clave in enumerate(self.campos, start=1):
            valor = self.vars[clave].get().lower()
            hoja_caja.cells(fila_destino, col).value = valor

        try:
            self.wb.save()
            messagebox.showinfo("Éxito", "Fila guardada correctamente.")
            
            # Limpiar todos los campos menos FECHA y Cant
            for k in self.vars:
                if k not in ["FECHA", "Cant"]:
                    self.vars[k].set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCaja(root)
    root.mainloop()