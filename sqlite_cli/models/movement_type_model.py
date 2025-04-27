# models/movement_type_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class MovementType:
    @staticmethod
    def all() -> List[Dict]:
        """Obtiene todos los tipos de movimiento."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movement_types')
        types = cursor.fetchall()
        conn.close()
        return [dict(type) for type in types]
    
    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """Obtiene un tipo de movimiento por su nombre."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movement_types WHERE name = ?', (name,))
        type_ = cursor.fetchone()
        conn.close()
        return dict(type_) if type_ else None
    
    @staticmethod
    def create(name: str, affects_quantity: bool, affects_stock: bool, description: str = None) -> int:
        """Crea un nuevo tipo de movimiento."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO movement_types (name, affects_quantity, affects_stock, description) VALUES (?, ?, ?, ?)',
            (name, affects_quantity, affects_stock, description)
        )
        conn.commit()
        id_ = cursor.lastrowid
        conn.close()
        return id_