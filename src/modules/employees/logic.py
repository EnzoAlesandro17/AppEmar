from src.constants.validations import opcional, requerido, validar_email
from src.exceptions import ValidationError
from src.modules.employees import db


def listar():
    return db.listar_activos()


def obtener(id_):
    return db.obtener_por_id(id_)


def crear(code, name, last_name, phone, email, branch_id):
    code = requerido(code, "Código")
    name = requerido(name, "Nombre")
    last_name = requerido(last_name, "Apellido")
    email = validar_email(email, "Email")
    if not branch_id:
        raise ValidationError("Tenés que elegir una sucursal")
    if db.existe_code(code):
        raise ValidationError(f"Ya existe un empleado con el código '{code}'")
    return db.insertar(code, name, last_name, opcional(phone), email, branch_id)


def actualizar(id_, code, name, last_name, phone, email, branch_id):
    code = requerido(code, "Código")
    name = requerido(name, "Nombre")
    last_name = requerido(last_name, "Apellido")
    email = validar_email(email, "Email")
    if not branch_id:
        raise ValidationError("Tenés que elegir una sucursal")
    if db.existe_code(code, excluir_id=id_):
        raise ValidationError(f"Ya existe un empleado con el código '{code}'")
    db.actualizar(id_, code, name, last_name, opcional(phone), email, branch_id)


def eliminar(id_):
    db.eliminar(id_)
