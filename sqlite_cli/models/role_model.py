# models/role_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Role:
    @staticmethod
    def create(name: str, description: Optional[str] = None) -> None:
        """Creates a new role in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO roles (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """Gets all roles from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles')
        roles = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return roles

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Dict]:
        """Gets a role by its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
        role = cursor.fetchone()
        conn.close()
        return dict(role) if role else None

    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        """Gets a role by its name."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles WHERE name = ?', (name,))
        role = cursor.fetchone()
        conn.close()
        return dict(role) if role else None