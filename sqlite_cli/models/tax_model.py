# models/tax_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Tax:
    @staticmethod
    def create(name: str, value: float = 0.0) -> None:
        """
        Crea un nuevo impuesto en la tabla `taxes`.
        
        :param name: Nombre del impuesto (ej. 'IVA')
        :param value: Valor del impuesto (default 0.0)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO taxes (name, value) VALUES (?, ?)',
            (name, value)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los impuestos con su estado.
        
        :return: Lista de diccionarios con los impuestos
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, s.name as status_name 
            FROM taxes t
            JOIN status s ON t.status_id = s.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """
        Obtiene un impuesto por su nombre.
        
        :param name: Nombre del impuesto
        :return: Diccionario con los datos del impuesto o None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, s.name as status_name 
            FROM taxes t
            JOIN status s ON t.status_id = s.id
            WHERE t.name = ?
        ''', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update_value(name: str, new_value: float) -> None:
        """
        Actualiza el valor de un impuesto.
        
        :param name: Nombre del impuesto
        :param new_value: Nuevo valor
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE taxes SET
                value = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (new_value, name))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(name: str, status_id: int) -> None:
        """
        Actualiza el estado de un impuesto.
        
        :param name: Nombre del impuesto
        :param status_id: ID del nuevo estado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE taxes SET
                status_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (status_id, name))
        conn.commit()
        conn.close()