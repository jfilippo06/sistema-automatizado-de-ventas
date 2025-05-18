import sqlite3
import os
import time
from typing import List, Dict, Optional, Union
from datetime import datetime
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.inventory_movement_model import InventoryMovement
from sqlite_cli.models.movement_type_model import MovementType
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.service_model import Service
from utils.session_manager import SessionManager

class Invoice:
    BUSY_TIMEOUT = 5000  # 5 segundos (en milisegundos)
    MAX_RETRIES = 3      # Intentos máximos por operación

    @staticmethod
    def get_db_connection() -> sqlite3.Connection:
        """Crea una conexión a la base de datos con configuración optimizada."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "..", "database", "db.db")

        conn = sqlite3.connect(
            db_path,
            timeout=Invoice.BUSY_TIMEOUT / 1000,
            isolation_level=None,
            check_same_thread=False
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f"PRAGMA busy_timeout={Invoice.BUSY_TIMEOUT}")
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
        
        for attempt in range(Invoice.MAX_RETRIES):
            try:
                conn = Invoice.get_db_connection()
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
                if "locked" in str(e).lower() and attempt < Invoice.MAX_RETRIES - 1:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise last_exception
            finally:
                if conn:
                    conn.close()

    @staticmethod
    def create_paid_invoice(
        customer_id: int,
        subtotal: float,
        taxes: float,
        total: float,
        items: List[Dict]
    ) -> int:
        """
        Crea una factura pagada completamente (tipo Venta)
        Maneja productos y servicios en registros separados
        """
        # Obtener ID del tipo de factura "Venta"
        invoice_type_id = Invoice._get_invoice_type_id("Venta")
        
        # 1. Registrar factura principal
        invoice_id = Invoice._create_invoice(customer_id, invoice_type_id, subtotal, taxes, total)
        
        # 2. Procesar items
        for item in items:
            if item.get('is_service', False):
                # Para servicios: crear service_request y luego detalle de servicio
                service_request_id = ServiceRequest.create(
                    customer_id=customer_id,
                    service_id=item['id'],
                    description=f"Servicio vendido en factura #{invoice_id}",
                    quantity=item['quantity']
                )
                
                # Registrar detalle de servicio (con service_request_id y product_id=NULL)
                Invoice._execute_sql(
                    '''
                    INSERT INTO invoice_details (
                        invoice_id, service_request_id, quantity, 
                        unit_price, subtotal
                    ) VALUES (?, ?, ?, ?, ?)
                    ''',
                    (invoice_id, service_request_id, item['quantity'], 
                     item['unit_price'], item['total'])
                )
            else:
                # Para productos: manejar inventario
                product = InventoryItem.get_by_id(item['id'])
                if not product:
                    raise ValueError(f"Producto ID {item['id']} no encontrado")
                
                new_quantity = product['quantity'] - item['quantity']
                new_stock = product['stock'] - item['quantity']
                
                if new_quantity < 0 or new_stock < 0:
                    raise ValueError(f"Stock insuficiente para el producto ID {item['id']}")
                
                # Actualizar inventario
                Invoice._execute_sql(
                    '''
                    UPDATE inventory SET
                        quantity = ?,
                        stock = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''',
                    (new_quantity, new_stock, item['id'])
                )
                
                # Registrar movimiento de inventario
                user_id = SessionManager.get_user_id()
                if not user_id:
                    raise ValueError("Usuario no autenticado")
                
                movement_type = MovementType.get_by_name("Venta")
                if not movement_type:
                    raise ValueError("Tipo de movimiento 'Venta' no encontrado")
                
                InventoryMovement.create(
                    inventory_id=item['id'],
                    movement_type_id=movement_type['id'],
                    quantity_change=-item['quantity'],
                    stock_change=-item['quantity'],
                    previous_quantity=product['quantity'],
                    new_quantity=new_quantity,
                    previous_stock=product['stock'],
                    new_stock=new_stock,
                    reference_id=invoice_id,
                    reference_type="invoice",
                    user_id=user_id,
                    notes=f"Venta factura #{invoice_id}"
                )
                
                # Registrar detalle de producto (con product_id y service_request_id=NULL)
                Invoice._execute_sql(
                    '''
                    INSERT INTO invoice_details (
                        invoice_id, product_id, quantity, 
                        unit_price, subtotal
                    ) VALUES (?, ?, ?, ?, ?)
                    ''',
                    (invoice_id, item['id'], item['quantity'], 
                     item['unit_price'], item['total'])
                )
        
        return invoice_id

    @staticmethod
    def _create_invoice(
        customer_id: int,
        invoice_type_id: int,
        subtotal: float,
        taxes: float,
        total: float
    ) -> int:
        """Registra la factura principal en la tabla 'invoices'."""
        status_id = Invoice._get_status_id("Paid")
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return Invoice._execute_sql(
            '''
            INSERT INTO invoices (
                customer_id, invoice_type_id, issue_date, 
                subtotal, taxes, total, status_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (customer_id, invoice_type_id, issue_date, subtotal, taxes, total, status_id)
        )

    @staticmethod
    def _get_status_id(status_name: str) -> int:
        """Obtiene el ID de un estado de factura."""
        result = Invoice._execute_sql(
            "SELECT id FROM invoice_status WHERE name = ? LIMIT 1",
            (status_name,),
            fetch=True
        )
        if not result:
            raise ValueError(f"Estado '{status_name}' no encontrado")
        return result[0]['id']

    @staticmethod
    def get_by_id(invoice_id: int) -> Optional[Dict]:
        """Obtiene una factura por su ID con información del cliente y tipo."""
        result = Invoice._execute_sql(
            '''
            SELECT 
                i.*,
                c.first_name || ' ' || c.last_name as customer_name,
                c.id_number as customer_id_number,
                s.name as status_name,
                it.name as invoice_type_name
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            JOIN invoice_status s ON i.status_id = s.id
            JOIN invoice_types it ON i.invoice_type_id = it.id
            WHERE i.id = ?
            ''',
            (invoice_id,),
            fetch=True
        )
        return result[0] if result else None
    
    @staticmethod
    def _get_invoice_type_id(type_name: str) -> int:
        """Obtiene el ID de un tipo de factura."""
        result = Invoice._execute_sql(
            "SELECT id FROM invoice_types WHERE name = ? LIMIT 1",
            (type_name,),
            fetch=True
        )
        if not result:
            raise ValueError(f"Tipo de factura '{type_name}' no encontrado")
        return result[0]['id']

    @staticmethod
    def get_details(invoice_id: int) -> List[Dict]:
        """Obtiene los detalles de una factura con información específica para cada tipo"""
        # Detalles de productos
        product_details = Invoice._execute_sql(
            '''
            SELECT 
                d.id,
                d.invoice_id,
                d.product_id,
                NULL as service_request_id,
                d.quantity,
                d.unit_price,
                d.subtotal,
                d.created_at,
                d.updated_at,
                i.product as name,
                i.code,
                'product' as item_type
            FROM invoice_details d
            JOIN inventory i ON d.product_id = i.id
            WHERE d.invoice_id = ? AND d.product_id IS NOT NULL
            ''',
            (invoice_id,),
            fetch=True
        ) or []
        
        # Detalles de servicios
        service_details = Invoice._execute_sql(
            '''
            SELECT 
                d.id,
                d.invoice_id,
                NULL as product_id,
                d.service_request_id,
                d.quantity,
                d.unit_price,
                d.subtotal,
                d.created_at,
                d.updated_at,
                s.name as name,
                s.code,
                'service' as item_type
            FROM invoice_details d
            JOIN service_requests sr ON d.service_request_id = sr.id
            JOIN services s ON sr.service_id = s.id
            WHERE d.invoice_id = ? AND d.service_request_id IS NOT NULL
            ''',
            (invoice_id,),
            fetch=True
        ) or []
        
        return product_details + service_details

    @staticmethod
    def update_status(invoice_id: int, new_status: str) -> bool:
        """Actualiza el estado de una factura."""
        valid_statuses = ["Paid", "Pending", "Cancelled", "Partial"]
        if new_status not in valid_statuses:
            raise ValueError(f"Estado inválido. Opciones: {', '.join(valid_statuses)}")
        
        status_id = Invoice._get_status_id(new_status)
        
        Invoice._execute_sql(
            '''
            UPDATE invoices
            SET status_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (status_id, invoice_id)
        )
        
        if new_status == "Cancelled":
            Invoice._handle_cancellation(invoice_id)
        
        return True

    @staticmethod
    def _handle_cancellation(invoice_id: int) -> None:
        """Maneja la lógica de cancelación de facturas (solo para productos)."""
        details = Invoice.get_details(invoice_id)
        user_id = SessionManager.get_user_id()
        if not user_id:
            raise ValueError("Usuario no autenticado")
        
        movement_type = MovementType.get_by_name("Ajuste positivo")
        if not movement_type:
            raise ValueError("Tipo de movimiento 'Ajuste positivo' no encontrado")
        
        for detail in details:
            if detail['item_type'] == 'product' and detail['product_id']:
                product = InventoryItem.get_by_id(detail['product_id'])
                if not product:
                    continue
                
                new_quantity = product['quantity'] + detail['quantity']
                new_stock = product['stock'] + detail['quantity']
                
                # Actualizar inventario
                Invoice._execute_sql(
                    '''
                    UPDATE inventory SET
                        quantity = ?,
                        stock = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''',
                    (new_quantity, new_stock, detail['product_id'])
                )
                
                # Registrar movimiento
                InventoryMovement.create(
                    inventory_id=detail['product_id'],
                    movement_type_id=movement_type['id'],
                    quantity_change=detail['quantity'],
                    stock_change=detail['quantity'],
                    previous_quantity=product['quantity'],
                    new_quantity=new_quantity,
                    previous_stock=product['stock'],
                    new_stock=new_stock,
                    reference_id=invoice_id,
                    reference_type="invoice_cancellation",
                    user_id=user_id,
                    notes=f"Cancelación factura #{invoice_id}"
                )

    @staticmethod
    def search(
        customer_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Dict]:
        """Busca facturas con filtros opcionales."""
        query = '''
            SELECT 
                i.*,
                c.first_name || ' ' || c.last_name as customer_name,
                s.name as status_name
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            JOIN invoice_status s ON i.status_id = s.id
            WHERE 1=1
        '''
        params = []
        
        if customer_id:
            query += " AND i.customer_id = ?"
            params.append(customer_id)
        
        if status:
            query += " AND s.name = ?"
            params.append(status)
        
        if start_date:
            query += " AND DATE(i.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(i.issue_date) <= ?"
            params.append(end_date)
        
        if search_term:
            query += " AND (i.id LIKE ? OR c.first_name LIKE ? OR c.last_name LIKE ? OR c.id_number LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param] * 4)
        
        query += " ORDER BY i.issue_date DESC"
        
        return Invoice._execute_sql(query, tuple(params), fetch=True) or []