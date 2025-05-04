import sqlite3
import os
import time
from typing import List, Dict, Optional, Union
from datetime import datetime
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.inventory_movement_model import InventoryMovement
from sqlite_cli.models.movement_type_model import MovementType
from utils.session_manager import SessionManager

class Sales:
    BUSY_TIMEOUT = 5000  # 5 segundos (en milisegundos)
    MAX_RETRIES = 3      # Intentos máximos por operación

    @staticmethod
    def get_db_connection() -> sqlite3.Connection:
        """Crea una conexión a la base de datos con configuración optimizada."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "..", "database", "db.db")

        conn = sqlite3.connect(
            db_path,
            timeout=Sales.BUSY_TIMEOUT / 1000,
            isolation_level=None,
            check_same_thread=False
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f"PRAGMA busy_timeout={Sales.BUSY_TIMEOUT}")
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
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta
            fetch: Si es True, retorna los resultados
            
        Returns:
            - Lista de diccionarios si fetch=True
            - ID del último registro si es INSERT
            - None para otras operaciones
        """
        conn = None
        last_exception = None
        
        for attempt in range(Sales.MAX_RETRIES):
            try:
                conn = Sales.get_db_connection()
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
                if "locked" in str(e).lower() and attempt < Sales.MAX_RETRIES - 1:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise last_exception
            finally:
                if conn:
                    conn.close()

    @staticmethod
    def create_complete_purchase(
        supplier_id: int,
        subtotal: float,
        taxes: float,
        total: float,
        items: List[Dict]
    ) -> int:
        """
        Crea una compra completa (tipo Compra)
        """
        # Obtener ID del tipo de factura "Compra"
        invoice_type_id = Sales._get_invoice_type_id("Compra")
        
        # 1. Registrar compra principal
        purchase_id = Sales._create_purchase_invoice(
            supplier_id=supplier_id,
            invoice_type_id=invoice_type_id,
            subtotal=subtotal,
            taxes=taxes,
            total=total
        )
        
        # 2. Procesar cada item secuencialmente
        for item in items:
            Sales._process_purchase_item(purchase_id, item)
        
        return purchase_id

    @staticmethod
    def _create_purchase_invoice(
        supplier_id: int,
        invoice_type_id: int,
        subtotal: float,
        taxes: float,
        total: float
    ) -> int:
        """Registra la compra principal en la tabla 'invoices'."""
        status_id = Sales._get_invoice_status_id("Paid")
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return Sales._execute_sql(
            '''
            INSERT INTO invoices (
                customer_id, invoice_type_id, issue_date, 
                subtotal, taxes, total, status_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (supplier_id, invoice_type_id, issue_date, subtotal, taxes, total, status_id)
        )

    @staticmethod
    def _process_purchase_item(purchase_id: int, item: Dict) -> None:
        """Procesa un item completo (detalle + inventario + movimiento)."""
        # 1. Registrar detalle
        Sales._create_purchase_detail(purchase_id, item)
        
        # 2. Actualizar solo quantity (no stock)
        product = InventoryItem.get_by_id(item['id'])
        if not product:
            raise ValueError(f"Producto ID {item['id']} no encontrado")
        
        new_quantity = product['quantity'] + item['quantity']
        
        Sales._update_inventory(
            product_id=item['id'],
            new_quantity=new_quantity,
            new_stock=product['stock']  # Mantener el stock igual
        )
        
        # 3. Registrar movimiento (solo cambio en quantity)
        user_id = SessionManager.get_user_id()
        if not user_id:
            raise ValueError("Usuario no autenticado")
        
        movement_type = MovementType.get_by_name("Compra")
        if not movement_type:
            raise ValueError("Tipo de movimiento 'Entrada por compra' no encontrado")
        
        InventoryMovement.create(
            inventory_id=item['id'],
            movement_type_id=movement_type['id'],
            quantity_change=item['quantity'],
            stock_change=0,  # No cambia el stock
            previous_quantity=product['quantity'],
            new_quantity=new_quantity,
            previous_stock=product['stock'],
            new_stock=product['stock'],  # Stock permanece igual
            reference_id=purchase_id,
            reference_type="purchase",
            user_id=user_id,
            notes=f"Compra #{purchase_id}"
        )

    @staticmethod
    def _create_purchase_detail(invoice_id: int, item: Dict) -> None:
        """Registra un detalle de compra en 'invoice_details'."""
        Sales._execute_sql(
            '''
            INSERT INTO invoice_details (
                invoice_id, product_id, quantity, unit_price, subtotal
            ) VALUES (?, ?, ?, ?, ?)
            ''',
            (invoice_id, item['id'], item['quantity'], item['unit_price'], item['total'])
        )

    @staticmethod
    def _update_inventory(product_id: int, new_quantity: int, new_stock: int) -> None:
        """Actualiza solo la cantidad en el inventario."""
        Sales._execute_sql(
            '''
            UPDATE inventory SET
                quantity = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (new_quantity, product_id)
        )

    @staticmethod
    def _get_invoice_status_id(status_name: str) -> int:
        """Obtiene el ID de un estado de factura."""
        result = Sales._execute_sql(
            "SELECT id FROM invoice_status WHERE name = ? LIMIT 1",
            (status_name,),
            fetch=True
        )
        if not result:
            raise ValueError(f"Estado '{status_name}' no encontrado")
        return result[0]['id']

    @staticmethod
    def get_by_id(purchase_id: int) -> Optional[Dict]:
        """Obtiene una compra por su ID con información del proveedor y tipo."""
        result = Sales._execute_sql(
            '''
            SELECT 
                i.*,
                s.company as supplier_name,
                s.id_number as supplier_id_number,
                st.name as status_name,
                it.name as invoice_type_name
            FROM invoices i
            JOIN suppliers s ON i.customer_id = s.id
            JOIN invoice_status st ON i.status_id = st.id
            JOIN invoice_types it ON i.invoice_type_id = it.id
            WHERE i.id = ?
            ''',
            (purchase_id,),
            fetch=True
        )
        return result[0] if result else None
    
    @staticmethod
    def _get_invoice_type_id(type_name: str) -> int:
        """Obtiene el ID de un tipo de factura."""
        result = Sales._execute_sql(
            "SELECT id FROM invoice_types WHERE name = ? LIMIT 1",
            (type_name,),
            fetch=True
        )
        if not result:
            raise ValueError(f"Tipo de factura '{type_name}' no encontrado")
        return result[0]['id']

    @staticmethod
    def get_details(purchase_id: int) -> List[Dict]:
        """Obtiene los detalles de una compra con información de productos."""
        return Sales._execute_sql(
            '''
            SELECT 
                d.*,
                inv.product as product_name,
                inv.code as product_code
            FROM invoice_details d
            JOIN inventory inv ON d.product_id = inv.id
            WHERE d.invoice_id = ?
            ''',
            (purchase_id,),
            fetch=True
        ) or []

    @staticmethod
    def update_status(purchase_id: int, new_status: str) -> bool:
        """Actualiza el estado de una compra."""
        valid_statuses = ["Paid", "Pending", "Cancelled", "Partial"]
        if new_status not in valid_statuses:
            raise ValueError(f"Estado inválido. Opciones: {', '.join(valid_statuses)}")
        
        status_id = Sales._get_invoice_status_id(new_status)
        
        Sales._execute_sql(
            '''
            UPDATE invoices
            SET status_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (status_id, purchase_id)
        )
        
        if new_status == "Cancelled":
            Sales._handle_cancellation(purchase_id)
        
        return True

    @staticmethod
    def _handle_cancellation(purchase_id: int) -> None:
        """Maneja la lógica de cancelación de compras."""
        details = Sales.get_details(purchase_id)
        user_id = SessionManager.get_user_id()
        if not user_id:
            raise ValueError("Usuario no autenticado")
        
        movement_type = MovementType.get_by_name("Ajuste negativo")
        if not movement_type:
            raise ValueError("Tipo de movimiento 'Ajuste negativo' no encontrado")
        
        for detail in details:
            product = InventoryItem.get_by_id(detail['product_id'])
            if not product:
                continue
            
            new_quantity = product['quantity'] - detail['quantity']
            new_stock = product['stock'] - detail['quantity']
            
            # Validar que no queden valores negativos
            if new_quantity < 0 or new_stock < 0:
                raise ValueError(f"No se puede cancelar - stock insuficiente para el producto ID {detail['product_id']}")
            
            Sales._update_inventory(detail['product_id'], new_quantity, new_stock)
            
            InventoryMovement.create(
                inventory_id=detail['product_id'],
                movement_type_id=movement_type['id'],
                quantity_change=-detail['quantity'],
                stock_change=-detail['quantity'],
                previous_quantity=product['quantity'],
                new_quantity=new_quantity,
                previous_stock=product['stock'],
                new_stock=new_stock,
                reference_id=purchase_id,
                reference_type="purchase_cancellation",
                user_id=user_id,
                notes=f"Cancelación compra #{purchase_id}"
            )

    @staticmethod
    def search(
        supplier_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Dict]:
        """Busca compras con filtros opcionales."""
        query = '''
            SELECT 
                i.*,
                s.company as supplier_name,
                st.name as status_name
            FROM invoices i
            JOIN suppliers s ON i.customer_id = s.id
            JOIN invoice_status st ON i.status_id = st.id
            WHERE 1=1
        '''
        params = []
        
        if supplier_id:
            query += " AND i.customer_id = ?"
            params.append(supplier_id)
        
        if status:
            query += " AND st.name = ?"
            params.append(status)
        
        if start_date:
            query += " AND DATE(i.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(i.issue_date) <= ?"
            params.append(end_date)
        
        if search_term:
            query += " AND (i.id LIKE ? OR s.company LIKE ? OR s.id_number LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param] * 3)
        
        query += " ORDER BY i.issue_date DESC"
        
        return Sales._execute_sql(query, tuple(params), fetch=True) or []