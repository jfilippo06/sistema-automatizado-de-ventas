from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class PurchaseOrderStatus:
    @staticmethod
    def create(name: str, description: Optional[str] = None) -> int:
        """
        Crea un nuevo estado de orden de compra.
        
        :param name: Nombre del estado (debe ser único)
        :param description: Descripción opcional del estado
        :return: ID del estado creado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO purchase_order_status (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los estados de orden de compra.
        
        :return: Lista de diccionarios con los estados
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM purchase_order_status')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(status_id: int) -> Optional[Dict]:
        """
        Obtiene un estado por su ID.
        
        :param status_id: ID del estado
        :return: Diccionario con los datos del estado o None si no existe
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM purchase_order_status WHERE id = ?', (status_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def delete(status_id: int) -> bool:
        """
        Elimina un estado por su ID.
        
        :param status_id: ID del estado a eliminar
        :return: True si se eliminó, False si no existía
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM purchase_order_status WHERE id = ?', (status_id,))
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return affected_rows > 0