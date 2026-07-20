from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CrudListWidget(QWidget):
    """Pantalla genérica de listado: tabla + Agregar/Editar/Eliminar/Volver.

    Cada módulo define `titulo`/`columnas` y los métodos de abajo; esta
    clase arma la pantalla una sola vez para no repetirla por módulo.
    """

    titulo = ""
    columnas = []

    def __init__(self, ventana):
        super().__init__()
        self._ventana = ventana
        self._construir_ui()
        self._cargar_datos()

    # --- a definir en cada módulo ---

    def listar(self):
        raise NotImplementedError

    def fila_a_valores(self, fila):
        """Lista de strings a mostrar en la fila de la tabla, una por columna."""
        raise NotImplementedError

    def abrir_dialogo(self, id_=None):
        """Devuelve el QDialog de alta (id_=None) o edición (id_ existente)."""
        raise NotImplementedError

    def eliminar(self, id_):
        raise NotImplementedError

    def texto_confirmacion_eliminar(self):
        return "¿Eliminar el registro seleccionado?"

    # --- UI compartida ---

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        encabezado = QHBoxLayout()
        titulo = QLabel(self.titulo)
        titulo.setObjectName("titleLabel")
        encabezado.addWidget(titulo)
        encabezado.addStretch()

        boton_volver = QPushButton("Volver")
        boton_volver.setObjectName("secondaryButton")
        boton_volver.clicked.connect(self._ventana.mostrar_menu_principal)
        encabezado.addWidget(boton_volver)
        layout.addLayout(encabezado)

        self._tabla = QTableWidget(0, len(self.columnas))
        self._tabla.setHorizontalHeaderLabels(self.columnas)
        self._tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self._tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tabla.doubleClicked.connect(self._editar)
        layout.addWidget(self._tabla)

        acciones = QHBoxLayout()
        boton_agregar = QPushButton("Agregar")
        boton_agregar.setObjectName("secondaryButton")
        boton_agregar.clicked.connect(self._agregar)
        acciones.addWidget(boton_agregar)

        boton_editar = QPushButton("Editar")
        boton_editar.setObjectName("secondaryButton")
        boton_editar.clicked.connect(self._editar)
        acciones.addWidget(boton_editar)

        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.setObjectName("secondaryButton")
        boton_eliminar.clicked.connect(self._eliminar)
        acciones.addWidget(boton_eliminar)
        acciones.addStretch()
        layout.addLayout(acciones)

    def _cargar_datos(self):
        filas = self.listar()
        self._tabla.setRowCount(len(filas))
        for indice, fila in enumerate(filas):
            for columna, valor in enumerate(self.fila_a_valores(fila)):
                self._tabla.setItem(indice, columna, QTableWidgetItem(valor))
            self._tabla.item(indice, 0).setData(Qt.UserRole, fila["id"])

    def _fila_seleccionada_id(self):
        indice = self._tabla.currentRow()
        if indice < 0:
            return None
        return self._tabla.item(indice, 0).data(Qt.UserRole)

    def _agregar(self):
        if self.abrir_dialogo().exec():
            self._cargar_datos()

    def _editar(self):
        id_ = self._fila_seleccionada_id()
        if id_ is None:
            QMessageBox.information(self, "Editar", "Seleccioná un registro primero")
            return
        if self.abrir_dialogo(id_).exec():
            self._cargar_datos()

    def _eliminar(self):
        id_ = self._fila_seleccionada_id()
        if id_ is None:
            QMessageBox.information(self, "Eliminar", "Seleccioná un registro primero")
            return
        respuesta = QMessageBox.question(self, "Eliminar", self.texto_confirmacion_eliminar())
        if respuesta == QMessageBox.Yes:
            self.eliminar(id_)
            self._cargar_datos()
