import tkinter as tk
from tkinter import ttk

class HomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configurar la interfaz de usuario
        self.configure_ui()

    def configure_ui(self):
        # Añadir un título
        title = ttk.Label(self, text="Welcome to My App", font=("Arial", 24))
        title.pack(pady=20)