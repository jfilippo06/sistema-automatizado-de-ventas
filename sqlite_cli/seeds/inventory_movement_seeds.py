# seeds/inventory_movement_seeds.py
from models.inventory_movement_model import InventoryMovement
from models.inventory_model import InventoryItem
from models.user_model import User
from models.movement_type_model import MovementType
from typing import List, Dict
from datetime import datetime

def seed_initial_inventory_movements() -> None:
    """Registra los movimientos iniciales de inventario realizados por el admin."""
    # Asegurarse que existan los tipos de movimiento
    from seeds.movement_type_seeds import seed_movement_types
    seed_movement_types()
    
    # Obtener el usuario admin
    admin = User.get_by_username('admin')
    if not admin:
        from seeds.user_seeds import seed_users
        seed_users()
        admin = User.get_by_username('admin')
    
    # Obtener el tipo de movimiento "Entrada inicial"
    initial_entry_type = MovementType.get_by_name('Entrada inicial')
    
    # Obtener todos los items de inventario
    inventory_items = InventoryItem.all()
    
    # Registrar un movimiento por cada item
    for item in inventory_items:
        movement_data = {
            'inventory_id': item['id'],
            'movement_type_id': initial_entry_type['id'],
            'quantity_change': item['quantity'],
            'stock_change': item['stock'],
            'previous_quantity': 0,
            'new_quantity': item['quantity'],
            'previous_stock': 0,
            'new_stock': item['stock'],
            'reference_id': None,
            'reference_type': 'initial',
            'user_id': admin['id'],
            'notes': 'Ingreso inicial de inventario realizado por el administrador'
        }
        
        InventoryMovement.create(**movement_data)