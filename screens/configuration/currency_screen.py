import tkinter as tk
from tkinter import messagebox
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from sqlite_cli.models.currency_model import Currency
from sqlite_cli.models.status_model import Status
from typing import Any, Callable, Dict
from utils.valdations import Validations  # Importamos las validaciones

class CurrencyManagementScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")  # Mismo fondo que Suppliers
        self.currency_widgets = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("500x400")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título - Estilo similar a Suppliers
        header_frame = tk.Frame(self, bg="#4a6fa5")  # Mismo color de header
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Monedas",
            font=("Arial", 20, "bold"),  # Mismo tamaño de fuente
            fg="white",
            bg="#4a6fa5"  # Mismo fondo
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Frame para botón de regreso - Estilo similar
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Contenido principal - Estilo actualizado
        content_frame = tk.Frame(self, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Cargar monedas desde la base de datos
        currencies = Currency.all()
        
        for currency in currencies:
            self.create_currency_widget(content_frame, currency)

        # Barra de estado - Igual que en Suppliers
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def create_currency_widget(self, parent: tk.Widget, currency: Dict) -> None:
        """Crea los widgets para una moneda específica con el nuevo estilo"""
        # Frame principal para cada moneda - Estilo actualizado
        currency_frame = tk.Frame(
            parent, 
            bg="white",  # Fondo blanco para contrastar
            bd=1, 
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        currency_frame.pack(fill=tk.X, pady=10, padx=20, ipady=10)

        # Subtítulo con nombre de la moneda - Estilo actualizado
        subtitle = CustomLabel(
            currency_frame,
            text=f"{currency['name']} ({currency['symbol']})",
            font=("Arial", 14, "bold"),  # Tamaño aumentado
            fg="#333",
            bg="white"
        )
        subtitle.pack(anchor=tk.W, pady=(0, 10))

        # Frame para controles - Estilo actualizado
        controls_frame = tk.Frame(currency_frame, bg="white")
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # Valor de la moneda - Estilo actualizado
        value_label = CustomLabel(
            controls_frame,
            text="Valor:",
            font=("Arial", 12),  # Tamaño aumentado
            fg="#333",
            bg="white"
        )
        value_label.pack(side=tk.LEFT, padx=(0, 10))

        value_var = tk.StringVar(value=str(currency['value']))
        value_entry = CustomEntry(
            controls_frame,
            textvariable=value_var,
            width=15,
            font=("Arial", 12),  # Tamaño aumentado
            state="normal" if currency['status_name'] == 'active' else "disabled"
        )
        # Configuramos la validación para números decimales
        value_entry.configure(validate="key")
        value_entry.configure(validatecommand=(
            value_entry.register(Validations.validate_decimal),
            '%P'
        ))
        value_entry.pack(side=tk.LEFT, padx=(0, 20))

        # Frame para botones - Estilo actualizado
        buttons_frame = tk.Frame(controls_frame, bg="white")
        buttons_frame.pack(side=tk.RIGHT)

        # Botón de actualizar - Estilo consistente
        btn_update = CustomButton(
            buttons_frame,
            text="Actualizar",
            command=lambda: self.update_currency_value(
                currency['name'], 
                value_var.get(), 
                currency['status_name'] == 'active'
            ),
            padding=8,  # Mismo padding que en Suppliers
            width=12   # Mismo ancho aproximado
        )
        # Configurar estado inicial del botón
        if currency['status_name'] != 'active':
            btn_update.disable()
        btn_update.pack(side=tk.LEFT, padx=5)

        # Botón de activar/desactivar - Estilo consistente
        btn_toggle = CustomButton(
            buttons_frame,
            text="Desactivar" if currency['status_name'] == 'active' else "Activar",
            command=lambda: self.toggle_currency_status(
                currency['name'], 
                currency['status_name'] != 'active'
            ),
            padding=8,  # Mismo padding que en Suppliers
            width=12    # Mismo ancho aproximado
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
            return
            
        try:
            value = float(new_value)
            if value < 0:
                raise ValueError("El valor no puede ser negativo")
            
            Currency.update_value(currency_name, value)
            messagebox.showinfo(
                "Éxito", 
                f"Valor de {currency_name} actualizado correctamente", 
                parent=self
            )
            self.status_bar.configure(text=f"Valor de {currency_name} actualizado")  # Actualizar barra de estado
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {str(e)}", parent=self)
            self.status_bar.configure(text=f"Error: {str(e)}")  # Actualizar barra de estado

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
                
                if activate:
                    widgets['btn_update'].enable()
                else:
                    widgets['btn_update'].disable()
                    widgets['btn_update'].command = None
                
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
            self.status_bar.configure(
                text=f"Moneda {currency_name} {'activada' if activate else 'desactivada'}"
            )
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado de la moneda", parent=self)
            self.status_bar.configure(text="Error al cambiar estado de la moneda")

    def go_back(self) -> None:
        self.parent.state('normal')  # Restaurar tamaño de ventana como en Suppliers
        self.open_previous_screen_callback()