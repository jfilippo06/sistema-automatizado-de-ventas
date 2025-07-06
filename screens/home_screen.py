import tkinter as tk
from tkinter import Menu, ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from typing import Callable, Any
from utils.session_manager import SessionManager
import tkinter.messagebox as messagebox
import os
import shutil
from datetime import datetime
import sqlite3

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
        open_billing_callback: Callable[[], None],
        open_catalog_callback: Callable[[], None],
        open_purchase_orders_callback: Callable[[], None],
        # Callbacks para funcionalidades de submenús
        open_sales_report_callback: Callable[[], None],
        open_purchase_order_report_callback: Callable[[], None],
        open_full_inventory_report_callback: Callable[[], None],
        open_inventory_query_callback: Callable[[], None],
        open_services_query_callback: Callable[[], None],
        open_recovery_suppliers_callback: Callable[[], None],
        open_recovery_inventory_callback: Callable[[], None],
        open_recovery_service_requests_callback: Callable[[], None],
        open_recovery_services_callback: Callable[[], None],
        open_recovery_users_callback: Callable[[], None],
        open_users_management_callback: Callable[[], None],
        open_currency_management_callback: Callable[[], None],
        open_taxes_management_callback: Callable[[], None],
        open_system_info_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_login_screen_callback = open_login_screen_callback
        
        # Callbacks principales
        self.main_callbacks = {
            "inventory": open_inventory_callback,
            "suppliers": open_suppliers_callback,
            "customers": open_customers_callback,
            "service_requests": open_service_requests_callback,
            "services": open_services_callback,
            "billing": open_billing_callback,
            "catalog": open_catalog_callback,
            "purchase_orders": open_purchase_orders_callback
        }
        
        # Callbacks para submenús
        self.reports_callbacks = {
            "sales_report": open_sales_report_callback,
            "purchase_order_report": open_purchase_order_report_callback,
            "full_inventory_report": open_full_inventory_report_callback
        }
        
        self.queries_callbacks = {
            "inventory_query": open_inventory_query_callback,
            "services_query": open_services_query_callback
        }
        
        self.recovery_callbacks = {
            "recovery_suppliers": open_recovery_suppliers_callback,
            "recovery_inventory": open_recovery_inventory_callback,
            "recovery_service_requests": open_recovery_service_requests_callback,
            "recovery_services": open_recovery_services_callback,
            "recovery_users": open_recovery_users_callback
        }
        
        self.config_callbacks = {
            "users_management": open_users_management_callback,
            "currency_management": open_currency_management_callback,
            "taxes_management": open_taxes_management_callback,
            "system_info": open_system_info_callback
        }

        self.images = {}
        self.menu_buttons = {}  # Para almacenar referencias a los botones de menú
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
        self.style.configure("Menu.TButton", padding=5, font=("Arial", 9), width=20)
        self.style.configure("Submenu.TButton", padding=3, font=("Arial", 8), width=18)
        
        # Header
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
        
        # Botón de salir
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

        # Frame para menú
        menu_frame = tk.Frame(main_frame, bg="#f0f0f0", width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5))

        # Botones principales del menú
        main_buttons = [
            ("Proveedores", "suppliers"),
            ("Productos", "inventory"),
            ("Orden de compra", "purchase_orders"),
            ("Ventas", "billing"),
            ("Clientes", "customers"),
            ("Solicitudes de servicio", "service_requests"),
            ("Servicios", "services"),
            ("Catálogo", "catalog")
        ]

        # Crear botones principales
        for label, key in main_buttons:
            btn = ttk.Button(
                menu_frame, 
                text=label, 
                command=lambda k=key: self.navigate(k),
                style="Menu.TButton"
            )
            btn.pack(pady=3, padx=5, fill=tk.X)
            self.menu_buttons[key] = btn

        # Menú desplegable para Reportes
        self.create_dropdown_menu(
            menu_frame, 
            "Reportes", 
            {
                "Reporte de Ventas": "sales_report",
                "Reporte de Órdenes de Compra": "purchase_order_report",
                "Reporte de Inventario": "full_inventory_report"
            },
            self.reports_callbacks
        )

        # Menú desplegable para Consultas
        self.create_dropdown_menu(
            menu_frame, 
            "Consultas", 
            {
                "Consulta de Productos": "inventory_query",
                "Consulta de Servicios": "services_query"
            },
            self.queries_callbacks
        )

        # Menú desplegable para Mantenimiento
        self.create_maintenance_menu(menu_frame)

        # Menú desplegable para Recuperación
        self.create_dropdown_menu(
            menu_frame, 
            "Recuperación", 
            {
                "Recuperar Proveedores": "recovery_suppliers",
                "Recuperar Productos": "recovery_inventory",
                "Recuperar Solicitudes": "recovery_service_requests",
                "Recuperar Servicios": "recovery_services",
                "Recuperar Usuarios": "recovery_users"
            },
            self.recovery_callbacks
        )

        # Menú desplegable para Configuración
        self.create_dropdown_menu(
            menu_frame, 
            "Configuración", 
            {
                "Gestión de Usuarios": "users_management",
                "Gestión de Monedas": "currency_management",
                "Gestión de Impuestos": "taxes_management",
                "Información del Sistema": "system_info"
            },
            self.config_callbacks
        )

        # Área de imagen principal
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        central_img = self.load_image(image_frame, "assets/central_image.png", (500, 350))
        central_img.pack(expand=True, padx=5, pady=5)

        # Pie de página con imágenes
        bottom_frame = tk.Frame(self, bg="white", height=50)
        bottom_frame.pack(fill=tk.X, pady=(0,5))
        
        # Imagen izquierda
        self.load_image(bottom_frame, "assets/republica.png", (40, 40)).pack(side=tk.LEFT, padx=10)
        
        # Espacio central
        tk.Frame(bottom_frame, bg="white").pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Imagen derecha
        self.load_image(bottom_frame, "assets/universidad.png", (40, 40)).pack(side=tk.RIGHT, padx=10)

    def create_dropdown_menu(self, parent, title, options, callbacks_dict):
        """Crea un menú desplegable estilo menú contextual"""
        # Botón principal del menú
        main_btn = ttk.Button(
            parent,
            text=title,
            command=lambda: self.show_context_menu(title, options, callbacks_dict, main_btn),
            style="Menu.TButton"
        )
        main_btn.pack(pady=3, padx=5, fill=tk.X)
        self.menu_buttons[title] = main_btn

    def create_maintenance_menu(self, parent):
        """Menú especial para Mantenimiento con funciones integradas"""
        # Botón principal
        main_btn = ttk.Button(
            parent,
            text="Mantenimiento",
            command=lambda: self.show_maintenance_menu(main_btn),
            style="Menu.TButton"
        )
        main_btn.pack(pady=3, padx=5, fill=tk.X)
        self.menu_buttons["Mantenimiento"] = main_btn

    def show_context_menu(self, title, options, callbacks_dict, widget):
        """Muestra un menú contextual al hacer clic en el botón"""
        menu = Menu(self, tearoff=0)
        
        for option_text, option_key in options.items():
            menu.add_command(
                label=option_text,
                command=lambda k=option_key: callbacks_dict[k]()
            )
        
        # Mostrar el menú contextual en la posición del botón
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height()
        menu.post(x, y)

    def show_maintenance_menu(self, widget):
        """Muestra el menú de mantenimiento como menú contextual"""
        menu = Menu(self, tearoff=0)
        
        menu.add_command(
            label="Compactar Base de Datos",
            command=self.compress_database
        )
        
        menu.add_command(
            label="Exportar Base de Datos",
            command=self.export_database
        )
        
        menu.add_command(
            label="Importar Base de Datos",
            command=self.import_database
        )
        
        # Mostrar el menú contextual en la posición del botón
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height()
        menu.post(x, y)

    def navigate(self, key):
        """Navegación para botones principales"""
        if key == "exit":
            self.exit()
        elif key in self.main_callbacks:
            self.main_callbacks[key]()

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

    def exit(self):
        SessionManager.logout()
        self.open_login_screen_callback()

    # Funciones de mantenimiento
    def get_db_path(self) -> str:
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(project_dir, 'sqlite_cli', 'database', 'db.db')

    def compress_database(self) -> None:
        confirm = messagebox.askyesno(
            "Compactar Base de Datos",
            "¿Está seguro que desea compactar la base de datos?\n"
            "Esta operación puede mejorar el rendimiento pero tomará unos momentos.",
            parent=self
        )
        
        if not confirm:
            return

        try:
            db_path = self.get_db_path()
            conn = sqlite3.connect(db_path)
            conn.execute("VACUUM")
            conn.close()
            
            messagebox.showinfo(
                "Éxito",
                "Base de datos comprimida exitosamente",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo comprimir la base de datos:\n{str(e)}",
                parent=self
            )

    def export_database(self) -> None:
        default_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar Base de Datos",
            defaultextension=".db",
            initialfile=default_filename,
            filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if not file_path:
            return

        try:
            db_path = self.get_db_path()
            shutil.copyfile(db_path, file_path)
            
            messagebox.showinfo(
                "Éxito",
                f"Base de datos exportada exitosamente a:\n{file_path}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo exportar la base de datos:\n{str(e)}",
                parent=self
            )

    def import_database(self) -> None:
        confirm = messagebox.askyesno(
            "Importar Base de Datos",
            "ADVERTENCIA: Esta operación reemplazará la base de datos actual.\n"
            "¿Desea continuar?",
            parent=self
        )
        
        if not confirm:
            return

        file_path = filedialog.askopenfilename(
            title="Seleccionar Base de Datos",
            filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if not file_path:
            return

        try:
            db_path = self.get_db_path()
            backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_filename = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            shutil.copyfile(db_path, backup_path)
            shutil.copyfile(file_path, db_path)
            
            messagebox.showinfo(
                "Éxito",
                f"Base de datos importada exitosamente desde:\n{file_path}\n\n"
                f"Se creó un backup en:\n{backup_path}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo importar la base de datos:\n{str(e)}",
                parent=self
            )