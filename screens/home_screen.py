import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
from utils.session_manager import SessionManager

class HomeScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_login_screen_callback: Callable[[], None],
        open_inventory_callback: Callable[[], None],
        open_suppliers_callback: Callable[[], None],
        open_customers_callback: Callable[[], None],
        open_service_requests_callback: Callable[[], None],
        open_services_callback: Callable[[], None],
        open_config_callback: Callable[[], None],
        open_maintenance_callback: Callable[[], None],
        open_recovery_callback: Callable[[], None],
        open_billing_callback: Callable[[], None],
        open_reports_callback: Callable[[], None],
        open_purchases_callback: Callable[[], None],
        open_catalog_callback: Callable[[], None]  # Nuevo callback
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_login_screen_callback = open_login_screen_callback
        self.open_inventory_callback = open_inventory_callback
        self.open_suppliers_callback = open_suppliers_callback
        self.open_customers_callback = open_customers_callback
        self.open_service_requests_callback = open_service_requests_callback
        self.open_services_callback = open_services_callback
        self.open_config_callback = open_config_callback
        self.open_maintenance_callback = open_maintenance_callback
        self.open_recovery_callback = open_recovery_callback
        self.open_billing_callback = open_billing_callback
        self.open_reports_callback = open_reports_callback
        self.open_purchases_callback = open_purchases_callback
        self.open_catalog_callback = open_catalog_callback  # Nuevo callback
        
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """Sobrescribimos pack para verificar autenticación"""
        if not SessionManager.is_authenticated():
            self.open_login_screen_callback()
            return
            
        self.parent.state('normal')  # Ensure normal state when showing home screen
        self.parent.geometry("700x600")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        title = CustomLabel(
            main_frame,
            text="Sistema de Gestión",
            font=("Arial", 24, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 30))

        buttons = [
            ("Gestión de proveedores", self.suppliers_control),
            ("Inventario de productos", self.inventory_control),
            ("Gestión de compras", self.purchases_control),
            ("Reportes", self.reports_control),
            ("Facturación", self.billing_control),
            ("Gestión de clientes", self.customers_control),
            ("Solicitudes de servicio", self.service_requests_control),
            ("Gestión de servicios", self.services_control),
            ("Catálogo", self.catalog_control),  # Actualizado
            ("Mantenimiento", self.maintenance),
            ("Recuperación", self.recovery),
            ("Configuración", self.config_control),
            ("Salir", self.exit)
        ]

        for i, (text, command) in enumerate(buttons):
            row = (i // 3) + 1
            col = i % 3
            
            btn = CustomButton(
                main_frame,
                text=text,
                command=command,
                padding=20,
                width=30,
                wraplength=150 if text == "Catálogo" else None
            )
            btn.grid(row=row, column=col, padx=10, pady=10, ipady=20, sticky="nsew")

        for i in range(5):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

    def suppliers_control(self) -> None:
        self.open_suppliers_callback()

    def inventory_control(self) -> None:
        self.open_inventory_callback()

    def purchases_control(self) -> None:
        self.open_purchases_callback()

    def reports_control(self) -> None:
        self.open_reports_callback()

    def billing_control(self) -> None:
        self.open_billing_callback()

    def customers_control(self) -> None:
        self.open_customers_callback()

    def service_requests_control(self) -> None:
        self.open_service_requests_callback()

    def services_control(self) -> None:
        self.open_services_callback()

    def catalog_control(self) -> None:  # Actualizado
        self.open_catalog_callback()

    def maintenance(self) -> None:
        self.open_maintenance_callback()

    def recovery(self) -> None:
        self.open_recovery_callback()

    def config_control(self) -> None:
        self.open_config_callback()

    def exit(self) -> None:
        SessionManager.logout()
        self.open_login_screen_callback()