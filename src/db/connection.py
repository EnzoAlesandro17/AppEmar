import sys
import sqlite3
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import DB_PATH

class GestorDB:
    @staticmethod
    def conectar():
        """Crea la carpeta si no existe, conecta y devuelve la conexión."""
        # Asegura que exista la carpeta 'data' definida en config
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        try:
            conexion = sqlite3.connect(DB_PATH)
            conexion.row_factory = sqlite3.Row 
            return conexion
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None