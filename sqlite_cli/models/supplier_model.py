from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Supplier:
    @staticmethod
    def create(
        code: str,
        first_name: str,
        last_name: str,
        id_number: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        tax_id: Optional[str] = None,
        company: Optional[str] = None,
        status_id: int = 1  # Por defecto activo
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO suppliers (
                code, id_number, first_name, last_name, 
                address, phone, email, tax_id, company, status_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, id_number, first_name, last_name, address, phone, email, tax_id, company, status_id))
        conn.commit()
        conn.close()

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT s.*, st.name as status_name 
            FROM suppliers s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "s.id",
                    "Código": "s.code",
                    "Cédula": "s.id_number",
                    "Nombres": "s.first_name",
                    "Apellidos": "s.last_name",
                    "Empresa": "s.company",
                    "RIF": "s.tax_id",
                    "Teléfono": "s.phone"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            supplier_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(supplier_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(s.code) LIKE ? OR 
                        LOWER(s.id_number) LIKE ? OR 
                        LOWER(s.first_name) LIKE ? OR 
                        LOWER(s.last_name) LIKE ? OR 
                        LOWER(s.address) LIKE ? OR 
                        LOWER(s.phone) LIKE ? OR 
                        LOWER(s.email) LIKE ? OR 
                        LOWER(s.tax_id) LIKE ? OR 
                        LOWER(s.company) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 9)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def search_inactive(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT s.*, st.name as status_name 
            FROM suppliers s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'inactive'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "s.id",
                    "Código": "s.code",
                    "Cédula": "s.id_number",
                    "Nombres": "s.first_name",
                    "Apellidos": "s.last_name",
                    "Empresa": "s.company",
                    "RIF": "s.tax_id",
                    "Teléfono": "s.phone"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            supplier_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(supplier_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(s.code) LIKE ? OR 
                        LOWER(s.id_number) LIKE ? OR 
                        LOWER(s.first_name) LIKE ? OR 
                        LOWER(s.last_name) LIKE ? OR 
                        LOWER(s.address) LIKE ? OR 
                        LOWER(s.phone) LIKE ? OR 
                        LOWER(s.email) LIKE ? OR 
                        LOWER(s.tax_id) LIKE ? OR 
                        LOWER(s.company) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 9)
        
        cursor.execute(base_query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name 
            FROM suppliers s
            JOIN status st ON s.status_id = st.id
            WHERE s.id = ?
        ''', (supplier_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(
        supplier_id: int,
        code: str,
        id_number: str,
        first_name: str,
        last_name: str,
        address: str,
        phone: str,
        email: str,
        tax_id: str,
        company: str
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers SET
                code = ?,
                id_number = ?,
                first_name = ?,
                last_name = ?,
                address = ?,
                phone = ?,
                email = ?,
                tax_id = ?,
                company = ?
            WHERE id = ?
        ''', (code, id_number, first_name, last_name, address, phone, email, tax_id, company, supplier_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(supplier_id: int, status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers SET
                status_id = ?
            WHERE id = ?
        ''', (status_id, supplier_id))
        conn.commit()
        conn.close()