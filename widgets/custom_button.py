import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Button):
    def __init__(self, parent, text, command=None, *args, **kwargs):
        super().__init__(parent, text=text, command=command, *args, **kwargs)
        
        # Configurar propiedades por defecto
        self.configure(
            style="Custom.TButton",  # Estilo personalizado
            width=15                # Ancho del botón
        )

    def disable(self):
        """
        Método para deshabilitar el botón.
        """
        self.configure(state=tk.DISABLED)

    def enable(self):
        """
        Método para habilitar el botón.
        """
        self.configure(state=tk.NORMAL)