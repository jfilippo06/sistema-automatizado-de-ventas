# database/database.py
import sqlite3

def get_db_connection():
    """
    Obtiene una conexión a la base de datos SQLite.
    """
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row  # Para acceder a las filas como diccionarios
    return conn

def init_db():
    """
    Inicializa la base de datos y crea la tabla `inventory` si no existe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()