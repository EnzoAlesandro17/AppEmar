import re
from datetime import date, datetime

from src.exceptions import ValidationError

_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DNI_REGEX = re.compile(r"^\d{7,8}$")
_CUIT_REGEX = re.compile(r"^\d{11}$")
_PHONE_REGEX = re.compile(r"^\d{13}$")
_FORMATO_FECHA = "%Y-%m-%d"


def validar_email(email):
    if not _EMAIL_REGEX.match(email):
        raise ValidationError("El email no tiene un formato válido.")


def validar_telefono(phone):
    """Valida que tenga 13 dígitos (código de país + área + número, ej: 54 9 341 5018444).

    Devuelve el teléfono normalizado (solo dígitos, sin espacios ni guiones).
    """
    limpio = re.sub(r"[\s-]", "", phone)
    if not _PHONE_REGEX.match(limpio):
        raise ValidationError(
            "El teléfono debe tener 13 dígitos con código de país y de área, "
            "ej: 54 9 341 5018444."
        )
    return limpio


def validar_dni(dni):
    if not _DNI_REGEX.match(dni):
        raise ValidationError("El DNI debe tener entre 7 y 8 dígitos, sin puntos ni letras.")


def validar_cuit(cuit):
    """Valida que tenga 11 dígitos (formato XX-XXXXXXXX-X).

    Devuelve el CUIT normalizado (solo dígitos, sin guiones).
    """
    limpio = re.sub(r"-", "", cuit)
    if not _CUIT_REGEX.match(limpio):
        raise ValidationError("El CUIT debe tener 11 dígitos, ej: 20-12345678-9.")
    return limpio


def validar_fecha(fecha_str):
    """Valida formato AAAA-MM-DD y devuelve un date."""
    try:
        return datetime.strptime(fecha_str, _FORMATO_FECHA).date()
    except (ValueError, TypeError):
        raise ValidationError("La fecha debe tener formato AAAA-MM-DD y ser una fecha válida.")


def validar_mayor_edad(fecha_nacimiento, edad_minima=18):
    """Recibe un date (ver validar_fecha) y valida una edad mínima."""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )
    if edad < edad_minima:
        raise ValidationError(f"La persona debe ser mayor de {edad_minima} años.")


def validar_campos_obligatorios(campos):
    """Recibe {nombre_campo: valor} y lanza ValidationError con el primero vacío."""
    for campo, valor in campos.items():
        if not valor or not str(valor).strip():
            raise ValidationError(f"Falta {campo}")


def limpiar_documento(valor):
    return valor.replace("-", "").replace(" ", "")


def validar_documento(dni_cuit):
    """Detecta si es DNI (7-8 dígitos) o CUIT (11 dígitos), valida y devuelve el valor normalizado."""
    limpio = limpiar_documento(dni_cuit)
    if len(limpio) in (7, 8):
        validar_dni(limpio)
    elif len(limpio) == 11:
        validar_cuit(limpio)
    else:
        raise ValidationError("El documento debe tener 7-8 dígitos (DNI) u 11 dígitos (CUIT).")
    return limpio
