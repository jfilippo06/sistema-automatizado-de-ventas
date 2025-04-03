# screens/customers/reports_screen.py
import tkinter as tk
from typing import Any

class CustomerReportsScreen(tk.Toplevel):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.title("Reportes de Clientes")
        self.geometry("600x400")
        
        label = tk.Label(self, text="Pantalla de Reportes de Clientes (en desarrollo)", font=("Arial", 14))
        label.pack(expand=True)
        
        btn_close = tk.Button(self, text="Cerrar", command=self.destroy)
        btn_close.pack(pady=20)