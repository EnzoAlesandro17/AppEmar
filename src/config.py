import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de base de datos
DB_FOLDER = 'data'
DB_NAME = 'database.db'
DB_PATH = os.path.join(BASE_DIR, DB_FOLDER, DB_NAME)