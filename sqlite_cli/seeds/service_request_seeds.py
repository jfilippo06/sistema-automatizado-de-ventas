# seeds/service_request_seeds.py
from models.service_request_model import ServiceRequest
from models.request_status_model import RequestStatus

def seed_service_requests() -> None:
    # Obtener los IDs de los estados
    status_started = RequestStatus.get_by_name('started')['id']
    status_in_progress = RequestStatus.get_by_name('in_progress')['id']
    status_completed = RequestStatus.get_by_name('completed')['id']
    
    # First customer (John Doe) requests Web Development
    ServiceRequest.create(
        customer_id=1,
        service_id=1,
        description='Need a company website with 5 pages',
        quantity=1,
        request_status_id=status_in_progress
    )
    
    # Second customer (Jane Smith) requests Graphic Design
    ServiceRequest.create(
        customer_id=2,
        service_id=4,
        description='Need a new logo and brand identity',
        quantity=1,
        request_status_id=status_started
    )
    
    # Second customer (Jane Smith) requests Content Writing
    ServiceRequest.create(
        customer_id=2,
        service_id=5,
        description='Website content for 10 pages',
        quantity=10,
        request_status_id=status_completed
    )