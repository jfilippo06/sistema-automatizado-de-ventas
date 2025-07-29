# models/service_request_movement_type_model.py
from sqlite_cli.database.database import get_db_connection
from typing import Dict, Optional

class ServiceRequestMovementType:
    @classmethod
    def create(cls, name: str, description: str = None) -> None:
        """Crea un nuevo tipo de movimiento para solicitudes de servicio."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO service_request_movement_types (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        conn.close()

    @classmethod
    def all(cls) -> list:
        """Obtiene todos los tipos de movimiento de solicitudes de servicio."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service_request_movement_types")
        types = cursor.fetchall()
        conn.close()
        return types

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Dict]:
        """Obtiene un tipo de movimiento por su nombre."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM service_request_movement_types WHERE name = ? LIMIT 1",
            (name,)
        )
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None