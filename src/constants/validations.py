import re

from src.exceptions import ValidationError

_PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def requerido(valor, campo):
    valor = (valor or "").strip()
    if not valor:
        raise ValidationError(f"{campo} es obligatorio")
    return valor


def opcional(valor):
    return (valor or "").strip()


def validar_email(valor, campo="Email", obligatorio=False):
    valor = (valor or "").strip()
    if not valor:
        if obligatorio:
            raise ValidationError(f"{campo} es obligatorio")
        return ""
    if not _PATRON_EMAIL.match(valor):
        raise ValidationError(f"{campo} no tiene un formato válido")
    return valor
