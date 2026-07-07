"""Reglas de que rol puede hacer que accion, centralizadas para reusar entre modulos."""

_GESTIONAN_USUARIOS = ("Admin", "Supervisor")


def puede_gestionar_usuarios(role):
    return role in _GESTIONAN_USUARIOS


def puede_cambiar_alguna_password(role):
    """True si ese rol puede cambiar la contrasena de alguien (aunque sea la propia)."""
    return role != "Invitado"


def puede_cambiar_password(actor_role, target_role, es_uno_mismo):
    """Jerarquia: Admin > Supervisor > Vendedor > Invitado.

    - Admin cambia la de cualquiera.
    - Supervisor cambia la de cualquiera menos Admin.
    - Vendedor solo cambia la de otros Vendedores.
    - Invitado no cambia ninguna (ni la propia: entra sin password).
    - Cualquiera (menos Invitado) puede cambiar la propia.
    """
    if actor_role == "Invitado":
        return False
    if es_uno_mismo:
        return True
    if actor_role == "Admin":
        return True
    if actor_role == "Supervisor":
        return target_role != "Admin"
    if actor_role == "Vendedor":
        return target_role == "Vendedor"
    return False
