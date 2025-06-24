# seeds/customer_seeds.py
from models.customer_model import Customer

def seed_customers() -> None:
    customers = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'id_number': '123456789',
            'email': 'john.doe@example.com',
            'address': '123 Main St, Springfield',
            'phone': '5551234'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'id_number': '987654321',
            'email': 'jane.smith@example.com',
            'address': '456 Oak Ave, Shelbyville',
            'phone': '5555678'
        },
        {
            'first_name': 'Robert',
            'last_name': 'Johnson',
            'id_number': '456123789',
            'email': 'robert.j@example.com',
            'address': '789 Pine Rd, Capital City',
            'phone': '5559012'
        }
    ]
    
    for customer in customers:
        Customer.create(
            first_name=customer['first_name'],
            last_name=customer['last_name'],
            id_number=customer['id_number'],
            email=customer['email'],
            address=customer['address'],
            phone=customer['phone']
        )