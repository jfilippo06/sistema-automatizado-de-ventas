import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Any, Callable
from sqlite_cli.models.purchase_order_model import PurchaseOrder
from sqlite_cli.models.inventory_model import InventoryItem
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class PurchaseOrdersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.current_supplier_id = None  # To store the selected supplier ID
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Órden de Compra",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Buttons in header
        buttons_frame = tk.Frame(header_frame, bg="#4a6fa5")
        buttons_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_view_orders = CustomButton(
            buttons_frame,
            text="Ver Órdenes",
            command=self.view_orders,
            padding=8,
            width=12,
        )
        btn_view_orders.pack(side=tk.RIGHT, padx=5)

        btn_search_product = CustomButton(
            buttons_frame,
            text="Buscar Producto",
            command=self.search_product,
            padding=8,
            width=12,
        )
        btn_search_product.pack(side=tk.RIGHT, padx=5)

        btn_search_supplier = CustomButton(
            buttons_frame,
            text="Buscar Proveedor",
            command=self.open_suppliers_search,
            padding=8,
            width=12,
        )
        btn_search_supplier.pack(side=tk.RIGHT, padx=5)

        btn_back = CustomButton(
            buttons_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Main form container
        form_frame = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief=tk.SUNKEN)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Document header
        doc_header_frame = tk.Frame(form_frame, bg="white")
        doc_header_frame.pack(fill=tk.X, pady=10)

        # Order number (right)
        order_num_frame = tk.Frame(doc_header_frame, bg="white")
        order_num_frame.pack(side=tk.RIGHT)

        CustomLabel(
            order_num_frame,
            text="ORDEN DE COMPRA N°:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)

        self.order_number_entry = CustomEntry(
            order_num_frame,
            font=("Arial", 12, "bold"),
            width=15,
        )
        self.order_number_entry.pack(side=tk.LEFT, padx=5)
        self.order_number_entry.insert(0, PurchaseOrder.get_next_order_number())

        # Company info (left)
        company_frame = tk.Frame(doc_header_frame, bg="white")
        company_frame.pack(side=tk.LEFT)

        CustomLabel(
            company_frame,
            text="EMPRESA XYZ, C.A.",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        CustomLabel(
            company_frame,
            text="RIF: J-12345678-9",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)

        CustomLabel(
            company_frame,
            text="Av. Principal, Edif. Empresarial",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)

        # Separator
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Notebook (tabs)
        notebook_frame = tk.Frame(form_frame, bg="white")
        notebook_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Supplier Tab
        supplier_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(supplier_tab, text="Información del Proveedor")

        # Supplier section (2 rows with 4 columns)
        supplier_frame = tk.Frame(supplier_tab, bg="white")
        supplier_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # First row of supplier fields (4 columns)
        row1_frame = tk.Frame(supplier_frame, bg="white")
        row1_frame.pack(fill=tk.X, pady=5)

        fields_row1 = [
            ("Cédula/RIF:", "supplier_id", 20),
            ("Nombre:", "supplier_first_name", 20),
            ("Apellido:", "supplier_last_name", 20),
            ("Empresa:", "supplier_company", 25)
        ]

        for label, var_name, width in fields_row1:
            col = tk.Frame(row1_frame, bg="white")
            col.pack(side=tk.LEFT, padx=5, expand=True)
            
            frame = tk.Frame(col, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            setattr(self, var_name, entry)

        # Second row of supplier fields (4 columns)
        row2_frame = tk.Frame(supplier_frame, bg="white")
        row2_frame.pack(fill=tk.X, pady=5)

        fields_row2 = [
            ("Teléfono:", "supplier_phone", 15),
            ("Email:", "supplier_email", 25),
            ("Dirección:", "supplier_address", 30),
            ("Fecha Entrega:", "delivery_date", 15)
        ]

        for label, var_name, width in fields_row2:
            col = tk.Frame(row2_frame, bg="white")
            col.pack(side=tk.LEFT, padx=5, expand=True)
            
            frame = tk.Frame(col, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            setattr(self, var_name, entry)

        # Products Tab (only input fields, no table)
        products_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(products_tab, text="Agregar Productos")

        # Add Products section
        add_products_frame = tk.Frame(products_tab, bg="white")
        add_products_frame.pack(fill=tk.X, pady=10)

        CustomLabel(
            add_products_frame,
            text="AGREGAR PRODUCTOS:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        # Product fields in one row
        product_fields_frame = tk.Frame(add_products_frame, bg="white")
        product_fields_frame.pack(fill=tk.X, pady=5)

        product_fields = [
            ("Código:", "product_code", 15),
            ("Descripción:", "product_description", 30),
            ("Cantidad:", "product_quantity", 10),
            ("Precio Unit.:", "product_unit_price", 15)
        ]

        for label, var_name, width in product_fields:
            col = tk.Frame(product_fields_frame, bg="white")
            col.pack(side=tk.LEFT, padx=5)
            
            frame = tk.Frame(col, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5)
            setattr(self, var_name, entry)

        # Button to add product (in the same line)
        btn_add_product = CustomButton(
            product_fields_frame,
            text="Agregar",
            command=self.add_product,
            padding=6,
            width=10
        )
        btn_add_product.pack(side=tk.LEFT, padx=5)

        # Products table (outside notebook)
        table_frame = tk.Frame(form_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Table header
        table_header = tk.Frame(table_frame, bg="white")
        table_header.pack(fill=tk.X)
        
        headers = ["Código", "Descripción", "Cant.", "Precio Unit.", "Total", "Acciones"]
        widths = [100, 300, 80, 120, 120, 100]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            frame = tk.Frame(table_header, bg="#4a6fa5", bd=1, relief=tk.SOLID)
            frame.pack(side=tk.LEFT)
            frame.pack_propagate(False)
            frame.configure(width=width, height=30)
            
            CustomLabel(
                frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#4a6fa5"
            ).pack(expand=True, fill=tk.BOTH)

        # Table body with scroll
        self.table_body = tk.Frame(table_frame, bg="white", bd=1, relief=tk.SUNKEN)
        self.table_body.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(self.table_body, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for table
        self.canvas = tk.Canvas(self.table_body, bg="white", yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        # Inner frame for products
        self.products_inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.products_inner_frame, anchor=tk.NW)

        # Configure scroll
        self.products_inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Separator
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Totals
        totals_frame = tk.Frame(form_frame, bg="white")
        totals_frame.pack(fill=tk.X, pady=10)

        # Subtotal, IVA, Total (right aligned)
        self.totals = {
            "subtotal": tk.StringVar(value="0.00"),
            "iva": tk.StringVar(value="0.00"),
            "total": tk.StringVar(value="0.00")
        }

        for label, var in [("Subtotal:", "subtotal"), 
                          ("IVA (16%):", "iva"), 
                          ("TOTAL:", "total")]:
            frame = tk.Frame(totals_frame, bg="white")
            frame.pack(anchor=tk.E, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg="white",
                width=15,
                anchor=tk.E
            ).pack(side=tk.LEFT)
            
            CustomLabel(
                frame,
                text=self.totals[var],
                font=("Arial", 12, "bold"),
                bg="white",
                width=15,
                anchor=tk.E
            ).pack(side=tk.LEFT)

        # Action buttons
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        buttons = [
            ("Crear Orden", self.create_order),
            ("Limpiar", self.clear_form)
        ]

        for text, command in buttons:
            btn = CustomButton(
                action_frame,
                text=text,
                command=command,
                padding=8,
                width=12,
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def open_suppliers_search(self) -> None:
        """Open supplier search window"""
        search_window = tk.Toplevel(self)
        search_window.title("Seleccionar Proveedor")
        search_window.geometry("800x600")
        search_window.transient(self)
        search_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(search_window, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search bar
        search_frame = tk.Frame(main_frame, bg="#f5f5f5")
        search_frame.pack(fill=tk.X, pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 12)
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.search_suppliers)
        
        # Search button
        btn_search = CustomButton(
            search_frame,
            text="Buscar",
            command=lambda: self.search_suppliers(),
            padding=8,
            width=10
        )
        btn_search.pack(side=tk.LEFT, padx=5)
        
        # Treeview to show suppliers
        tree_frame = tk.Frame(main_frame, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Código", "Cédula", "Nombres", "Apellidos", 
            "Empresa", "Teléfono", "Email", "RIF"
        ), show="headings")
        
        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Cédula", 100, tk.CENTER),
            ("Nombres", 150, tk.W),
            ("Apellidos", 150, tk.W),
            ("Empresa", 200, tk.W),
            ("Teléfono", 100, tk.CENTER),
            ("Email", 150, tk.W),
            ("RIF", 100, tk.CENTER)
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_select = CustomButton(
            btn_frame,
            text="Seleccionar",
            command=lambda: self.select_supplier(search_window),
            padding=8,
            width=12
        )
        btn_select.pack(side=tk.LEFT, padx=5)
        
        btn_cancel = CustomButton(
            btn_frame,
            text="Cancelar",
            command=search_window.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Load initial data
        self.search_suppliers()
    
    def search_suppliers(self, event=None) -> None:
        """Search suppliers based on search term"""
        search_term = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        suppliers = PurchaseOrder.get_suppliers(search_term)
        
        for supplier in suppliers:
            self.tree.insert("", tk.END, values=(
                supplier['id'],
                supplier['code'],
                supplier['id_number'],
                supplier['first_name'],
                supplier['last_name'],
                supplier['company'],
                supplier['phone'],
                supplier['email'],
                supplier['tax_id']
            ))
    
    def select_supplier(self, window: tk.Toplevel) -> None:
        """Select supplier and fill fields in main screen"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor", parent=window)
            return
            
        supplier_id = self.tree.item(selected[0])['values'][0]
        supplier = PurchaseOrder.get_supplier_by_id(supplier_id)
        
        if supplier:
            self.current_supplier_id = supplier_id
            
            self.supplier_id.delete(0, tk.END)
            self.supplier_id.insert(0, supplier['id_number'])
            
            self.supplier_first_name.delete(0, tk.END)
            self.supplier_first_name.insert(0, supplier['first_name'])
            
            self.supplier_last_name.delete(0, tk.END)
            self.supplier_last_name.insert(0, supplier['last_name'])
            
            self.supplier_company.delete(0, tk.END)
            self.supplier_company.insert(0, supplier['company'])
            
            self.supplier_phone.delete(0, tk.END)
            self.supplier_phone.insert(0, supplier['phone'])
            
            self.supplier_email.delete(0, tk.END)
            self.supplier_email.insert(0, supplier['email'])
            
            self.supplier_address.delete(0, tk.END)
            self.supplier_address.insert(0, supplier['address'])
            
            window.destroy()
            self.status_bar.config(text=f"Proveedor seleccionado: {supplier['company']}")

    def search_product(self) -> None:
        """Open product search window for the selected supplier"""
        if not self.current_supplier_id:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor primero", parent=self)
            return
            
        search_window = tk.Toplevel(self)
        search_window.title("Seleccionar Producto")
        search_window.geometry("800x600")
        search_window.transient(self)
        search_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(search_window, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search bar
        search_frame = tk.Frame(main_frame, bg="#f5f5f5")
        search_frame.pack(fill=tk.X, pady=10)
        
        self.product_search_var = tk.StringVar()
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.product_search_var,
            width=40,
            font=("Arial", 12)
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.search_products)
        
        # Search field combobox
        self.product_search_field_var = tk.StringVar(value="Todos los campos")
        search_fields = [
            "Todos los campos",
            "ID",
            "Código",
            "Producto",
            "Descripción",
            "Cantidad",
            "Precio de compra",
            "Precio de venta"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.product_search_field_var,
            values=search_fields,
            state="readonly",
            width=20
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.search_products)
        
        # Treeview to show products
        tree_frame = tk.Frame(main_frame, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.product_tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Código", "Producto", "Descripción", "Cantidad", 
            "Precio Compra", "Precio Venta"
        ), show="headings")
        
        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Precio Compra", 100, tk.CENTER),
            ("Precio Venta", 100, tk.CENTER)
        ]
        
        for col, width, anchor in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_select = CustomButton(
            btn_frame,
            text="Seleccionar",
            command=lambda: self.select_product(search_window),
            padding=8,
            width=12
        )
        btn_select.pack(side=tk.LEFT, padx=5)
        
        btn_cancel = CustomButton(
            btn_frame,
            text="Cancelar",
            command=search_window.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Load initial data
        self.search_products()
    
    def search_products(self, event=None) -> None:
        """Search products for the selected supplier"""
        if not self.current_supplier_id:
            return
            
        search_term = self.product_search_var.get().lower()
        field = self.product_search_field_var.get()
        
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # Search products for this supplier
        products = InventoryItem.search_active(search_term, field if field != "Todos los campos" else None)
        supplier_products = [p for p in products if p.get('supplier_id') == self.current_supplier_id]
        
        for product in supplier_products:
            self.product_tree.insert("", tk.END, values=(
                product['id'],
                product['code'],
                product['product'],
                product['description'],
                product['quantity'],
                product['cost'],
                product['price']
            ))
    
    def select_product(self, window: tk.Toplevel) -> None:
        """Select product and fill fields in products tab"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=window)
            return
            
        product = self.product_tree.item(selected[0])['values']
        
        # Fill product fields
        self.product_code.delete(0, tk.END)
        self.product_code.insert(0, product[1])  # Code
        
        self.product_description.delete(0, tk.END)
        self.product_description.insert(0, product[2])  # Product name
        
        # Set unit price to purchase price
        self.product_unit_price.delete(0, tk.END)
        self.product_unit_price.insert(0, product[5])  # Purchase price
        
        window.destroy()
        self.status_bar.config(text=f"Producto seleccionado: {product[2]}")

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def create_order(self) -> None:
        """Create a new purchase order"""
        # Validate required fields
        if not self.supplier_id.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor", parent=self)
            return
            
        if not any(self.products_inner_frame.winfo_children()):
            messagebox.showwarning("Advertencia", "Por favor agregue al menos un producto", parent=self)
            return
            
        # Get order data
        order_number = self.order_number_entry.get()
        supplier_id = self.current_supplier_id
        delivery_date = self.delivery_date.get()
        
        # Get products from table
        products = []
        for child in self.products_inner_frame.winfo_children():
            if isinstance(child, tk.Frame):
                children = child.winfo_children()
                if len(children) >= 5:  # Ensure we have all columns
                    code = children[0].winfo_children()[0].cget("text")
                    description = children[1].winfo_children()[0].cget("text")
                    quantity = float(children[2].winfo_children()[0].cget("text"))
                    unit_price = float(children[3].winfo_children()[0].cget("text").replace(",", ""))
                    total = float(children[4].winfo_children()[0].cget("text").replace(",", ""))
                    
                    products.append({
                        "code": code,
                        "description": description,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": total
                    })
        
        # Get totals
        subtotal = float(self.totals["subtotal"].get().replace(",", ""))
        iva = float(self.totals["iva"].get().replace(",", ""))
        total = float(self.totals["total"].get().replace(",", ""))
        
        # Create order
        success = PurchaseOrder.create_order(
            order_number=order_number,
            supplier_id=supplier_id,
            delivery_date=delivery_date,
            products=products,
            subtotal=subtotal,
            iva=iva,
            total=total
        )
        
        if success:
            messagebox.showinfo("Éxito", "Orden de compra creada exitosamente", parent=self)
            self.clear_form()
            self.order_number_entry.delete(0, tk.END)
            self.order_number_entry.insert(0, PurchaseOrder.get_next_order_number())
        else:
            messagebox.showerror("Error", "No se pudo crear la orden de compra", parent=self)

    def clear_form(self) -> None:
        # Clear supplier fields
        for field in ["supplier_id", "supplier_first_name", "supplier_last_name",
                     "supplier_company", "supplier_address", "supplier_phone",
                     "supplier_email", "delivery_date"]:
            getattr(self, field).delete(0, tk.END)
        
        # Clear product fields
        for field in ["product_code", "product_description", 
                     "product_quantity", "product_unit_price"]:
            getattr(self, field).delete(0, tk.END)
        
        # Clear products table
        for widget in self.products_inner_frame.winfo_children():
            widget.destroy()
        
        # Reset totals
        for var in self.totals.values():
            var.set("0.00")
        
        self.current_supplier_id = None
        self.status_bar.config(text="Formulario limpiado")

    def view_orders(self) -> None:
        self.status_bar.config(text="Mostrando órdenes existentes...")

    def add_product(self) -> None:
        """Add product to the order table"""
        # Get product data
        code = self.product_code.get()
        description = self.product_description.get()
        quantity = self.product_quantity.get()
        unit_price = self.product_unit_price.get()
        
        if not code or not description or not quantity or not unit_price:
            self.status_bar.config(text="Error: Todos los campos del producto son requeridos")
            return
        
        try:
            quantity = float(quantity)
            unit_price = float(unit_price)
            total = quantity * unit_price
        except ValueError:
            self.status_bar.config(text="Error: Cantidad y precio deben ser números válidos")
            return
        
        # Create row in table
        row_frame = tk.Frame(self.products_inner_frame, bg="white")
        row_frame.pack(fill=tk.X, pady=1)
        
        # Row fields
        fields = [code, description, f"{quantity:.2f}", f"{unit_price:.2f}", f"{total:.2f}"]
        widths = [100, 300, 80, 120, 120]
        
        for i, (value, width) in enumerate(zip(fields, widths)):
            frame = tk.Frame(row_frame, bg="white", bd=1, relief=tk.SOLID)
            frame.pack(side=tk.LEFT)
            frame.pack_propagate(False)
            frame.configure(width=width, height=30)
            
            CustomLabel(
                frame,
                text=value,
                font=("Arial", 11),
                bg="white"
            ).pack(expand=True, fill=tk.BOTH)
        
        # Remove button
        frame = tk.Frame(row_frame, bg="white", bd=1, relief=tk.SOLID)
        frame.pack(side=tk.LEFT)
        frame.pack_propagate(False)
        frame.configure(width=100, height=30)
        
        btn_remove = CustomButton(
            frame,
            text="Eliminar",
            command=lambda: self.remove_product(row_frame, total),
            padding=2,
            width=8
        )
        btn_remove.pack(expand=True, fill=tk.BOTH)
        
        # Update totals
        self.update_totals(total, add=True)
        
        # Clear product fields
        self.product_code.delete(0, tk.END)
        self.product_description.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
        self.product_unit_price.delete(0, tk.END)
        
        self.status_bar.config(text="Producto agregado a la orden")

    def remove_product(self, row_frame: tk.Frame, total: float) -> None:
        """Remove product from the order table"""
        row_frame.destroy()
        self.update_totals(total, add=False)
        self.status_bar.config(text="Producto eliminado de la orden")

    def update_totals(self, amount: float, add: bool = True) -> None:
        """Update order totals (subtotal, IVA, total)"""
        try:
            subtotal = float(self.totals["subtotal"].get().replace(",", ""))
            iva = float(self.totals["iva"].get().replace(",", ""))
            total = float(self.totals["total"].get().replace(",", ""))
            
            if add:
                subtotal += amount
            else:
                subtotal -= amount
            
            iva = subtotal * 0.16
            total = subtotal + iva
            
            self.totals["subtotal"].set(f"{subtotal:,.2f}")
            self.totals["iva"].set(f"{iva:,.2f}")
            self.totals["total"].set(f"{total:,.2f}")
        except ValueError:
            self.status_bar.config(text="Error actualizando totales")