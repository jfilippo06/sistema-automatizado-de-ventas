# models/service_request_model.py
from database.database import get_db_connection
from typing import List, Dict, Optional

class ServiceRequest:
    @staticmethod
    def create(
        customer_id: int,
        service_id: int,
        description: str,
        quantity: int = 1,
        request_status_id: int = 1,  # 1 = started por defecto
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get service price
        cursor.execute('SELECT price FROM services WHERE id = ?', (service_id,))
        service = cursor.fetchone()
        if not service:
            conn.close()
            raise ValueError("Service not found")
            
        price = service['price']
        total = price * quantity
        
        cursor.execute(
            '''INSERT INTO service_requests 
            (customer_id, service_id, description, quantity, total, request_status_id, status_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (customer_id, service_id, description, quantity, total, request_status_id, status_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sr.*, 
                   c.first_name || ' ' || c.last_name as customer_name,
                   s.name as service_name,
                   rs.name as request_status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update_request_status(request_id: int, request_status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE service_requests SET request_status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (request_status_id, request_id)
        )
        conn.commit()
        conn.close()