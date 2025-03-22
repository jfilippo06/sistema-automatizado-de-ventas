from models.inventory_model import InventoryItem
from typing import List, Dict, Any

def seed_inventory() -> None:
    """
    Inserta datos iniciales en la tabla `inventory`.
    """
    items: List[Dict[str, Any]] = [
        {'name': 'Producto 1', 'quantity': 10, 'price': 100.50},
        {'name': 'Producto 2', 'quantity': 5, 'price': 200.75},
        {'name': 'Producto 3', 'quantity': 20, 'price': 50.00},
        {'name': 'Producto 4', 'quantity': 15, 'price': 300.25},
    ]
    for item in items:
        InventoryItem.create(item['name'], item['quantity'], item['price'])