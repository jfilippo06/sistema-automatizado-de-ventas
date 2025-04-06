from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class InventoryItem:
    @staticmethod
    def create(
        code: str,
        product: str,
        quantity: int,
        stock: int,
        price: float,
        supplier_id: Optional[int] = None
    ) -> None:
        """Crea un nuevo producto en el inventario (siempre activo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (
                code, product, quantity, stock, price, supplier_id, status_id
            ) VALUES (?, ?, ?, ?, ?, ?, 1)  -- 1 = activo por defecto
        ''', (code, product, quantity, stock, price, supplier_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """Obtiene todos los productos activos del inventario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.*, st.name as status_name, sp.company as supplier_company
            FROM inventory i
            JOIN status st ON i.status_id = st.id
            LEFT JOIN suppliers sp ON i.supplier_id = sp.id
            WHERE st.name = 'active'
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        """Busca productos activos con filtro opcional"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT i.*, st.name as status_name, sp.company as supplier_company
            FROM inventory i
            JOIN status st ON i.status_id = st.id
            LEFT JOIN suppliers sp ON i.supplier_id = sp.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "i.id",
                    "Código": "i.code",
                    "Producto": "i.product",
                    "Proveedor": "sp.company"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            item_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(item_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(i.code) LIKE ? OR 
                        LOWER(i.product) LIKE ? OR 
                        LOWER(sp.company) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 3)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(item_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID (solo si está activo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.*, st.name as status_name, sp.company as supplier_company
            FROM inventory i
            JOIN status st ON i.status_id = st.id
            LEFT JOIN suppliers sp ON i.supplier_id = sp.id
            WHERE i.id = ? AND st.name = 'active'
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
        supplier_id: Optional[int] = None
    ) -> None:
        """Actualiza un producto existente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET
                code = ?,
                product = ?,
                quantity = ?,
                stock = ?,
                price = ?,
                supplier_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (code, product, quantity, stock, price, supplier_id, item_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(item_id: int, status_id: int) -> None:
        """Actualiza solo el estado de un producto"""
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