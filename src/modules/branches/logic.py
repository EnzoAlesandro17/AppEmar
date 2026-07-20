from src.constants.validations import opcional, requerido, validar_email
from src.exceptions import ValidationError
from src.modules.branches import db


def listar():
    return db.listar_activas()


def obtener(id_):
    return db.obtener_por_id(id_)


def crear(code, name, address, street_number, email, city, state, country):
    code = requerido(code, "Código")
    name = requerido(name, "Nombre")
    email = validar_email(email, "Email")
    if db.existe_code(code):
        raise ValidationError(f"Ya existe una sucursal con el código '{code}'")
    return db.insertar(
        code, name, opcional(address), opcional(street_number), email,
        opcional(city), opcional(state), opcional(country),
    )


def actualizar(id_, code, name, address, street_number, email, city, state, country):
    code = requerido(code, "Código")
    name = requerido(name, "Nombre")
    email = validar_email(email, "Email")
    if db.existe_code(code, excluir_id=id_):
        raise ValidationError(f"Ya existe una sucursal con el código '{code}'")
    db.actualizar(
        id_, code, name, opcional(address), opcional(street_number), email,
        opcional(city), opcional(state), opcional(country),
    )


def eliminar(id_):
    db.eliminar(id_)
