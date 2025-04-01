# models/customer_model.py
from database.database import get_db_connection
from typing import List, Dict, Optional

class Customer:
    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        id_number: str,
        email: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO customers 
            (first_name, last_name, id_number, email, address, phone, status_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (first_name, last_name, id_number, email, address, phone, status_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update(
        customer_id: int,
        first_name: str,
        last_name: str,
        id_number: str,
        email: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE customers SET
            first_name = ?,
            last_name = ?,
            id_number = ?,
            email = ?,
            address = ?,
            phone = ?,
            status_id = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (first_name, last_name, id_number, email, address, phone, status_id, customer_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(customer_id: int, status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE customers SET status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status_id, customer_id)
        )
        conn.commit()
        conn.close()