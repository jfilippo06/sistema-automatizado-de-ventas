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
        """
        Obtiene un reporte completo de ventas con información de facturas y sus detalles.
        
        :param start_date: Fecha de inicio en formato YYYY-MM-DD
        :param end_date: Fecha de fin en formato YYYY-MM-DD
        :param customer_id: ID del cliente para filtrar
        :param invoice_id: ID de factura específico
        :param search_term: Término para buscar en ID factura, nombre o cédula del cliente
        :return: Lista de diccionarios con los datos completos de las ventas
        """
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
            invoice_query += " AND DATE(i.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            invoice_query += " AND DATE(i.issue_date) <= ?"
            params.append(end_date)
        
        if customer_id:
            invoice_query += " AND i.customer_id = ?"
            params.append(customer_id)
        
        if invoice_id:
            invoice_query += " AND i.id = ?"
            params.append(invoice_id)
        
        if search_term:
            invoice_query += '''
                AND (i.id LIKE ? 
                OR c.first_name LIKE ? 
                OR c.last_name LIKE ? 
                OR c.id_number LIKE ?)
            '''
            search_param = f"%{search_term}%"
            params.extend([search_param] * 4)
        
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

    @staticmethod
    def get_sales_summary(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Obtiene un resumen estadístico de las ventas.
        
        :param start_date: Fecha de inicio en formato YYYY-MM-DD
        :param end_date: Fecha de fin en formato YYYY-MM-DD
        :return: Diccionario con estadísticas de ventas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consulta base
        query = '''
            SELECT 
                COUNT(*) as total_invoices,
                SUM(total) as total_amount,
                SUM(taxes) as total_taxes,
                SUM(subtotal) as total_subtotal,
                AVG(total) as average_sale,
                MIN(total) as min_sale,
                MAX(total) as max_sale
            FROM invoices
            WHERE 1=1
        '''
        
        params = []
        
        if start_date:
            query += " AND DATE(issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(issue_date) <= ?"
            params.append(end_date)
        
        cursor.execute(query, tuple(params))
        summary = dict(cursor.fetchone())
        
        # Obtener ventas por tipo
        cursor.execute('''
            SELECT 
                it.name as invoice_type,
                COUNT(*) as count,
                SUM(i.total) as total
            FROM invoices i
            JOIN invoice_types it ON i.invoice_type_id = it.id
            WHERE DATE(i.issue_date) BETWEEN ? AND ?
            GROUP BY it.name
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['by_type'] = [dict(row) for row in cursor.fetchall()]
        
        # Obtener productos más vendidos
        cursor.execute('''
            SELECT 
                p.product as name,
                p.code,
                SUM(d.quantity) as total_quantity,
                SUM(d.subtotal) as total_amount
            FROM invoice_details d
            JOIN invoices i ON d.invoice_id = i.id
            JOIN inventory p ON d.product_id = p.id
            WHERE DATE(i.issue_date) BETWEEN ? AND ?
            GROUP BY p.product, p.code
            ORDER BY total_quantity DESC
            LIMIT 10
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['top_products'] = [dict(row) for row in cursor.fetchall()]
        
        # Obtener servicios más vendidos
        cursor.execute('''
            SELECT 
                s.name,
                s.code,
                COUNT(*) as total_services,
                SUM(d.subtotal) as total_amount
            FROM invoice_details d
            JOIN invoices i ON d.invoice_id = i.id
            JOIN service_requests sr ON d.service_request_id = sr.id
            JOIN services s ON sr.service_id = s.id
            WHERE DATE(i.issue_date) BETWEEN ? AND ?
            GROUP BY s.name, s.code
            ORDER BY total_services DESC
            LIMIT 10
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['top_services'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return summary