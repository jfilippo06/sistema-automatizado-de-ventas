import sqlite3
import os

def get_db_connection() -> sqlite3.Connection:
    """
    Obtiene una conexión a la base de datos SQLite.

    :return: Una conexión a la base de datos SQLite.
    """
    # Obtener la ruta del directorio actual del script
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta completa a la base de datos
    db_path: str = os.path.join(current_dir, "db.db")
    
    # Conectar a la base de datos
    conn: sqlite3.Connection = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acceder a las filas como diccionarios
    return conn

def init_db() -> None:
    """
    Inicializa la base de datos y crea la tabla `inventory` si no existe.
    """
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
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