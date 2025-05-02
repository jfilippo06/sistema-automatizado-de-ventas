from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.inventory_movement_model import InventoryMovement
from sqlite_cli.models.movement_type_model import MovementType

class Purchase:
    @staticmethod
    def create(
        supplier_id: int,
        user_id: int,
        subtotal: float,
        taxes: float,
        total: float,
        items: List[Dict],
        notes: str = None
    ) -> int:
        """
        Crea un nuevo registro de compra.
        
        :param supplier_id: ID del proveedor
        :param user_id: ID del usuario que realiza la compra
        :param subtotal: Subtotal de la compra
        :param taxes: Impuestos aplicados
        :param total: Total de la compra
        :param items: Lista de items comprados
        :param notes: Notas adicionales
        :return: ID de la compra creada
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insertar la compra
        cursor.execute('''
            INSERT INTO purchases (
                supplier_id, user_id, subtotal, taxes, total, notes
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (supplier_id, user_id, subtotal, taxes, total, notes))
        
        purchase_id = cursor.lastrowid
        
        # Insertar los items de la compra
        for item in items:
            cursor.execute('''
                INSERT INTO purchase_items (
                    purchase_id, inventory_id, quantity, unit_price, total_price
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                purchase_id,
                item['id'],
                item['quantity'],
                item['unit_price'],
                item['total']
            ))
            
            # Registrar movimiento de inventario (entrada)
            movement_type = MovementType.get_by_name("Entrada por compra")
            if movement_type:
                inventory_item = InventoryItem.get_by_id(item['id'])
                
                if inventory_item:
                    new_quantity = inventory_item['quantity'] + item['quantity']
                    new_stock = inventory_item['stock'] + item['quantity']
                    
                    InventoryMovement.create(
                        inventory_id=item['id'],
                        movement_type_id=movement_type['id'],
                        quantity_change=item['quantity'],
                        stock_change=item['quantity'],
                        previous_quantity=inventory_item['quantity'],
                        new_quantity=new_quantity,
                        previous_stock=inventory_item['stock'],
                        new_stock=new_stock,
                        user_id=user_id,
                        reference_id=purchase_id,
                        reference_type="purchase",
                        notes=f"Compra #{purchase_id}"
                    )
                    
                    # Actualizar el inventario
                    cursor.execute('''
                        UPDATE inventory SET
                            quantity = ?,
                            stock = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (new_quantity, new_stock, item['id']))
        
        conn.commit()
        conn.close()
        return purchase_id

    @staticmethod
    def get_by_id(purchase_id: int) -> Optional[Dict]:
        """Obtiene una compra por su ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, s.company as supplier_name, u.username as user_name
            FROM purchases p
            JOIN suppliers s ON p.supplier_id = s.id
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (purchase_id,))
        purchase = cursor.fetchone()
        
        if purchase:
            purchase = dict(purchase)
            cursor.execute('''
                SELECT pi.*, i.product as product_name, i.code as product_code
                FROM purchase_items pi
                JOIN inventory i ON pi.inventory_id = i.id
                WHERE pi.purchase_id = ?
            ''', (purchase_id,))
            purchase['items'] = [dict(item) for item in cursor.fetchall()]
        
        conn.close()
        return purchase

    @staticmethod
    def search(
        supplier_id: int = None,
        user_id: int = None,
        start_date: str = None,
        end_date: str = None,
        min_total: float = None,
        max_total: float = None
    ) -> List[Dict]:
        """Busca compras según los criterios proporcionados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT p.*, s.company as supplier_name, u.username as user_name
            FROM purchases p
            JOIN suppliers s ON p.supplier_id = s.id
            JOIN users u ON p.user_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if supplier_id:
            query += " AND p.supplier_id = ?"
            params.append(supplier_id)
            
        if user_id:
            query += " AND p.user_id = ?"
            params.append(user_id)
            
        if start_date:
            query += " AND DATE(p.created_at) >= DATE(?)"
            params.append(start_date)
            
        if end_date:
            query += " AND DATE(p.created_at) <= DATE(?)"
            params.append(end_date)
            
        if min_total:
            query += " AND p.total >= ?"
            params.append(min_total)
            
        if max_total:
            query += " AND p.total <= ?"
            params.append(max_total)
            
        query += " ORDER BY p.created_at DESC"
        
        cursor.execute(query, params)
        purchases = [dict(purchase) for purchase in cursor.fetchall()]
        conn.close()
        return purchases