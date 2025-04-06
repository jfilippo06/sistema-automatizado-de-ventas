import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

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
        open_config_callback: Callable[[], None]
    ) -> None:
        """
        Pantalla principal del sistema con acceso a todos los módulos.
        
        Args:
            parent: Widget padre (ventana principal)
            open_login_screen_callback: Función para volver al login
            open_inventory_callback: Función para abrir módulo de inventario
            open_suppliers_callback: Función para abrir módulo de proveedores
            open_customers_callback: Función para abrir módulo de clientes
            open_service_requests_callback: Función para abrir solicitudes de servicio
            open_services_callback: Función para abrir módulo de servicios
            open_config_callback: Función para abrir pantalla de configuración
        """
        super().__init__(parent)
        self.parent = parent
        self.open_login_screen_callback = open_login_screen_callback
        self.open_inventory_callback = open_inventory_callback
        self.open_suppliers_callback = open_suppliers_callback
        self.open_customers_callback = open_customers_callback
        self.open_service_requests_callback = open_service_requests_callback
        self.open_services_callback = open_services_callback
        self.open_config_callback = open_config_callback
        
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """Configura el tamaño de la ventana al mostrar la pantalla."""
        self.parent.geometry("700x600")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        """Configura los elementos de la interfaz de usuario."""
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título principal
        title = CustomLabel(
            main_frame,
            text="Sistema de Gestión",
            font=("Arial", 24, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 30))

        # Botones de los módulos
        buttons = [
            ("Gestión de proveedores", self.suppliers_control),
            ("Inventario de productos", self.inventory_control),
            ("Gestión de ventas", self.purchases_module),
            ("Reportes", self.reports),
            ("Facturación", self.billing_control),
            ("Gestión de clientes", self.customers_control),
            ("Solicitudes de servicio", self.service_requests_control),
            ("Gestión de servicios", self.services_control),
            ("Catálogo", self.catalog),
            ("Mantenimiento", self.maintenance),
            ("Recuperación", self.recovery),
            ("Configuración", self.config_control),
            ("Salir", self.exit)
        ]

        # Crear y posicionar los botones
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

        # Configurar el grid para que sea responsivo
        for i in range(5):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

    # Métodos para controlar los botones
    def suppliers_control(self) -> None:
        """Abre el módulo de proveedores."""
        self.open_suppliers_callback()

    def inventory_control(self) -> None:
        """Abre el módulo de inventario."""
        self.open_inventory_callback()

    def purchases_module(self) -> None:
        """Abre el módulo de compras (pendiente de implementación)."""
        print("Function: Módulo de compras")

    def reports(self) -> None:
        """Abre el módulo de reportes (pendiente de implementación)."""
        print("Function: Reportes")

    def billing_control(self) -> None:
        """Abre el módulo de facturación (pendiente de implementación)."""
        print("Function: Control de facturación")

    def customers_control(self) -> None:
        """Abre el módulo de clientes."""
        self.open_customers_callback()

    def service_requests_control(self) -> None:
        """Abre el módulo de solicitudes de servicio."""
        self.open_service_requests_callback()

    def services_control(self) -> None:
        """Abre el módulo de servicios."""
        self.open_services_callback()

    def catalog(self) -> None:
        """Abre el catálogo de productos (pendiente de implementación)."""
        print("Function: Catálogo de productos y servicios")

    def maintenance(self) -> None:
        """Abre el módulo de mantenimiento (pendiente de implementación)."""
        print("Function: Mantenimiento del sistema")

    def recovery(self) -> None:
        """Abre el módulo de recuperación de registros."""
        print("Function: Recuperación de registros deshabilitados")

    def config_control(self) -> None:
        """Abre la pantalla de configuración del sistema."""
        self.open_config_callback()

    def exit(self) -> None:
        """Regresa a la pantalla de login."""
        self.open_login_screen_callback()