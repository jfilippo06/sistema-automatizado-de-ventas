import tkinter as tk
from tkinter import ttk
from typing import Optional

class CustomCombobox(ttk.Combobox):
    def __init__(
        self,
        parent: tk.Widget,
        validate_type: Optional[str] = None,  # 'text', 'number', 'decimal'
        *args,
        **kwargs
    ):
        """
        Combobox personalizado con validación de entrada.
        
        Args:
            parent: Widget padre
            validate_type: Tipo de validación ('text', 'number', 'decimal')
            *args: Argumentos adicionales para ttk.Combobox
            **kwargs: Argumentos clave adicionales para ttk.Combobox
        """
        super().__init__(parent, *args, **kwargs)
        self.validate_type = validate_type
        self.configure(font=("Arial", 10))
        
        # Configurar validación según el tipo
        if validate_type:
            self.configure(validate="key")
            if validate_type == 'number':
                val_cmd = (self.register(self.validate_integer), '%P')
            elif validate_type == 'decimal':
                val_cmd = (self.register(self.validate_decimal), '%P')
            elif validate_type == 'text':
                val_cmd = (self.register(self.validate_text), '%P')
            
            self.configure(validatecommand=val_cmd)

    def validate_integer(self, text: str) -> bool:
        """Valida que el texto sea un entero válido."""
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False

    def validate_decimal(self, text: str) -> bool:
        """Valida que el texto sea un decimal válido."""
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

    def validate_text(self, text: str) -> bool:
        """Valida que el texto solo contenga letras y espacios."""
        if text == "":
            return True
        return all(c.isalpha() or c.isspace() for c in text)