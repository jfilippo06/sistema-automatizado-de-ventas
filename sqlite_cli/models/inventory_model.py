from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
import os
import shutil

class InventoryItem:
    IMAGE_FOLDER = "inventory_images"
    
    @staticmethod
    def _ensure_image_folder():
        if not os.path.exists(InventoryItem.IMAGE_FOLDER):
            os.makedirs(InventoryItem.IMAGE_FOLDER)

    @staticmethod
    def _save_image(image_path: Optional[str]) -> Optional[str]:
        if not image_path:
            return None
            
        InventoryItem._ensure_image_folder()
        
        try:
            filename = os.path.basename(image_path)
            dest_path = os.path.join(InventoryItem.IMAGE_FOLDER, filename)
            
            # If file exists, add a suffix
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                dest_path = os.path.join(InventoryItem.IMAGE_FOLDER, f"{name}_{counter}{ext}")
                counter += 1
            
            shutil.copy2(image_path, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    @staticmethod
    def create(
        code: str,
        product: str,
        quantity: int,
        min_stock: int,
        max_stock: int,
        price: float,
        supplier_id: Optional[int] = None,
        expiration_date: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> None:
        """Crea un nuevo producto en el inventario (siempre activo)"""
        saved_image_path = InventoryItem._save_image(image_path)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (
                code, product, quantity, min_stock, max_stock, price, 
                supplier_id, expiration_date, image_path, status_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)  -- 1 = activo por defecto
        ''', (
            code, product, quantity, min_stock, max_stock, price, 
            supplier_id, expiration_date, saved_image_path
        ))
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
                    "Proveedor": "sp.company",
                    "Existencias": "i.quantity",
                    "Stock mínimo": "i.min_stock",
                    "Stock máximo": "i.max_stock"
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
                        LOWER(sp.company) LIKE ? OR
                        CAST(i.quantity AS TEXT) LIKE ? OR
                        CAST(i.min_stock AS TEXT) LIKE ? OR
                        CAST(i.max_stock AS TEXT) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 6)
        
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
        min_stock: int,
        max_stock: int,
        price: float,
        supplier_id: Optional[int] = None,
        expiration_date: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> None:
        """Actualiza un producto existente"""
        # Obtener el producto actual para manejar la imagen
        current_item = InventoryItem.get_by_id(item_id)
        current_image = current_item.get('image_path') if current_item else None
        
        # Manejar la nueva imagen
        saved_image_path = None
        if image_path:
            if image_path != current_image:
                # Eliminar la imagen anterior si es diferente
                if current_image and os.path.exists(current_image):
                    try:
                        os.remove(current_image)
                    except Exception as e:
                        print(f"Error deleting old image: {e}")
                
                saved_image_path = InventoryItem._save_image(image_path)
            else:
                saved_image_path = current_image
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET
                code = ?,
                product = ?,
                quantity = ?,
                min_stock = ?,
                max_stock = ?,
                price = ?,
                supplier_id = ?,
                expiration_date = ?,
                image_path = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            code, product, quantity, min_stock, max_stock, price, 
            supplier_id, expiration_date, saved_image_path, item_id
        ))
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