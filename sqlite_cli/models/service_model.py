from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Service:
    @staticmethod
    def create(
        code: str,
        name: str,
        price: float,
        description: Optional[str] = None
    ) -> None:
        """Crea un nuevo servicio (siempre activo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO services 
            (code, name, price, description, status_id)
            VALUES (?, ?, ?, ?, 1)''',  # 1 = activo por defecto
            (code, name, price, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """Obtiene todos los servicios activos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'active'
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        """Busca servicios activos con filtro opcional"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT s.*, st.name as status_name
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "s.id",
                    "Código": "s.code",
                    "Nombre": "s.name",
                    "Descripción": "s.description"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            service_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(service_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(s.code) LIKE ? OR 
                        LOWER(s.name) LIKE ? OR 
                        LOWER(s.description) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 3)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_inactive(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        """Busca servicios inactivos con filtro opcional"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT s.*, st.name as status_name
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'inactive'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "s.id",
                    "Código": "s.code",
                    "Nombre": "s.name",
                    "Descripción": "s.description"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            service_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(service_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(s.code) LIKE ? OR 
                        LOWER(s.name) LIKE ? OR 
                        LOWER(s.description) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 3)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(service_id: int) -> Optional[Dict]:
        """Obtiene un servicio por su ID (sin importar estado)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE s.id = ?
        ''', (service_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def get_by_code(code: str) -> Optional[Dict]:
        """Obtiene un servicio por su código (solo si está activo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE s.code = ? AND st.name = 'active'
        ''', (code,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(
        service_id: int,
        code: str,
        name: str,
        price: float,
        description: Optional[str] = None
    ) -> None:
        """Actualiza un servicio existente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE services SET
            code = ?,
            name = ?,
            price = ?,
            description = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (code, name, price, description, service_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def disable(service_id: int) -> None:
        """Deshabilita un servicio (estado inactivo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE services SET
                status_id = (SELECT id FROM status WHERE name = 'inactive'),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (service_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def enable(service_id: int) -> None:
        """Habilita un servicio (estado activo)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE services SET
                status_id = (SELECT id FROM status WHERE name = 'active'),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (service_id,))
        conn.commit()
        conn.close()