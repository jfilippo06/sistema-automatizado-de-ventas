from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class SalesReport:
    @staticmethod
    def get_sales_report(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        customer_id: Optional[int] = None,
        invoice_id: Optional[int] = None,
        search_term: Optional[str] = None
    ) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consulta principal para obtener las facturas
        invoice_query = '''
            SELECT 
                i.id as invoice_id,
                i.issue_date,
                i.subtotal,
                i.taxes,
                i.total,
                c.id as customer_id,
                c.first_name || ' ' || c.last_name as customer_name,
                c.id_number as customer_id_number,
                it.name as invoice_type,
                s.name as status_name,
                i.created_at
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            JOIN invoice_status s ON i.status_id = s.id
            JOIN invoice_types it ON i.invoice_type_id = it.id
            WHERE 1=1
        '''
        
        params = []
        
        if start_date:
            # Aseguramos que la fecha esté en formato YYYY-MM-DD para SQLite
            start_date = start_date.replace("/", "-")
            invoice_query += " AND DATE(i.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            # Aseguramos que la fecha esté en formato YYYY-MM-DD para SQLite
            end_date = end_date.replace("/", "-")
            invoice_query += " AND DATE(i.issue_date) <= ?"
            params.append(end_date)
        
        if search_term:
            search_param = f"%{search_term}%"
            invoice_query += '''
                AND (i.id LIKE ? 
                OR c.first_name LIKE ? 
                OR c.last_name LIKE ? 
                OR c.id_number LIKE ?
                OR it.name LIKE ?
                OR i.total LIKE ?)
            '''
            params.extend([search_param] * 6)
        
        invoice_query += " ORDER BY i.issue_date DESC"
        
        cursor.execute(invoice_query, tuple(params))
        sales = [dict(row) for row in cursor.fetchall()]
        
        if not sales:
            conn.close()
            return []
        
        # Consulta para obtener los detalles de cada factura
        detail_query = '''
            SELECT 
                d.id,
                d.quantity,
                d.unit_price,
                d.subtotal,
                CASE
                    WHEN d.product_id IS NOT NULL THEN 'product'
                    WHEN d.service_request_id IS NOT NULL THEN 'service'
                END as item_type,
                COALESCE(
                    p.product, 
                    s.name
                ) as item_name,
                COALESCE(
                    p.code,
                    sr.service_id || '-' || sr.id
                ) as item_code,
                CASE
                    WHEN d.product_id IS NOT NULL THEN p.price
                    WHEN d.service_request_id IS NOT NULL THEN sr.total / sr.quantity
                END as item_price,
                d.created_at as detail_created_at
            FROM invoice_details d
            LEFT JOIN inventory p ON d.product_id = p.id
            LEFT JOIN service_requests sr ON d.service_request_id = sr.id
            LEFT JOIN services s ON sr.service_id = s.id
            WHERE d.invoice_id = ?
            ORDER BY d.id
        '''
        
        # Obtener detalles para cada venta
        for sale in sales:
            cursor.execute(detail_query, (sale['invoice_id'],))
            sale['items'] = [dict(row) for row in cursor.fetchall()]
            
            # Calcular cantidades por tipo de ítem
            sale['product_count'] = sum(1 for item in sale['items'] if item['item_type'] == 'product')
            sale['service_count'] = sum(1 for item in sale['items'] if item['item_type'] == 'service')
        
        conn.close()
        return sales

    @staticmethod
    def get_invoice_details(invoice_id: int) -> Dict:
        """
        Obtiene todos los detalles de una factura específica.
        
        :param invoice_id: ID de la factura
        :return: Diccionario con los datos de la factura y sus detalles
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener información de la factura
        cursor.execute('''
            SELECT 
                i.*,
                c.first_name || ' ' || c.last_name as customer_name,
                c.id_number as customer_id_number,
                c.email as customer_email,
                c.phone as customer_phone,
                it.name as invoice_type_name,
                s.name as status_name
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            JOIN invoice_types it ON i.invoice_type_id = it.id
            JOIN invoice_status s ON i.status_id = s.id
            WHERE i.id = ?
        ''', (invoice_id,))
        
        invoice = dict(cursor.fetchone())
        
        # Obtener detalles de la factura
        cursor.execute('''
            SELECT 
                d.*,
                CASE
                    WHEN d.product_id IS NOT NULL THEN 'product'
                    WHEN d.service_request_id IS NOT NULL THEN 'service'
                END as item_type,
                COALESCE(p.product, s.name) as item_name,
                COALESCE(p.code, s.code) as item_code,
                COALESCE(p.description, s.description) as item_description
            FROM invoice_details d
            LEFT JOIN inventory p ON d.product_id = p.id
            LEFT JOIN service_requests sr ON d.service_request_id = sr.id
            LEFT JOIN services s ON sr.service_id = s.id
            WHERE d.invoice_id = ?
        ''', (invoice_id,))
        
        invoice['items'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return invoice