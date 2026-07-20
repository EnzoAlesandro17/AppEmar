from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from src.exceptions import ValidationError
from src.modules.branches import logic as branches_logic
from src.modules.employees import logic
from src.widgets.crud_list_widget import CrudListWidget


class EmployeesListWidget(CrudListWidget):
    titulo = "Empleados"
    columnas = ["Código", "Nombre", "Apellido", "Sucursal", "Email"]

    def listar(self):
        return logic.listar()

    def fila_a_valores(self, fila):
        return [
            fila["code"],
            fila["name"],
            fila["last_name"],
            fila["branch_name"] or "",
            fila["email"] or "",
        ]

    def abrir_dialogo(self, id_=None):
        return EmployeeFormDialog(self, id_employee=id_)

    def eliminar(self, id_):
        logic.eliminar(id_)

    def texto_confirmacion_eliminar(self):
        return "¿Eliminar el empleado seleccionado?"


class EmployeeFormDialog(QDialog):
    def __init__(self, master, id_employee=None):
        super().__init__(master)
        self._id_employee = id_employee
        self.setWindowTitle("Editar empleado" if id_employee else "Nuevo empleado")
        self.setFixedWidth(360)
        self._construir_ui()
        if id_employee:
            self._cargar_datos(id_employee)

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self._campo_code = QLineEdit()
        self._campo_name = QLineEdit()
        self._campo_last_name = QLineEdit()
        self._campo_phone = QLineEdit()
        self._campo_email = QLineEdit()
        self._campo_branch = QComboBox()
        for sucursal in branches_logic.listar():
            self._campo_branch.addItem(f"{sucursal['code']} - {sucursal['name']}", sucursal["id"])

        formulario.addRow("Código", self._campo_code)
        formulario.addRow("Nombre", self._campo_name)
        formulario.addRow("Apellido", self._campo_last_name)
        formulario.addRow("Teléfono", self._campo_phone)
        formulario.addRow("Email", self._campo_email)
        formulario.addRow("Sucursal", self._campo_branch)
        layout.addLayout(formulario)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.setObjectName("primaryButton")
        boton_guardar.clicked.connect(self._guardar)
        layout.addWidget(boton_guardar)

    def _cargar_datos(self, id_employee):
        fila = logic.obtener(id_employee)
        self._campo_code.setText(fila["code"] or "")
        self._campo_name.setText(fila["name"] or "")
        self._campo_last_name.setText(fila["last_name"] or "")
        self._campo_phone.setText(fila["phone"] or "")
        self._campo_email.setText(fila["email"] or "")
        if fila["branch_id"]:
            indice = self._campo_branch.findData(fila["branch_id"])
            if indice >= 0:
                self._campo_branch.setCurrentIndex(indice)

    def _guardar(self):
        datos = (
            self._campo_code.text(),
            self._campo_name.text(),
            self._campo_last_name.text(),
            self._campo_phone.text(),
            self._campo_email.text(),
            self._campo_branch.currentData(),
        )
        try:
            if self._id_employee:
                logic.actualizar(self._id_employee, *datos)
            else:
                logic.crear(*datos)
        except ValidationError as error:
            QMessageBox.critical(self, "Error", str(error))
            return
        self.accept()
