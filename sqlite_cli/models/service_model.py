# models/service_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Service:
    @staticmethod
    def create(
        name: str,
        price: float,
        description: Optional[str] = None,
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO services 
            (name, price, description, status_id)
            VALUES (?, ?, ?, ?)''',
            (name, price, description, status_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name 
            FROM services s
            JOIN status st ON s.status_id = st.id
        ''')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(service_id: int) -> Optional[Dict]:
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
    def get_by_name(name: str) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, st.name as status_name 
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE s.name = ?
        ''', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(
        service_id: int,
        name: str,
        price: float,
        description: Optional[str] = None,
        status_id: int = 1
    ) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE services SET
            name = ?,
            price = ?,
            description = ?,
            status_id = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?''',
            (name, price, description, status_id, service_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(service_id: int, status_id: int) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE services SET status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status_id, service_id)
        )
        conn.commit()
        conn.close()