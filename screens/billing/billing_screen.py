import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any, Optional
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.tax_model import Tax
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
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_checkout = CustomButton(
            button_frame,
            text="Realizar Compra",
            command=self.checkout,
            padding=8,
            width=15
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
        products_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.products_tree = ttk.Treeview(products_frame, columns=(
            "ID", "Código", "Producto", "Existencias", "Stock mínimo", 
            "Stock máximo", "Precio"
        ), show="headings")

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
        cart_frame.pack(fill=tk.BOTH, expand=True)

        self.cart_tree = ttk.Treeview(cart_frame, columns=(
            "ID", "Producto", "Cantidad", "Precio Unitario", "Total"
        ), show="headings")

        cart_columns = [
            ("ID", 50, tk.CENTER),
            ("Producto", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Precio Unitario", 100, tk.CENTER),
            ("Total", 100, tk.CENTER)
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

        # Obtener información de impuestos
        iva_tax = Tax.get_by_name("IVA")

        # Mostrar u ocultar según estén activos
        if iva_tax and iva_tax.get('status_name') == 'active':
            self.lbl_subtotal = CustomLabel(
                totals_frame,
                text="Subtotal: Bs. 0.00",
                font=("Arial", 10, "bold"),
                fg="#333"
            )
            self.lbl_subtotal.pack(side=tk.LEFT, padx=10)

            self.lbl_iva = CustomLabel(
                totals_frame,
                text=f"IVA ({iva_tax['value']}%): Bs. 0.00",
                font=("Arial", 10, "bold"),
                fg="#333"
            )
            self.lbl_iva.pack(side=tk.LEFT, padx=10)

        self.lbl_total = CustomLabel(
            totals_frame,
            text="Total: Bs. 0.00",
            font=("Arial", 10, "bold"),
            fg="#333"
        )
        self.lbl_total.pack(side=tk.LEFT, padx=10)

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
                item['price']
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

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def checkout(self) -> None:
        if not self.current_customer:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para realizar la compra", parent=self)
            return
            
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un producto al carrito", parent=self)
            return
            
        response = messagebox.askyesno(
            "Confirmar Compra", 
            "¿Está seguro que desea realizar la compra?",
            parent=self
        )
        
        if response:
            try:
                # Aquí iría la lógica para guardar la factura en la base de datos
                messagebox.showinfo("Éxito", "Compra realizada correctamente", parent=self)
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo completar la compra: {str(e)}", parent=self)

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
            self.search_customer()
        
        CrudCustomer(
            self,
            mode="create",
            initial_id_number=id_number,
            refresh_callback=on_customer_created
        )

    def on_product_click(self, event) -> None:
        selected = self.products_tree.identify_row(event.y)
        if not selected:
            return
            
        item_id = self.products_tree.item(selected)['values'][0]
        product_name = self.products_tree.item(selected)['values'][2]
        stock = self.products_tree.item(selected)['values'][3]
        min_stock = self.products_tree.item(selected)['values'][4]
        max_stock = self.products_tree.item(selected)['values'][5]
        price = self.products_tree.item(selected)['values'][6]
        
        # Verificar si el producto ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['id'] == item_id), None)
        
        # Crear ventana para seleccionar cantidad
        add_window = tk.Toplevel(self)
        add_window.title(f"Agregar {product_name}")
        add_window.geometry("400x300")
        add_window.resizable(False, False)
        
        # Centrar la ventana
        window_width = 400
        window_height = 300
        screen_width = add_window.winfo_screenwidth()
        screen_height = add_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        add_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        add_window.transient(self)
        add_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(add_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del producto
        tk.Label(
            main_frame, 
            text=f"Producto: {product_name}",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10), anchor=tk.W)
        
        tk.Label(
            main_frame, 
            text=f"Existencias: {stock}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        tk.Label(
            main_frame, 
            text=f"Stock mínimo: {min_stock}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        tk.Label(
            main_frame, 
            text=f"Stock máximo: {max_stock}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        tk.Label(
            main_frame, 
            text=f"Precio unitario: Bs. {price:.2f}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        # Cantidad
        tk.Label(
            main_frame, 
            text="Cantidad:",
            font=("Arial", 10)
        ).pack(pady=(10, 5), anchor=tk.W)
        
        quantity_var = tk.StringVar(value=str(min_stock) if not existing_item else str(existing_item['quantity']))
        quantity_entry = CustomEntry(
            main_frame,
            textvariable=quantity_var,
            font=("Arial", 12),
            width=10,
            validate="key",
            validatecommand=(add_window.register(self.validate_quantity), '%P')
        )
        quantity_entry.pack(anchor=tk.W)
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(20, 0))
        
        def add_to_cart():
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a cero", parent=add_window)
                    return
                    
                if quantity < min_stock:
                    messagebox.showwarning("Advertencia", f"La cantidad mínima permitida es {min_stock}", parent=add_window)
                    return
                    
                if quantity > max_stock:
                    messagebox.showwarning("Advertencia", f"La cantidad máxima permitida es {max_stock}", parent=add_window)
                    return
                    
                if quantity > stock:
                    messagebox.showwarning("Advertencia", "No hay suficiente stock disponible", parent=add_window)
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
                add_window.destroy()
                
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingrese una cantidad válida", parent=add_window)
        
        CustomButton(
            btn_frame,
            text="Agregar",
            command=add_to_cart,
            padding=8,
            width=12
        ).pack(side=tk.LEFT, padx=10)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=add_window.destroy,
            padding=8,
            width=12
        ).pack(side=tk.LEFT, padx=10)

    def on_cart_item_click(self, event) -> None:
        selected = self.cart_tree.identify_row(event.y)
        if not selected:
            return
            
        item_id = self.cart_tree.item(selected)['values'][0]
        product_name = self.cart_tree.item(selected)['values'][1]
        quantity = self.cart_tree.item(selected)['values'][2]
        price = float(self.cart_tree.item(selected)['values'][3].replace("Bs. ", ""))
        
        # Crear ventana de confirmación para eliminar
        confirm_window = tk.Toplevel(self)
        confirm_window.title("Confirmar Eliminación")
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        
        # Centrar la ventana
        window_width = 400
        window_height = 200
        screen_width = confirm_window.winfo_screenwidth()
        screen_height = confirm_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        confirm_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        confirm_window.transient(self)
        confirm_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(confirm_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje de confirmación
        tk.Label(
            main_frame, 
            text=f"¿Está seguro que desea eliminar este producto del carrito?",
            font=("Arial", 12)
        ).pack(pady=(10, 20))
        
        tk.Label(
            main_frame, 
            text=f"Producto: {product_name}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        tk.Label(
            main_frame, 
            text=f"Cantidad: {quantity} - Total: Bs. {quantity * price:.2f}",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(20, 0))
        
        CustomButton(
            btn_frame,
            text="Eliminar",
            command=lambda: self.remove_from_cart(item_id, confirm_window),
            padding=8,
            width=12
        ).pack(side=tk.LEFT, padx=10)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=confirm_window.destroy,
            padding=8,
            width=12
        ).pack(side=tk.LEFT, padx=10)

    def remove_from_cart(self, item_id: int, window=None) -> None:
        self.cart_items = [item for item in self.cart_items if item['id'] != item_id]
        self.update_cart_tree()
        self.update_totals()
        if window:
            window.destroy()

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
                f"Bs. {item['unit_price']:.2f}",
                f"Bs. {item['total']:.2f}"
            ))

    def update_totals(self) -> None:
        subtotal = sum(item['total'] for item in self.cart_items)
        
        # Obtener impuestos
        iva_tax = Tax.get_by_name("IVA")
        
        # Calcular totales
        if iva_tax and iva_tax.get('status_name') == 'active':
            iva_amount = subtotal * (iva_tax['value'] / 100)
            total = subtotal + iva_amount
            
            self.lbl_subtotal.configure(text=f"Subtotal: Bs. {subtotal:.2f}")
            self.lbl_iva.configure(text=f"IVA ({iva_tax['value']}%): Bs. {iva_amount:.2f}")
        else:
            total = subtotal
        
        self.lbl_total.configure(text=f"Total: Bs. {total:.2f}")