from src.db.connection import obtener_conexion

TABLE = "branches"


def crear_tabla():
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                address TEXT,
                street_number TEXT,
                email TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                status INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conexion.commit()


def listar_activas():
    with obtener_conexion() as conexion:
        return conexion.execute(
            f"SELECT * FROM {TABLE} WHERE status = 1 ORDER BY name"
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


def insertar(code, name, address, street_number, email, city, state, country):
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"""
            INSERT INTO {TABLE} (code, name, address, street_number, email, city, state, country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (code, name, address, street_number, email, city, state, country),
        )
        conexion.commit()
        return cursor.lastrowid


def actualizar(id_, code, name, address, street_number, email, city, state, country):
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            UPDATE {TABLE}
            SET code = ?, name = ?, address = ?, street_number = ?, email = ?,
                city = ?, state = ?, country = ?
            WHERE id = ?
            """,
            (code, name, address, street_number, email, city, state, country, id_),
        )
        conexion.commit()


def eliminar(id_):
    with obtener_conexion() as conexion:
        conexion.execute(f"UPDATE {TABLE} SET status = 0 WHERE id = ?", (id_,))
        conexion.commit()
