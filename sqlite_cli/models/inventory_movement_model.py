# models/inventory_movement_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class InventoryMovement:
    @staticmethod
    def all() -> List[Dict]:
        """Obtiene todos los movimientos de inventario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory_movements')
        movements = cursor.fetchall()
        conn.close()
        return [dict(movement) for movement in movements]
    
    @staticmethod
    def create(
        inventory_id: int,
        movement_type_id: int,
        quantity_change: int,
        stock_change: int,
        previous_quantity: int,
        new_quantity: int,
        previous_stock: int,
        new_stock: int,
        user_id: int,
        reference_id: int = None,
        reference_type: str = None,
        notes: str = None
    ) -> int:
        """Registra un nuevo movimiento de inventario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO inventory_movements (
                inventory_id, movement_type_id, quantity_change, stock_change,
                previous_quantity, new_quantity, previous_stock, new_stock,
                reference_id, reference_type, user_id, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                inventory_id, movement_type_id, quantity_change, stock_change,
                previous_quantity, new_quantity, previous_stock, new_stock,
                reference_id, reference_type, user_id, notes
            )
        )
        conn.commit()
        id_ = cursor.lastrowid
        conn.close()
        return id_