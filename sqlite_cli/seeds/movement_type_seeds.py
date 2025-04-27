# seeds/movement_type_seeds.py
from models.movement_type_model import MovementType
from typing import List, Dict

def seed_movement_types() -> None:
    """Inserta los tipos de movimiento iniciales en la base de datos."""
    movement_types: List[Dict] = [
        {
            'name': 'Entrada inicial',
            'affects_quantity': True,
            'affects_stock': True,
            'description': 'Primer ingreso de productos al inventario'
        },
        {
            'name': 'Compra',
            'affects_quantity': True,
            'affects_stock': True,
            'description': 'Ingreso de productos por compra a proveedores'
        },
        {
            'name': 'Venta',
            'affects_quantity': True,
            'affects_stock': True,
            'description': 'Salida de productos por venta a clientes'
        },
        {
            'name': 'Ajuste positivo',
            'affects_quantity': True,
            'affects_stock': True,
            'description': 'Ajuste manual para corregir existencias (incremento)'
        },
        {
            'name': 'Ajuste negativo',
            'affects_quantity': True,
            'affects_stock': True,
            'description': 'Ajuste manual para corregir existencias (decremento)'
        },
        {
            'name': 'Reserva',
            'affects_quantity': False,
            'affects_stock': True,
            'description': 'Reserva de productos para futuras ventas'
        },
        {
            'name': 'Liberación de reserva',
            'affects_quantity': False,
            'affects_stock': True,
            'description': 'Liberación de productos previamente reservados'
        },
        {
            'name': 'Daño/Pérdida',
            'affects_quantity': True,
            'affects_stock': False,
            'description': 'Productos dañados o perdidos que no pueden venderse'
        }
    ]
    
    # Verificar si ya existen tipos de movimiento
    existing_types = MovementType.all()
    if len(existing_types) == 0:
        for movement_type in movement_types:
            MovementType.create(
                name=movement_type['name'],
                affects_quantity=movement_type['affects_quantity'],
                affects_stock=movement_type['affects_stock'],
                description=movement_type['description']
            )