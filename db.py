import sqlite3
import os

def inicializar_db():
    # Crea la carpeta data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Conecta a la base de datos (se crea si no existe)
    conexion = sqlite3.connect('data/database.db')
    cursor = conexion.cursor()

    tablas = {
        "branches": "id INTEGER PRIMARY KEY, code TEXT, name TEXT, address TEXT, phone_number TEXT, mail TEXT, user TEXT, state INTEGER",
        "sellers": "id INTEGER PRIMARY KEY, code TEXT, last_name TEXT, first_name TEXT, DNI TEXT, phone_number TEXT, mail TEXT, user TEXT, password TEXT, state INTEGER",
        "accounts": "id INTEGER PRIMARY KEY, name TEXT, balance REAL, state INTEGER",
        "plans": "id INTEGER PRIMARY KEY, category TEXT, code TEXT, name TEXT, gigas INTEGER, price REAL, state INTEGER",
        "promos": "id INTEGER PRIMARY KEY, category TEXT, code TEXT, name TEXT, description TEXT, state INTEGER",
        "products": "id INTEGER PRIMARY KEY, code TEXT, category TEXT, name TEXT, cost REAL, price REAL, stock INTEGER, state INTEGER",
        "actions": "id INTEGER PRIMARY KEY, name TEXT, state INTEGER",
        "client": "id INTEGER PRIMARY KEY, last_name TEXT, first_name TEXT, DNI_CUIT TEXT, number TEXT, state INTEGER",
        "registry": "id INTEGER PRIMARY KEY, date TEXT, time TEXT, id_branches INTEGER, id_sellers INTEGER, id_actions INTEGER, state INTEGER",
        "casim": "id INTEGER PRIMARY KEY, id_registry INTEGER, id_client INTEGER, id_products INTEGER, ICCID TEXT, state INTEGER",
        "cater": "id INTEGER PRIMARY KEY, id_registry INTEGER, id_client INTEGER, id_products INTEGER, IMEI TEXT, state INTEGER",
        "porta": "id INTEGER PRIMARY KEY, id_registry INTEGER, id_client INTEGER, id_products INTEGER, ICCID TEXT, id_plans INTEGER, id_promos INTEGER, id_system TEXT, NIM TEXT, PIN TEXT, state INTEGER",
        "regular": "id INTEGER PRIMARY KEY, id_registry INTEGER, id_client INTEGER, id_products INTEGER, ICCID TEXT, id_plans INTEGER, id_promos INTEGER, id_system TEXT, NIM TEXT, state INTEGER",
        "baf": "id INTEGER PRIMARY KEY, id_registry INTEGER, date_system TEXT, date_instalation TEXT, form_state TEXT, id_seller INTEGER, street TEXT, stree_number TEXT, apartment TEXT, cross_street TEXT, type_house TEXT, id_client INTEGER, birthday TEXT, principal_number TEXT, alternative_number TEXT, mail TEXT, speed_internet TEXT, amount_tv INTEGER, observations TEXT, ot_number TEXT, sds_code TEXT, date_agreed TEXT, stime_slot TEXT, state INTEGER"
    }

    # Generar todas las tablas iterando el diccionario
    for tabla, columnas in tablas.items():
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({columnas})")

    conexion.commit()
    conexion.close()
    print("database.db y tablas creadas con éxito en la carpeta data.")

if __name__ == '__main__':
    inicializar_db()