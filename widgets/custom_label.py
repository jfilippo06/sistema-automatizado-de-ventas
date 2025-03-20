import tkinter as tk
from tkinter import ttk

class CustomLabel(ttk.Label):
    def __init__(self, parent, text, font=("Arial", 12), fg="black", bg=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Configurar propiedades personalizadas
        self.configure(
            text=text,          # Texto del label
            font=font,          # Fuente y tamaño
            foreground=fg,      # Color del texto
            background=bg       # Color de fondo (opcional)
        )
        
        # Si se proporciona un color de fondo, configurar el estilo
        if bg:
            self.configure(style="CustomLabel.TLabel")
            self.configure_style(bg)

    def configure_style(self, bg):
        """
        Método para configurar el estilo del label si tiene un fondo personalizado.
        """
        style = ttk.Style()
        style.configure("CustomLabel.TLabel", background=bg)