import tkinter as tk
from tkinter import messagebox
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from sqlite_cli.models.currency_model import Currency
from sqlite_cli.models.status_model import Status
from typing import Any, Callable, Dict

class CurrencyManagementScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f0f0f0")
        self.currency_widgets = {}
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
            text="Gestión de Monedas",
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

        # Cargar monedas desde la base de datos
        currencies = Currency.all()
        
        for currency in currencies:
            self.create_currency_widget(content_frame, currency)

    def create_currency_widget(self, parent: tk.Widget, currency: Dict) -> None:
        """Crea los widgets para una moneda específica"""
        currency_frame = tk.Frame(parent, bg="#f0f0f0", bd=1, relief=tk.GROOVE)
        currency_frame.pack(fill=tk.X, pady=10, padx=5, ipady=5)

        # Subtítulo con nombre de la moneda
        subtitle = CustomLabel(
            currency_frame,
            text=f"{currency['name']} ({currency['symbol']})",
            font=("Arial", 12, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        subtitle.pack(anchor=tk.W, pady=(5, 10))

        # Frame para controles
        controls_frame = tk.Frame(currency_frame, bg="#f0f0f0")
        controls_frame.pack(fill=tk.X, padx=10)

        # Valor de la moneda
        value_label = CustomLabel(
            controls_frame,
            text="Valor:",
            font=("Arial", 10),
            fg="#333",
            bg="#f0f0f0"
        )
        value_label.pack(side=tk.LEFT, padx=(0, 5))

        value_var = tk.StringVar(value=str(currency['value']))
        value_entry = CustomEntry(
            controls_frame,
            textvariable=value_var,
            width=15,
            state="normal" if currency['status_name'] == 'active' else "disabled"
        )
        value_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Frame para botones
        buttons_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        buttons_frame.pack(side=tk.RIGHT)

        # Botón de actualizar
        btn_update = CustomButton(
            buttons_frame,
            text="Actualizar",
            command=lambda: self.update_currency_value(currency['name'], value_var.get(), currency['status_name'] == 'active'),
            padding=5,
            width=10
        )
        # Configurar estado inicial del botón
        if currency['status_name'] != 'active':
            btn_update.disable()
        btn_update.pack(side=tk.LEFT, padx=5)

        # Botón de activar/desactivar
        btn_toggle = CustomButton(
            buttons_frame,
            text="Desactivar" if currency['status_name'] == 'active' else "Activar",
            command=lambda: self.toggle_currency_status(currency['name'], currency['status_name'] != 'active'),
            padding=5,
            width=10
        )
        btn_toggle.pack(side=tk.LEFT, padx=5)

        # Guardar referencias para actualización
        self.currency_widgets[currency['name']] = {
            'value_var': value_var,
            'value_entry': value_entry,
            'btn_update': btn_update,
            'btn_toggle': btn_toggle,
            'is_active': currency['status_name'] == 'active'
        }

    def update_currency_value(self, currency_name: str, new_value: str, is_active: bool) -> None:
        """Actualiza el valor de una moneda"""
        if not is_active:
            messagebox.showwarning("Advertencia", f"No se puede actualizar {currency_name} porque está desactivada", parent=self)
            return
            
        try:
            value = float(new_value)
            if value < 0:
                raise ValueError("El valor no puede ser negativo")
            
            Currency.update_value(currency_name, value)
            messagebox.showinfo("Éxito", f"Valor de {currency_name} actualizado correctamente", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {str(e)}", parent=self)

    def toggle_currency_status(self, currency_name: str, activate: bool) -> None:
        """Activa o desactiva una moneda"""
        status = Status.all()
        status_id = next((s['id'] for s in status if s['name'] == ('active' if activate else 'inactive')), None)
        
        if status_id:
            Currency.update_status(currency_name, status_id)
            
            # Actualizar estado de los widgets
            widgets = self.currency_widgets.get(currency_name)
            if widgets:
                widgets['is_active'] = activate
                widgets['value_entry'].config(state="normal" if activate else "disabled")
                
                # Actualizar botón de actualizar
                if activate:
                    widgets['btn_update'].enable()
                    # Actualizamos la función del botón con el nuevo estado
                    widgets['btn_update'].command = lambda: self.update_currency_value(
                        currency_name, 
                        widgets['value_var'].get(), 
                        activate
                    )
                else:
                    widgets['btn_update'].disable()
                
                # Actualizar botón de toggle
                widgets['btn_toggle'].label.configure(
                    text="Desactivar" if activate else "Activar"
                )
                widgets['btn_toggle'].command = lambda: self.toggle_currency_status(
                    currency_name, not activate
                )
            
            messagebox.showinfo(
                "Éxito", 
                f"Moneda {currency_name} {'activada' if activate else 'desactivada'} correctamente",
                parent=self
            )
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado de la moneda", parent=self)

    def go_back(self) -> None:
        self.open_previous_screen_callback()