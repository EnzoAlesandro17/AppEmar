from src.db.connection import obtener_conexion
from src.modules.branches.db import TABLE as TABLE_BRANCHES

TABLE = "employees"


def crear_tabla():
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                branch_id INTEGER REFERENCES {TABLE_BRANCHES}(id),
                status INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conexion.commit()


def listar_activos():
    with obtener_conexion() as conexion:
        return conexion.execute(
            f"""
            SELECT {TABLE}.*, {TABLE_BRANCHES}.name AS branch_name
            FROM {TABLE}
            LEFT JOIN {TABLE_BRANCHES} ON {TABLE_BRANCHES}.id = {TABLE}.branch_id
            WHERE {TABLE}.status = 1
            ORDER BY {TABLE}.last_name, {TABLE}.name
            """
        ).fetchall()


def obtener_por_id(id_):
    with obtener_conexion() as conexion:
        return conexion.execute(f"SELECT * FROM {TABLE} WHERE id = ?", (id_,)).fetchone()


def existe_code(code, excluir_id=None):
    with obtener_conexion() as conexion:
        if excluir_id:
            fila = conexion.execute(
                f"SELECT id FROM {TABLE} WHERE code = ? AND id != ?", (code, excluir_id)
            ).fetchone()
        else:
            fila = conexion.execute(f"SELECT id FROM {TABLE} WHERE code = ?", (code,)).fetchone()
        return fila is not None


def insertar(code, name, last_name, phone, email, branch_id):
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"""
            INSERT INTO {TABLE} (code, name, last_name, phone, email, branch_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (code, name, last_name, phone, email, branch_id),
        )
        conexion.commit()
        return cursor.lastrowid


def actualizar(id_, code, name, last_name, phone, email, branch_id):
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            UPDATE {TABLE}
            SET code = ?, name = ?, last_name = ?, phone = ?, email = ?, branch_id = ?
            WHERE id = ?
            """,
            (code, name, last_name, phone, email, branch_id, id_),
        )
        conexion.commit()


def eliminar(id_):
    with obtener_conexion() as conexion:
        conexion.execute(f"UPDATE {TABLE} SET status = 0 WHERE id = ?", (id_,))
        conexion.commit()
