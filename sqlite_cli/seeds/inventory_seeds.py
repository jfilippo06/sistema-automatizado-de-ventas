from models.inventory_model import InventoryItem
from typing import List, Dict
from datetime import datetime, timedelta

def seed_inventory() -> None:
    """
    Inserta datos iniciales en la tabla `inventory` con los nuevos campos.
    """
    # Fechas de vencimiento (1-2 años en el futuro)
    expiration_date1 = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    expiration_date2 = (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d')
    
    items: List[Dict] = [
        {
            'code': 'PROD001',
            'product': 'Laptop HP 15',
            'quantity': 50,
            'min_stock': 10,
            'max_stock': 100,
            'price': 1200.00,
            'supplier_id': 1,
            'expiration_date': expiration_date2,
            'image_path': None  # Imagen vacía
        },
        {
            'code': 'PROD002',
            'product': 'Teclado inalámbrico',
            'quantity': 100,
            'min_stock': 20,
            'max_stock': 150,
            'price': 45.50,
            'supplier_id': None,
            'expiration_date': expiration_date1,
            'image_path': None  # Imagen vacía
        },
        {
            'code': 'PROD003',
            'product': 'Mouse gaming',
            'quantity': 75,
            'min_stock': 15,
            'max_stock': 100,
            'price': 35.75,
            'supplier_id': 2,
            'expiration_date': expiration_date1,
            'image_path': None  # Imagen vacía
        },
        {
            'code': 'PROD004',
            'product': 'Monitor 24"',
            'quantity': 30,
            'min_stock': 5,
            'max_stock': 50,
            'price': 250.00,
            'supplier_id': 1,
            'expiration_date': expiration_date2,
            'image_path': None  # Imagen vacía
        },
        {
            'code': 'PROD005',
            'product': 'Disco SSD 500GB',
            'quantity': 60,
            'min_stock': 10,
            'max_stock': 80,
            'price': 89.99,
            'supplier_id': 3,
            'expiration_date': None,  # Sin fecha de vencimiento
            'image_path': None  # Imagen vacía
        }
    ]
    
    for item in items:
        InventoryItem.create(**item)