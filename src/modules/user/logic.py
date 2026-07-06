import hashlib
import os
import sqlite3

from src.constants.validations import validar_dni, validar_email, validar_fecha, validar_mayor_edad, validar_telefono
from src.db.connection import obtener_conexion
from src.exceptions import ValidationError
from src.modules.user.db import TABLA

_ITERACIONES_HASH = 100_000


def _hashear_contrasena(contrasena):
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, _ITERACIONES_HASH)
    return f"{salt.hex()}${hash_bytes.hex()}"


def _verificar_hash(contrasena, contrasena_guardada):
    salt_hex, hash_hex = contrasena_guardada.split("$")
    salt = bytes.fromhex(salt_hex)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, _ITERACIONES_HASH)
    return hash_bytes.hex() == hash_hex


def _validar_datos(name, last_name, dni, username, password, email, birth_date, phone):
    if not name or not name.strip():
        raise ValidationError("El nombre es obligatorio.")
    if not last_name or not last_name.strip():
        raise ValidationError("El apellido es obligatorio.")
    if not dni or not dni.strip():
        raise ValidationError("El DNI es obligatorio.")
    validar_dni(dni)

    if bool(username) != bool(password):
        raise ValidationError("Usuario y contraseña deben cargarse juntos, o dejarse los dos vacíos.")

    if email:
        validar_email(email)

    telefono_normalizado = validar_telefono(phone) if phone else None

    if birth_date:
        fecha = validar_fecha(birth_date)
        validar_mayor_edad(fecha)

    return telefono_normalizado


def _traducir_error_integridad(error):
    mensaje = str(error)
    if "code" in mensaje:
        return ValidationError("Ya existe un usuario con ese code.")
    if "dni" in mensaje:
        return ValidationError("Ya existe un usuario con ese DNI.")
    if "username" in mensaje:
        return ValidationError("Ese nombre de usuario ya está en uso.")
    return ValidationError("Ya existe un usuario con alguno de esos datos únicos.")


def crear_usuario(name, last_name, dni, code=None, username=None, password=None,
                   email=None, birth_date=None, phone=None):
    """Valida y crea un usuario nuevo. Devuelve el id generado."""
    telefono_normalizado = _validar_datos(name, last_name, dni, username, password, email, birth_date, phone)

    contrasena_hasheada = _hashear_contrasena(password) if password else None

    with obtener_conexion() as conexion:
        try:
            cursor = conexion.execute(
                f"""
                INSERT INTO {TABLA}
                    (code, name, last_name, dni, username, password, email, birth_date, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (code, name, last_name, dni, username, contrasena_hasheada, email, birth_date,
                 telefono_normalizado),
            )
            conexion.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as error:
            raise _traducir_error_integridad(error) from error


def obtener_por_id(id_usuario):
    with obtener_conexion() as conexion:
        return conexion.execute(f"SELECT * FROM {TABLA} WHERE id = ?", (id_usuario,)).fetchone()


def obtener_por_username(username):
    with obtener_conexion() as conexion:
        return conexion.execute(
            f"SELECT * FROM {TABLA} WHERE username = ?", (username,)
        ).fetchone()


def listar_usuarios(incluir_borrados=False):
    consulta = f"SELECT * FROM {TABLA}"
    if not incluir_borrados:
        consulta += " WHERE status = 1"
    consulta += " ORDER BY last_name, name"

    with obtener_conexion() as conexion:
        return conexion.execute(consulta).fetchall()


def actualizar_usuario(id_usuario, name=None, last_name=None, dni=None, code=None,
                        username=None, password=None, email=None, birth_date=None, phone=None):
    """Actualiza los campos recibidos; los que se pasan en None mantienen su valor actual."""
    usuario_actual = obtener_por_id(id_usuario)
    if usuario_actual is None:
        raise ValidationError("El usuario no existe.")

    nuevos = {
        "name": name if name is not None else usuario_actual["name"],
        "last_name": last_name if last_name is not None else usuario_actual["last_name"],
        "dni": dni if dni is not None else usuario_actual["dni"],
        "code": code if code is not None else usuario_actual["code"],
        "username": username if username is not None else usuario_actual["username"],
        "email": email if email is not None else usuario_actual["email"],
        "birth_date": birth_date if birth_date is not None else usuario_actual["birth_date"],
        "phone": phone if phone is not None else usuario_actual["phone"],
    }
    password_efectivo = password if password is not None else usuario_actual["password"]

    telefono_normalizado = _validar_datos(
        nuevos["name"], nuevos["last_name"], nuevos["dni"], nuevos["username"],
        password_efectivo, nuevos["email"], nuevos["birth_date"], nuevos["phone"],
    )

    contrasena_hasheada = _hashear_contrasena(password) if password else usuario_actual["password"]

    with obtener_conexion() as conexion:
        try:
            conexion.execute(
                f"""
                UPDATE {TABLA}
                SET code = ?, name = ?, last_name = ?, dni = ?, username = ?,
                    password = ?, email = ?, birth_date = ?, phone = ?
                WHERE id = ?
                """,
                (
                    nuevos["code"], nuevos["name"], nuevos["last_name"], nuevos["dni"],
                    nuevos["username"], contrasena_hasheada, nuevos["email"],
                    nuevos["birth_date"], telefono_normalizado, id_usuario,
                ),
            )
            conexion.commit()
        except sqlite3.IntegrityError as error:
            raise _traducir_error_integridad(error) from error


def borrar_usuario(id_usuario):
    """Borrado lógico: marca status = 0 en vez de eliminar la fila."""
    with obtener_conexion() as conexion:
        conexion.execute(f"UPDATE {TABLA} SET status = 0 WHERE id = ?", (id_usuario,))
        conexion.commit()


def reactivar_usuario(id_usuario):
    """Revierte un borrado lógico: vuelve a marcar status = 1."""
    with obtener_conexion() as conexion:
        conexion.execute(f"UPDATE {TABLA} SET status = 1 WHERE id = ?", (id_usuario,))
        conexion.commit()


def verificar_contrasena(username, password):
    """Para el futuro login: True si la contraseña coincide con la del usuario."""
    usuario = obtener_por_username(username)
    if usuario is None or usuario["password"] is None:
        return False
    return _verificar_hash(password, usuario["password"])
