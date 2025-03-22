import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel  # Importar el widget personalizado de label

class HomeScreen(tk.Frame):
    def __init__(self, parent, open_login_screen_callback, open_inventory_callback):
        super().__init__(parent)
        self.parent = parent  # Guardar referencia a la ventana principal
        self.open_login_screen_callback = open_login_screen_callback  # Callback para abrir LoginScreen
        self.open_inventory_callback = open_inventory_callback  # Callback para abrir Inventory
        
        # Configurar la interfaz de usuario
        self.configure_ui()

    def pack(self, **kwargs):
        """
        Configura la ventana principal cuando se muestra la pantalla de inicio.
        """
        self.parent.geometry("800x600")  # Tamaño específico para la pantalla de inicio
        self.parent.resizable(False, False)  # No redimensionable
        super().pack(**kwargs)  # Mostrar la pantalla

    def configure_ui(self):
        """
        Configura la interfaz de usuario de la pantalla de inicio.
        """
        # Añadir un título con CustomLabel
        title = CustomLabel(self, text="Menú principal", font=("Arial", 24))
        title.place(x=300, y=20)  # Colocar el título en una posición específica

        # Posiciones iniciales para los botones
        start_x = 80  # Posición inicial en el eje X
        start_y = 70  # Posición inicial en el eje Y
        button_width = 200  # Ancho de los botones
        button_height = 100  # Alto de los botones
        padding = 30  # Espaciado entre botones

        # Botón 1: Control de proveedores
        btn_suppliers = CustomButton(self, text="Control de proveedores", padding=padding, command=self.suppliers_control)
        btn_suppliers.place(x=start_x, y=start_y, width=button_width, height=button_height)

        # Botón 2: Inventario de productos
        btn_inventory = CustomButton(self, text="Inventario de productos", padding=padding, command=self.inventory_control)
        btn_inventory.place(x=start_x + (button_width + padding) * 1, y=start_y, width=button_width, height=button_height)

        # Botón 3: Módulo de compras
        btn_purchases = CustomButton(self, text="Módulo de compras", padding=padding, command=self.purchases_module)
        btn_purchases.place(x=start_x + (button_width + padding) * 2, y=start_y, width=button_width, height=button_height)

        # Botón 4: Reportes
        btn_reports = CustomButton(self, text="Reportes", padding=padding, command=self.reports)
        btn_reports.place(x=start_x, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 5: Control de facturación
        btn_billing = CustomButton(self, text="Control de facturación", padding=padding, command=self.billing_control)
        btn_billing.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 6: Control de clientes
        btn_customers = CustomButton(self, text="Control de clientes", padding=padding, command=self.customers_control)
        btn_customers.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 1, width=button_width, height=button_height)

        # Botón 7: Control de servicios
        btn_services = CustomButton(self, text="Control de servicios", padding=padding, command=self.services_control)
        btn_services.place(x=start_x, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)

        # Botón 8: Catálogo de productos y servicios
        btn_catalog = CustomButton(self, text="Catálogo de productos y servicios", padding=10, command=self.catalog, wraplength=150)
        btn_catalog.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)
        # Botón 9: Tipos de pagos
        btn_payments = CustomButton(self, text="Tipos de pagos", padding=padding, command=self.payments)
        btn_payments.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 2, width=button_width, height=button_height)

        # Botón 10: Usuarios
        btn_users = CustomButton(self, text="Usuarios", padding=padding, command=self.users)
        btn_users.place(x=start_x, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

        # Botón 11: Configuración del sistema
        btn_config = CustomButton(self, text="Configuración del sistema", padding=padding, command=self.system_config)
        btn_config.place(x=start_x + (button_width + padding) * 1, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

        # Botón 12: Salir
        btn_exit = CustomButton(self, text="Salir", padding=padding, command=self.exit)
        btn_exit.place(x=start_x + (button_width + padding) * 2, y=start_y + (button_height + padding) * 3, width=button_width, height=button_height)

    # Funciones para cada botón
    def suppliers_control(self):
        print("Function: Control de proveedores")

    def inventory_control(self):
        """
        Método para abrir la pantalla de inventario.
        """
        print("Function: Inventario de productos")
        self.open_inventory_callback()  # Llamar al callback para abrir Inventory

    def purchases_module(self):
        print("Function: Módulo de compras")

    def reports(self):
        print("Function: Reportes")

    def billing_control(self):
        print("Function: Control de facturación")

    def customers_control(self):
        print("Function: Control de clientes")

    def services_control(self):
        print("Function: Control de servicios")

    def catalog(self):
        print("Function: Catálogo de productos y servicios")

    def payments(self):
        print("Function: Tipos de pagos")

    def users(self):
        print("Function: Usuarios")

    def system_config(self):
        print("Function: Configuración del sistema")

    def exit(self):
        """
        Cierra la pantalla actual (HomeScreen) y abre la pantalla de inicio de sesión (LoginScreen).
        """
        print("Function: Salir")
        self.open_login_screen_callback()  # Llamar al callback para abrir LoginScreen