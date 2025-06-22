import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Any, Callable
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
            "catalog": open_catalog_callback,
            "purchase_orders": open_purchase_orders_callback,
            "purchase_order_report": open_purchase_order_report_callback
        }
        
        self.configure(bg="#f5f5f5")
        self.images = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        if not SessionManager.is_authenticated():
            self.open_login_screen_callback()
            return
            
        self.parent.state('normal')
        self.parent.geometry("700x500")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Frame principal con organización vertical
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mostrar las tres imágenes en una fila
        self.load_and_display_images(main_frame)
        
        # Título del sistema
        title = CustomLabel(
            main_frame,
            text="Sistema de Gestión",
            font=("Arial", 24, "bold"),
            fg="#2356a2",
            bg="#f5f5f5"
        )
        title.pack(pady=(20, 30))
        
        # Contenedor para los botones
        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones principales en el orden solicitado
        buttons = [
            ("Proveedores", "suppliers", "#2356a2"),
            ("Productos", "inventory", "#3a6eb5"),
            ("Orden de compra", "purchase_orders", "#4d87d1"),
            ("Reportes", "reports", "#5c9ae0"),
            ("Ventas", "billing", "#6eabed"),
            ("Clientes", "customers", "#2356a2"),
            ("Solicitudes de servicio", "service_requests", "#3a6eb5"),
            ("Servicios", "services", "#4d87d1"),
            ("Catálogo", "catalog", "#5c9ae0"),
            ("Mantenimiento", "maintenance", "#6eabed"),
            ("Recuperación", "recovery", "#2356a2"),
            ("Configuración", "config", "#3a6eb5"),
            ("Salir", "exit", "#d9534f")
        ]
        
        # Organización de botones en 4 columnas (para acomodar los 13 botones mejor)
        columns = 4
        for i, (text, key, color) in enumerate(buttons):
            row = i // columns
            col = i % columns
            
            btn = self.create_menu_button(
                buttons_frame, 
                text, 
                color,
                lambda k=key: self.navigate(k))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configurar expansión uniforme
            buttons_frame.grid_columnconfigure(col, weight=1)
            buttons_frame.grid_rowconfigure(row, weight=1)

    def load_and_display_images(self, parent):
        try:
            img_frame = tk.Frame(parent, bg="#f5f5f5")
            img_frame.pack()
            
            # Cargar las tres imágenes existentes
            img_paths = [
                ("assets/republica.png", (70, 70)),
                ("assets/empresa.png", (70, 70)),
                ("assets/universidad.png", (70, 70))
            ]
            
            for path, size in img_paths:
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                self.images[path] = ImageTk.PhotoImage(img)
                label = tk.Label(img_frame, image=self.images[path], bg="#f5f5f5")
                label.pack(side=tk.LEFT, padx=10)
                
        except Exception as e:
            print(f"Error cargando imágenes: {e}")

    def create_menu_button(self, parent, text, bg_color, command):
        btn = tk.Frame(parent, bg=bg_color, bd=0, highlightthickness=0)
        
        btn.bind("<Button-1>", lambda e: command())
        
        # Texto del botón
        label = tk.Label(
            btn, 
            text=text, 
            bg=bg_color, 
            fg="white", 
            font=("Arial", 11), 
            padx=10, 
            pady=15,
            wraplength=100
        )
        label.pack(fill=tk.BOTH, expand=True)
        
        # Hacer todo el label clickeable
        label.bind("<Button-1>", lambda e: command())
        
        return btn

    def navigate(self, key):
        if key == "exit":
            self.exit()
        elif key in self.callbacks:
            self.callbacks[key]()

    def exit(self) -> None:
        SessionManager.logout()
        self.open_login_screen_callback()