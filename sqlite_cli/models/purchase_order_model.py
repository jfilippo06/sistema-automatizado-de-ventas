from sqlite_cli.models.supplier_model import Supplier
from typing import List, Dict, Optional
from datetime import datetime

class PurchaseOrder:
    @staticmethod
    def get_next_order_number() -> str:
        """Obtiene el próximo número de orden de compra"""
        # En una implementación real, esto consultaría la base de datos
        now = datetime.now()
        return f"OC-{now.year}{now.month:02d}{now.day:02d}-0001"

    @staticmethod
    def get_suppliers(search_term: str = "") -> List[Dict]:
        """Obtiene proveedores activos con opción de búsqueda"""
        return Supplier.search_active(search_term)

    @staticmethod
    def get_supplier_by_id(supplier_id: int) -> Optional[Dict]:
        """Obtiene un proveedor por su ID"""
        return Supplier.get_by_id(supplier_id)

    @staticmethod
    def create_order(
        order_number: str,
        supplier_id: int,
        delivery_date: str,
        products: List[Dict],
        subtotal: float,
        iva: float,
        total: float
    ) -> bool:
        """Crea una nueva orden de compra en la base de datos"""
        # Implementación temporal - debería guardar en la base de datos
        print(f"Orden creada: {order_number}")
        print(f"Proveedor ID: {supplier_id}")
        print(f"Fecha entrega: {delivery_date}")
        print(f"Productos: {products}")
        print(f"Subtotal: {subtotal}")
        print(f"IVA: {iva}")
        print(f"Total: {total}")
        return True