import hashlib
import os

from src.constants.validations import requerido, validar_email
from src.exceptions import ValidationError
from src.modules.users import db

_ITERACIONES_HASH = 100_000


def _hashear_contrasena(contrasena):
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, _ITERACIONES_HASH)
    return f"{salt.hex()}${hash_bytes.hex()}"


def _verificar_contrasena(contrasena, contrasena_guardada):
    salt_hex, hash_hex = contrasena_guardada.split("$")
    salt = bytes.fromhex(salt_hex)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, _ITERACIONES_HASH)
    return hash_bytes.hex() == hash_hex


def sembrar_admin():
    """Por ahora, único usuario de arranque: Admin/Admin con rol IT."""
    if not db.existe_algun_usuario():
        db.insertar("Admin", _hashear_contrasena("Admin"), "", "IT", None)


def iniciar_sesion(username, password):
    fila = db.obtener_por_username(username)
    if fila is None or not _verificar_contrasena(password, fila["password"]):
        raise ValidationError("Usuario o contraseña incorrectos")
    return fila


def listar():
    return db.listar_activos()


def obtener(id_):
    return db.obtener_por_id(id_)


def crear(username, password, email, role, employee_id):
    username = requerido(username, "Usuario")
    password = requerido(password, "Contraseña")
    email = validar_email(email, "Email")
    if db.existe_username(username):
        raise ValidationError(f"Ya existe un usuario '{username}'")
    return db.insertar(username, _hashear_contrasena(password), email, role, employee_id)


def actualizar(id_, username, password, email, role, employee_id):
    username = requerido(username, "Usuario")
    email = validar_email(email, "Email")
    if db.existe_username(username, excluir_id=id_):
        raise ValidationError(f"Ya existe un usuario '{username}'")
    password_hash = _hashear_contrasena(password) if password else None
    db.actualizar(id_, username, password_hash, email, role, employee_id)


def eliminar(id_):
    db.eliminar(id_)
