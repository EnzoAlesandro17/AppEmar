"""Usuario logueado, guardado en memoria para que cualquier pantalla lo consulte."""

_usuario_actual = None


def iniciar(usuario):
    global _usuario_actual
    _usuario_actual = usuario


def cerrar():
    global _usuario_actual
    _usuario_actual = None


def obtener_usuario():
    return _usuario_actual
