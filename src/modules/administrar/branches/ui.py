from src.constants.styles import Colors
from src.modules.administrar.branches.logic import listar_sucursales
from src.modules.administrar.listado_frame import ListadoFrame


class SucursalesFrame(ListadoFrame):
    """Listado de sucursales, de solo lectura: el alta/edición se gestiona fuera de la app por ahora."""

    TITULO = "Sucursales"
    COLUMNAS = ("code", "name", "country", "city", "address", "phone")
    ENCABEZADOS = {
        "code": "Código",
        "name": "Nombre",
        "country": "País",
        "city": "Ciudad",
        "address": "Dirección",
        "phone": "Teléfono",
    }

    def _definir_botones(self):
        # Sin command: quedan siempre deshabilitados (actualizar_botones no
        # se sobreescribe) hasta que el módulo tenga alta/edición real.
        return [
            {"clave": "eliminar", "texto": "Eliminar", "color": Colors.BTN_DANGER},
            {"clave": "editar", "texto": "Editar"},
            {"clave": "nueva", "texto": "Nueva sucursal"},
        ]

    def refrescar(self):
        self.limpiar_filas()
        for sucursal in listar_sucursales():
            self.insertar_fila(
                sucursal["id"],
                (
                    sucursal["code"] or "",
                    sucursal["name"],
                    sucursal["country"] or "",
                    sucursal["city"] or "",
                    sucursal["address"] or "",
                    sucursal["phone"] or "",
                ),
            )
