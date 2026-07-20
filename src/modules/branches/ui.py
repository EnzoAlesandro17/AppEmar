from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

from src.exceptions import ValidationError
from src.modules.branches import logic
from src.widgets.crud_list_widget import CrudListWidget


class BranchesListWidget(CrudListWidget):
    titulo = "Sucursales"
    columnas = ["Código", "Nombre", "Ciudad", "Provincia", "País", "Email"]

    def listar(self):
        return logic.listar()

    def fila_a_valores(self, fila):
        return [
            fila["code"],
            fila["name"],
            fila["city"] or "",
            fila["state"] or "",
            fila["country"] or "",
            fila["email"] or "",
        ]

    def abrir_dialogo(self, id_=None):
        return BranchFormDialog(self, id_branch=id_)

    def eliminar(self, id_):
        logic.eliminar(id_)

    def texto_confirmacion_eliminar(self):
        return "¿Eliminar la sucursal seleccionada?"


class BranchFormDialog(QDialog):
    def __init__(self, master, id_branch=None):
        super().__init__(master)
        self._id_branch = id_branch
        self.setWindowTitle("Editar sucursal" if id_branch else "Nueva sucursal")
        self.setFixedWidth(360)
        self._construir_ui()
        if id_branch:
            self._cargar_datos(id_branch)

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self._campo_code = QLineEdit()
        self._campo_name = QLineEdit()
        self._campo_address = QLineEdit()
        self._campo_street_number = QLineEdit()
        self._campo_email = QLineEdit()
        self._campo_city = QLineEdit()
        self._campo_state = QLineEdit()
        self._campo_country = QLineEdit()

        formulario.addRow("Código", self._campo_code)
        formulario.addRow("Nombre", self._campo_name)
        formulario.addRow("Dirección", self._campo_address)
        formulario.addRow("Número", self._campo_street_number)
        formulario.addRow("Email", self._campo_email)
        formulario.addRow("Ciudad", self._campo_city)
        formulario.addRow("Provincia", self._campo_state)
        formulario.addRow("País", self._campo_country)
        layout.addLayout(formulario)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.setObjectName("primaryButton")
        boton_guardar.clicked.connect(self._guardar)
        layout.addWidget(boton_guardar)

    def _cargar_datos(self, id_branch):
        fila = logic.obtener(id_branch)
        self._campo_code.setText(fila["code"] or "")
        self._campo_name.setText(fila["name"] or "")
        self._campo_address.setText(fila["address"] or "")
        self._campo_street_number.setText(fila["street_number"] or "")
        self._campo_email.setText(fila["email"] or "")
        self._campo_city.setText(fila["city"] or "")
        self._campo_state.setText(fila["state"] or "")
        self._campo_country.setText(fila["country"] or "")

    def _guardar(self):
        datos = (
            self._campo_code.text(),
            self._campo_name.text(),
            self._campo_address.text(),
            self._campo_street_number.text(),
            self._campo_email.text(),
            self._campo_city.text(),
            self._campo_state.text(),
            self._campo_country.text(),
        )
        try:
            if self._id_branch:
                logic.actualizar(self._id_branch, *datos)
            else:
                logic.crear(*datos)
        except ValidationError as error:
            QMessageBox.critical(self, "Error", str(error))
            return
        self.accept()
