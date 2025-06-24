import re
from typing import Callable, Dict, Optional, Tuple
import tkinter as tk
from tkinter import messagebox

class FieldFormatter:
    @staticmethod
    def format_code(text: str) -> str:
        """Formatea el código: todo en mayúsculas, permite letras y números"""
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
        return cleaned.upper()

    @staticmethod
    def format_id_number(text: str) -> str:
        """Formatea la cédula: solo números y puntos"""
        cleaned = re.sub(r'[^0-9.]', '', text)
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = f"{parts[0]}.{''.join(parts[1:])}"
        return cleaned

    @staticmethod
    def format_name(text: str) -> str:
        """Formatea nombres: solo letras, cada palabra con primera mayúscula"""
        cleaned = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text)
        return ' '.join(word.capitalize() for word in cleaned.split(' '))

    @staticmethod
    def format_first_name(text: str) -> str:
        """Formatea dirección: alfanumérico, primera letra mayúscula"""
        cleaned = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s,.-]', '', text)
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
        """Formatea email: todo en minúsculas"""
        return text.lower()

    @staticmethod
    def format_tax_id(text: str) -> str:
        """Formatea RIF: permite caracteres especiales y primera letra mayúscula"""
        if text and text[0].isalpha():
            return text[0].upper() + text[1:]
        return text

    @staticmethod
    def format_company(text: str) -> str:
        """Formatea empresa: permite caracteres especiales y primera letra mayúscula"""
        if text:
            return text[0].upper() + text[1:]
        return text

    @staticmethod
    def format_integer(text: str) -> str:
        """Formatea números enteros: solo dígitos"""
        return re.sub(r'[^0-9]', '', text)

    @staticmethod
    def format_decimal(text: str) -> str:
        """Formatea números decimales: dígitos y un punto decimal"""
        cleaned = re.sub(r'[^0-9.]', '', text)
        parts = cleaned.split('.')
        if len(parts) > 1:
            cleaned = f"{parts[0]}.{''.join(parts[1:])}"
        return cleaned

    @staticmethod
    def format_date(text: str) -> str:
        """Formatea fecha: YYYY/MM/DD, autoinserta barras"""
        cleaned = re.sub(r'[^0-9]', '', text)
        formatted = []
        for i, char in enumerate(cleaned):
            if i in (4, 6):  # Inserta barras después del año (4) y mes (6)
                formatted.append('/')
            if i < 8:  # Limita a 8 dígitos (YYYYMMDD)
                formatted.append(char)
        return ''.join(formatted)

    @staticmethod
    def validate_and_format(widget: tk.Widget, field_type: str) -> None:
        """Valida y formatea el contenido de un widget según su tipo"""
        current_text = widget.get()
        
        formatters = {
            'code': FieldFormatter.format_code,
            'id_number': FieldFormatter.format_id_number,
            'name': FieldFormatter.format_name,
            'first_name': FieldFormatter.format_name,
            'last_name': FieldFormatter.format_name,
            'address': FieldFormatter.format_first_name,
            'description': FieldFormatter.format_first_name,
            'phone': FieldFormatter.format_phone,
            'email': FieldFormatter.format_email,
            'tax_id': FieldFormatter.format_tax_id,
            'company': FieldFormatter.format_company,
            'integer': FieldFormatter.format_integer,
            'decimal': FieldFormatter.format_decimal,
            'date': FieldFormatter.format_date
        }
        
        if field_type in formatters:
            formatted_text = formatters[field_type](current_text)
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
        """Valida que todos los campos requeridos estén completos"""
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
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            messagebox.showerror("Error", "El formato del email no es válido", parent=parent)
            return False
        return True