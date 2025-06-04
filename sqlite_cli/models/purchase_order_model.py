import sqlite3
import os
import time
from datetime import datetime
from typing import List, Dict, Optional, Union
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.purchase_order_status_model import PurchaseOrderStatus
from utils.session_manager import SessionManager

class PurchaseOrder:
    BUSY_TIMEOUT = 5000  # 5 segundos (en milisegundos)
    MAX_RETRIES = 3      # Intentos máximos por operación

    @staticmethod
    def get_db_connection() -> sqlite3.Connection:
        """Crea una conexión a la base de datos con configuración optimizada."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "..", "database", "db.db")

        conn = sqlite3.connect(
            db_path,
            timeout=PurchaseOrder.BUSY_TIMEOUT / 1000,
            isolation_level=None,
            check_same_thread=False
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f"PRAGMA busy_timeout={PurchaseOrder.BUSY_TIMEOUT}")
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _execute_sql(
        query: str,
        params: Optional[tuple] = None,
        fetch: bool = False
    ) -> Union[List[Dict], int, None]:
        """
        Ejecuta una consulta SQL con manejo de errores y reintentos.
        """
        conn = None
        last_exception = None
        
        for attempt in range(PurchaseOrder.MAX_RETRIES):
            try:
                conn = PurchaseOrder.get_db_connection()
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch:
                    result = [dict(row) for row in cursor.fetchall()]
                    conn.close()
                    return result
                
                last_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                return last_id if "INSERT" in query.upper() else None
                
            except sqlite3.OperationalError as e:
                last_exception = e
                if "locked" in str(e).lower() and attempt < PurchaseOrder.MAX_RETRIES - 1:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise last_exception
            finally:
                if conn:
                    conn.close()

    @staticmethod
    def get_next_order_number() -> str:
        """Get next purchase order number in format OC-0001, OC-0002, etc."""
        # Buscar el último número de orden
        last_order = PurchaseOrder._execute_sql(
            "SELECT order_number FROM purchase_orders WHERE order_number LIKE 'OC-%' ORDER BY id DESC LIMIT 1",
            fetch=True
        )
        
        if last_order:
            try:
                last_number = int(last_order[0]['order_number'].split('-')[-1])
                return f"OC-{last_number + 1:04d}"
            except (IndexError, ValueError):
                # Si hay algún error al parsear el último número, empezamos desde 1
                return "OC-0001"
        else:
            return "OC-0001"

    @staticmethod
    def get_suppliers(search_term: str = "") -> List[Dict]:
        """Get active suppliers with optional search"""
        return Supplier.search_active(search_term)

    @staticmethod
    def get_supplier_by_id(supplier_id: int) -> Optional[Dict]:
        """Get supplier by ID"""
        return Supplier.get_by_id(supplier_id)

    @staticmethod
    def create_order(
        order_number: str,
        supplier_id: int,
        delivery_date: str,
        products: List[Dict],
        subtotal: float,
        iva: float,
        total: float,
        notes: str = "",
        created_by: str = ""
    ) -> bool:
        """Create a new purchase order in the database"""
        try:
            # Verificar si el número de orden ya existe
            existing_order = PurchaseOrder._execute_sql(
                "SELECT id FROM purchase_orders WHERE order_number = ?",
                (order_number,),
                fetch=True
            )
            
            if existing_order:
                # Si ya existe, generar un nuevo número
                order_number = PurchaseOrder.get_next_order_number()
            
            # Obtener el estado inicial (Borrador)
            status = PurchaseOrderStatus.get_by_name("draft")
            if not status:
                raise ValueError("Estado 'draft' no encontrado en purchase_order_status")
            
            # 1. Registrar la orden principal
            order_id = PurchaseOrder._execute_sql(
                '''
                INSERT INTO purchase_orders (
                    order_number, supplier_id, issue_date,
                    expected_delivery_date, status_id, subtotal,
                    taxes, total, notes, created_by
                ) VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    order_number, supplier_id, delivery_date,
                    status['id'], subtotal, iva, total, notes, created_by
                )
            )
            
            if not order_id:
                raise ValueError("No se pudo crear la orden principal")
            
            # 2. Registrar los detalles de la orden
            for product in products:
                # Buscar el producto por código si no tiene ID
                product_id = None
                if product.get('id'):
                    product_id = product['id']
                elif product.get('code'):
                    item = InventoryItem.get_by_code(product['code'])
                    if item:
                        product_id = item['id']
                
                PurchaseOrder._execute_sql(
                    '''
                    INSERT INTO purchase_order_details (
                        order_id, product_id, product_name, quantity,
                        unit_price, reference_price, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        order_id, product_id, product.get('name', product.get('description', '')), 
                        product['quantity'], product['unit_price'], product['unit_price'],
                        f"Agregado en orden {order_number}"
                    )
                )
            
            return True
        except Exception as e:
            print(f"Error al crear orden de compra: {str(e)}")
            return False

    @staticmethod
    def get_order_details(order_id: int) -> List[Dict]:
        """Obtiene los detalles de una orden de compra"""
        return PurchaseOrder._execute_sql(
            '''
            SELECT 
                d.id,
                d.order_id,
                d.product_id,
                d.product_name,
                d.quantity,
                d.unit_price,
                d.reference_price,
                d.received_quantity,
                d.notes,
                d.subtotal,
                i.product as product_name,
                i.code as product_code,
                i.description as product_description,
                CASE WHEN d.product_id IS NULL THEN 'manual' ELSE 'inventory' END as product_type
            FROM purchase_order_details d
            LEFT JOIN inventory i ON d.product_id = i.id
            WHERE d.order_id = ?
            ''',
            (order_id,),
            fetch=True
        ) or []

    @staticmethod
    def get_orders_by_status(status_name: str) -> List[Dict]:
        """Obtiene órdenes por estado"""
        status = PurchaseOrderStatus.get_by_name(status_name)
        if not status:
            return []
            
        return PurchaseOrder._execute_sql(
            '''
            SELECT 
                o.*,
                s.name as status_name,
                sup.company as supplier_company,
                sup.first_name || ' ' || sup.last_name as supplier_name
            FROM purchase_orders o
            JOIN purchase_order_status s ON o.status_id = s.id
            JOIN suppliers sup ON o.supplier_id = sup.id
            WHERE o.status_id = ?
            ORDER BY o.issue_date DESC
            ''',
            (status['id'],),
            fetch=True
        ) or []