import tkinter as tk
from tkinter import ttk
from datetime import datetime

class CustomDatePicker(ttk.Frame):
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        """
        Componente personalizado para selección de fechas con calendario desplegable.
        
        Args:
            parent: Widget padre
            *args: Argumentos adicionales para ttk.Frame
            **kwargs: Argumentos clave adicionales para ttk.Frame
        """
        super().__init__(parent, *args, **kwargs)
        
        self.date_var = tk.StringVar()
        
        self.entry = ttk.Entry(
            self,
            textvariable=self.date_var,
            width=12,
            font=("Arial", 10),
            justify=tk.CENTER
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_calendar = ttk.Button(
            self,
            text="📅",
            width=3,
            command=self.show_calendar
        )
        self.btn_calendar.pack(side=tk.LEFT)
        
        # Configurar validación de fecha
        self.entry.configure(validate="key")
        self.entry.configure(validatecommand=(
            self.register(self.validate_date_format),
            '%P'
        ))
    
    def validate_date_format(self, text: str) -> bool:
        """Valida que el texto tenga formato de fecha DD/MM/AAAA"""
        if text == "":
            return True
        parts = text.split('/')
        if len(parts) != 3:
            return False
        try:
            day, month, year = map(int, parts)
            if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100:
                return True
            return False
        except ValueError:
            return False
    
    def show_calendar(self):
        """Muestra el calendario para selección de fecha"""
        # Implementación básica - puedes mejorarla con un calendario real
        today = datetime.now().strftime("%d/%m/%Y")
        self.date_var.set(today)
    
    def get_date(self) -> str:
        """Obtiene la fecha en formato DD/MM/AAAA"""
        return self.date_var.get()
    
    def set_date(self, date_str: str):
        """Establece la fecha en formato DD/MM/AAAA"""
        self.date_var.set(date_str)
