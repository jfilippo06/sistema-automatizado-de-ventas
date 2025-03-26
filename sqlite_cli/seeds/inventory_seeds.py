# seeds/inventory_seeds.py
from models.inventory_model import InventoryItem
from typing import List, Dict

def seed_inventory() -> None:
    """
    Inserta datos iniciales en la tabla `inventory`.
    """
    items: List[Dict] = [
        {
            'code': 'PROD001',
            'product': 'Laptop HP 15',
            'quantity': 50,
            'stock': 50,
            'price': 1200.00,
            'status_id': 1,  # active
            'supplier_id': 1
        },
        {
            'code': 'PROD002',
            'product': 'Teclado inalámbrico',
            'quantity': 100,
            'stock': 80,
            'price': 45.50,
            'status_id': 1,  # active
            'supplier_id': None
        },
        {
            'code': 'PROD003',
            'product': 'Mouse gaming',
            'quantity': 75,
            'stock': 20,
            'price': 35.75,
            'status_id': 1,  # active
            'supplier_id': 2
        },
        {
            'code': 'PROD004',
            'product': 'Monitor 24"',
            'quantity': 30,
            'stock': 5,
            'price': 250.00,
            'status_id': 2,  # inactive
            'supplier_id': 1
        }
    ]
    for item in items:
        InventoryItem.create(**item)