import sqlite3
from contextlib import contextmanager

from src.config import DB_PATH


class GestorDB:
    @staticmethod
    def conectar():
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion


@contextmanager
def obtener_conexion():
    conexion = GestorDB.conectar()
    try:
        yield conexion
    finally:
        conexion.close()
