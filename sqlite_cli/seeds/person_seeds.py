# seeds/person_seeds.py
from database.database import get_db_connection
from models.person_model import Person
from typing import List, Dict

def seed_persons() -> None:
    """Inserts initial person data into the database."""
    persons: List[Dict] = [
        {
            'first_name': 'Admin',
            'last_name': 'User',
            'id_number': '11111111',
            'email': 'admin@example.com',
            'department': 'Management',
            'position': 'System Administrator'
        },
        {
            'first_name': 'Regular',
            'last_name': 'Employee',
            'id_number': '22222222',
            'email': 'employee@example.com',
            'department': 'Operations',
            'position': 'Service Technician'
        },
        {
            'first_name': 'System',
            'last_name': 'Client',
            'id_number': '33333333',
            'email': 'client@example.com',
            'address': '123 Main St',
            'phone': '555-1234'
        }
    ]
    
    # Check if persons already exist
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM person')
    if cursor.fetchone()[0] == 0:
        for person in persons:
            Person.create(
                first_name=person['first_name'],
                last_name=person['last_name'],
                id_number=person['id_number'],
                email=person['email'],
                address=person.get('address'),
                phone=person.get('phone'),
                department=person.get('department'),
                position=person.get('position')
            )
    conn.close()