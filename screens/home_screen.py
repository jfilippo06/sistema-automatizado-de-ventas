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
        open_suppliers_callback: Callable[[], None]
    ) -> None:
        """
        Pantalla principal del sistema con menú de opciones.
        
        Args:
            parent: Widget padre contenedor
            open_login_screen_callback: Función para volver a la pantalla de login
            open_inventory_callback: Función para abrir el módulo de inventario
            open_suppliers_callback: Función para abrir el módulo de proveedores
        """
        super().__init__(parent)
        self.parent = parent
        self.open_login_screen_callback = open_login_screen_callback
        self.open_inventory_callback = open_inventory_callback
        self.open_suppliers_callback = open_suppliers_callback
        
        self.configure(bg="#f0f0f0")  # Fondo claro para mejor contraste
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """Configura la ventana al mostrar esta pantalla."""
        self.parent.geometry("700x600")  # Tamaño más adecuado para los botones
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        """Configura todos los elementos de la interfaz."""
        # Frame principal para centrar contenido
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

        # Configuración de botones
        buttons = [
            ("Gestión de proveedores", self.suppliers_control),
            ("Inventario de productos", self.inventory_control),
            ("Gestión de ventas", self.purchases_module),
            ("Reportes", self.reports),
            ("Facturación", self.billing_control),
            ("Gestión de clientes", self.customers_control),
            ("Gestión de servicios", self.services_control),
            ("Catálogo", self.catalog),
            ("Tipos de pagos", self.payments),
            ("Usuarios", self.users),
            ("Configuración", self.system_config),
            ("Salir", self.exit)
        ]

        # Crear botones en grid 4x3
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

        # Configurar grid para expansión
        for i in range(4):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

    # Métodos de los botones
    def suppliers_control(self) -> None:
        """Abre el módulo de proveedores."""
        self.open_suppliers_callback()

    def inventory_control(self) -> None:
        """Abre el módulo de inventario."""
        self.open_inventory_callback()

    def purchases_module(self) -> None:
        """Módulo de compras (pendiente implementación)."""
        print("Function: Módulo de compras")

    def reports(self) -> None:
        """Módulo de reportes (pendiente implementación)."""
        print("Function: Reportes")

    def billing_control(self) -> None:
        """Módulo de facturación (pendiente implementación)."""
        print("Function: Control de facturación")

    def customers_control(self) -> None:
        """Módulo de clientes (pendiente implementación)."""
        print("Function: Control de clientes")

    def services_control(self) -> None:
        """Módulo de servicios (pendiente implementación)."""
        print("Function: Control de servicios")

    def catalog(self) -> None:
        """Módulo de catálogo (pendiente implementación)."""
        print("Function: Catálogo de productos y servicios")

    def payments(self) -> None:
        """Módulo de pagos (pendiente implementación)."""
        print("Function: Tipos de pagos")

    def users(self) -> None:
        """Módulo de usuarios (pendiente implementación)."""
        print("Function: Usuarios")

    def system_config(self) -> None:
        """Módulo de configuración (pendiente implementación)."""
        print("Function: Configuración del sistema")

    def exit(self) -> None:
        """Regresa a la pantalla de login."""
        self.open_login_screen_callback()