from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class InventoryReport:
    @staticmethod
    def get_inventory_report(
        search_term: Optional[str] = None,
        supplier_id: Optional[int] = None,
        min_stock: Optional[int] = None,
        max_stock: Optional[int] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        expired_only: bool = False
    ) -> List[Dict]:
        """
        Obtiene un reporte completo del inventario con filtros opcionales.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                i.id,
                i.code,
                i.product,
                i.description,
                i.quantity,
                i.stock,
                i.min_stock,
                i.max_stock,
                i.cost,
                i.price,
                i.expiration_date,
                s.company as supplier_company,
                CASE 
                    WHEN i.expiration_date IS NOT NULL AND DATE(i.expiration_date) < DATE('now') THEN 'Vencido'
                    WHEN i.stock <= i.min_stock THEN 'Bajo stock'
                    ELSE 'Disponible'
                END as status
            FROM inventory i
            LEFT JOIN suppliers s ON i.supplier_id = s.id
            JOIN status st ON i.status_id = st.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            query += '''
                AND (LOWER(i.code) LIKE ? OR 
                    LOWER(i.product) LIKE ? OR 
                    LOWER(i.description) LIKE ?)
            '''
            search_param = f"%{search_term.lower()}%"
            params.extend([search_param] * 3)
        
        if supplier_id:
            query += " AND i.supplier_id = ?"
            params.append(supplier_id)
            
        if min_stock is not None:
            query += " AND i.stock >= ?"
            params.append(min_stock)
            
        if max_stock is not None:
            query += " AND i.stock <= ?"
            params.append(max_stock)
            
        if min_quantity is not None:
            query += " AND i.quantity >= ?"
            params.append(min_quantity)
            
        if max_quantity is not None:
            query += " AND i.quantity <= ?"
            params.append(max_quantity)
            
        if expired_only:
            query += " AND i.expiration_date IS NOT NULL AND DATE(i.expiration_date) < DATE('now')"
        
        query += " ORDER BY i.product ASC"
        
        cursor.execute(query, tuple(params))
        items = []
        for row in cursor.fetchall():
            item = dict(row)
            # Reemplazar None por "None" en los campos relevantes
            for key in ['code', 'product', 'description', 'supplier_company', 'expiration_date']:
                if item[key] is None:
                    item[key] = "None"
            items.append(item)
        conn.close()
        return items

    @staticmethod
    def get_inventory_movements_report(
        inventory_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        movement_type: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Obtiene un reporte de movimientos de inventario con filtros opcionales.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                im.id,
                im.created_at,
                i.code as product_code,
                i.product as product_name,
                mt.name as movement_type,
                im.quantity_change,
                im.stock_change,
                im.previous_quantity,
                im.new_quantity,
                im.previous_stock,
                im.new_stock,
                u.username as user,
                im.notes,
                CASE 
                    WHEN im.reference_type = 'invoice' THEN 'Factura'
                    WHEN im.reference_type = 'purchase' THEN 'Compra'
                    WHEN im.reference_type = 'adjustment' THEN 'Ajuste'
                    ELSE im.reference_type
                END as reference_type,
                im.reference_id
            FROM inventory_movements im
            JOIN inventory i ON im.inventory_id = i.id
            JOIN movement_types mt ON im.movement_type_id = mt.id
            JOIN users u ON im.user_id = u.id
            WHERE 1=1
        '''
        
        params = []
        
        if inventory_id:
            query += " AND im.inventory_id = ?"
            params.append(inventory_id)
            
        if start_date:
            query += " AND DATE(im.created_at) >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND DATE(im.created_at) <= ?"
            params.append(end_date)
            
        if movement_type:
            query += " AND mt.name = ?"
            params.append(movement_type)
            
        if user_id:
            query += " AND im.user_id = ?"
            params.append(user_id)
            
        query += " ORDER BY im.created_at DESC"
        
        cursor.execute(query, tuple(params))
        movements = []
        for row in cursor.fetchall():
            movement = dict(row)
            # Reemplazar None por "None" en los campos relevantes
            for key in ['notes', 'reference_type', 'reference_id']:
                if movement[key] is None:
                    movement[key] = "None"
            movements.append(movement)
        conn.close()
        return movements