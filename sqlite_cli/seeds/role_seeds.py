# seeds/role_seeds.py
from database.database import get_db_connection

def seed_roles() -> None:
    """Inserta datos iniciales en la tabla `roles`."""
    roles = [
        {'name': 'admin', 'description': 'Administrator with full access'},
        {'name': 'employee', 'description': 'Regular employee'},
        {'name': 'client', 'description': 'System client'}
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si la tabla ya tiene datos
    cursor.execute('SELECT COUNT(*) FROM roles')
    if cursor.fetchone()[0] == 0:
        for role in roles:
            cursor.execute(
                'INSERT INTO roles (name, description) VALUES (?, ?)',
                (role['name'], role['description'])
            )
    
    conn.commit()
    conn.close()