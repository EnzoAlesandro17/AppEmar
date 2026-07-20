from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src import session
from src.constants.settings import Settings
from src.constants.styles import build_stylesheet
from src.modules.branches.ui import BranchesListWidget
from src.modules.employees.ui import EmployeesListWidget
from src.modules.users.ui import LoginWidget, UsersListWidget


class MainWindow(QMainWindow):
    """Ventana principal: 1000x600, centrada, tamaño fijo. Arranca en el login."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(Settings.APP_NAME)
        self.setFixedSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self._centrar_ventana()

        self._modo_oscuro = False
        self._aplicar_tema()

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self.mostrar_login()

    def _centrar_ventana(self):
        pantalla = QGuiApplication.primaryScreen().geometry()
        x = (pantalla.width() - self.width()) // 2
        y = (pantalla.height() - self.height()) // 2
        self.move(x, y)

    def _aplicar_tema(self):
        self.setStyleSheet(build_stylesheet(dark=self._modo_oscuro))

    def mostrar_login(self):
        self._cambiar_pantalla(LoginWidget(on_login_success=self.mostrar_menu_principal))

    def mostrar_menu_principal(self):
        self._cambiar_pantalla(MainMenuWidget(self))

    def mostrar_sucursales(self):
        self._cambiar_pantalla(BranchesListWidget(self))

    def mostrar_empleados(self):
        self._cambiar_pantalla(EmployeesListWidget(self))

    def mostrar_usuarios(self):
        self._cambiar_pantalla(UsersListWidget(self))

    def alternar_tema(self):
        self._modo_oscuro = not self._modo_oscuro
        self._aplicar_tema()
        # Recrea la pantalla actual para que el avatar (colores hardcodeados
        # en su texto/fondo, no heredados del stylesheet) tome la paleta nueva.
        self.mostrar_menu_principal()

    def cerrar_sesion(self):
        session.cerrar()
        self.mostrar_login()

    def _cambiar_pantalla(self, widget):
        while self._stack.count():
            anterior = self._stack.widget(0)
            self._stack.removeWidget(anterior)
            anterior.deleteLater()
        self._stack.addWidget(widget)


class HeaderBar(QWidget):
    """Barra superior azul: título de la app a la izquierda, tema y usuario a la derecha."""

    def __init__(self, ventana):
        super().__init__()
        self._ventana = ventana
        self.setObjectName("headerBar")
        self._construir_ui()

    def _construir_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(14)

        titulo = QLabel("App de gestión - Emar Ceiba")
        titulo.setObjectName("headerTitle")
        layout.addWidget(titulo)

        layout.addStretch()

        boton_tema = QPushButton("🌙" if not self._ventana._modo_oscuro else "☀️")
        boton_tema.setObjectName("themeToggleButton")
        boton_tema.setCursor(Qt.PointingHandCursor)
        boton_tema.setFixedSize(28, 28)
        boton_tema.clicked.connect(self._ventana.alternar_tema)
        layout.addWidget(boton_tema)

        usuario = session.obtener_usuario()
        inicial = usuario["username"][0].upper() if usuario else "?"
        avatar = QPushButton(inicial)
        avatar.setObjectName("avatarButton")
        avatar.setCursor(Qt.PointingHandCursor)
        avatar.setFixedSize(36, 36)
        menu = QMenu(avatar)
        menu.addAction("Cerrar sesión", self._ventana.cerrar_sesion)
        avatar.setMenu(menu)
        layout.addWidget(avatar)


class MainMenuWidget(QWidget):
    """Pantalla principal: barra superior + los 3 botones, sin pantallas detrás todavía."""

    def __init__(self, ventana):
        super().__init__()
        self._ventana = ventana
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(HeaderBar(self._ventana))

        contenido = QVBoxLayout()
        contenido.setSpacing(8)

        acciones = {
            "Sucursales": self._ventana.mostrar_sucursales,
            "Empleados": self._ventana.mostrar_empleados,
            "Usuarios": self._ventana.mostrar_usuarios,
        }
        for etiqueta, accion in acciones.items():
            boton = QPushButton(etiqueta)
            boton.setObjectName("secondaryButton")
            boton.setFixedWidth(240)
            boton.clicked.connect(accion)
            contenido.addWidget(boton, alignment=Qt.AlignCenter)

        layout.addStretch()
        layout.addLayout(contenido)
        layout.addStretch()
