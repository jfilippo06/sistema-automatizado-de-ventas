import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Frame):
    def __init__(self, parent, text, command=None, width=None, padding=None, wraplength=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Guardar la función de comando
        self.command = command
        
        # Configurar el estilo del botón
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=padding if padding is not None else 5)
        
        # Crear un Label para el texto del botón
        self.label = ttk.Label(
            self,
            text=text,
            style="Custom.TButton",
            wraplength=wraplength,  # Dividir el texto si supera este ancho
            width=width if width is not None else 15,  # Ancho del botón
            anchor="center",  # Centrar el texto horizontalmente
            justify="center",  # Centrar el texto verticalmente
            padding=5
        )
        self.label.pack(fill=tk.BOTH, expand=True)  # Expandir el Label dentro del Frame
        
        # Configurar eventos de clic
        self.label.bind("<Button-1>", self.on_click)
        self.bind("<Button-1>", self.on_click)
        
        # Configurar el estilo para simular un botón
        self.configure(relief=tk.RAISED)  # Borde elevado como un botón
        self.label.configure(background="lightgray")  # Fondo del botón

    def on_click(self, event):
        """
        Método para manejar el evento de clic.
        """
        if self.command:
            self.command()

    def disable(self):
        """
        Método para deshabilitar el botón.
        """
        self.label.state(["disabled"])
        self.configure(relief=tk.SUNKEN)  # Cambiar el borde para indicar deshabilitado

    def enable(self):
        """
        Método para habilitar el botón.
        """
        self.label.state(["!disabled"])
        self.configure(relief=tk.RAISED)  # Restaurar el borde elevado