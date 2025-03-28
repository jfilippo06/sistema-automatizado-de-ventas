# seeds/supplier_seeds.py
from models.supplier_model import Supplier
from typing import List, Dict

def seed_suppliers() -> None:
    """
    Inserta datos iniciales en la tabla `suppliers`.
    Asume que:
    - status_id 1 = active
    - status_id 2 = inactive
    """
    suppliers: List[Dict] = [
        {
            'code': 'PROV001',
            'id_number': '12345678',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'address': 'Av. Principal 123',
            'phone': '04121234567',
            'email': 'juan@proveedor.com',
            'tax_id': 'J-12345678-9',
            'company': 'Distribuidora Pérez',
            'status_id': 1  # active
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
            'company': 'Alimentos Gómez',
            'status_id': 1  # active
        }
    ]
    
    for supplier in suppliers:
        # Verificación opcional para evitar duplicados
        Supplier.create(**supplier)