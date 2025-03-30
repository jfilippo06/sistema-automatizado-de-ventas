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
        open_suppliers_callback: Callable[[], None]  # Nuevo callback para proveedores
    ) -> None:
        """
        Inicializa la pantalla de inicio.

        :param parent: El widget padre al que pertenece esta pantalla.
        :param open_login_screen_callback: Función para abrir la pantalla de login.
        :param open_inventory_callback: Función para abrir la pantalla de inventario.
        :param open_suppliers_callback: Función para abrir la pantalla de proveedores.
        """
        super().__init__(parent)
        self.parent: tk.Widget = parent
        self.open_login_screen_callback: Callable[[], None] = open_login_screen_callback
        self.open_inventory_callback: Callable[[], None] = open_inventory_callback
        self.open_suppliers_callback: Callable[[], None] = open_suppliers_callback  # Guardamos el callback
        
        # Configurar la interfaz de usuario
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """
        Configura la ventana principal cuando se muestra la pantalla de inicio.
        """
        self.parent.geometry("800x600")  # Tamaño específico para la pantalla de inicio
        self.parent.resizable(False, False)  # No redimensionable
        super().pack(**kwargs)  # Mostrar la pantalla

    def configure_ui(self) -> None:
        """
        Configura la interfaz de usuario de la pantalla de inicio.
        """
        # Añadir un título con CustomLabel
        title: CustomLabel = CustomLabel(self, text="Menú principal", font=("Arial", 24))
        title.place(x=300, y=20)  # Colocar el título en una posición específica

        # Posiciones iniciales para los botones
        start_x: int = 80  # Posición inicial en el eje X
        start_y: int = 70  # Posición inicial en el eje Y
        button_width: int = 200  # Ancho de los botones
        button_height: int = 100  # Alto de los botones
        padding: int = 30  # Espaciado entre botones

        # Botón 1: Gestión de proveedores (MODIFICADO para usar el nuevo callback)
        btn_suppliers: CustomButton = CustomButton(
            self, 
            text="Gestión de proveedores", 
            padding=padding, 
            command=self.suppliers_control
        )
        btn_suppliers.place(x=start_x, y=start_y, width=button_width, height=button_height)

        # Botón 2: Inventario de productos
        btn_inventory: CustomButton = CustomButton(
            self, 
            text="Inventario de productos", 
            padding=padding, 
            command=self.inventory_control
        )
        btn_inventory.place(x=start_x + (button_width + padding) * 1, y=start_y, width=button_width, height=button_height)

        # Botón 3: Gestión de ventas
        btn_purchases: CustomButton = CustomButton(
            self, 
            text="Gestión de ventas", 
            padding=padding, 
            command=self.purchases_module
        )
        btn_purchases.place(x=start_x + (button_width + padding) * 2, y=start_y, width=button_width, height=button_height)

        # Botón 4: Reportes
        btn_reports: CustomButton = CustomButton(
            self, 
            text="Reportes", 
            padding=padding, 
            command=self.reports
        )
        btn_reports.place(x=start_x, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 5: Facturación
        btn_billing: CustomButton = CustomButton(
            self, 
            text="Facturación", 
            padding=padding, 
            command=self.billing_control
        )
        btn_billing.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 6: Gestión de clientes
        btn_customers: CustomButton = CustomButton(
            self, 
            text="Gestión de clientes", 
            padding=padding, 
            command=self.customers_control
        )
        btn_customers.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 7: Gestión de servicios
        btn_services: CustomButton = CustomButton(
            self, 
            text="Gestión de servicios", 
            padding=padding, 
            command=self.services_control
        )
        btn_services.place(x=start_x, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)

        # Botón 8: Catálogo de productos y servicios
        btn_catalog: CustomButton = CustomButton(
            self, 
            text="Catálogo de productos y servicios", 
            padding=10, 
            command=self.catalog, 
            wraplength=150
        )
        btn_catalog.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)

        # Botón 9: Tipos de pagos
        btn_payments: CustomButton = CustomButton(
            self, 
            text="Tipos de pagos", 
            padding=padding, 
            command=self.payments
        )
        btn_payments.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)

        # Botón 10: Usuarios
        btn_users: CustomButton = CustomButton(
            self, 
            text="Usuarios", 
            padding=padding, 
            command=self.users
        )
        btn_users.place(x=start_x, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

        # Botón 11: Configuración del sistema
        btn_config: CustomButton = CustomButton(
            self, 
            text="Configuración del sistema", 
            padding=padding, 
            command=self.system_config
        )
        btn_config.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

        # Botón 12: Salir
        btn_exit: CustomButton = CustomButton(
            self, 
            text="Salir", 
            padding=padding, 
            command=self.exit
        )
        btn_exit.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

    # Funciones para cada botón
    def suppliers_control(self) -> None:
        """
        Método para abrir la pantalla de proveedores.
        """
        print("Function: Control de proveedores")
        self.open_suppliers_callback()  # Llama al callback para abrir Suppliers

    def inventory_control(self) -> None:
        """
        Método para abrir la pantalla de inventario.
        """
        print("Function: Inventario de productos")
        self.open_inventory_callback()

    def purchases_module(self) -> None:
        print("Function: Módulo de compras")

    def reports(self) -> None:
        print("Function: Reportes")

    def billing_control(self) -> None:
        print("Function: Control de facturación")

    def customers_control(self) -> None:
        print("Function: Control de clientes")

    def services_control(self) -> None:
        print("Function: Control de servicios")

    def catalog(self) -> None:
        print("Function: Catálogo de productos y servicios")

    def payments(self) -> None:
        print("Function: Tipos de pagos")

    def users(self) -> None:
        print("Function: Usuarios")

    def system_config(self) -> None:
        print("Function: Configuración del sistema")

    def exit(self) -> None:
        """
        Cierra la pantalla actual (HomeScreen) y abre la pantalla de inicio de sesión (LoginScreen).
        """
        print("Function: Salir")
        self.open_login_screen_callback()