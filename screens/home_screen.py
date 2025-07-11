import tkinter as tk
from tkinter import Menu, ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
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
        self.menu_buttons = {}
        self.carousel_images = []
        self.current_image_index = 0
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        if not SessionManager.is_authenticated():
            self.open_login_screen_callback()
            return

        window_width = 1000  # Aumentado para acomodar imágenes más grandes
        window_height = 700  # Aumentado para acomodar imágenes más grandes

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
        header_frame = tk.Frame(self, bg="white", height=80)  # Aumentado para imagen más grande
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Imagen de la empresa (principal) - más grande (80x80)
        self.load_image(header_frame, "assets/empresa.png", (80, 80)).pack(side=tk.LEFT, padx=10)
        
        # Título
        title = tk.Label(
            header_frame, 
            text="Gestión de Ventas y Servicios",
            font=("Arial", 16, "bold"),  # Tamaño de fuente aumentado
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
        menu_frame = tk.Frame(main_frame, bg="#f0f0f0", width=220)  # Ancho aumentado
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
                "Reporte de Productos": "full_inventory_report"
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

        # Área del carrusel de imágenes
        carousel_frame = tk.Frame(main_frame, bg="white")
        carousel_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para la imagen del carrusel (sin bordes)
        self.image_container = tk.Frame(carousel_frame, bg="white")
        self.image_container.pack(expand=True, fill=tk.BOTH)

        # Cargar imágenes del carrusel
        self.load_carousel_images()
        
        # Mostrar la primera imagen
        self.show_current_image()

        # Programar el cambio automático de imágenes (8 segundos en lugar de 5)
        self.after(8000, self.rotate_carousel)

        # Pie de página con imágenes
        bottom_frame = tk.Frame(self, bg="white", height=70)  # Aumentado para imágenes más grandes
        bottom_frame.pack(fill=tk.X, pady=(0,5))
        
        # Imagen izquierda - más grande (60x60)
        self.load_image(bottom_frame, "assets/republica.png", (60, 60)).pack(side=tk.LEFT, padx=15)
        
        # Espacio central
        tk.Frame(bottom_frame, bg="white").pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Imagen derecha - más grande (60x60)
        self.load_image(bottom_frame, "assets/universidad.png", (60, 60)).pack(side=tk.RIGHT, padx=15)

    def create_rounded_image(self, image_path, size):
        """Crea una imagen con bordes redondeados"""
        img = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
        
        # Crear máscara para bordes redondeados
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + size, radius=20, fill=255)
        
        # Aplicar máscara
        result = Image.new('RGBA', size)
        result.paste(img, (0, 0), mask)
        
        return ImageTk.PhotoImage(result)

    def load_carousel_images(self):
        """Carga las imágenes del carrusel desde la carpeta assets/carrusel"""
        try:
            for i in range(1, 7):  # Imágenes del 1.png al 6.png
                img_path = f"assets/carrusel/{i}.png"
                # Tamaño más grande (750x450) con bordes redondeados
                photo = self.create_rounded_image(img_path, (750, 450))
                self.carousel_images.append(photo)
        except Exception as e:
            print(f"Error cargando imágenes del carrusel: {e}")
            # Si hay error, crear imagen de respaldo con bordes redondeados
            backup_img = Image.new('RGB', (750, 450), color='white')
            mask = Image.new('L', (750, 450), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, 750, 450), radius=20, fill=255)
            result = Image.new('RGBA', (750, 450))
            result.paste(backup_img, (0, 0), mask)
            photo = ImageTk.PhotoImage(result)
            self.carousel_images = [photo] * 6

    def show_current_image(self):
        """Muestra la imagen actual del carrusel"""
        if hasattr(self, 'current_image_label'):
            self.current_image_label.destroy()

        if not self.carousel_images:
            return

        self.current_image_label = tk.Label(
            self.image_container,
            image=self.carousel_images[self.current_image_index],
            bg="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.current_image_label.pack(expand=True, fill=tk.BOTH)

    def rotate_carousel(self):
        """Rota las imágenes del carrusel automáticamente"""
        if not self.carousel_images:
            return

        self.current_image_index = (self.current_image_index + 1) % len(self.carousel_images)
        self.show_current_image()
        
        # Programar el próximo cambio (8 segundos en lugar de 5)
        self.after(8000, self.rotate_carousel)

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