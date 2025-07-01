from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class PurchaseOrderReport:
    @staticmethod
    def get_purchase_orders_report(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Dict]:
        """
        Obtiene un reporte completo de órdenes de compra con sus detalles.
        
        :param start_date: Fecha de inicio en formato YYYY-MM-DD
        :param end_date: Fecha de fin en formato YYYY-MM-DD
        :param search_term: Término para buscar en todos los campos relevantes
        :return: Lista de diccionarios con los datos completos de las órdenes
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consulta principal para obtener las órdenes
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
                s.company as supplier_company,
                s.id_number as supplier_id_number,
                u.username as created_by
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON po.created_by = u.id
            WHERE 1=1
        '''
        
        params = []
        
        if start_date:
            order_query += " AND DATE(po.issue_date) >= ?"
            params.append(start_date)
        
        if end_date:
            order_query += " AND DATE(po.issue_date) <= ?"
            params.append(end_date)
        
        if search_term:
            search_param = f"%{search_term}%"
            order_query += '''
                AND (po.order_number LIKE ? 
                OR s.company LIKE ? 
                OR s.id_number LIKE ?
                OR po.subtotal LIKE ?
                OR po.taxes LIKE ?
                OR po.total LIKE ?
                OR po.notes LIKE ?)
            '''
            params.extend([search_param] * 7)
        
        order_query += " ORDER BY po.issue_date DESC"
        
        cursor.execute(order_query, tuple(params))
        orders = [dict(row) for row in cursor.fetchall()]
        
        if not orders:
            conn.close()
            return []
        
        # Consulta para obtener los detalles de cada orden
        detail_query = '''
            SELECT 
                pod.*,
                i.code as product_code,
                i.product as product_name
            FROM purchase_order_details pod
            LEFT JOIN inventory i ON pod.product_id = i.id
            WHERE pod.order_id = ?
            ORDER BY pod.id
        '''
        
        # Obtener detalles para cada orden
        for order in orders:
            cursor.execute(detail_query, (order['id'],))
            order['items'] = [dict(row) for row in cursor.fetchall()]
            
            # Calcular cantidad de productos
            order['product_count'] = len(order['items'])
        
        conn.close()
        return orders

    @staticmethod
    def get_order_details(order_id: int) -> Dict:
        """
        Obtiene todos los detalles de una orden específica.
        
        :param order_id: ID de la orden
        :return: Diccionario con los datos de la orden y sus detalles
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener información de la orden
        cursor.execute('''
            SELECT 
                po.*,
                s.company as supplier_company,
                s.id_number as supplier_id_number,
                u.username as created_by
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON po.created_by = u.id
            WHERE po.id = ?
        ''', (order_id,))
        
        order = dict(cursor.fetchone())
        
        # Obtener detalles de la orden
        cursor.execute('''
            SELECT 
                pod.*,
                i.code as product_code,
                i.product as product_name
            FROM purchase_order_details pod
            LEFT JOIN inventory i ON pod.product_id = i.id
            WHERE pod.order_id = ?
        ''', (order_id,))
        
        order['items'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return order