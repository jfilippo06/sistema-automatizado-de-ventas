import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_text import CustomText
from typing import Any, Callable

class LoginScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_home_screen_callback: Callable[[], None]) -> None:
        """
        Pantalla de inicio de sesión del sistema.
        
        Args:
            parent: Widget padre contenedor
            open_home_screen_callback: Función para abrir la pantalla principal
        """
        super().__init__(parent)
        self.parent = parent
        self.open_home_screen_callback = open_home_screen_callback
        
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """Configura la ventana al mostrar esta pantalla."""
        self.parent.geometry("600x500")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        """Configura todos los elementos de la interfaz."""
        # Frame principal para centrar contenido
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        title = CustomLabel(
            main_frame,
            text="Inicio de Sesión",
            font=("Arial", 24, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Campo de usuario
        user_label = CustomLabel(
            main_frame,
            text="Usuario:",
            font=("Arial", 12),
            fg="#555",
            bg="#f0f0f0"
        )
        user_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.user_entry = CustomText(
            main_frame,
            height=1,
            width=25,
            font=("Arial", 12)
        )
        self.user_entry.grid(row=1, column=1, pady=5, padx=10)

        # Campo de contraseña (versión con CustomText)
        password_label = CustomLabel(
            main_frame,
            text="Contraseña:",
            font=("Arial", 12),
            fg="#555",
            bg="#f0f0f0"
        )
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.password_entry = CustomText(
            main_frame,
            height=1,
            width=25,
            font=("Arial", 12),
            password_char="*"  # Nuevo parámetro para caracteres de contraseña
        )
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        # Botón de login
        login_btn = CustomButton(
            main_frame,
            text="Iniciar Sesión",
            command=self.authenticate,
            padding=10,
            width=15
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def authenticate(self) -> None:
        """Valida las credenciales y abre la pantalla principal."""
        self.open_home_screen_callback()