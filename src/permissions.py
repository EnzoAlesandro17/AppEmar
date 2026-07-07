"""Reglas de que rol puede hacer que accion, centralizadas para reusar entre modulos."""

_GESTIONAN_USUARIOS = ("Admin", "Gerente")
_CAMBIAN_CONTRASENAS = ("Admin", "Gerente", "Vendedor")


def puede_gestionar_usuarios(role):
    return role in _GESTIONAN_USUARIOS


def puede_cambiar_contrasenas(role):
    return role in _CAMBIAN_CONTRASENAS
