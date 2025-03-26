# models/inventory_model.py
from database.database import get_db_connection
from typing import List, Dict, Optional

class InventoryItem:
    @staticmethod
    def create(
        code: str,
        product: str,
        quantity: int,
        stock: int,
        price: float,
        status_id: int,
        supplier_id: Optional[int] = None
    ) -> None:
        """
        Crea un nuevo ítem en la tabla `inventory`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (
                code, product, quantity, stock, price, status_id, supplier_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (code, product, quantity, stock, price, status_id, supplier_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los ítems de la tabla `inventory`.
        
        :return: Lista de diccionarios con los ítems de inventario
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.*, s.name as status_name, sp.company as supplier_company
            FROM inventory i
            LEFT JOIN status s ON i.status_id = s.id
            LEFT JOIN suppliers sp ON i.supplier_id = sp.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items