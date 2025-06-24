import re
from typing import Callable, Dict, Optional, Tuple
import tkinter as tk
from tkinter import messagebox

class FieldFormatter:
    @staticmethod
    def format_code(text: str) -> str:
        """Formatea el código: todo en mayúsculas, permite letras y números"""
        # Elimina caracteres no permitidos
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
        return cleaned.upper()

    @staticmethod
    def format_id_number(text: str) -> str:
        """Formatea la cédula: solo números y puntos"""
        # Elimina caracteres no permitidos
        cleaned = re.sub(r'[^0-9.]', '', text)
        
        # Validación adicional para puntos (solo permite un punto)
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = f"{parts[0]}.{''.join(parts[1:])}"
        
        return cleaned

    @staticmethod
    def format_name(text: str) -> str:
        """Formatea nombres: solo letras, cada palabra con primera mayúscula"""
        # Elimina números y caracteres especiales
        cleaned = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text)
        
        # Capitaliza cada palabra
        return ' '.join(word.capitalize() for word in cleaned.split(' '))

    @staticmethod
    def format_address(text: str) -> str:
        """Formatea dirección: alfanumérico, primera letra mayúscula"""
        # Elimina caracteres especiales no permitidos (permite espacios, comas, puntos)
        cleaned = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s,.-]', '', text)
        
        # Capitaliza la primera letra de cada palabra
        words = cleaned.split(' ')
        if words:
            words[0] = words[0].capitalize()
        return ' '.join(words)

    @staticmethod
    def format_phone(text: str) -> str:
        """Formatea teléfono: solo números"""
        return re.sub(r'[^0-9]', '', text)

    @staticmethod
    def format_email(text: str) -> str:
        """Formatea email: valida formato de email, todo en minúsculas"""
        cleaned = text.lower()
        # No aplicamos validación estricta aquí, solo formateo
        return cleaned

    @staticmethod
    def format_tax_id(text: str) -> str:
        """Formatea RIF: permite caracteres especiales y primera letra mayúscula"""
        # Solo capitaliza la primera letra si existe
        if len(text) > 0 and text[0].isalpha():
            return text[0].upper() + text[1:]
        return text

    @staticmethod
    def format_company(text: str) -> str:
        """Formatea empresa: permite caracteres especiales y primera letra mayúscula"""
        # Capitaliza la primera letra del texto (si existe)
        if len(text) > 0:
            return text[0].upper() + text[1:]
        return text

    @staticmethod
    def validate_and_format(widget: tk.Widget, field_type: str) -> None:
        """Valida y formatea el contenido de un widget según su tipo"""
        current_text = widget.get()
        
        # Mapeo de tipos de campo a funciones de formateo
        formatters = {
            'code': FieldFormatter.format_code,
            'id_number': FieldFormatter.format_id_number,
            'first_name': FieldFormatter.format_name,
            'last_name': FieldFormatter.format_name,
            'address': FieldFormatter.format_address,
            'phone': FieldFormatter.format_phone,
            'email': FieldFormatter.format_email,
            'tax_id': FieldFormatter.format_tax_id,
            'company': FieldFormatter.format_company
        }
        
        if field_type in formatters:
            # Aplicar el formateo correspondiente
            formatted_text = formatters[field_type](current_text)
            
            # Solo actualizar si hubo cambios para evitar problemas con el cursor
            if formatted_text != current_text:
                widget.delete(0, tk.END)
                widget.insert(0, formatted_text)

    @staticmethod
    def bind_validation(widget: tk.Widget, field_type: str) -> None:
        """Configura la validación para un widget específico"""
        widget.bind('<KeyRelease>', lambda e: FieldFormatter.validate_and_format(e.widget, field_type))
        widget.bind('<FocusOut>', lambda e: FieldFormatter.validate_and_format(e.widget, field_type))

    @staticmethod
    def validate_required_fields(entries: Dict[str, Tuple[tk.Widget, str]], parent: Optional[tk.Widget] = None) -> bool:
        """
        Valida que todos los campos requeridos estén completos.
        
        Args:
            entries: Diccionario de {nombre_campo: (widget, valor)}
            parent: Widget padre para mostrar mensajes
            
        Returns:
            bool: True si todos los campos son válidos, False de lo contrario
        """
        for field_name, (widget, value) in entries.items():
            if not value.strip():
                messagebox.showwarning(
                    "Campo requerido", 
                    f"El campo {field_name} es obligatorio", 
                    parent=parent
                )
                widget.focus_set()
                return False
        return True

    @staticmethod
    def validate_email_format(email: str, parent: Optional[tk.Widget] = None) -> bool:
        """Valida que el email tenga un formato válido"""
        if not email:  # Si está vacío, la validación de campo requerido ya lo capturará
            return True
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            messagebox.showerror(
                "Error", 
                "El formato del email no es válido", 
                parent=parent
            )
            return False
        return True