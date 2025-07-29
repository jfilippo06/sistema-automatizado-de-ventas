from sqlite_cli.database.database import get_db_connection
from typing import Dict, Optional, List
from utils.session_manager import SessionManager

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

    @classmethod
    def record_movement(
        cls,
        request_id: int,
        movement_type_name: str,
        previous_employee_id: Optional[int] = None,
        new_employee_id: Optional[int] = None,
        previous_status_id: Optional[int] = None,
        new_status_id: Optional[int] = None,
        previous_request_status_id: Optional[int] = None,
        new_request_status_id: Optional[int] = None,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None,
        notes: Optional[str] = None
    ) -> None:
        """Registra un movimiento en el historial de solicitudes de servicio."""
        conn = None
        try:
            # Obtener el tipo de movimiento
            movement_type = cls.get_by_name(movement_type_name)
            if not movement_type:
                raise ValueError(f"Tipo de movimiento '{movement_type_name}' no encontrado")
            
            # Obtener el usuario actual
            user_id = SessionManager.get_user_id()
            if not user_id:
                raise ValueError("Usuario no autenticado")
            
            # Registrar el movimiento
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO service_request_movements (
                    request_id, movement_type_id, previous_employee_id,
                    new_employee_id, previous_status_id, new_status_id,
                    previous_request_status_id, new_request_status_id,
                    reference_id, reference_type, user_id, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    request_id, movement_type['id'], previous_employee_id,
                    new_employee_id, previous_status_id, new_status_id,
                    previous_request_status_id, new_request_status_id,
                    reference_id, reference_type, user_id, notes
                )
            )
            conn.commit()
            
        except Exception as e:
            raise Exception(f"Error al registrar movimiento: {str(e)}")
        finally:
            if conn:
                conn.close()