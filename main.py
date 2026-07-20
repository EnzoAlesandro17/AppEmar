import sys

from PySide6.QtWidgets import QApplication

from src.app import MainWindow
from src.modules.branches.db import crear_tabla as crear_tabla_branches
from src.modules.employees.db import crear_tabla as crear_tabla_employees
from src.modules.users.db import crear_tabla as crear_tabla_users
from src.modules.users.logic import sembrar_admin


def inicializar_db():
    crear_tabla_branches()
    crear_tabla_employees()
    crear_tabla_users()
    sembrar_admin()


if __name__ == "__main__":
    inicializar_db()
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
