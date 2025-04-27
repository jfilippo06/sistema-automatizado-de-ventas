from typing import Dict, Optional
import bcrypt

class SessionManager:
    _current_user = None

    @classmethod
    def login(cls, username: str, password: str) -> bool:
        """Autentica al usuario y establece la sesión si es exitoso."""
        from sqlite_cli.models.user_model import User
        user = User.get_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            cls._current_user = user
            return True
        return False

    @classmethod
    def logout(cls) -> None:
        """Cierra la sesión actual."""
        cls._current_user = None

    @classmethod
    def get_current_user(cls) -> Optional[Dict]:
        """Obtiene los datos del usuario actual."""
        return cls._current_user

    @classmethod
    def is_authenticated(cls) -> bool:
        """Verifica si hay un usuario autenticado."""
        return cls._current_user is not None

    @classmethod
    def get_user_id(cls) -> Optional[int]:
        """Obtiene el ID del usuario actual."""
        return cls._current_user['id'] if cls._current_user else None

    @classmethod
    def get_username(cls) -> Optional[str]:
        """Obtiene el nombre de usuario."""
        return cls._current_user['username'] if cls._current_user else None

    @classmethod
    def get_role(cls) -> Optional[str]:
        """Obtiene el rol del usuario."""
        return cls._current_user['role_name'] if cls._current_user else None