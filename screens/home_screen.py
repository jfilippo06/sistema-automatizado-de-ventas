import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
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
        open_queries_callback: Callable[[], None],
        open_catalog_callback: Callable[[], None],
        open_purchase_orders_callback: Callable[[], None],
        open_purchase_order_report_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_login_screen_callback = open_login_screen_callback
        self.callbacks = {
            "inventory": open_inventory_callback,
            "suppliers": open_suppliers_callback,
            "customers": open_customers_callback,
            "service_requests": open_service_requests_callback,
            "services": open_services_callback,
            "config": open_config_callback,
            "maintenance": open_maintenance_callback,
            "recovery": open_recovery_callback,
            "billing": open_billing_callback,
            "reports": open_reports_callback,
            "queries": open_queries_callback,
            "catalog": open_catalog_callback,
            "purchase_orders": open_purchase_orders_callback,
            "purchase_order_report": open_purchase_order_report_callback
        }

        self.images = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        if not SessionManager.is_authenticated():
            self.open_login_screen_callback()
            return

        window_width = 1000
        window_height = 600

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        self.load_image(header_frame, "assets/republica.png", (70, 70)).pack(side=tk.LEFT, padx=5)

        tk.Label(header_frame, text="Sistema de Gestión de Ventas y Servicios", font=("Arial", 18, "bold"), bg="white").pack(side=tk.LEFT, padx=10)

        self.load_image(header_frame, "assets/empresa.png", (70, 70)).pack(side=tk.LEFT, padx=5)
        self.load_image(header_frame, "assets/universidad.png", (70, 70)).pack(side=tk.LEFT, padx=5)

        salir_button = tk.Button(header_frame, text="Salir", command=self.exit, bg="#eeeeee", padx=10)
        salir_button.pack(side=tk.RIGHT, padx=10)

        # Main content
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left menu
        menu_frame = tk.Frame(main_frame, bg="#f0f0f0", width=300)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons = [
            ("Proveedores", "suppliers"),
            ("Productos", "inventory"),
            ("Orden de compra", "purchase_orders"),
            ("Consultas", "queries"),
            ("Reportes", "reports"),
            ("Ventas", "billing"),
            ("Clientes", "customers"),
            ("Solicitudes de servicio", "service_requests"),
            ("Servicios", "services"),
            ("Catálogo", "catalog"),
            ("Mantenimiento", "maintenance"),
            ("Recuperación", "recovery"),
            ("Configuración", "config"),
            ("Salir", "exit")
        ]

        for label, key in buttons:
            color = "#d9534f" if key == "exit" else "#2356a2"
            btn = tk.Button(menu_frame, text=label, command=lambda k=key: self.navigate(k), bg=color, fg="white", font=("Arial", 10), width=25, pady=10)
            btn.pack(pady=3, padx=10, anchor="w")

        # Right image
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        central_img = self.load_image(image_frame, "assets/central_image.png", (800, 500))
        central_img.pack(expand=True)

        # Bottom logo
        bottom_frame = tk.Frame(self, bg="white")
        bottom_frame.pack(fill=tk.X, pady=5)

        tk.Label(bottom_frame, text="Gobierno Bolivariano de Venezuela", font=("Arial", 12, "bold"), bg="white").pack()

    def load_image(self, parent, path, size):
        try:
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images[path] = photo
            label = tk.Label(parent, image=photo, bg="white")
            return label
        except:
            label = tk.Label(parent, bg="white")
            return label

    def navigate(self, key):
        if key == "exit":
            self.exit()
        elif key in self.callbacks:
            self.callbacks[key]()

    def exit(self):
        SessionManager.logout()
        self.open_login_screen_callback()
