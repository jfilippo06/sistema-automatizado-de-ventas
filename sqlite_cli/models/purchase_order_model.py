from sqlite_cli.models.supplier_model import Supplier
from typing import List, Dict, Optional
from datetime import datetime

class PurchaseOrder:
    @staticmethod
    def get_next_order_number() -> str:
        """Get next purchase order number"""
        now = datetime.now()
        return f"OC-{now.year}{now.month:02d}{now.day:02d}-0001"

    @staticmethod
    def get_suppliers(search_term: str = "") -> List[Dict]:
        """Get active suppliers with optional search"""
        return Supplier.search_active(search_term)

    @staticmethod
    def get_supplier_by_id(supplier_id: int) -> Optional[Dict]:
        """Get supplier by ID"""
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
        """Create a new purchase order in the database"""
        # Implementation should save to database
        print(f"Order created: {order_number}")
        print(f"Supplier ID: {supplier_id}")
        print(f"Delivery date: {delivery_date}")
        print(f"Products: {products}")
        print(f"Subtotal: {subtotal}")
        print(f"IVA: {iva}")
        print(f"Total: {total}")
        return True