# models/service_request_movement_type_model.py
from database.database import get_db_connection

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