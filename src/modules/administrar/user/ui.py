from tkinter import messagebox

from src import session
from src.constants.styles import Colors
from src.modules.administrar.branches.logic import listar_sucursales
from src.modules.administrar.listado_frame import ListadoFrame
from src.modules.administrar.user.logic import borrar_usuario, listar_usuarios, obtener_por_id
from src.modules.administrar.user.password_dialog import CambiarContrasenaDialog
from src.modules.administrar.user.user_form_dialog import UsuarioFormDialog
from src.permissions import puede_cambiar_password, puede_gestionar_usuarios


class UsuariosFrame(ListadoFrame):
    """Interfaz del módulo de usuarios: listado + alta/edición/baja/cambio de contraseña."""

    TITULO = "Usuarios"
    COLUMNAS = ("code", "name", "last_name", "dni", "username", "role", "branch")
    ENCABEZADOS = {
        "code": "Código",
        "name": "Nombre",
        "last_name": "Apellido",
        "dni": "DNI",
        "username": "Usuario",
        "role": "Rol",
        "branch": "Sucursal",
    }

    def __init__(self, master):
        usuario_logueado = session.usuario_actual
        self._rol_actual = usuario_logueado["role"] if usuario_logueado else None
        super().__init__(master)

    def _definir_botones(self):
        # Se empaquetan de derecha a izquierda: esta lista queda en orden de
        # lectura normal (Nuevo, Editar, Eliminar, Cambiar contraseña).
        return [
            {"clave": "password", "texto": "Cambiar contraseña", "command": self._cambiar_password},
            {"clave": "eliminar", "texto": "Eliminar", "command": self._eliminar, "color": Colors.BTN_DANGER},
            {"clave": "editar", "texto": "Editar", "command": self._editar},
            {"clave": "nuevo", "texto": "Nuevo usuario", "command": self._nuevo},
        ]

    def actualizar_botones(self):
        id_usuario = self.id_seleccionado()
        gestion_ok = puede_gestionar_usuarios(self._rol_actual)
        estado_gestion = "normal" if gestion_ok and id_usuario is not None else "disabled"

        self.boton("nuevo").configure(state="normal" if gestion_ok else "disabled")
        self.boton("editar").configure(state=estado_gestion)
        self.boton("eliminar").configure(state=estado_gestion)
        self.boton("password").configure(state=self._estado_password(id_usuario))

    def _estado_password(self, id_usuario):
        if id_usuario is None:
            return "disabled"
        objetivo = obtener_por_id(id_usuario)
        usuario_logueado = session.usuario_actual
        es_uno_mismo = usuario_logueado is not None and usuario_logueado["id"] == id_usuario
        puede = puede_cambiar_password(self._rol_actual, objetivo["role"], es_uno_mismo)
        return "normal" if puede else "disabled"

    def refrescar(self):
        self.limpiar_filas()
        nombres_sucursal = {s["id"]: s["name"] for s in listar_sucursales()}

        for usuario in listar_usuarios():
            self.insertar_fila(
                usuario["id"],
                (
                    usuario["code"] or "",
                    usuario["name"],
                    usuario["last_name"],
                    usuario["dni"],
                    usuario["username"] or "",
                    usuario["role"],
                    nombres_sucursal.get(usuario["branch_id"], ""),
                ),
            )

        self.actualizar_botones()

    def _nuevo(self):
        UsuarioFormDialog(self, on_exito=self.refrescar)

    def _editar(self):
        id_usuario = self.id_seleccionado()
        if id_usuario is None:
            return
        usuario = obtener_por_id(id_usuario)
        UsuarioFormDialog(self, on_exito=self.refrescar, usuario=usuario)

    def _eliminar(self):
        id_usuario = self.id_seleccionado()
        if id_usuario is None:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            borrar_usuario(id_usuario)
            self.refrescar()

    def _cambiar_password(self):
        id_usuario = self.id_seleccionado()
        if id_usuario is None:
            return
        CambiarContrasenaDialog(self, on_exito=self.refrescar, id_usuario=id_usuario)
