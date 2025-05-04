import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from PIL import Image, ImageTk
import os
from sqlite_cli.models.catalog_model import CatalogModel  # Importamos el modelo de catálogo

class CatalogScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Productos")
        self.current_image = None
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Configurar el fondo con un color atractivo
        self.configure(bg="#f5f5f5")
        
        # Header con título
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Catálogo de Productos y Servicios",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Frame para botón de regreso
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Frame principal para controles
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame de búsqueda
        search_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Combobox para seleccionar tipo de búsqueda
        search_types = ["Productos", "Servicios"]
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_types,
            state="readonly",
            width=15
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Campo de búsqueda
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 12)
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Frame para el notebook (pestañas)
        notebook_frame = tk.Frame(self, bg="#f5f5f5")
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Crear Notebook (pestañas)
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Frame para productos
        self.products_frame = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.products_frame, text="Productos")

        # Frame para servicios
        self.services_frame = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(self.services_frame, text="Servicios")

        # Configurar el frame de productos
        self.setup_products_frame()
        
        # Configurar el frame de servicios
        self.setup_services_frame()

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def setup_products_frame(self):
        # Canvas y scrollbar para productos
        self.products_canvas = tk.Canvas(self.products_frame, bg="#f5f5f5", highlightthickness=0)
        self.products_scrollbar = ttk.Scrollbar(self.products_frame, orient="vertical", command=self.products_canvas.yview)
        self.products_scrollable_frame = tk.Frame(self.products_canvas, bg="#f5f5f5")

        self.products_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(
                scrollregion=self.products_canvas.bbox("all")
            )
        )

        self.products_canvas.create_window((0, 0), window=self.products_scrollable_frame, anchor="nw")
        self.products_canvas.configure(yscrollcommand=self.products_scrollbar.set)

        self.products_scrollbar.pack(side="right", fill="y")
        self.products_canvas.pack(side="left", fill="both", expand=True)

    def setup_services_frame(self):
        # Canvas y scrollbar para servicios
        self.services_canvas = tk.Canvas(self.services_frame, bg="#f5f5f5", highlightthickness=0)
        self.services_scrollbar = ttk.Scrollbar(self.services_frame, orient="vertical", command=self.services_canvas.yview)
        self.services_scrollable_frame = tk.Frame(self.services_canvas, bg="#f5f5f5")

        self.services_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.services_canvas.configure(
                scrollregion=self.services_canvas.bbox("all")
            )
        )

        self.services_canvas.create_window((0, 0), window=self.services_scrollable_frame, anchor="nw")
        self.services_canvas.configure(yscrollcommand=self.services_scrollbar.set)

        self.services_scrollbar.pack(side="right", fill="y")
        self.services_canvas.pack(side="left", fill="both", expand=True)

    def display_products(self, products: List[Dict]) -> None:
        # Limpiar frame de productos
        for widget in self.products_scrollable_frame.winfo_children():
            widget.destroy()

        if not products:
            no_products_label = CustomLabel(
                self.products_scrollable_frame,
                text="No se encontraron productos",
                font=("Arial", 12),
                fg="#666",
                bg="#f5f5f5"
            )
            no_products_label.pack(pady=20)
            return

        # Mostrar productos en un grid
        row = 0
        col = 0
        max_cols = 3

        for i, product in enumerate(products):
            product_frame = tk.Frame(
                self.products_scrollable_frame,
                bg="white",
                bd=1,
                relief=tk.RAISED,
                padx=10,
                pady=10
            )
            product_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Mostrar imagen si existe
            if product.get('image_path') and os.path.exists(product['image_path']):
                try:
                    img = Image.open(product['image_path'])
                    img.thumbnail((150, 150))
                    photo = ImageTk.PhotoImage(img)
                    
                    img_label = tk.Label(product_frame, image=photo, bg="white")
                    img_label.image = photo  # keep a reference!
                    img_label.pack(pady=(0, 10))
                except Exception as e:
                    print(f"Error loading image: {e}")
                    no_img_label = CustomLabel(
                        product_frame,
                        text="Imagen no disponible",
                        font=("Arial", 10),
                        fg="#999",
                        bg="white"
                    )
                    no_img_label.pack(pady=(0, 10))
            else:
                no_img_label = CustomLabel(
                    product_frame,
                    text="Imagen no disponible",
                    font=("Arial", 10),
                    fg="#999",
                    bg="white"
                )
                no_img_label.pack(pady=(0, 10))

            # Mostrar información del producto
            name_label = CustomLabel(
                product_frame,
                text=product['product'],
                font=("Arial", 12, "bold"),
                fg="#333",
                bg="white"
            )
            name_label.pack()

            price_label = CustomLabel(
                product_frame,
                text=f"Precio: ${product['price']:.2f}",
                font=("Arial", 11),
                fg="#2ecc71",
                bg="white"
            )
            price_label.pack()

            stock_label = CustomLabel(
                product_frame,
                text=f"Disponibles: {product['stock']}",
                font=("Arial", 10),
                fg="#666",
                bg="white"
            )
            stock_label.pack()

            if product.get('expiration_date'):
                exp_label = CustomLabel(
                    product_frame,
                    text=f"Vence: {product['expiration_date']}",
                    font=("Arial", 9),
                    fg="#e74c3c",
                    bg="white"
                )
                exp_label.pack()

            # Actualizar grid
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Configurar grid
        for i in range(row + 1):
            self.products_scrollable_frame.grid_rowconfigure(i, weight=1)
        for i in range(max_cols):
            self.products_scrollable_frame.grid_columnconfigure(i, weight=1)

    def display_services(self, services: List[Dict]) -> None:
        # Limpiar frame de servicios
        for widget in self.services_scrollable_frame.winfo_children():
            widget.destroy()

        if not services:
            no_services_label = CustomLabel(
                self.services_scrollable_frame,
                text="No se encontraron servicios",
                font=("Arial", 12),
                fg="#666",
                bg="#f5f5f5"
            )
            no_services_label.pack(pady=20)
            return

        # Mostrar servicios en un grid
        row = 0
        col = 0
        max_cols = 3

        for i, service in enumerate(services):
            service_frame = tk.Frame(
                self.services_scrollable_frame,
                bg="white",
                bd=1,
                relief=tk.RAISED,
                padx=15,
                pady=15
            )
            service_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Mostrar icono de servicio
            service_icon = CustomLabel(
                service_frame,
                text="⚙️",
                font=("Arial", 24),
                bg="white"
            )
            service_icon.pack(pady=(0, 10))

            # Mostrar información del servicio
            name_label = CustomLabel(
                service_frame,
                text=service['name'],
                font=("Arial", 12, "bold"),
                fg="#333",
                bg="white"
            )
            name_label.pack()

            price_label = CustomLabel(
                service_frame,
                text=f"Precio: ${service['price']:.2f}",
                font=("Arial", 11),
                fg="#2ecc71",
                bg="white"
            )
            price_label.pack()

            if service.get('description'):
                desc_label = CustomLabel(
                    service_frame,
                    text=service['description'],
                    font=("Arial", 10),
                    fg="#666",
                    bg="white",
                    wraplength=200
                )
                desc_label.pack()

            # Actualizar grid
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Configurar grid
        for i in range(row + 1):
            self.services_scrollable_frame.grid_rowconfigure(i, weight=1)
        for i in range(max_cols):
            self.services_scrollable_frame.grid_columnconfigure(i, weight=1)

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        search_type = self.search_field_var.get()
        
        if search_type == "Productos":
            # Usamos el modelo de catálogo para obtener productos
            if search_term:
                products = CatalogModel.search_products(search_term)
            else:
                products = CatalogModel.get_all_products()
                
            self.display_products(products)
            self.notebook.select(self.products_frame)
            self.status_bar.configure(text=f"Mostrando {len(products)} productos")
        else:
            # Usamos el modelo de catálogo para obtener servicios
            if search_term:
                services = CatalogModel.search_services(search_term)
            else:
                services = CatalogModel.get_all_services()
                
            self.display_services(services)
            self.notebook.select(self.services_frame)
            self.status_bar.configure(text=f"Mostrando {len(services)} servicios")

    def refresh_data(self) -> None:
        """Actualiza los datos del catálogo"""
        self.search_var.set("")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()