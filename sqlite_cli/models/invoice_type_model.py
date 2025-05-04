# models/invoice_type_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class InvoiceType:
    @staticmethod
    def create(name: str, description: str = None) -> None:
        """
        Crea un nuevo tipo de factura en la tabla `invoice_types`.
        
        :param name: Nombre del tipo (ej. 'Compra', 'Venta')
        :param description: Descripción del tipo (opcional)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO invoice_types (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """
        Obtiene todos los tipos de factura.
        
        :return: Lista de diccionarios con los tipos de factura
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoice_types')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """
        Obtiene un tipo de factura por su nombre.
        
        :param name: Nombre del tipo de factura
        :return: Diccionario con los datos del tipo o None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoice_types WHERE name = ?', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict]:
        """
        Obtiene un tipo de factura por su ID.
        
        :param id: ID del tipo de factura
        :return: Diccionario con los datos del tipo o None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoice_types WHERE id = ?', (id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None