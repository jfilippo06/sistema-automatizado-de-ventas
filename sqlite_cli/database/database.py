# database/database.py
import sqlite3
import os
from typing import Optional

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
    Inicializa la base de datos y crea todas las tablas si no existen.
    """
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Create status table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Create suppliers table (MODIFICADA para incluir status_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            id_number TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            tax_id TEXT,
            company TEXT,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    # Create inventory table with foreign keys
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status_id INTEGER NOT NULL,
            supplier_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    ''')
    
    conn.commit()
    conn.close()