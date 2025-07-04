from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Bank:
    @staticmethod
    def create(code: str, name: str) -> None:
        """
        Crea un nuevo banco en la tabla `banks`.
        
        :param code: Código del banco (ej. '0102')
        :param name: Nombre del banco (ej. 'Banco de Venezuela')
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO banks (code, name) VALUES (?, ?)',
            (code, name)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los bancos con su estado.
        
        :return: Lista de diccionarios con los bancos
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, s.name as status_name 
            FROM banks b
            JOIN status s ON b.status_id = s.id
            ORDER BY b.name
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """
        Obtiene un banco por su nombre.
        
        :param name: Nombre del banco
        :return: Diccionario con los datos del banco o None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, s.name as status_name 
            FROM banks b
            JOIN status s ON b.status_id = s.id
            WHERE b.name = ?
        ''', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def get_active_banks() -> List[Dict]:
        """
        Obtiene solo los bancos activos.
        
        :return: Lista de diccionarios con los bancos activos
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, s.name as status_name 
            FROM banks b
            JOIN status s ON b.status_id = s.id
            WHERE s.name = 'active'
            ORDER BY b.name
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update_status(code: str, status_id: int) -> None:
        """
        Actualiza el estado de un banco.
        
        :param code: Código del banco
        :param status_id: ID del nuevo estado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE banks SET
                status_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE code = ?
        ''', (status_id, code))
        conn.commit()
        conn.close()