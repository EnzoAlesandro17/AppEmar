from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src import session
from src.constants.settings import Settings
from src.exceptions import ValidationError
from src.modules.employees import logic as employees_logic
from src.modules.users import logic
from src.widgets.crud_list_widget import CrudListWidget


class LoginWidget(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self._on_login_success = on_login_success
        self._construir_ui()

    def _construir_ui(self):
        layout_externo = QVBoxLayout(self)
        layout_externo.addStretch()

        formulario = QWidget()
        formulario.setFixedWidth(320)
        layout = QVBoxLayout(formulario)
        layout.setSpacing(8)

        titulo = QLabel("AppEmar")
        titulo.setObjectName("titleLabel")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        layout.addSpacing(16)

        layout.addWidget(QLabel("Usuario"))
        self._entrada_usuario = QLineEdit()
        layout.addWidget(self._entrada_usuario)

        layout.addWidget(QLabel("Contraseña"))
        self._entrada_contrasena = QLineEdit()
        self._entrada_contrasena.setEchoMode(QLineEdit.Password)
        self._entrada_contrasena.returnPressed.connect(self._iniciar_sesion)
        layout.addWidget(self._entrada_contrasena)
        layout.addSpacing(12)

        boton = QPushButton("Ingresar")
        boton.setObjectName("primaryButton")
        boton.clicked.connect(self._iniciar_sesion)
        layout.addWidget(boton)

        layout_externo.addWidget(formulario, alignment=Qt.AlignCenter)
        layout_externo.addStretch()

        self._entrada_usuario.setFocus()

    def _iniciar_sesion(self):
        username = self._entrada_usuario.text().strip()
        password = self._entrada_contrasena.text()
        try:
            usuario = logic.iniciar_sesion(username, password)
        except ValidationError as error:
            QMessageBox.critical(self, "Error", str(error))
            return
        session.iniciar(usuario)
        self._on_login_success()


class UsersListWidget(CrudListWidget):
    titulo = "Usuarios"
    columnas = ["Usuario", "Rol", "Empleado", "Email"]

    def listar(self):
        return logic.listar()

    def fila_a_valores(self, fila):
        empleado = ""
        if fila["employee_name"]:
            empleado = f"{fila['employee_name']} {fila['employee_last_name']}"
        return [fila["username"], fila["role"], empleado, fila["email"] or ""]

    def abrir_dialogo(self, id_=None):
        return UserFormDialog(self, id_user=id_)

    def eliminar(self, id_):
        logic.eliminar(id_)

    def texto_confirmacion_eliminar(self):
        return "¿Eliminar el usuario seleccionado?"


class UserFormDialog(QDialog):
    def __init__(self, master, id_user=None):
        super().__init__(master)
        self._id_user = id_user
        self.setWindowTitle("Editar usuario" if id_user else "Nuevo usuario")
        self.setFixedWidth(360)
        self._construir_ui()
        if id_user:
            self._cargar_datos(id_user)

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self._campo_username = QLineEdit()
        self._campo_password = QLineEdit()
        self._campo_password.setEchoMode(QLineEdit.Password)
        self._campo_email = QLineEdit()
        self._campo_role = QComboBox()
        self._campo_role.addItems(Settings.ROLES)
        self._campo_employee = QComboBox()
        self._campo_employee.addItem("(sin empleado vinculado)", None)
        for empleado in employees_logic.listar():
            self._campo_employee.addItem(
                f"{empleado['code']} - {empleado['name']} {empleado['last_name']}", empleado["id"]
            )

        formulario.addRow("Usuario", self._campo_username)
        pista_password = "Contraseña" if self._id_user is None else "Contraseña (vacío = no cambiar)"
        formulario.addRow(pista_password, self._campo_password)
        formulario.addRow("Email", self._campo_email)
        formulario.addRow("Rol", self._campo_role)
        formulario.addRow("Empleado", self._campo_employee)
        layout.addLayout(formulario)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.setObjectName("primaryButton")
        boton_guardar.clicked.connect(self._guardar)
        layout.addWidget(boton_guardar)

    def _cargar_datos(self, id_user):
        fila = logic.obtener(id_user)
        self._campo_username.setText(fila["username"] or "")
        self._campo_email.setText(fila["email"] or "")
        indice_rol = self._campo_role.findText(fila["role"])
        if indice_rol >= 0:
            self._campo_role.setCurrentIndex(indice_rol)
        if fila["employee_id"]:
            indice_empleado = self._campo_employee.findData(fila["employee_id"])
            if indice_empleado >= 0:
                self._campo_employee.setCurrentIndex(indice_empleado)

    def _guardar(self):
        datos = (
            self._campo_username.text(),
            self._campo_password.text(),
            self._campo_email.text(),
            self._campo_role.currentText(),
            self._campo_employee.currentData(),
        )
        try:
            if self._id_user:
                logic.actualizar(self._id_user, *datos)
            else:
                logic.crear(*datos)
        except ValidationError as error:
            QMessageBox.critical(self, "Error", str(error))
            return
        self.accept()
