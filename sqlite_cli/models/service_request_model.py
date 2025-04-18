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
        request_status_id: int = 1
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
            VALUES (?, ?, ?, ?, ?, ?, 1)''',  # 1 = active by default
            (customer_id, service_id, description, quantity, total, request_status_id)
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
                   rs.name as request_status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE st.name = 'active'
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        """Busca solicitudes activas con filtro opcional"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT sr.*, 
                   c.first_name || ' ' || c.last_name as customer_name,
                   c.id_number as customer_id_number,
                   s.name as service_name,
                   s.price as service_price,
                   rs.name as request_status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "sr.id",
                    "Cliente": "c.first_name || ' ' || c.last_name",
                    "Servicio": "s.name",
                    "Estado Solicitud": "rs.name"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            item_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(item_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(sr.id) LIKE ? OR 
                        LOWER(c.first_name || ' ' || c.last_name) LIKE ? OR 
                        LOWER(s.name) LIKE ? OR
                        LOWER(rs.name) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 4)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(request_id: int) -> Optional[Dict]:
        """Obtiene una solicitud por su ID (solo si está activa)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sr.*, 
                   c.first_name, c.last_name, c.id_number,
                   s.name as service_name,
                   rs.name as request_status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE sr.id = ? AND st.name = 'active'
        ''', (request_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(
        request_id: int,
        customer_id: int,
        service_id: int,
        description: str,
        quantity: int,
        request_status_id: int
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
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (customer_id, service_id, description, quantity, total, request_status_id, request_id)
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
    def deactivate(request_id: int) -> None:
        """Desactiva una solicitud (estado inactivo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE service_requests 
            SET status_id = (SELECT id FROM status WHERE name = 'inactive'),
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (request_id,)
        )
        conn.commit()
        conn.close()