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

        window_width = 900
        window_height = 650

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Configuración de estilos
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=("Arial", 9))
        
        # Header compacto
        header_frame = tk.Frame(self, bg="white", height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Imagen de la empresa (principal)
        self.load_image(header_frame, "assets/empresa.png", (50, 50)).pack(side=tk.LEFT, padx=10)
        
        # Título
        title = tk.Label(
            header_frame, 
            text="Gestión de Ventas y Servicios",
            font=("Arial", 14, "bold"), 
            bg="white"
        )
        title.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Único botón de salir en esquina derecha
        salir_button = ttk.Button(
            header_frame, 
            text="Salir", 
            command=self.exit,
            style="TButton"
        )
        salir_button.pack(side=tk.RIGHT, padx=10)

        # Contenido principal
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para menú con scrollbar
        menu_container = tk.Frame(main_frame, bg="#f0f0f0")
        menu_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5))

        # Canvas y scrollbar
        canvas = tk.Canvas(menu_container, bg="#f0f0f0", width=200, highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botones del menú en una sola columna
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
            ("Configuración", "config")
        ]

        for label, key in buttons:
            btn = ttk.Button(
                scrollable_frame, 
                text=label, 
                command=lambda k=key: self.navigate(k),
                style="TButton",
                width=20
            )
            btn.pack(pady=3, padx=5, fill=tk.X)

        # Área de imagen principal
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        central_img = self.load_image(image_frame, "assets/central_image.png", (500, 350))
        central_img.pack(expand=True, padx=5, pady=5)

        # Pie de página con imágenes en esquinas
        bottom_frame = tk.Frame(self, bg="white", height=50)
        bottom_frame.pack(fill=tk.X, pady=(0,5))
        
        # Imagen en esquina izquierda
        self.load_image(bottom_frame, "assets/republica.png", (40, 40)).pack(side=tk.LEFT, padx=10)
        
        # Espacio central vacío
        tk.Frame(bottom_frame, bg="white").pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Imagen en esquina derecha
        self.load_image(bottom_frame, "assets/universidad.png", (40, 40)).pack(side=tk.RIGHT, padx=10)

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