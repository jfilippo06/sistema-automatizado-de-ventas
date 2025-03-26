# seeds/status_seeds.py
from models.status_model import Status

def seed_status() -> None:
    """
    Inserta datos iniciales en la tabla `status`.
    """
    statuses = [
        {'name': 'active', 'description': 'Registro activo y visible'},
        {'name': 'inactive', 'description': 'Registro inactivo (borrado lógico)'}
    ]
    for status in statuses:
        Status.create(status['name'], status['description'])