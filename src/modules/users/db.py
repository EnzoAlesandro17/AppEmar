from src.db.connection import obtener_conexion
from src.modules.employees.db import TABLE as TABLE_EMPLOYEES

TABLE = "users"


def crear_tabla():
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL DEFAULT 'Vendedor',
                employee_id INTEGER REFERENCES {TABLE_EMPLOYEES}(id),
                status INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conexion.commit()


def existe_algun_usuario():
    with obtener_conexion() as conexion:
        fila = conexion.execute(f"SELECT COUNT(*) AS total FROM {TABLE}").fetchone()
        return fila["total"] > 0


def existe_username(username, excluir_id=None):
    with obtener_conexion() as conexion:
        if excluir_id:
            fila = conexion.execute(
                f"SELECT id FROM {TABLE} WHERE username = ? AND id != ?", (username, excluir_id)
            ).fetchone()
        else:
            fila = conexion.execute(
                f"SELECT id FROM {TABLE} WHERE username = ?", (username,)
            ).fetchone()
        return fila is not None


def listar_activos():
    with obtener_conexion() as conexion:
        return conexion.execute(
            f"""
            SELECT {TABLE}.*, {TABLE_EMPLOYEES}.name AS employee_name,
                   {TABLE_EMPLOYEES}.last_name AS employee_last_name
            FROM {TABLE}
            LEFT JOIN {TABLE_EMPLOYEES} ON {TABLE_EMPLOYEES}.id = {TABLE}.employee_id
            WHERE {TABLE}.status = 1
            ORDER BY {TABLE}.username
            """
        ).fetchall()


def obtener_por_id(id_):
    with obtener_conexion() as conexion:
        return conexion.execute(f"SELECT * FROM {TABLE} WHERE id = ?", (id_,)).fetchone()


def obtener_por_username(username):
    with obtener_conexion() as conexion:
        return conexion.execute(
            f"SELECT * FROM {TABLE} WHERE username = ? AND status = 1", (username,)
        ).fetchone()


def insertar(username, password_hash, email, role, employee_id):
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"""
            INSERT INTO {TABLE} (username, password, email, role, employee_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, password_hash, email, role, employee_id),
        )
        conexion.commit()
        return cursor.lastrowid


def actualizar(id_, username, password_hash, email, role, employee_id):
    with obtener_conexion() as conexion:
        if password_hash:
            conexion.execute(
                f"""
                UPDATE {TABLE}
                SET username = ?, password = ?, email = ?, role = ?, employee_id = ?
                WHERE id = ?
                """,
                (username, password_hash, email, role, employee_id, id_),
            )
        else:
            conexion.execute(
                f"""
                UPDATE {TABLE}
                SET username = ?, email = ?, role = ?, employee_id = ?
                WHERE id = ?
                """,
                (username, email, role, employee_id, id_),
            )
        conexion.commit()


def eliminar(id_):
    with obtener_conexion() as conexion:
        conexion.execute(f"UPDATE {TABLE} SET status = 0 WHERE id = ?", (id_,))
        conexion.commit()
