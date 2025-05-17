import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any, Optional
from reports.InvoiceViewer import InvoiceViewer
from sqlite_cli.models.invoice_model import Invoice
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.tax_model import Tax
from sqlite_cli.models.currency_model import Currency
from sqlite_cli.models.service_model import Service
from screens.customers.crud_customer import CrudCustomer

class BillingScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.customer_id_var = tk.StringVar()
        self.cart_items = []
        self.current_customer = None
        
        # Configuración de estilos
        self.configure(bg="#f5f5f5")  # Fondo general
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        """Configura la interfaz de usuario con estilos mejorados"""
        # Encabezado azul
        header_frame = tk.Frame(self, bg="#4a6fa5", height=80)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Título del sistema
        title_label = CustomLabel(
            header_frame,
            text="Ventas",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Frame principal para controles
        controls_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame de búsqueda de cliente
        customer_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        customer_frame.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        lbl_customer = CustomLabel(
            customer_frame,
            text="Cédula Cliente:",
            font=("Arial", 12),
            fg="#555",
            bg="#f5f5f5"
        )
        lbl_customer.pack(side=tk.LEFT, padx=5)

        self.entry_customer = CustomEntry(
            customer_frame,
            textvariable=self.customer_id_var,
            font=("Arial", 12),
            width=20
        )
        self.entry_customer.pack(side=tk.LEFT, padx=5)

        btn_search_customer = CustomButton(
            customer_frame,
            text="Buscar",
            command=self.search_customer,
            padding=6,
            width=10
        )
        btn_search_customer.pack(side=tk.LEFT, padx=5)

        self.lbl_customer_info = CustomLabel(
            customer_frame,
            text="Seleccione un cliente",
            font=("Arial", 12, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        self.lbl_customer_info.pack(side=tk.LEFT, padx=10)

        # Frame de acciones
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        btn_cancel = CustomButton(
            action_frame,
            text="Cancelar Venta",
            command=self.cancel_purchase,
            padding=8,
            width=18
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_checkout = CustomButton(
            action_frame,
            text="Realizar Venta",
            command=self.checkout,
            padding=8,
            width=18
        )
        btn_checkout.pack(side=tk.LEFT, padx=5)

        # Frame de búsqueda de productos/servicios
        search_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=5)
        search_frame.pack(side=tk.TOP, fill=tk.X)

        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.on_search)

        search_fields = [
            "Todos los campos",
            "ID",
            "Código",
            "Nombre",
            "Existencias",
            "Precio"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_fields,
            state="readonly",
            width=20,
            font=("Arial", 12)
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Frame para las tablas
        tables_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        tables_frame.pack(fill=tk.BOTH, expand=True)

        # Create Notebook (tabs)
        self.catalog_notebook = ttk.Notebook(tables_frame)
        self.catalog_notebook.pack(fill=tk.BOTH, expand=True)

        # Products tab
        products_tab = tk.Frame(self.catalog_notebook, bg="#f5f5f5")
        self.catalog_notebook.add(products_tab, text="Productos")

        # Services tab
        services_tab = tk.Frame(self.catalog_notebook, bg="#f5f5f5")
        self.catalog_notebook.add(services_tab, text="Servicios")

        # Treeview para productos disponibles
        lbl_products = CustomLabel(
            products_tab,
            text="Productos Disponibles",
            font=("Arial", 14),
            fg="#333",
            bg="#f5f5f5"
        )
        lbl_products.pack(anchor=tk.W)

        products_frame = tk.Frame(products_tab)
        products_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.products_tree = ttk.Treeview(
            products_frame, 
            columns=("ID", "Código", "Producto", "Existencias", "Stock mínimo", "Stock máximo", "Precio"),
            show="headings",
            height=5,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 200, tk.W),
            ("Existencias", 80, tk.CENTER),
            ("Stock mínimo", 80, tk.CENTER),
            ("Stock máximo", 80, tk.CENTER),
            ("Precio", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(
            products_frame, 
            orient=tk.VERTICAL, 
            command=self.products_tree.yview
        )
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        self.products_tree.bind("<Button-1>", self.on_product_click)

        # Treeview para servicios disponibles
        lbl_services = CustomLabel(
            services_tab,
            text="Servicios Disponibles",
            font=("Arial", 14),
            fg="#333",
            bg="#f5f5f5"
        )
        lbl_services.pack(anchor=tk.W)

        services_frame = tk.Frame(services_tab)
        services_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.services_tree = ttk.Treeview(
            services_frame, 
            columns=("ID", "Código", "Servicio", "Precio", "Descripción"),
            show="headings",
            height=5,
            style="Custom.Treeview"
        )

        service_columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Servicio", 200, tk.W),
            ("Precio", 100, tk.CENTER),
            ("Descripción", 300, tk.W)
        ]

        for col, width, anchor in service_columns:
            self.services_tree.heading(col, text=col)
            self.services_tree.column(col, width=width, anchor=anchor)

        service_scrollbar = ttk.Scrollbar(
            services_frame, 
            orient=tk.VERTICAL, 
            command=self.services_tree.yview
        )
        self.services_tree.configure(yscroll=service_scrollbar.set)
        service_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.services_tree.pack(fill=tk.BOTH, expand=True)
        self.services_tree.bind("<Button-1>", self.on_service_click)

        # Treeview para carrito de compras
        lbl_cart = CustomLabel(
            tables_frame,
            text="Carrito de Compras",
            font=("Arial", 14),
            fg="#333",
            bg="#f5f5f5"
        )
        lbl_cart.pack(anchor=tk.W)

        cart_frame = tk.Frame(tables_frame)
        cart_frame.pack(fill=tk.X)

        self.cart_tree = ttk.Treeview(
            cart_frame, 
            columns=("ID", "Tipo", "Nombre", "Cantidad", "Precio Unitario", "Total", "Acción"),
            show="headings",
            height=5,
            style="Custom.Treeview"
        )

        cart_columns = [
            ("ID", 50, tk.CENTER),
            ("Tipo", 80, tk.CENTER),
            ("Nombre", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Precio Unitario", 120, tk.CENTER),
            ("Total", 120, tk.CENTER),
            ("Acción", 80, tk.CENTER)
        ]

        for col, width, anchor in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=width, anchor=anchor)

        cart_scrollbar = ttk.Scrollbar(
            cart_frame, 
            orient=tk.VERTICAL, 
            command=self.cart_tree.yview
        )
        self.cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        self.cart_tree.bind("<Button-1>", self.on_cart_item_click)

        # Frame para totales
        totals_frame = tk.Frame(self, bg="#4a6fa5", padx=20, pady=10)
        totals_frame.pack(fill=tk.X)

        # Inicializar todos los labels de totales (siempre se crean)
        self.lbl_subtotal = CustomLabel(
            totals_frame,
            text="Subtotal: 0.00",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        
        self.lbl_iva = CustomLabel(
            totals_frame,
            text="IVA (0%): 0.00",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        
        self.lbl_total = CustomLabel(
            totals_frame,
            text="Total: 0.00",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        
        self.lbl_dollar = CustomLabel(
            totals_frame,
            text="Dólares: $0.00",
            font=("Arial", 12),
            fg="white",
            bg="#4a6fa5"
        )
        
        self.lbl_euro = CustomLabel(
            totals_frame,
            text="Euros: €0.00",
            font=("Arial", 12),
            fg="white",
            bg="#4a6fa5"
        )
        
        # Verificar qué impuestos/divisas están activos y mostrar los labels correspondientes
        iva_tax = Tax.get_by_name("IVA")
        dollar = Currency.get_by_name("Dólar")
        euro = Currency.get_by_name("Euro")
        
        if iva_tax and iva_tax.get('status_name') == 'active':
            self.lbl_subtotal.pack(side=tk.LEFT, padx=10)
            self.lbl_iva.pack(side=tk.LEFT, padx=10)
            self.lbl_iva.configure(text=f"IVA ({iva_tax['value']}%): 0.00")
        
        self.lbl_total.pack(side=tk.LEFT, padx=10)
        
        if dollar and dollar.get('status_name') == 'active':
            self.lbl_dollar.pack(side=tk.LEFT, padx=10)
        
        if euro and euro.get('status_name') == 'active':
            self.lbl_euro.pack(side=tk.LEFT, padx=10)

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        # Clear both trees
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        # Search products
        products = InventoryItem.search_active(
            search_term, 
            field if field != "Todos los campos" else None
        )
        
        for item in products:
            self.products_tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['stock'],
                item['min_stock'],
                item['max_stock'],
                f"{float(item['price']):.2f}" if item['price'] else "0.00"
            ))
        
        # Search services
        services = Service.search_active(
            search_term,
            field if field != "Todos los campos" else None
        )
        
        for service in services:
            self.services_tree.insert("", tk.END, values=(
                service['id'],
                service['code'],
                service['name'],
                f"{service['price']:.2f}",
                service.get('description', '')[:50] + "..." if service.get('description') else ""
            ))
        
        self.status_bar.configure(
            text=f"Mostrando {len(products)} productos y {len(services)} servicios disponibles"
        )

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.customer_id_var.set("")
        self.lbl_customer_info.configure(text="Seleccione un cliente")
        self.current_customer = None
        self.cart_items = []
        self.update_cart_tree()
        self.on_search()
        self.update_totals()
        self.catalog_notebook.select(0)  # Select products tab by default

    def cancel_purchase(self) -> None:
        if not self.cart_items:
            self.go_back()
            return
            
        response = messagebox.askyesno(
            "Cancelar Venta", 
            "¿Está seguro que desea cancelar la venta? Se perderán todos los productos seleccionados.",
            parent=self
        )
        
        if response:
            self.refresh_data()
            self.go_back()

    def go_back(self) -> None:
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()

    def checkout(self) -> None:
        if not self.current_customer:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para realizar la venta", parent=self)
            return
            
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un producto o servicio al carrito", parent=self)
            return
            
        response = messagebox.askyesno(
            "Confirmar Venta", 
            "¿Está seguro que desea realizar la venta?\nLa factura se marcará como Pagada Completamente.",
            parent=self
        )
        
        if response:
            try:
                # Calcular totales
                iva_tax = Tax.get_by_name("IVA")
                subtotal = sum(item['total'] for item in self.cart_items)
                
                if iva_tax and iva_tax.get('status_name') == 'active':
                    taxes = subtotal * (iva_tax['value'] / 100)
                else:
                    taxes = 0.0
                    
                total = subtotal + taxes
                
                # Preparar items para la factura
                invoice_items = [{
                    'id': item['id'],
                    'name': item['name'],
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price'],
                    'total': item['total'],
                    'is_service': item.get('is_service', False)
                } for item in self.cart_items]
                
                # Crear la factura como pagada completamente (tipo Venta)
                invoice_id = Invoice.create_paid_invoice(
                    customer_id=self.current_customer['id'],
                    subtotal=subtotal,
                    taxes=taxes,
                    total=total,
                    items=invoice_items
                )
                
                # Mostrar mensaje de éxito con el número de factura
                messagebox.showinfo(
                    "Éxito", 
                    f"Venta realizada y facturada correctamente\nNúmero de factura: {invoice_id}\nEstado: Pagada completamente",
                    parent=self
                )
                
                # Mostrar factura digital
                customer_info = f"{self.current_customer['first_name']} {self.current_customer['last_name']} - {self.current_customer['id_number']}"
                InvoiceViewer(
                    self,
                    invoice_id,
                    customer_info,
                    invoice_items,
                    subtotal,
                    taxes,
                    total
                )
                
                # Limpiar y actualizar
                self.refresh_data()
                
            except ValueError as e:
                messagebox.showerror("Error de validación", str(e), parent=self)
            except Exception as e:
                messagebox.showerror(
                    "Error", 
                    f"No se pudo completar la venta: {str(e)}", 
                    parent=self
                )

    def search_customer(self) -> None:
        id_number = self.customer_id_var.get().strip()
        if not id_number:
            messagebox.showwarning("Advertencia", "Ingrese una cédula para buscar", parent=self)
            return
        
        try:
            customer = Customer.get_by_id_number(id_number)
            if customer:
                self.current_customer = customer
                self.lbl_customer_info.configure(
                    text=f"{customer['first_name']} {customer['last_name']} - {customer['id_number']}"
                )
            else:
                response = messagebox.askyesno(
                    "Cliente no encontrado", 
                    "El cliente no está registrado. ¿Desea registrarlo ahora?",
                    parent=self
                )
                if response:
                    self.register_new_customer(id_number)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el cliente: {str(e)}", parent=self)

    def register_new_customer(self, id_number: str) -> None:
        def on_customer_created():
            self.search_customer()  # Volver a buscar después de crear

        CrudCustomer(
            self,
            mode="create",
            initial_id_number=id_number,
            refresh_callback=on_customer_created
        )

    def on_product_click(self, event) -> None:
        if not self.current_customer:
            messagebox.showwarning(
                "Cliente requerido", 
                "Debe seleccionar un cliente antes de agregar productos al carrito.\n"
                "Por favor busque o registre un cliente usando el campo de cédula.",
                parent=self
            )
            return
        
        selected = self.products_tree.identify_row(event.y)
        if not selected:
            return
            
        item_data = self.products_tree.item(selected)['values']
        item_id = item_data[0]
        product_name = item_data[2]
        stock = int(item_data[3])
        min_stock = int(item_data[4])
        max_stock = int(item_data[5])
        price = float(item_data[6])
        
        # Verificar si el producto ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['id'] == item_id and not item.get('is_service', False)), None)
        
        # Crear ventana para seleccionar cantidad
        quantity_window = tk.Toplevel(self)
        quantity_window.title(f"Agregar {product_name}")
        
        # Calcular posición para centrar la ventana
        window_width = 350
        window_height = 325
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        quantity_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        quantity_window.resizable(False, False)
        quantity_window.transient(self)
        quantity_window.grab_set()
        
        # Frame principal para mejor organización
        main_frame = tk.Frame(quantity_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del producto
        tk.Label(
            main_frame, 
            text=f"Producto: {product_name}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        tk.Label(
            main_frame, 
            text=f"Existencias: {stock}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        tk.Label(
            main_frame, 
            text=f"Rango permitido: {min_stock} - {max_stock}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        tk.Label(
            main_frame, 
            text=f"Precio unitario: {price:.2f}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        # Frame para cantidad
        quantity_frame = tk.Frame(main_frame)
        quantity_frame.pack(pady=10)
        
        tk.Label(
            quantity_frame, 
            text="Cantidad:",
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        quantity_var = tk.StringVar(value=str(min_stock if not existing_item else existing_item['quantity']))
        quantity_entry = CustomEntry(
            quantity_frame,
            textvariable=quantity_var,
            font=("Arial", 10),
            width=10,
            validate="key",
            validatecommand=(quantity_window.register(self.validate_quantity), '%P')
        )
        quantity_entry.pack(side=tk.LEFT, padx=5)
        
        def add_to_cart():
            try:
                quantity = int(quantity_var.get())
                
                if quantity < min_stock:
                    messagebox.showwarning(
                        "Advertencia", 
                        f"La cantidad mínima permitida es {min_stock}", 
                        parent=quantity_window
                    )
                    return
                    
                if quantity > max_stock:
                    messagebox.showwarning(
                        "Advertencia", 
                        f"La cantidad máxima permitida es {max_stock}", 
                        parent=quantity_window
                    )
                    return
                    
                if quantity > stock:
                    messagebox.showwarning(
                        "Advertencia", 
                        "No hay suficiente stock disponible", 
                        parent=quantity_window
                    )
                    return
                    
                # Actualizar o agregar al carrito
                if existing_item:
                    existing_item['quantity'] = quantity
                    existing_item['total'] = quantity * price
                else:
                    self.cart_items.append({
                        'id': item_id,
                        'name': product_name,
                        'quantity': quantity,
                        'unit_price': price,
                        'total': quantity * price,
                        'is_service': False
                    })
                
                self.update_cart_tree()
                self.update_totals()
                quantity_window.destroy()
                
            except ValueError:
                messagebox.showwarning(
                    "Advertencia", 
                    "Ingrese una cantidad válida", 
                    parent=quantity_window
                )
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        CustomButton(
            btn_frame,
            text="Agregar",
            command=add_to_cart,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=quantity_window.destroy,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Poner foco en el campo de cantidad
        quantity_entry.focus_set()

    def on_service_click(self, event) -> None:
        if not self.current_customer:
            messagebox.showwarning(
                "Cliente requerido", 
                "Debe seleccionar un cliente antes de agregar servicios al carrito.\n"
                "Por favor busque o registre un cliente usando el campo de cédula.",
                parent=self
            )
            return
        
        selected = self.services_tree.identify_row(event.y)
        if not selected:
            return
            
        item_data = self.services_tree.item(selected)['values']
        item_id = item_data[0]
        service_name = item_data[2]
        price = float(item_data[3])
        
        # Verificar si el servicio ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['id'] == item_id and item.get('is_service', False)), None)
        
        # Crear ventana para confirmar agregar servicio
        confirm_window = tk.Toplevel(self)
        confirm_window.title(f"Agregar {service_name}")
        
        # Calcular posición para centrar la ventana
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        confirm_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        confirm_window.resizable(False, False)
        confirm_window.transient(self)
        confirm_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(confirm_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del servicio
        tk.Label(
            main_frame, 
            text=f"Servicio: {service_name}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        tk.Label(
            main_frame, 
            text=f"Precio: {price:.2f}",
            font=("Arial", 10)
        ).pack(pady=5)
        
        def add_to_cart():
            # Actualizar o agregar al carrito
            if existing_item:
                existing_item['quantity'] += 1
                existing_item['total'] = existing_item['quantity'] * price
            else:
                self.cart_items.append({
                    'id': item_id,
                    'name': service_name,
                    'quantity': 1,
                    'unit_price': price,
                    'total': price,
                    'is_service': True
                })
            
            self.update_cart_tree()
            self.update_totals()
            confirm_window.destroy()
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        CustomButton(
            btn_frame,
            text="Agregar",
            command=add_to_cart,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=confirm_window.destroy,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)

    def validate_quantity(self, text: str) -> bool:
        if not text:
            return True
        return text.isdigit()

    def update_cart_tree(self) -> None:
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        for item in self.cart_items:
            item_type = "Servicio" if item.get('is_service', False) else "Producto"
            self.cart_tree.insert("", tk.END, values=(
                item['id'],
                item_type,
                item['name'],
                item['quantity'],
                f"{item['unit_price']:.2f}",
                f"{item['total']:.2f}",
                "Eliminar"
            ))
        
        # Configurar evento para el botón eliminar
        self.cart_tree.bind("<Button-1>", self.on_cart_item_click)

    def on_cart_item_click(self, event) -> None:
        region = self.cart_tree.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        column = self.cart_tree.identify_column(event.x)
        selected = self.cart_tree.identify_row(event.y)
        
        if column == "#7":  # Columna de acción
            item_id = self.cart_tree.item(selected)['values'][0]
            self.remove_from_cart(item_id)

    def remove_from_cart(self, item_id: int) -> None:
        self.cart_items = [item for item in self.cart_items if item['id'] != item_id]
        self.update_cart_tree()
        self.update_totals()

    def update_totals(self) -> None:
        subtotal = sum(item['total'] for item in self.cart_items)
        
        # Obtener impuestos y monedas
        iva_tax = Tax.get_by_name("IVA")
        dollar = Currency.get_by_name("Dólar")
        euro = Currency.get_by_name("Euro")
        
        # Actualizar labels según estén activos
        if iva_tax and iva_tax.get('status_name') == 'active':
            iva_amount = subtotal * (iva_tax['value'] / 100)
            total = subtotal + iva_amount
            
            self.lbl_subtotal.configure(text=f"Subtotal: {subtotal:.2f}")
            self.lbl_iva.configure(text=f"IVA ({iva_tax['value']}%): {iva_amount:.2f}")
            self.lbl_subtotal.pack(side=tk.LEFT, padx=10)
            self.lbl_iva.pack(side=tk.LEFT, padx=10)
        else:
            total = subtotal
            self.lbl_subtotal.pack_forget()
            self.lbl_iva.pack_forget()
        
        self.lbl_total.configure(text=f"Total: {total:.2f}")
        
        if dollar and dollar.get('status_name') == 'active':
            dollar_amount = total / dollar['value'] if dollar['value'] != 0 else 0
            self.lbl_dollar.configure(text=f"Dólares: ${dollar_amount:.2f}")
            self.lbl_dollar.pack(side=tk.LEFT, padx=10)
        else:
            self.lbl_dollar.pack_forget()
        
        if euro and euro.get('status_name') == 'active':
            euro_amount = total / euro['value'] if euro['value'] != 0 else 0
            self.lbl_euro.configure(text=f"Euros: €{euro_amount:.2f}")
            self.lbl_euro.pack(side=tk.LEFT, padx=10)
        else:
            self.lbl_euro.pack_forget()