# Archivo de conexión a la base de datos SQLite
# Centraliza la configuración y el acceso a la base de datos del sistema

import sqlite3
import os

# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo de base de datos SQLite
DB_PATH = os.path.join(BASE_DIR, "database", "database.db")


# Función que crea y retorna una conexión a la base de datos
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    # Permite acceder a las columnas por nombre (row["columna"])
    conn.row_factory = sqlite3.Row
    return conn