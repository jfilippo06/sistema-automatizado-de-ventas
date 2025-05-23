# models/request_status_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class RequestStatus:
    @staticmethod
    def create(name: str, description: Optional[str] = None) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO request_status (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM request_status')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def get_by_id(status_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM request_status WHERE id = ?', (status_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM request_status WHERE name = ?', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def update(status_id: int, name: str, description: Optional[str] = None) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE request_status SET name = ?, description = ? WHERE id = ?',
            (name, description, status_id)
        )
        conn.commit()
        conn.close()