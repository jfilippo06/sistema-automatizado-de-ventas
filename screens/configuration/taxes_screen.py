import tkinter as tk
from tkinter import messagebox
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from sqlite_cli.models.tax_model import Tax
from sqlite_cli.models.status_model import Status
from typing import Any, Callable, Dict
from utils.valdations import Validations  # Importamos las validaciones

class TaxesManagementScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f0f0f0")
        self.tax_widgets = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("500x400")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Impuestos",
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)

        # Frame para botones
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_back = CustomButton(
            button_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Contenido principal
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Cargar impuestos desde la base de datos
        taxes = Tax.all()
        
        for tax in taxes:
            self.create_tax_widget(content_frame, tax)

    def create_tax_widget(self, parent: tk.Widget, tax: Dict) -> None:
        """Crea los widgets para un impuesto específico"""
        tax_frame = tk.Frame(parent, bg="#f0f0f0", bd=1, relief=tk.GROOVE)
        tax_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)

        # Subtítulo con nombre del impuesto
        subtitle = CustomLabel(
            tax_frame,
            text=f"{tax['name']}",
            font=("Arial", 12, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        subtitle.pack(anchor=tk.W, pady=(5, 10))

        # Frame para controles
        controls_frame = tk.Frame(tax_frame, bg="#f0f0f0")
        controls_frame.pack(fill=tk.X, padx=10)

        # Valor del impuesto
        value_label = CustomLabel(
            controls_frame,
            text="Valor:",
            font=("Arial", 10),
            fg="#333",
            bg="#f0f0f0"
        )
        value_label.pack(side=tk.LEFT, padx=(0, 5))

        value_var = tk.StringVar(value=str(tax['value']))
        value_entry = CustomEntry(
            controls_frame,
            textvariable=value_var,
            width=15,
            state="normal" if tax['status_name'] == 'active' else "disabled"
        )
        # Configuramos la validación para números decimales
        value_entry.configure(validate="key")
        value_entry.configure(validatecommand=(
            value_entry.register(Validations.validate_decimal),
            '%P'
        ))
        value_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Frame para botones
        buttons_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        buttons_frame.pack(side=tk.RIGHT)

        # Botón de actualizar
        btn_update = CustomButton(
            buttons_frame,
            text="Actualizar",
            command=lambda: self.update_tax_value(tax['name'], value_var.get(), tax['status_name'] == 'active'),
            padding=5,
            width=10
        )
        # Configurar estado inicial del botón
        if tax['status_name'] != 'active':
            btn_update.disable()
        btn_update.pack(side=tk.LEFT, padx=5)

        # Botón de activar/desactivar
        btn_toggle = CustomButton(
            buttons_frame,
            text="Desactivar" if tax['status_name'] == 'active' else "Activar",
            command=lambda: self.toggle_tax_status(tax['name'], tax['status_name'] != 'active'),
            padding=5,
            width=10
        )
        btn_toggle.pack(side=tk.LEFT, padx=5)

        # Guardar referencias para actualización
        self.tax_widgets[tax['name']] = {
            'value_var': value_var,
            'value_entry': value_entry,
            'btn_update': btn_update,
            'btn_toggle': btn_toggle,
            'is_active': tax['status_name'] == 'active'
        }

    def update_tax_value(self, tax_name: str, new_value: str, is_active: bool) -> None:
        """Actualiza el valor de un impuesto"""
        # Protección adicional - aunque el botón debería estar deshabilitado
        if not is_active:
            return  # Simplemente salir sin hacer nada
            
        try:
            value = float(new_value)
            if value < 0:
                raise ValueError("El valor no puede ser negativo")
            
            Tax.update_value(tax_name, value)
            messagebox.showinfo("Éxito", f"Valor de {tax_name} actualizado correctamente", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {str(e)}", parent=self)

    def toggle_tax_status(self, tax_name: str, activate: bool) -> None:
        """Activa o desactiva un impuesto"""
        status = Status.all()
        status_id = next((s['id'] for s in status if s['name'] == ('active' if activate else 'inactive')), None)
        
        if status_id:
            Tax.update_status(tax_name, status_id)
            
            # Actualizar estado de los widgets
            widgets = self.tax_widgets.get(tax_name)
            if widgets:
                widgets['is_active'] = activate
                widgets['value_entry'].config(state="normal" if activate else "disabled")
                
                # Actualizar botón de actualizar
                if activate:
                    widgets['btn_update'].enable()
                    widgets['btn_update'].command = lambda: self.update_tax_value(
                        tax_name, 
                        widgets['value_var'].get(), 
                        activate
                    )
                else:
                    widgets['btn_update'].disable()
                    # Eliminar cualquier comando pendiente
                    widgets['btn_update'].command = None
                
                # Actualizar botón de toggle
                widgets['btn_toggle'].label.configure(
                    text="Desactivar" if activate else "Activar"
                )
                widgets['btn_toggle'].command = lambda: self.toggle_tax_status(
                    tax_name, not activate
                )
            
            messagebox.showinfo(
                "Éxito", 
                f"Impuesto {tax_name} {'activado' if activate else 'desactivado'} correctamente",
                parent=self
            )
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado del impuesto", parent=self)

    def go_back(self) -> None:
        self.open_previous_screen_callback()