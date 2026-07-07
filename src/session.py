"""Guarda el usuario logueado en memoria para toda la app."""

usuario_actual = None


def iniciar(usuario):
    global usuario_actual
    usuario_actual = usuario


def cerrar():
    global usuario_actual
    usuario_actual = None
