from src.db.connection import obtener_conexion

TABLA = "users"


def crear_tabla():
    """Crea la tabla de usuarios si no existe todavía."""
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLA} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                birth_date TEXT,
                phone TEXT,
                status INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conexion.commit()
