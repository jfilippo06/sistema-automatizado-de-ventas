# seeds/service_request_movement_type_seeds.py
from models.service_request_movement_type_model import ServiceRequestMovementType
from typing import List, Dict

def seed_service_request_movement_types() -> None:
    """Inserta los tipos de movimiento iniciales para solicitudes de servicio."""
    movement_types: List[Dict] = [
        {
            'name': 'ASIGNACION_EMPLEADO',
            'description': 'Cambio de empleado asignado a la solicitud'
        },
        {
            'name': 'CAMBIO_ESTADO',
            'description': 'Habilitación/Deshabilitación de la solicitud'
        },
        {
            'name': 'ACTUALIZACION_ESTADO',
            'description': 'Cambio en el estado de progreso de la solicitud'
        },
        {
            'name': 'CREACION',
            'description': 'Creación inicial de la solicitud de servicio'
        },
        {
            'name': 'CANCELACION',
            'description': 'Cancelación de la solicitud de servicio'
        }
    ]
    
    # Verificar si ya existen tipos de movimiento
    existing_types = ServiceRequestMovementType.all()
    if len(existing_types) == 0:
        for movement_type in movement_types:
            ServiceRequestMovementType.create(
                name=movement_type['name'],
                description=movement_type['description']
            )
        print("Tipos de movimiento para solicitudes de servicio creados exitosamente.")
    else:
        print("Los tipos de movimiento para solicitudes de servicio ya existen en la base de datos.")