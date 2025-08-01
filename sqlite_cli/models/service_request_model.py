from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class ServiceRequest:
    @staticmethod
    def create(
        customer_id: int,
        service_id: int,
        description: str,
        quantity: int = 1,
        employee_id: int = 0,  # Valor por defecto
        request_status_id: int = 1
    ) -> int:  # Cambiado el tipo de retorno a int
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT price FROM services WHERE id = ?', (service_id,))
            service = cursor.fetchone()
            if not service:
                raise ValueError("Servicio no encontrado")
                
            price = service['price']
            total = price * quantity
            
            cursor.execute(
                '''INSERT INTO service_requests 
                (request_number, customer_id, service_id, employee_id, 
                description, quantity, total, request_status_id, status_id)
                VALUES ('SR-', ?, ?, ?, ?, ?, ?, ?, 1)''',
                (customer_id, service_id, employee_id, description, 
                quantity, total, request_status_id)
            )
            
            request_id = cursor.lastrowid
            cursor.execute(
                'UPDATE service_requests SET request_number = ? WHERE id = ?',
                (f"SR-{request_id}", request_id)
            )
            
            conn.commit()
            return request_id  # Devolvemos el ID del registro creado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
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
                   CASE 
                       WHEN u.id IS NULL THEN 'Sin asignar'
                       ELSE p.first_name || ' ' || p.last_name 
                   END as employee_name,
                   u.username as employee_username
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            LEFT JOIN users u ON sr.employee_id = u.id
            LEFT JOIN person p ON u.person_id = p.id
            WHERE st.name = 'active'
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT sr.*, 
                   c.first_name || ' ' || c.last_name as customer_name,
                   c.id_number as customer_id_number,
                   s.name as service_name,
                   s.price as service_price,
                   rs.name as request_status_name,
                   CASE 
                       WHEN u.id IS NULL THEN 'Sin asignar'
                       ELSE p.first_name || ' ' || p.last_name 
                   END as employee_name,
                   u.username as employee_username
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            LEFT JOIN users u ON sr.employee_id = u.id
            LEFT JOIN person p ON u.person_id = p.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "sr.id",
                    "Número de solicitud": "sr.request_number",
                    "Cliente": "c.first_name || ' ' || c.last_name",
                    "Servicio": "s.name",
                    "Estado Solicitud": "rs.name",
                    "Empleado": "employee_name"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field in ["ID", "Número de solicitud"]:
                        base_query += f" AND {field_name} LIKE ?"
                        params.append(f"%{search_term}%")
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term.lower()}%")
            else:
                base_query += '''
                    AND (LOWER(sr.id) LIKE ? OR 
                        LOWER(sr.request_number) LIKE ? OR
                        LOWER(c.first_name || ' ' || c.last_name) LIKE ? OR 
                        LOWER(s.name) LIKE ? OR
                        LOWER(rs.name) LIKE ? OR
                        LOWER(employee_name) LIKE ?)
                '''
                params.extend([f"%{search_term.lower()}%"] * 6)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @classmethod
    def get_by_id(cls, request_id: int) -> Optional[Dict]:
        """Obtiene una solicitud de servicio por su ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                sr.*,
                rs.name as request_status_name,
                s.name as status_name,
                c.first_name || ' ' || c.last_name as customer_name,
                sv.name as service_name,
                u.username as employee_name
            FROM service_requests sr
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status s ON sr.status_id = s.id
            JOIN customers c ON sr.customer_id = c.id
            JOIN services sv ON sr.service_id = sv.id
            LEFT JOIN users u ON sr.employee_id = u.id
            WHERE sr.id = ?
        '''
        
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return dict(result)
        return None

    @staticmethod
    def update_employee(request_id: int, employee_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''UPDATE service_requests SET
            employee_id = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (employee_id, request_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(request_id: int, request_status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE service_requests SET status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (request_status_id, request_id)
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

    @staticmethod
    def search_inactive(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT sr.*, 
                   c.first_name || ' ' || c.last_name as customer_name,
                   c.id_number as customer_id_number,
                   s.name as service_name,
                   s.price as service_price,
                   rs.name as request_status_name,
                   CASE 
                       WHEN u.id IS NULL THEN 'Sin asignar'
                       ELSE p.first_name || ' ' || p.last_name 
                   END as employee_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            LEFT JOIN users u ON sr.employee_id = u.id
            LEFT JOIN person p ON u.person_id = p.id
            WHERE st.name = 'inactive'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "sr.id",
                    "Cliente": "c.first_name || ' ' || c.last_name",
                    "Servicio": "s.name",
                    "Estado Solicitud": "rs.name",
                    "Empleado": "employee_name"
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
                        params.append(f"%{search_term.lower()}%")
            else:
                base_query += '''
                    AND (LOWER(sr.id) LIKE ? OR 
                        LOWER(c.first_name || ' ' || c.last_name) LIKE ? OR 
                        LOWER(s.name) LIKE ? OR
                        LOWER(rs.name) LIKE ? OR
                        LOWER(employee_name) LIKE ?)
                '''
                params.extend([f"%{search_term.lower()}%"] * 5)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def activate(request_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE service_requests 
            SET status_id = (SELECT id FROM status WHERE name = 'active'),
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (request_id,)
        )
        conn.commit()
        conn.close()