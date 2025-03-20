import tkinter as tk
from widgets.custom_label import CustomLabel  # Importar el widget personalizado de label

class HomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Guardar referencia a la ventana principal
        
        # Configurar la ventana para esta pantalla
        self.configure_window()
        
        # Configurar la interfaz de usuario
        self.configure_ui()

    def configure_window(self):
        """
        Configura el tamaño y el comportamiento de redimensionamiento para esta pantalla.
        """
        self.parent.geometry("800x600")  # Tamaño específico para la pantalla de inicio
        self.parent.resizable(True, True)  # Redimensionable

    def configure_ui(self):
        # Añadir un título con CustomLabel
        title = CustomLabel(self, text="Bienvenido a Home", font=("Arial", 24))
        title.pack(pady=100)  # Colocar el título en una posición específica