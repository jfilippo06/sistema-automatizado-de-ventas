# models/person_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class Person:
    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        id_number: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None
    ) -> int:
        """Crea una nueva persona y devuelve su ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO person (
                first_name, last_name, id_number, address, phone, email, department, position
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, id_number, address, phone, email, department, position))
        person_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return person_id

    @staticmethod
    def update(
        person_id: int,
        first_name: str,
        last_name: str,
        id_number: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None
    ) -> None:
        """Actualiza los datos de una persona."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE person SET
                first_name = ?,
                last_name = ?,
                id_number = ?,
                address = ?,
                phone = ?,
                email = ?,
                department = ?,
                position = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (first_name, last_name, id_number, address, phone, email, department, position, person_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(person_id: int) -> Optional[Dict]:
        """Obtiene una persona por su ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM person WHERE id = ?', (person_id,))
        person = cursor.fetchone()
        conn.close()
        return dict(person) if person else None

    @staticmethod
    def search(search_term: str = "") -> List[Dict]:
        """Busca personas por término de búsqueda."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM person 
            WHERE LOWER(first_name || ' ' || last_name) LIKE ? 
            OR LOWER(id_number) LIKE ?
        ''', (f"%{search_term}%", f"%{search_term}%"))
        persons = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return persons