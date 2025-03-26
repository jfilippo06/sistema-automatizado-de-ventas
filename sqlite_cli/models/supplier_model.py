# models/supplier_model.py
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
        company: Optional[str] = None
    ) -> None:
        """
        Crea un nuevo proveedor en la tabla `suppliers`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO suppliers (
                code, id_number, first_name, last_name, 
                address, phone, email, tax_id, company
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, id_number, first_name, last_name, address, phone, email, tax_id, company))
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los proveedores de la tabla `suppliers`.
        
        :return: Lista de diccionarios con los proveedores
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM suppliers')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items