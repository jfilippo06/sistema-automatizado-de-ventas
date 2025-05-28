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
        Obtiene un reporte de ventas con filtros opcionales.
        
        :param start_date: Fecha de inicio en formato YYYY-MM-DD
        :param end_date: Fecha de fin en formato YYYY-MM-DD
        :param customer_id: ID del cliente para filtrar
        :param invoice_id: ID de factura específico
        :param search_term: Término para buscar en nombre, cédula o ID de factura
        :return: Lista de diccionarios con los datos de las ventas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                i.id as invoice_id,
                i.issue_date,
                i.subtotal,
                i.taxes,
                i.total,
                c.id as customer_id,
                c.first_name || ' ' || c.last_name as customer_name,
                c.id_number as customer_id_number,
                s.name as status_name,
                it.name as invoice_type_name
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            JOIN invoice_status s ON i.status_id = s.id
            JOIN invoice_types it ON i.invoice_type_id = it.id
            WHERE 1=1
        '''
        
        params = []
        
        if start_date:
            query += " AND DATE(i.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(i.issue_date) <= ?"
            params.append(end_date)
        
        if customer_id:
            query += " AND i.customer_id = ?"
            params.append(customer_id)
        
        if invoice_id:
            query += " AND i.id = ?"
            params.append(invoice_id)
        
        if search_term:
            query += " AND (i.id LIKE ? OR c.first_name LIKE ? OR c.last_name LIKE ? OR c.id_number LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param] * 4)
        
        query += " ORDER BY i.issue_date DESC"
        
        cursor.execute(query, tuple(params))
        sales = [dict(row) for row in cursor.fetchall()]
        
        # Obtener detalles para cada venta
        for sale in sales:
            cursor.execute('''
                SELECT 
                    d.id,
                    d.quantity,
                    d.unit_price,
                    d.subtotal,
                    COALESCE(i.product, s.name) as item_name,
                    CASE 
                        WHEN d.product_id IS NOT NULL THEN 'product'
                        WHEN d.service_request_id IS NOT NULL THEN 'service'
                    END as item_type
                FROM invoice_details d
                LEFT JOIN inventory i ON d.product_id = i.id
                LEFT JOIN service_requests sr ON d.service_request_id = sr.id
                LEFT JOIN services s ON sr.service_id = s.id
                WHERE d.invoice_id = ?
            ''', (sale['invoice_id'],))
            
            sale['items'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return sales

    @staticmethod
    def get_sales_summary(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Obtiene un resumen de ventas para un período.
        
        :param start_date: Fecha de inicio en formato YYYY-MM-DD
        :param end_date: Fecha de fin en formato YYYY-MM-DD
        :return: Diccionario con el resumen de ventas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                COUNT(*) as total_sales,
                SUM(total) as total_amount,
                SUM(taxes) as total_taxes,
                SUM(subtotal) as total_subtotal
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
        
        # Obtener ventas por día para gráfico
        cursor.execute('''
            SELECT 
                DATE(issue_date) as sale_date,
                COUNT(*) as sales_count,
                SUM(total) as daily_total
            FROM invoices
            WHERE DATE(issue_date) BETWEEN ? AND ?
            GROUP BY DATE(issue_date)
            ORDER BY sale_date
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['daily_sales'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return summary