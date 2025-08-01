from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class ServiceRequestQuery:
    @staticmethod
    def get_service_requests_report(
        search_term: Optional[str] = None,
        customer_id: Optional[int] = None,
        service_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        request_status_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        request_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Obtiene un reporte de solicitudes de servicio con filtros opcionales.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                sr.id,
                sr.request_number,
                u.username as employee,
                c.first_name || ' ' || c.last_name as customer,
                s.name as service,
                sr.description,
                sr.quantity,
                sr.total,
                rs.name as request_status,
                sr.created_at
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN users u ON sr.employee_id = u.id
            JOIN request_status rs ON sr.request_status_id = rs.id
        '''
        
        params = []
        
        if request_id:
            query += " AND sr.id = ?"
            params.append(request_id)
            
        if search_term:
            query += '''
                AND (LOWER(sr.request_number) LIKE ? OR 
                    LOWER(c.first_name || ' ' || c.last_name) LIKE ? OR 
                    LOWER(s.name) LIKE ?)
            '''
            search_param = f"%{search_term.lower()}%"
            params.extend([search_param] * 3)
        
        if customer_id:
            query += " AND sr.customer_id = ?"
            params.append(customer_id)
            
        if service_id:
            query += " AND sr.service_id = ?"
            params.append(service_id)
            
        if employee_id:
            query += " AND sr.employee_id = ?"
            params.append(employee_id)
            
        if request_status_id:
            query += " AND sr.request_status_id = ?"
            params.append(request_status_id)
            
        if start_date:
            query += " AND DATE(sr.created_at) >= ?"
            params.append(start_date.replace("/", "-"))
            
        if end_date:
            query += " AND DATE(sr.created_at) <= ?"
            params.append(end_date.replace("/", "-"))
        
        query += " ORDER BY sr.created_at DESC"
        
        cursor.execute(query, tuple(params))
        requests = []
        for row in cursor.fetchall():
            request = dict(row)
            # Formatear fecha
            if 'created_at' in request and request['created_at']:
                try:
                    dt = datetime.strptime(request['created_at'], '%Y-%m-%d %H:%M:%S')
                    request['created_at'] = dt.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    pass
            requests.append(request)
        
        conn.close()
        return requests

    @staticmethod
    def get_service_request_movements_report(
        request_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        movement_type: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Obtiene un reporte de movimientos de solicitudes de servicio con filtros opcionales.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Traducción de tipos de movimiento
        movement_type_translations = {
            'ASIGNACION_EMPLEADO': 'Asignación de empleado',
            'CAMBIO_ESTADO': 'Cambio de estado',
            'ACTUALIZACION_ESTADO': 'Actualización de estado',
            'CREACION': 'Creación',
            'CANCELACION': 'Cancelación',
            'Todos': None
        }
        
        # Convertir tipo de movimiento de español a inglés si es necesario
        reverse_translation = {v: k for k, v in movement_type_translations.items()}
        db_movement_type = reverse_translation.get(movement_type, movement_type)
        
        query = '''
            SELECT 
                srm.id,
                srm.created_at,
                mt.name as movement_type,
                u.username as user,
                u_prev.username as previous_employee,
                u_new.username as new_employee,
                s_prev.name as previous_status,
                s_new.name as new_status,
                rs_prev.name as previous_request_status,
                rs_new.name as new_request_status,
                srm.reference_type,
                srm.reference_id,
                srm.notes
            FROM service_request_movements srm
            JOIN service_request_movement_types mt ON srm.movement_type_id = mt.id
            JOIN users u ON srm.user_id = u.id
            LEFT JOIN users u_prev ON srm.previous_employee_id = u_prev.id
            LEFT JOIN users u_new ON srm.new_employee_id = u_new.id
            LEFT JOIN status s_prev ON srm.previous_status_id = s_prev.id
            LEFT JOIN status s_new ON srm.new_status_id = s_new.id
            LEFT JOIN request_status rs_prev ON srm.previous_request_status_id = rs_prev.id
            LEFT JOIN request_status rs_new ON srm.new_request_status_id = rs_new.id
            WHERE 1=1
        '''
        
        params = []
        
        if request_id:
            query += " AND srm.request_id = ?"
            params.append(request_id)
            
        if start_date:
            query += " AND DATE(srm.created_at) >= ?"
            params.append(start_date.replace("/", "-"))
            
        if end_date:
            query += " AND DATE(srm.created_at) <= ?"
            params.append(end_date.replace("/", "-"))
            
        if db_movement_type and db_movement_type != "Todos":
            query += " AND mt.name = ?"
            params.append(db_movement_type)
            
        if user_id:
            query += " AND srm.user_id = ?"
            params.append(user_id)
            
        query += " ORDER BY srm.created_at DESC"
        
        cursor.execute(query, tuple(params))
        movements = []
        for row in cursor.fetchall():
            movement = dict(row)
            # Formatear la fecha
            if 'created_at' in movement and movement['created_at']:
                try:
                    dt = datetime.strptime(movement['created_at'], '%Y-%m-%d %H:%M:%S')
                    movement['created_at'] = dt.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    pass
            
            # Traducir tipos de movimiento
            if movement['movement_type'] in movement_type_translations:
                movement['movement_type'] = movement_type_translations[movement['movement_type']]
            
            # Manejar valores nulos
            for key in movement:
                if movement[key] is None:
                    if key in ['previous_request_status', 'new_request_status', 'previous_status', 'new_status']:
                        movement[key] = "N/A"
                    elif key == 'notes':
                        movement[key] = "Sin comentarios"
                    elif key in ['previous_employee', 'new_employee']:
                        movement[key] = "N/A"
                    else:
                        movement[key] = ""
                    
            movements.append(movement)
        
        conn.close()
        return movements

    @staticmethod
    def get_service_request_details(request_id: int) -> Optional[Dict]:
        """
        Obtiene los detalles completos de una solicitud de servicio específica.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                sr.id,
                sr.request_number,
                c.first_name || ' ' || c.last_name as customer,
                s.name as service,
                sr.description,
                sr.quantity,
                sr.total,
                rs.name as request_status,
                u.username as employee,
                sr.created_at
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN users u ON sr.employee_id = u.id
            WHERE sr.id = ?
        '''
        
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            request = dict(result)
            # Formatear fecha
            if 'created_at' in request and request['created_at']:
                try:
                    dt = datetime.strptime(request['created_at'], '%Y-%m-%d %H:%M:%S')
                    request['created_at'] = dt.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    pass
            return request
        return None