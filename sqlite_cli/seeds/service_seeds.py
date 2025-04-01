# seeds/service_seeds.py
from models.service_model import Service

def seed_services() -> None:
    services = [
        {'name': 'Web Development', 'price': 1000.00, 'description': 'Custom website development'},
        {'name': 'Mobile App Development', 'price': 1500.00, 'description': 'iOS/Android app development'},
        {'name': 'SEO Optimization', 'price': 500.00, 'description': 'Search engine optimization'},
        {'name': 'Graphic Design', 'price': 300.00, 'description': 'Logo and branding design'},
        {'name': 'Content Writing', 'price': 200.00, 'description': 'Professional content creation'},
        {'name': 'IT Consulting', 'price': 250.00, 'description': 'Hourly IT consulting services'}
    ]
    
    for service in services:
        Service.create(
            name=service['name'],
            price=service['price'],
            description=service['description']
        )