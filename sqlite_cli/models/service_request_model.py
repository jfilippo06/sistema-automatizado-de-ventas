# models/service_request_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class ServiceRequest:
    @staticmethod
    def create(
        customer_id: int,
        service_id: int,
        description: str,
        quantity: int = 1,
        request_status_id: int = 1,
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
                   c.id_number as customer_id_number,
                   s.name as service_name,
                   s.price as service_price,
                   rs.name as request_status_name,
                   st.name as status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(request_id: int) -> Optional[Dict]:
        """Obtiene una solicitud por su ID con información relacionada."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sr.*, 
                   c.first_name, c.last_name, c.id_number,
                   s.name as service_name,
                   rs.name as request_status_name,
                   st.name as status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE sr.id = ?
        ''', (request_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def get_by_customer(customer_id: int) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sr.*, 
                   s.name as service_name,
                   rs.name as request_status_name,
                   st.name as status_name
            FROM service_requests sr
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE sr.customer_id = ?
        ''', (customer_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update(
        request_id: int,
        customer_id: int,
        service_id: int,
        description: str,
        quantity: int,
        request_status_id: int,
        status_id: int
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT price FROM services WHERE id = ?', (service_id,))
        service = cursor.fetchone()
        if not service:
            conn.close()
            raise ValueError("Service not found")
            
        price = service['price']
        total = price * quantity
        
        cursor.execute(
            '''UPDATE service_requests SET
            customer_id = ?,
            service_id = ?,
            description = ?,
            quantity = ?,
            total = ?,
            request_status_id = ?,
            status_id = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (customer_id, service_id, description, quantity, total, request_status_id, status_id, request_id)
        )
        conn.commit()
        conn.close()

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

    @staticmethod
    def update_status(request_id: int, status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE service_requests SET status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status_id, request_id)
        )
        conn.commit()
        conn.close()