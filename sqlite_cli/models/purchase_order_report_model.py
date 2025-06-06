from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class PurchaseOrderReport:
    @staticmethod
    def get_purchase_orders_report(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        supplier_id: Optional[int] = None,
        order_id: Optional[int] = None,
        search_term: Optional[str] = None
    ) -> List[Dict]:
        """
        Get a complete report of purchase orders with their details.
        
        :param start_date: Start date in YYYY-MM-DD format
        :param end_date: End date in YYYY-MM-DD format
        :param supplier_id: Supplier ID to filter
        :param order_id: Specific order ID
        :param search_term: Term to search in order number, supplier name or ID
        :return: List of dictionaries with complete purchase order data
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Main query to get purchase orders
        order_query = '''
            SELECT 
                po.id,
                po.order_number,
                po.issue_date,
                po.expected_delivery_date,
                po.subtotal,
                po.taxes,
                po.total,
                po.notes,
                s.id as supplier_id,
                s.company as supplier_company,
                s.first_name || ' ' || s.last_name as supplier_name,
                s.id_number as supplier_id_number,
                s.phone as supplier_phone,
                s.email as supplier_email,
                u.username as created_by,
                a.username as approved_by
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON po.created_by = u.id
            LEFT JOIN users a ON po.approved_by = a.id
            WHERE 1=1
        '''
        
        params = []
        
        if start_date:
            order_query += " AND DATE(po.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            order_query += " AND DATE(po.issue_date) <= ?"
            params.append(end_date)
        
        if supplier_id:
            order_query += " AND po.supplier_id = ?"
            params.append(supplier_id)
        
        if order_id:
            order_query += " AND po.id = ?"
            params.append(order_id)
        
        if search_term:
            order_query += '''
                AND (po.order_number LIKE ? 
                OR s.company LIKE ? 
                OR s.first_name LIKE ? 
                OR s.last_name LIKE ? 
                OR s.id_number LIKE ?)
            '''
            search_param = f"%{search_term}%"
            params.extend([search_param] * 5)
        
        order_query += " ORDER BY po.issue_date DESC"
        
        cursor.execute(order_query, tuple(params))
        orders = [dict(row) for row in cursor.fetchall()]
        
        if not orders:
            conn.close()
            return []
        
        # Query to get order details
        detail_query = '''
            SELECT 
                pod.id,
                pod.product_id,
                pod.product_name,
                pod.quantity,
                pod.unit_price,
                pod.reference_price,
                pod.subtotal,
                pod.received_quantity,
                pod.notes,
                i.code as product_code,
                i.product as product_name,
                i.description as product_description
            FROM purchase_order_details pod
            LEFT JOIN inventory i ON pod.product_id = i.id
            WHERE pod.order_id = ?
            ORDER BY pod.id
        '''
        
        # Get details for each order
        for order in orders:
            cursor.execute(detail_query, (order['id'],))
            order['items'] = [dict(row) for row in cursor.fetchall()]
            
            # Calculate product count
            order['product_count'] = len([item for item in order['items'] if item['product_id']])
        
        conn.close()
        return orders

    @staticmethod
    def get_order_details(order_id: int) -> Dict:
        """
        Get all details of a specific purchase order.
        
        :param order_id: Order ID
        :return: Dictionary with order data and its details
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get order information
        cursor.execute('''
            SELECT 
                po.*,
                s.company as supplier_company,
                s.first_name || ' ' || s.last_name as supplier_name,
                s.id_number as supplier_id_number,
                s.phone as supplier_phone,
                s.email as supplier_email,
                u.username as created_by,
                a.username as approved_by
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON po.created_by = u.id
            LEFT JOIN users a ON po.approved_by = a.id
            WHERE po.id = ?
        ''', (order_id,))
        
        order = dict(cursor.fetchone())
        
        # Get order details
        cursor.execute('''
            SELECT 
                pod.*,
                i.code as product_code,
                i.product as product_name,
                i.description as product_description
            FROM purchase_order_details pod
            LEFT JOIN inventory i ON pod.product_id = i.id
            WHERE pod.order_id = ?
        ''', (order_id,))
        
        order['items'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return order

    @staticmethod
    def get_purchase_summary(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Get statistical summary of purchase orders.
        
        :param start_date: Start date in YYYY-MM-DD format
        :param end_date: End date in YYYY-MM-DD format
        :return: Dictionary with purchase statistics
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query
        query = '''
            SELECT 
                COUNT(*) as total_orders,
                SUM(total) as total_amount,
                SUM(taxes) as total_taxes,
                SUM(subtotal) as total_subtotal,
                AVG(total) as average_order,
                MIN(total) as min_order,
                MAX(total) as max_order
            FROM purchase_orders
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
        
        # Get top suppliers
        cursor.execute('''
            SELECT 
                s.company as supplier_name,
                COUNT(*) as order_count,
                SUM(po.total) as total_amount
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            WHERE DATE(po.issue_date) BETWEEN ? AND ?
            GROUP BY s.company
            ORDER BY total_amount DESC
            LIMIT 10
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['top_suppliers'] = [dict(row) for row in cursor.fetchall()]
        
        # Get top products
        cursor.execute('''
            SELECT 
                i.product as product_name,
                i.code as product_code,
                SUM(pod.quantity) as total_quantity,
                SUM(pod.subtotal) as total_amount
            FROM purchase_order_details pod
            JOIN purchase_orders po ON pod.order_id = po.id
            JOIN inventory i ON pod.product_id = i.id
            WHERE DATE(po.issue_date) BETWEEN ? AND ?
            GROUP BY i.product, i.code
            ORDER BY total_quantity DESC
            LIMIT 10
        ''', (start_date or '2000-01-01', end_date or '2100-01-01'))
        
        summary['top_products'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return summary