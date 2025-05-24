from models.purchase_order_status_model import PurchaseOrderStatus

def seed_purchase_order_statuses():
    """Semilla de datos iniciales para estados de orden de compra"""
    statuses = [
        {"name": "draft", "description": "Orden en borrador, no enviada"},
        {"name": "sent", "description": "Orden enviada al proveedor"},
        {"name": "partial", "description": "Entrega parcial recibida"},
        {"name": "received", "description": "Completamente recibida"},
        {"name": "cancelled", "description": "Orden cancelada"},
        {"name": "approved", "description": "Orden aprobada para procesar"},
        {"name": "rejected", "description": "Orden rechazada"}
    ]

    existing_statuses = PurchaseOrderStatus.all()
    existing_names = [s['name'] for s in existing_statuses]

    for status in statuses:
        if status['name'] not in existing_names:
            PurchaseOrderStatus.create(
                name=status['name'],
                description=status['description']
            )

if __name__ == "__main__":
    seed_purchase_order_statuses()