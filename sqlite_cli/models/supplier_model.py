from database.database import get_db_connection
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
        status_id: Optional[int] = None
    ) -> None:
        """
        Crea un nuevo proveedor en la tabla `suppliers`.
        """
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
    def all() -> List[Dict]:
        """
        Obtiene todos los proveedores activos de la tabla `suppliers`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name 
            FROM suppliers s
            JOIN status st ON s.status_id = st.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Dict]:
        """
        Obtiene un proveedor por su ID.
        """
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
        """
        Actualiza un proveedor existente.
        """
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
        """
        Actualiza solo el estado de un proveedor.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers SET
                status_id = ?
            WHERE id = ?
        ''', (status_id, supplier_id))
        conn.commit()
        conn.close()