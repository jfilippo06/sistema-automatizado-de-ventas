# models/currency_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Currency:
    @staticmethod
    def create(name: str, symbol: str, value: float = 0.0) -> None:
        """
        Crea una nueva moneda en la tabla `currencies`.
        
        :param name: Nombre de la moneda (ej. 'Dólar', 'Euro')
        :param symbol: Símbolo de la moneda (ej. '$', '€')
        :param value: Valor de la moneda (default 0.0)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO currencies (name, symbol, value) VALUES (?, ?, ?)',
            (name, symbol, value)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todas las monedas con su estado.
        
        :return: Lista de diccionarios con las monedas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, s.name as status_name 
            FROM currencies c
            JOIN status s ON c.status_id = s.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """
        Obtiene una moneda por su nombre.
        
        :param name: Nombre de la moneda
        :return: Diccionario con los datos de la moneda o None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, s.name as status_name 
            FROM currencies c
            JOIN status s ON c.status_id = s.id
            WHERE c.name = ?
        ''', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update_value(name: str, new_value: float) -> None:
        """
        Actualiza el valor de una moneda.
        
        :param name: Nombre de la moneda
        :param new_value: Nuevo valor
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE currencies SET
                value = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (new_value, name))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(name: str, status_id: int) -> None:
        """
        Actualiza el estado de una moneda.
        
        :param name: Nombre de la moneda
        :param status_id: ID del nuevo estado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE currencies SET
                status_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (status_id, name))
        conn.commit()
        conn.close()