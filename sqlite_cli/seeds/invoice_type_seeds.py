from models.invoice_type_model import InvoiceType
from typing import List, Dict

def seed_invoice_types() -> None:
    """Inserta los tipos de factura iniciales en la base de datos."""
    invoice_types: List[Dict] = [
        {
            'name': 'Compra',
            'description': 'Factura de compra a proveedores'
        },
        {
            'name': 'Venta',
            'description': 'Factura de venta a clientes'
        }
    ]
    
    existing_types = InvoiceType.all()
    if len(existing_types) == 0:
        for invoice_type in invoice_types:
            InvoiceType.create(
                name=invoice_type['name'],
                description=invoice_type['description']
            )