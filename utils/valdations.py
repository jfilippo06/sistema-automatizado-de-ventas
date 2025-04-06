import tkinter as tk
from typing import Callable, Dict

class Validations:
    @staticmethod
    def validate_entry(event: tk.Event, validation_func: Callable[[str], bool]) -> None:
        """Valida la entrada de un widget según la función de validación proporcionada."""
        widget = event.widget
        current_text = widget.get()
        
        if not validation_func(current_text):
            widget.delete(0, tk.END)
            widget.insert(0, current_text[:-1])

    @staticmethod
    def validate_text(text: str) -> bool:
        """Valida que el texto solo contenga letras, números y espacios."""
        return all(c.isalpha() or c.isspace() or c.isdigit() for c in text) if text else True

    @staticmethod
    def validate_integer(text: str) -> bool:
        """Valida que el texto sea un entero válido."""
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_decimal(text: str) -> bool:
        """Valida que el texto sea un decimal válido."""
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_required_fields(entries: Dict[str, tk.Widget], fields: Dict[str, str], parent: tk.Widget) -> bool:
        """
        Valida que todos los campos requeridos estén completos.
        
        Args:
            entries: Diccionario de widgets de entrada
            fields: Diccionario de {nombre_campo: valor}
            parent: Widget padre para mostrar mensajes
            
        Returns:
            bool: True si todos los campos son válidos, False de lo contrario
        """
        for field_name, value in fields.items():
            if not value:
                tk.messagebox.showwarning(
                    "Campo requerido", 
                    f"El campo {field_name} es obligatorio", 
                    parent=parent
                )
                entries[field_name].focus_set()
                return False
        return True

    @staticmethod
    def validate_numeric_fields(fields: Dict[str, tuple], parent: tk.Widget) -> bool:
        """
        Valida que los valores numéricos sean válidos.
        
        Args:
            fields: Diccionario de {nombre_campo: (valor, es_decimal)}
            parent: Widget padre para mostrar mensajes
            
        Returns:
            bool: True si todos los valores son válidos, False de lo contrario
        """
        for field_name, (value, is_float) in fields.items():
            try:
                float(value) if is_float else int(value)
            except ValueError:
                tk.messagebox.showerror(
                    "Error", 
                    f"El campo {field_name} debe ser un número válido", 
                    parent=parent
                )
                return False
        return True