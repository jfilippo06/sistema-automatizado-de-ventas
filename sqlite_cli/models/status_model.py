# models/status_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Status:
    @staticmethod
    def create(name: str, description: Optional[str] = None) -> None:
        """
        Crea un nuevo estado en la tabla `status`.
        
        :param name: Nombre del estado (ej. 'active', 'inactive')
        :param description: Descripción opcional del estado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO status (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los estados de la tabla `status`.
        
        :return: Lista de diccionarios con los estados
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM status')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items