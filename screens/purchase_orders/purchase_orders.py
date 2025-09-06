import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Any, Callable
from reports.purchase_order_viewer import PurchaseOrderViewer
from sqlite_cli.models.purchase_order_model import PurchaseOrder
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.tax_model import Tax
from sqlite_cli.models.currency_model import Currency
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.field_formatter import FieldFormatter

class PurchaseOrdersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.current_supplier_id = None
        self.configure(bg="#f5f5f5")
        self.configure_ui()
        self.update_totals()

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
        
        btn_create_order = CustomButton(
            buttons_frame,
            text="Crear Orden",
            command=self.create_order,
            padding=8,
            width=12,
        )
        btn_create_order.pack(side=tk.RIGHT, padx=5)

        btn_search_product = CustomButton(
            buttons_frame,
            text="Buscar Producto",
            command=self.search_product,
            padding=8,
            width=16,
        )
        btn_search_product.pack(side=tk.RIGHT, padx=5)

        btn_search_supplier = CustomButton(
            buttons_frame,
            text="Buscar Proveedor",
            command=self.open_suppliers_search,
            padding=8,
            width=16,
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

        self.order_number_label = CustomLabel(
            order_num_frame,
            text=PurchaseOrder.get_next_order_number(),
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.order_number_label.pack(side=tk.LEFT, padx=5)

        # Company info (left)
        company_frame = tk.Frame(doc_header_frame, bg="white")
        company_frame.pack(side=tk.LEFT)

        CustomLabel(
            company_frame,
            text="RN&M Servicios Integrales, C.A.",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        CustomLabel(
            company_frame,
            text="RIF: J-40339817-8",
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
            ("Cédula/RIF:", "supplier_id", 20, "readonly", "id_number"),
            ("Nombre:", "supplier_first_name", 20, "readonly", "first_name"),
            ("Apellido:", "supplier_last_name", 20, "readonly", "name"),
            ("Empresa:", "supplier_company", 25, "readonly", "company")
        ]

        for label, var_name, width, state, field_type in fields_row1:
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
                width=width,
                state=state
            )
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            setattr(self, var_name, entry)
            
            if state == "normal":
                FieldFormatter.bind_validation(entry, field_type)

        # Second row of supplier fields (4 columns)
        row2_frame = tk.Frame(supplier_frame, bg="white")
        row2_frame.pack(fill=tk.X, pady=5)

        fields_row2 = [
            ("Teléfono:", "supplier_phone", 15, "readonly", "phone"),
            ("Email:", "supplier_email", 25, "readonly", "email"),
            ("Dirección:", "supplier_address", 30, "readonly", "address"),
            ("Fecha Entrega*:", "delivery_date", 15, "normal", "date")
        ]

        for label, var_name, width, state, field_type in fields_row2:
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
                width=width,
                state=state
            )
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            setattr(self, var_name, entry)
            
            if state == "normal":
                FieldFormatter.bind_validation(entry, field_type)

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
            ("Código:", "product_code", 15, "code"),
            ("Descripción:", "product_description", 30, "first_name"),
            ("Cantidad:", "product_quantity", 10, "integer"),
            ("Precio Unit.:", "product_unit_price", 15, "decimal")
        ]

        for label, var_name, width, field_type in product_fields:
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
            FieldFormatter.bind_validation(entry, field_type)

        # Button to add product
        btn_add_product = CustomButton(
            product_fields_frame,
            text="Agregar",
            command=self.add_product,
            padding=6,
            width=10
        )
        btn_add_product.pack(side=tk.LEFT, padx=5)

        # Products table
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
        totals_frame = tk.Frame(form_frame, bg="#4a6fa5", padx=20, pady=10)
        totals_frame.pack(fill=tk.X)

        # Get taxes and currencies
        self.iva_tax = Tax.get_by_name("IVA")
        self.dollar = Currency.get_by_name("Dólar")
        self.euro = Currency.get_by_name("Euro")

        # Initialize total labels
        self.lbl_subtotal = CustomLabel(
            totals_frame,
            text="Subtotal: 0.00",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        
        self.lbl_iva = CustomLabel(
            totals_frame,
            text=f"IVA ({self.iva_tax['value']}%): 0.00" if self.iva_tax and self.iva_tax.get('status_name') == 'active' else "IVA (0%): 0.00",
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
            bg="#4a6fa5",
            image_path="assets/iconos/dolares.png",
            image_size=(18, 18),
            compound=tk.LEFT
        )
        
        self.lbl_euro = CustomLabel(
            totals_frame,
            text="Euros: €0.00",
            font=("Arial", 12),
            fg="white",
            bg="#4a6fa5",
            image_path="assets/iconos/euros.png",
            image_size=(18, 18),
            compound=tk.LEFT
        )

        # Show labels according to active taxes/currencies
        if self.iva_tax and self.iva_tax.get('status_name') == 'active':
            self.lbl_subtotal.pack(side=tk.LEFT, padx=10)
            self.lbl_iva.pack(side=tk.LEFT, padx=10)
        
        self.lbl_total.pack(side=tk.LEFT, padx=10)
        
        if self.dollar and self.dollar.get('status_name') == 'active':
            self.lbl_dollar.pack(side=tk.LEFT, padx=10)
        
        if self.euro and self.euro.get('status_name') == 'active':
            self.lbl_euro.pack(side=tk.LEFT, padx=10)

        # Action buttons
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        # Status bar
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def update_totals(self) -> None:
        """Calculate and update subtotal, taxes and total"""
        subtotal = 0.0
        
        for child in self.products_inner_frame.winfo_children():
            if isinstance(child, tk.Frame):
                children = child.winfo_children()
                if len(children) >= 5:
                    try:
                        total_text = children[4].winfo_children()[0].cget("text")
                        total = float(total_text.replace(",", ""))
                        subtotal += total
                    except (ValueError, AttributeError):
                        continue
        
        # Calculate totals based on active taxes
        if self.iva_tax and self.iva_tax.get('status_name') == 'active':
            iva_amount = subtotal * (self.iva_tax['value'] / 100)
            total = subtotal + iva_amount
            
            self.lbl_subtotal.config(text=f"Subtotal: {subtotal:,.2f}")
            self.lbl_iva.config(text=f"IVA ({self.iva_tax['value']}%): {iva_amount:,.2f}")
        else:
            total = subtotal
        
        self.lbl_total.config(text=f"Total: {total:,.2f}")
        
        # Update currency values if active
        if self.dollar and self.dollar.get('status_name') == 'active':
            dollar_amount = total / self.dollar['value'] if self.dollar['value'] != 0 else 0
            self.lbl_dollar.config(text=f"Dólares: ${dollar_amount:,.2f}")
        
        if self.euro and self.euro.get('status_name') == 'active':
            euro_amount = total / self.euro['value'] if self.euro['value'] != 0 else 0
            self.lbl_euro.config(text=f"Euros: €{euro_amount:,.2f}")

    def center_window(self, window: tk.Toplevel) -> None:
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def open_suppliers_search(self) -> None:
        """Open supplier search window"""
        search_window = tk.Toplevel(self)
        search_window.title("Seleccionar Proveedor")
        search_window.geometry("800x600")
        self.center_window(search_window)
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
        
        # Create supplier button
        btn_create = CustomButton(
            search_frame,
            text="Crear Proveedor",
            command=lambda: self.create_new_supplier(search_window),
            padding=8,
            width=15
        )
        btn_create.pack(side=tk.LEFT, padx=5)
        
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

        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_cancel = CustomButton(
            btn_frame,
            text="Cancelar",
            command=search_window.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)
        
        btn_select = CustomButton(
            btn_frame,
            text="Seleccionar",
            command=lambda: self.select_supplier(search_window),
            padding=8,
            width=12
        )
        btn_select.pack(side=tk.RIGHT, padx=5)
        
        # Load initial data
        self.search_suppliers()
    
    def create_new_supplier(self, search_window: tk.Toplevel) -> None:
        """Open the supplier creation form"""
        from screens.supplier.crud_supplier import CrudSupplier
        
        def refresh_suppliers():
            self.search_suppliers()
        
        supplier_form = CrudSupplier(
            parent=search_window,
            mode="create",
            refresh_callback=refresh_suppliers
        )
        
        self.center_window(supplier_form)
    
    def search_suppliers(self, event=None) -> None:
        """Search suppliers based on search term"""
        search_term = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        suppliers = PurchaseOrder.get_suppliers(search_term)
        
        for i, supplier in enumerate(suppliers):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
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
            ), tags=(tag,))
    
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
            
            # Temporarily enable fields to insert values
            fields = [
                self.supplier_id,
                self.supplier_first_name,
                self.supplier_last_name,
                self.supplier_company,
                self.supplier_phone,
                self.supplier_email,
                self.supplier_address
            ]
            
            for field in fields:
                field.config(state="normal")
                field.delete(0, tk.END)
            
            # Set values
            self.supplier_id.insert(0, supplier.get('id_number', ''))
            self.supplier_first_name.insert(0, supplier.get('first_name', ''))
            self.supplier_last_name.insert(0, supplier.get('last_name', ''))
            self.supplier_company.insert(0, supplier.get('company', ''))
            self.supplier_phone.insert(0, supplier.get('phone', ''))
            self.supplier_email.insert(0, supplier.get('email', ''))
            self.supplier_address.insert(0, supplier.get('address', ''))
            
            # Set back to readonly
            for field in fields:
                field.config(state="readonly")
            
            # Cambiar al tab del proveedor
            self.notebook.select(0)
            
            window.destroy()
            self.status_bar.config(text=f"Proveedor seleccionado: {supplier.get('company', '')}")

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def create_order(self) -> None:
        """Create a new purchase order"""
        if not self.supplier_id.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor", parent=self)
            return
            
        if not any(self.products_inner_frame.winfo_children()):
            messagebox.showwarning("Advertencia", "Por favor agregue al menos un producto", parent=self)
            return
            
        if not self.delivery_date.get():
            messagebox.showwarning("Advertencia", "Por favor ingrese la fecha de entrega", parent=self)
            return
            
        order_number = self.order_number_label.cget("text")
        if not order_number:
            order_number = PurchaseOrder.get_next_order_number()
            self.order_number_label.config(text=order_number)
        
        supplier_id = self.current_supplier_id
        delivery_date = self.delivery_date.get()
        
        products = []
        for child in self.products_inner_frame.winfo_children():
            if isinstance(child, tk.Frame):
                children = child.winfo_children()
                if len(children) >= 5:
                    code = children[0].winfo_children()[0].cget("text")
                    description = children[1].winfo_children()[0].cget("text")
                    quantity = int(children[2].winfo_children()[0].cget("text"))
                    unit_price = float(children[3].winfo_children()[0].cget("text").replace(",", ""))
                    total = float(children[4].winfo_children()[0].cget("text").replace(",", ""))
                    
                    product_id = None
                    product = InventoryItem.get_by_code(code)
                    if product:
                        product_id = product['id']
                    
                    products.append({
                        "id": product_id,
                        "name": description,
                        "code": code,
                        "description": description,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": total
                    })
        
        subtotal = float(self.lbl_subtotal.cget("text").split(":")[1].strip().replace(",", ""))
        iva = float(self.lbl_iva.cget("text").split(":")[1].strip().replace(",", "")) if self.iva_tax and self.iva_tax.get('status_name') == 'active' else 0.0
        total = float(self.lbl_total.cget("text").split(":")[1].strip().replace(",", ""))
        
        # Get current user info
        from utils.session_manager import SessionManager
        current_user = SessionManager.get_user_id()
        created_by = current_user
        
        success = PurchaseOrder.create_order(
            order_number=order_number,
            supplier_id=supplier_id,
            delivery_date=delivery_date,
            products=products,
            subtotal=subtotal,
            iva=iva,
            total=total,
            notes="Orden creada desde la interfaz gráfica",
            created_by=created_by
        )
        
        if success:
            # Mostrar la orden de compra
            supplier_info = f"{self.supplier_company.get()} - {self.supplier_id.get()}"
            PurchaseOrderViewer(
                self,
                order_number,
                supplier_info,
                products,
                subtotal,
                iva,
                total,
                delivery_date,
                created_by
            )
            
            self.clear_form()
            self.order_number_label.config(text=PurchaseOrder.get_next_order_number())
        else:
            messagebox.showerror("Error", "No se pudo crear la orden de compra", parent=self)

    def clear_form(self) -> None:
        """Clear the form and reset fields"""
        # Temporarily enable readonly fields to clear them
        fields = [
            self.supplier_id,
            self.supplier_first_name,
            self.supplier_last_name,
            self.supplier_company,
            self.supplier_phone,
            self.supplier_email,
            self.supplier_address
        ]
        
        for field in fields:
            field.config(state="normal")
            field.delete(0, tk.END)
            field.config(state="readonly")
        
        # Clear product fields
        for field in ["product_code", "product_description", 
                     "product_quantity", "product_unit_price"]:
            getattr(self, field).delete(0, tk.END)
        
        # Clear products table
        for widget in self.products_inner_frame.winfo_children():
            widget.destroy()
        
        # Clear delivery date
        self.delivery_date.delete(0, tk.END)
        
        # Reset totals
        self.lbl_subtotal.config(text="Subtotal: 0.00")
        self.lbl_iva.config(text=f"IVA ({self.iva_tax['value']}%): 0.00" if self.iva_tax and self.iva_tax.get('status_name') == 'active' else "IVA (0%): 0.00")
        self.lbl_total.config(text="Total: 0.00")
        
        if self.dollar and self.dollar.get('status_name') == 'active':
            self.lbl_dollar.config(text="Dólares: $0.00")
        
        if self.euro and self.euro.get('status_name') == 'active':
            self.lbl_euro.config(text="Euros: €0.00")
        
        self.current_supplier_id = None
        self.status_bar.config(text="Formulario limpiado")

    def search_product(self) -> None:
        """Open product search window for the selected supplier"""
        if not self.current_supplier_id or not self.validate_supplier_fields():
            messagebox.showwarning(
                "Advertencia", 
                "Por favor seleccione un proveedor primero usando el botón 'Buscar Proveedor'", 
                parent=self
            )
            return
            
        search_window = tk.Toplevel(self)
        search_window.title("Seleccionar Producto")
        search_window.geometry("800x600")
        self.center_window(search_window)
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

        self.product_tree.tag_configure('evenrow', background='#ffffff')
        self.product_tree.tag_configure('oddrow', background='#f0f0f0')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_cancel = CustomButton(
            btn_frame,
            text="Cancelar",
            command=search_window.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)
        
        btn_select = CustomButton(
            btn_frame,
            text="Seleccionar",
            command=lambda: self.select_product(search_window),
            padding=8,
            width=12
        )
        btn_select.pack(side=tk.RIGHT, padx=5)
        
        # Load initial data
        self.search_products()
    
    def validate_supplier_fields(self) -> bool:
        """Check if supplier fields match the selected supplier"""
        if not self.current_supplier_id:
            return False
            
        supplier = PurchaseOrder.get_supplier_by_id(self.current_supplier_id)
        if not supplier:
            return False
            
        return (self.supplier_id.get() == supplier['id_number'] and
                self.supplier_first_name.get() == supplier['first_name'] and
                self.supplier_last_name.get() == supplier['last_name'] and
                self.supplier_company.get() == supplier['company'] and
                self.supplier_phone.get() == supplier['phone'] and
                self.supplier_email.get() == supplier['email'] and
                self.supplier_address.get() == supplier['address'])
    
    def search_products(self, event=None) -> None:
        """Search products for the selected supplier"""
        if not self.current_supplier_id:
            return
            
        search_term = self.product_search_var.get().lower()
        field = self.product_search_field_var.get()
        
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        products = InventoryItem.search_active(search_term, field if field != "Todos los campos" else None)
        supplier_products = [p for p in products if p.get('supplier_id') == self.current_supplier_id]
        
        for i, product in enumerate(supplier_products):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.product_tree.insert("", tk.END, values=(
                product['id'],
                product['code'],
                product['product'],
                product['description'],
                product['quantity'],
                product['cost'],
                product['price']
            ), tags=(tag,))
    
    def select_product(self, window: tk.Toplevel) -> None:
        """Select product and fill fields in products tab"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=window)
            return
            
        product = self.product_tree.item(selected[0])['values']
        
        self.product_code.delete(0, tk.END)
        self.product_code.insert(0, product[1])
        
        self.product_description.delete(0, tk.END)
        self.product_description.insert(0, product[2])
        
        self.product_unit_price.delete(0, tk.END)
        self.product_unit_price.insert(0, product[5])
        
        # Cambiar al tab de productos
        self.notebook.select(1)
        
        window.destroy()
        self.status_bar.config(text=f"Producto seleccionado: {product[2]}")

    def add_product(self) -> None:
        """Add product to the order table"""
        code = self.product_code.get()
        description = self.product_description.get()
        quantity = self.product_quantity.get()
        unit_price = self.product_unit_price.get()
        
        if not code or not description or not quantity or not unit_price:
            self.status_bar.config(text="Error: Todos los campos del producto son requeridos")
            return
        
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
            total = quantity * unit_price
        except ValueError:
            self.status_bar.config(text="Error: Cantidad debe ser entero y precio debe ser número válido")
            return
        
        product = InventoryItem.get_by_code(code)
        product_id = product['id'] if product else None
        
        # Create row in table
        row_frame = tk.Frame(self.products_inner_frame, bg="white")
        row_frame.pack(fill=tk.X, pady=1)
        
        fields = [code, description, f"{quantity}", f"{unit_price:.2f}", f"{total:.2f}"]
        widths = [100, 300, 80, 120, 120]
        
        for i, (value, width) in enumerate(zip(fields, widths)):
            frame = tk.Frame(row_frame, bg="white", bd=1, relief=tk.SOLID)
            frame.pack(side=tk.LEFT)
            frame.pack_propagate(False)
            frame.configure(width=width, height=40)
            
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
        frame.configure(width=100, height=40)

        btn_remove = CustomButton(
            frame,
            text="Eliminar",
            command=lambda: self.remove_product(row_frame, total),
            padding=2,
            width=8
        )
        btn_remove.pack(expand=True, fill=tk.BOTH)
        
        self.update_totals()
        
        # Clear product fields
        self.product_code.delete(0, tk.END)
        self.product_description.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
        self.product_unit_price.delete(0, tk.END)
        
        self.status_bar.config(text="Producto agregado a la orden")

    def remove_product(self, row_frame: tk.Frame, total: float) -> None:
        """Remove product from the order table"""
        row_frame.destroy()
        self.update_totals()
        self.status_bar.config(text="Producto eliminado de la orden")