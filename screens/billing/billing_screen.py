import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any, Optional
from sqlite_cli.models.invoice_model import Invoice
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.tax_model import Tax
from sqlite_cli.models.currency_model import Currency
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
        
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Facturación",
            font=("Arial", 16, "bold"),
            fg="#333"
        )
        title_label.pack(side=tk.LEFT)

        # Frame principal para botones y búsqueda
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Frame de botones (izquierda)
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT)

        btn_cancel = CustomButton(
            button_frame,
            text="Cancelar Compra",
            command=self.cancel_purchase,
            padding=8,
            width=18
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_checkout = CustomButton(
            button_frame,
            text="Realizar Compra",
            command=self.checkout,
            padding=8,
            width=18
        )
        btn_checkout.pack(side=tk.LEFT, padx=5)

        # Frame de búsqueda de cliente (centro)
        customer_frame = tk.Frame(top_frame)
        customer_frame.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        lbl_customer = CustomLabel(
            customer_frame,
            text="Cédula Cliente:",
            font=("Arial", 10),
            fg="#555"
        )
        lbl_customer.pack(side=tk.LEFT, padx=5)

        self.entry_customer = CustomEntry(
            customer_frame,
            textvariable=self.customer_id_var,
            width=20
        )
        self.entry_customer.pack(side=tk.LEFT, padx=5)

        btn_search_customer = CustomButton(
            customer_frame,
            text="Buscar",
            command=self.search_customer,
            padding=4,
            width=8
        )
        btn_search_customer.pack(side=tk.LEFT, padx=5)

        self.lbl_customer_info = CustomLabel(
            customer_frame,
            text="",
            font=("Arial", 10, "bold"),
            fg="#333"
        )
        self.lbl_customer_info.pack(side=tk.LEFT, padx=10)

        # Frame de búsqueda de productos (abajo del frame de cliente)
        search_frame = tk.Frame(self)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.on_search)

        search_fields = [
            "Todos los campos",
            "ID",
            "Código",
            "Producto",
            "Existencias",
            "Precio"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_fields,
            state="readonly",
            width=20
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Frame para las tablas
        tables_frame = tk.Frame(self)
        tables_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview para productos disponibles
        lbl_products = CustomLabel(
            tables_frame,
            text="Productos Disponibles",
            font=("Arial", 12),
            fg="#333"
        )
        lbl_products.pack(anchor=tk.W)

        products_frame = tk.Frame(tables_frame)
        products_frame.pack(fill=tk.X, pady=(0, 20))

        self.products_tree = ttk.Treeview(products_frame, columns=(
            "ID", "Código", "Producto", "Existencias", "Stock mínimo", 
            "Stock máximo", "Precio"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Existencias", 80, tk.CENTER),
            ("Stock mínimo", 80, tk.CENTER),
            ("Stock máximo", 80, tk.CENTER),
            ("Precio", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        self.products_tree.bind("<Button-1>", self.on_product_click)

        # Treeview para carrito de compras
        lbl_cart = CustomLabel(
            tables_frame,
            text="Carrito de Compras",
            font=("Arial", 12),
            fg="#333"
        )
        lbl_cart.pack(anchor=tk.W)

        cart_frame = tk.Frame(tables_frame)
        cart_frame.pack(fill=tk.X)

        self.cart_tree = ttk.Treeview(cart_frame, columns=(
            "ID", "Producto", "Cantidad", "Precio Unitario", "Total", "Acción"
        ), show="headings")

        cart_columns = [
            ("ID", 50, tk.CENTER),
            ("Producto", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Precio Unitario", 100, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Acción", 80, tk.CENTER)
        ]

        for col, width, anchor in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=width, anchor=anchor)

        cart_scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        self.cart_tree.bind("<Button-1>", self.on_cart_item_click)

        # Frame para totales
        totals_frame = tk.Frame(self)
        totals_frame.pack(fill=tk.X, padx=10, pady=10)

        # Obtener información de impuestos y monedas
        iva_tax = Tax.get_by_name("IVA")
        dollar = Currency.get_by_name("Dólar")
        euro = Currency.get_by_name("Euro")

        # Mostrar u ocultar según estén activos
        if iva_tax and iva_tax.get('status_name') == 'active':
            self.lbl_subtotal = CustomLabel(
                totals_frame,
                text="Subtotal: 0.00",
                font=("Arial", 10, "bold"),
                fg="#333"
            )
            self.lbl_subtotal.pack(side=tk.LEFT, padx=10)

            self.lbl_iva = CustomLabel(
                totals_frame,
                text=f"IVA ({iva_tax['value']}%): 0.00",
                font=("Arial", 10, "bold"),
                fg="#333"
            )
            self.lbl_iva.pack(side=tk.LEFT, padx=10)

        self.lbl_total = CustomLabel(
            totals_frame,
            text="Total: 0.00",
            font=("Arial", 10, "bold"),
            fg="#333"
        )
        self.lbl_total.pack(side=tk.LEFT, padx=10)

        if dollar and dollar.get('status_name') == 'active':
            self.lbl_dollar = CustomLabel(
                totals_frame,
                text="Dólares: $0.00",
                font=("Arial", 10),
                fg="#666"
            )
            self.lbl_dollar.pack(side=tk.LEFT, padx=10)

        if euro and euro.get('status_name') == 'active':
            self.lbl_euro = CustomLabel(
                totals_frame,
                text="Euros: €0.00",
                font=("Arial", 10),
                fg="#666"
            )
            self.lbl_euro.pack(side=tk.LEFT, padx=10)

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        items = InventoryItem.search_active(search_term, field if field != "Todos los campos" else None)
        
        for item in items:
            self.products_tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['stock'],
                item['min_stock'],
                item['max_stock'],
                f"{float(item['price']):.2f}" if item['price'] else "0.00"
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(items)} productos disponibles")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.customer_id_var.set("")
        self.lbl_customer_info.configure(text="")
        self.current_customer = None
        self.cart_items = []
        self.update_cart_tree()
        self.on_search()
        self.update_totals()

    def cancel_purchase(self) -> None:
        if not self.cart_items:
            self.go_back()
            return
            
        response = messagebox.askyesno(
            "Cancelar Compra", 
            "¿Está seguro que desea cancelar la compra? Se perderán todos los productos seleccionados.",
            parent=self
        )
        
        if response:
            self.refresh_data()
            self.go_back()

    def go_back(self) -> None:
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()

    # screens/billing/billing_screen.py (solo el método checkout modificado)
    def checkout(self) -> None:
        if not self.current_customer:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para realizar la compra", parent=self)
            return
            
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un producto al carrito", parent=self)
            return
            
        response = messagebox.askyesno(
            "Confirmar Compra", 
            "¿Está seguro que desea realizar la compra?\nLa factura se marcará como Pagada Completamente.",
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
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price'],
                    'total': item['total']
                } for item in self.cart_items]
                
                # Crear la factura como pagada completamente
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
                    f"Compra realizada y facturada correctamente\nNúmero de factura: {invoice_id}\nEstado: Pagada completamente",
                    parent=self
                )
                
                # Limpiar y actualizar
                self.refresh_data()
                
            except ValueError as e:
                messagebox.showerror("Error de validación", str(e), parent=self)
            except Exception as e:
                messagebox.showerror(
                    "Error", 
                    f"No se pudo completar la compra: {str(e)}", 
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
        existing_item = next((item for item in self.cart_items if item['id'] == item_id), None)
        
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
                        'total': quantity * price
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

    def validate_quantity(self, text: str) -> bool:
        if not text:
            return True
        return text.isdigit()

    def update_cart_tree(self) -> None:
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        for item in self.cart_items:
            self.cart_tree.insert("", tk.END, values=(
                item['id'],
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
        
        if column == "#6":  # Columna de acción
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
        
        # Calcular totales
        if iva_tax and iva_tax.get('status_name') == 'active':
            iva_amount = subtotal * (iva_tax['value'] / 100)
            total = subtotal + iva_amount
            
            self.lbl_subtotal.configure(text=f"Subtotal: {subtotal:.2f}")
            self.lbl_iva.configure(text=f"IVA ({iva_tax['value']}%): {iva_amount:.2f}")
        else:
            total = subtotal
        
        self.lbl_total.configure(text=f"Total: {total:.2f}")
        
        if dollar and dollar.get('status_name') == 'active':
            dollar_amount = total / dollar['value'] if dollar['value'] != 0 else 0
            self.lbl_dollar.configure(text=f"Dólares: ${dollar_amount:.2f}")
        
        if euro and euro.get('status_name') == 'active':
            euro_amount = total / euro['value'] if euro['value'] != 0 else 0
            self.lbl_euro.configure(text=f"Euros: €{euro_amount:.2f}")