from models.service_model import Service

def seed_services() -> None:
    services = [
        {'code': 'WEB001', 'name': 'Web Development', 'price': 1000.00, 'description': 'Custom website development'},
        {'code': 'MOB001', 'name': 'Mobile App Development', 'price': 1500.00, 'description': 'iOS/Android app development'},
        {'code': 'SEO001', 'name': 'SEO Optimization', 'price': 500.00, 'description': 'Search engine optimization'},
        {'code': 'DES001', 'name': 'Graphic Design', 'price': 300.00, 'description': 'Logo and branding design'},
        {'code': 'CON001', 'name': 'Content Writing', 'price': 200.00, 'description': 'Professional content creation'},
        {'code': 'CON002', 'name': 'IT Consulting', 'price': 250.00, 'description': 'Hourly IT consulting services'}
    ]
    
    for service in services:
        Service.create(
            code=service['code'],
            name=service['name'],
            price=service['price'],
            description=service['description']
        )