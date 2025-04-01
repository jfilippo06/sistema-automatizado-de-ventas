# models/request_status_model.py
from database.database import get_db_connection
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
    def get_by_name(name: str) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM request_status WHERE name = ?', (name,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None