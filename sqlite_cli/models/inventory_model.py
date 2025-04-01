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
    
    # In inventory_model.py
    @staticmethod
    def get_by_id(item_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.*, s.name as status_name, sp.company as supplier_company
            FROM inventory i
            LEFT JOIN status s ON i.status_id = s.id
            LEFT JOIN suppliers sp ON i.supplier_id = sp.id
            WHERE i.id = ?
        ''', (item_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(
        item_id: int,
        code: str,
        product: str,
        quantity: int,
        stock: int,
        price: float,
        status_id: int,
        supplier_id: Optional[int] = None
    ) -> None:
        """Actualiza un producto existente."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET
                code = ?,
                product = ?,
                quantity = ?,
                stock = ?,
                price = ?,
                status_id = ?,
                supplier_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (code, product, quantity, stock, price, status_id, supplier_id, item_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(item_id: int, status_id: int) -> None:
        """Actualiza solo el estado de un producto."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET
                status_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status_id, item_id))
        conn.commit()
        conn.close()