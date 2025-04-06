from models.supplier_model import Supplier
from typing import List, Dict

def seed_suppliers() -> None:
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
        },
        {
            'code': 'PROV003',
            'id_number': '11111111',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'address': 'Av. Comercial 789',
            'phone': '04161111111',
            'email': 'carlos@inactivo.com',
            'tax_id': 'C-11111111-1',
            'company': 'Servicios Inactivos',
            'status_id': 2  # inactive
        },
        {
            'code': 'PROV004',
            'id_number': '22222222',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'address': 'Calle Vieja 101',
            'phone': '04162222222',
            'email': 'ana@antigua.com',
            'tax_id': 'A-22222222-2',
            'company': 'Empresa Antigua',
            'status_id': 2  # inactive
        }
    ]
    
    for supplier in suppliers:
        Supplier.create(**supplier)