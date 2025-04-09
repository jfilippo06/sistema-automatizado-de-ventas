# seeds/user_seeds.py (updated)
from models.user_model import User
from models.person_model import Person
from models.status_model import Status
from models.role_model import Role
from typing import List, Dict

from seeds.person_seeds import seed_persons
from seeds.role_seeds import seed_roles

def seed_users() -> None:
    """Inserts initial user data for each role."""
    
    # Ensure roles exist
    seed_roles()
    
    # Get roles
    roles = Role.all()
    role_ids = {role['name']: role['id'] for role in roles}
    
    # Get persons
    persons = Person.search("")
    if not persons:
        seed_persons()
        persons = Person.search("")
    
    users_data: List[Dict] = [
        {
            'username': 'admin',
            'password': 'admin',
            'person_id': next(p['id'] for p in persons if p['id_number'] == '11111111'),
            'role_id': role_ids['admin']
        },
        {
            'username': 'employee',
            'password': 'employee',
            'person_id': next(p['id'] for p in persons if p['id_number'] == '22222222'),
            'role_id': role_ids['employee']
        },
        {
            'username': 'client',
            'password': 'client',
            'person_id': next(p['id'] for p in persons if p['id_number'] == '33333333'),
            'role_id': role_ids['client']
        }
    ]
    
    # Check if users already exist
    existing_users = User.all()
    if len(existing_users) == 0:
        for user_data in users_data:
            User.create(
                username=user_data['username'],
                password=user_data['password'],
                person_id=user_data['person_id'],
                role_id=user_data['role_id']
            )