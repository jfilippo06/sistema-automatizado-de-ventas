import tkinter as tk
from widgets.custom_text import CustomText  # Importar el widget personalizado de texto
from widgets.custom_button import CustomButton  # Importar el widget personalizado de botón
from widgets.custom_label import CustomLabel  # Importar el widget personalizado de label
from typing import Any, Callable

class LoginScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_home_screen_callback: Callable[[], None]) -> None:
        """
        Inicializa la pantalla de login.

        :param parent: El widget padre al que pertenece esta pantalla.
        :param open_home_screen_callback: Función para abrir la pantalla de inicio.
        """
        super().__init__(parent)
        self.parent: tk.Widget = parent  # Guardar referencia a la ventana principal
        self.open_home_screen_callback: Callable[[], None] = open_home_screen_callback  # Callback para abrir HomeScreen
        
        # Configurar la interfaz de usuario
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """
        Configura la ventana principal cuando se muestra la pantalla de login.
        """
        self.parent.geometry("600x500")  # Tamaño específico para el login
        self.parent.resizable(False, False)  # No redimensionable
        super().pack(**kwargs)  # Mostrar la pantalla

    def configure_ui(self) -> None:
        """
        Configura la interfaz de usuario de la pantalla de login.
        """
        # Añadir un título con CustomLabel
        title: CustomLabel = CustomLabel(self, text="Iniciar sesión", font=("Arial", 24))
        title.place(x=220, y=80)  # Colocar el título en una posición específica

        # Añadir un label para el campo de usuario
        nameTitle: CustomLabel = CustomLabel(self, text="Usuario:", font=("Arial", 14))
        nameTitle.place(x=195, y=150)  # Posicionar el label de usuario

        # Añadir la caja de texto personalizada para el nombre de usuario
        self.nameText: CustomText = CustomText(self, height=1, width=25)  # Usar el widget personalizado
        self.nameText.place(x=195, y=180)  # Posicionar la caja de texto de usuario

        # Añadir un label para el campo de contraseña
        passwordTitle: CustomLabel = CustomLabel(self, text="Contraseña:", font=("Arial", 14))
        passwordTitle.place(x=195, y=220)  # Posicionar el label de contraseña

        # Añadir la caja de texto personalizada para la contraseña
        self.passwordText: CustomText = CustomText(self, height=1, width=25)  # Usar el widget personalizado
        self.passwordText.place(x=195, y=250)  # Posicionar la caja de texto de contraseña

        # Añadir un botón personalizado para iniciar sesión
        login_button: CustomButton = CustomButton(self, text="Iniciar sesión", command=self.open_home_screen)
        login_button.place(x=260, y=310)  # Posicionar el botón

    def open_home_screen(self) -> None:
        """
        Método para cerrar la pantalla de login y abrir la pantalla de inicio.
        """
        self.open_home_screen_callback()  # Llamar al callback para abrir HomeScreen