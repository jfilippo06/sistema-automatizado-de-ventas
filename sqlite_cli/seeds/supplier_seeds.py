# seeds/supplier_seeds.py
from models.supplier_model import Supplier

def seed_suppliers() -> None:
    """
    Inserta datos iniciales en la tabla `suppliers`.
    """
    suppliers = [
        {
            'code': 'PROV001',
            'id_number': '12345678',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'address': 'Av. Principal 123',
            'phone': '04121234567',
            'email': 'juan@proveedor.com',
            'tax_id': 'J-12345678-9',
            'company': 'Distribuidora Pérez'
        },
        {
            'code': 'PROV002',
            'id_number': '87654321',
            'first_name': 'María',
            'last_name': 'Gómez',
            'address': 'Calle Secundaria 456',
            'phone': '04241234567',
            'email': 'maria@gomez.com',
            'tax_id': 'M-87654321-0',
            'company': 'Alimentos Gómez'
        }
    ]
    for supplier in suppliers:
        Supplier.create(**supplier)