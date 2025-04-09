# models/user_model.py
from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional
import bcrypt

class User:
    @staticmethod
    def create(
        username: str,
        password: str,
        person_id: int,
        role_id: int,
        status_id: int = 1
    ) -> None:
        """Crea un nuevo usuario en la base de datos."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (
                username, password, person_id, status_id, role_id
            ) VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_password.decode('utf-8'), person_id, status_id, role_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all() -> List[Dict]:
        """Obtiene todos los usuarios activos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.*, p.first_name, p.last_name, p.email, r.name as role_name, s.name as status_name
            FROM users u
            JOIN person p ON u.person_id = p.id
            JOIN roles r ON u.role_id = r.id
            JOIN status s ON u.status_id = s.id
            WHERE s.name = 'active'
        ''')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users

    @staticmethod
    def search_active(search_term: str = "", field: Optional[str] = None) -> List[Dict]:
        """Busca usuarios activos con filtro opcional."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT u.*, p.first_name, p.last_name, p.email, r.name as role_name, s.name as status_name
            FROM users u
            JOIN person p ON u.person_id = p.id
            JOIN roles r ON u.role_id = r.id
            JOIN status s ON u.status_id = s.id
            WHERE s.name = 'active'
        '''
        
        params = []
        
        if search_term:
            if field:
                field_map = {
                    "ID": "u.id",
                    "Username": "u.username",
                    "Name": "p.first_name || ' ' || p.last_name",
                    "Email": "p.email",
                    "Role": "r.name"
                }
                field_name = field_map.get(field)
                if field_name:
                    if field == "ID":
                        try:
                            user_id = int(search_term)
                            base_query += f" AND {field_name} = ?"
                            params.append(user_id)
                        except ValueError:
                            base_query += " AND 1 = 0"
                    else:
                        base_query += f" AND LOWER({field_name}) LIKE ?"
                        params.append(f"%{search_term}%")
            else:
                base_query += '''
                    AND (LOWER(u.username) LIKE ? OR 
                        LOWER(p.first_name || ' ' || p.last_name) LIKE ? OR 
                        LOWER(p.email) LIKE ? OR
                        LOWER(r.name) LIKE ?)
                '''
                params.extend([f"%{search_term}%"] * 4)
        
        cursor.execute(base_query, params)
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por su ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.*, p.*, r.name as role_name
            FROM users u
            JOIN person p ON u.person_id = p.id
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = ?
        ''', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update(
        user_id: int,
        username: str,
        person_id: int,
        role_id: int,
        password: Optional[str] = None
    ) -> None:
        """Actualiza un usuario existente."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('''
                UPDATE users SET
                    username = ?,
                    password = ?,
                    person_id = ?,
                    role_id = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (username, hashed_password.decode('utf-8'), person_id, role_id, user_id))
        else:
            cursor.execute('''
                UPDATE users SET
                    username = ?,
                    person_id = ?,
                    role_id = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (username, person_id, role_id, user_id))
        
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(user_id: int, status_id: int) -> None:
        """Actualiza el estado de un usuario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET
                status_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status_id, user_id))
        conn.commit()
        conn.close()