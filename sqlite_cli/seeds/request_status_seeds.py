# seeds/request_status_seeds.py
from models.request_status_model import RequestStatus

def seed_request_status() -> None:
    statuses = [
        {'name': 'started', 'description': 'Solicitud iniciada'},
        {'name': 'in_progress', 'description': 'Solicitud en progreso'},
        {'name': 'completed', 'description': 'Solicitud completada'}
    ]
    for status in statuses:
        RequestStatus.create(status['name'], status['description'])