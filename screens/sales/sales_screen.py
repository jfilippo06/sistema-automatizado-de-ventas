import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any, Optional
from screens.inventory.crud_inventory import CrudInventory
from screens.supplier.crud_supplier import CrudSupplier
from sqlite_cli.models.sales_model import Sales
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.tax_model import Tax
from sqlite_cli.models.currency_model import Currency

class SalesScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.supplier_id_var = tk.StringVar()
        self.cart_items = []
        self.current_supplier = None
        
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
            text="Gestión de Compras",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Frame principal para controles
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame de búsqueda de proveedor
        supplier_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        supplier_frame.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        lbl_supplier = CustomLabel(
            supplier_frame,
            text="Cédula Proveedor:",
            font=("Arial", 12),
            fg="#555",
            bg="#f5f5f5"
        )
        lbl_supplier.pack(side=tk.LEFT, padx=5)

        self.entry_supplier = CustomEntry(
            supplier_frame,
            textvariable=self.supplier_id_var,
            font=("Arial", 12),
            width=20
        )
        self.entry_supplier.pack(side=tk.LEFT, padx=5)

        btn_search_supplier = CustomButton(
            supplier_frame,
            text="Buscar",
            command=self.search_supplier,
            padding=6,
            width=10
        )
        btn_search_supplier.pack(side=tk.LEFT, padx=5)

        self.lbl_supplier_info = CustomLabel(
            supplier_frame,
            text="Seleccione un proveedor",
            font=("Arial", 12, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        self.lbl_supplier_info.pack(side=tk.LEFT, padx=10)

        # Frame de acciones
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        btn_cancel = CustomButton(
            action_frame,
            text="Cancelar Compra",
            command=self.cancel_purchase,
            padding=8,
            width=18
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_checkout = CustomButton(
            action_frame,
            text="Realizar Compra",
            command=self.checkout,
            padding=8,
            width=18
        )
        btn_checkout.pack(side=tk.LEFT, padx=5)

        btn_create_product = CustomButton(
            action_frame,
            text="Crear Producto",
            command=self.create_product,
            padding=8,
            width=15
        )
        btn_create_product.pack(side=tk.LEFT, padx=5)

        # Frame para las tablas (ahora solo dos tablas)
        tables_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        tables_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview para productos del proveedor (ahora ocupa la mitad superior)
        lbl_supplier_products = CustomLabel(
            tables_frame,
            text="Productos del Proveedor",
            font=("Arial", 14),
            fg="#333",
            bg="#f5f5f5"
        )
        lbl_supplier_products.pack(anchor=tk.W)

        supplier_products_frame = tk.Frame(tables_frame)
        supplier_products_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.supplier_products_tree = ttk.Treeview(
            supplier_products_frame, 
            columns=("ID", "Código", "Producto", "Cantidad", "Precio"),
            show="headings",
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Precio", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.supplier_products_tree.heading(col, text=col)
            self.supplier_products_tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(
            supplier_products_frame, 
            orient=tk.VERTICAL, 
            command=self.supplier_products_tree.yview
        )
        self.supplier_products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.supplier_products_tree.pack(fill=tk.BOTH, expand=True)
        self.supplier_products_tree.bind("<Button-1>", self.on_supplier_product_click)

        # Treeview para carrito de compras (ahora ocupa la mitad inferior)
        lbl_cart = CustomLabel(
            tables_frame,
            text="Carrito de Compras",
            font=("Arial", 14),
            fg="#333",
            bg="#f5f5f5"
        )
        lbl_cart.pack(anchor=tk.W)

        cart_frame = tk.Frame(tables_frame)
        cart_frame.pack(fill=tk.BOTH, expand=True)

        self.cart_tree = ttk.Treeview(
            cart_frame, 
            columns=("ID", "Producto", "Cantidad", "Precio Unitario", "Total", "Acción"),
            show="headings",
            style="Custom.Treeview"
        )

        cart_columns = [
            ("ID", 50, tk.CENTER),
            ("Producto", 200, tk.W),
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

    # [Resto de los métodos permanecen iguales...]
    def create_product(self):
        """Abre el formulario para crear un nuevo producto con campos bloqueados"""
        def on_product_created():
            self.refresh_data()  # Refrescar los datos después de crear el producto
        
        # Crear el CRUD en modo creación
        crud = CrudInventory(
            self,
            mode="create",
            refresh_callback=on_product_created
        )
        
        # Configurar campos bloqueados como se solicita
        fields_to_lock = [
            "Cantidad:", 
            "Existencias:", 
            "Stock mínimo:", 
            "Stock máximo:", 
            "Proveedor:",
            "Vencimiento:"
        ]
        
        for field in fields_to_lock:
            if field in crud.entries:
                if isinstance(crud.entries[field], ttk.Combobox):
                    crud.entries[field].config(state='disabled')  # Para el Combobox de proveedor
                else:
                    crud.entries[field].config(state='readonly')  # Para los demás campos
        
        # Centrar la ventana
        window_width = 800
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        crud.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.supplier_id_var.set("")
        self.lbl_supplier_info.configure(text="Seleccione un proveedor")
        self.current_supplier = None
        self.cart_items = []
        
        # Limpiar tablas
        self.supplier_products_tree.delete(*self.supplier_products_tree.get_children())
        self.update_cart_tree()
        self.update_totals()
        
        # Enfocar en campo de búsqueda
        self.entry_supplier.focus_set()

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

    def checkout(self) -> None:
        if not self.current_supplier:
            messagebox.showwarning("Advertencia", "Debe seleccionar un proveedor para realizar la compra", parent=self)
            return
            
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un producto al carrito", parent=self)
            return
            
        response = messagebox.askyesno(
            "Confirmar Compra", 
            "¿Está seguro que desea realizar la compra?\nLa factura se registrará como tipo Compra.",
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
                
                # Preparar items para la compra
                purchase_items = [{
                    'id': item['id'],
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price'],
                    'total': item['total']
                } for item in self.cart_items]
                
                # Crear la compra (tipo Compra)
                purchase_id = Sales.create_complete_purchase(
                    supplier_id=self.current_supplier['id'],
                    subtotal=subtotal,
                    taxes=taxes,
                    total=total,
                    items=purchase_items
                )
                
                # Mostrar mensaje de éxito
                messagebox.showinfo(
                    "Éxito", 
                    f"Compra registrada correctamente\nNúmero de factura: {purchase_id}\nTipo: Compra",
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

    def search_supplier(self) -> None:
        id_number = self.supplier_id_var.get().strip()
        if not id_number:
            messagebox.showwarning("Advertencia", "Ingrese una cédula para buscar", parent=self)
            self.entry_supplier.focus_set()
            return
        
        try:
            supplier = Supplier.get_by_id_number(id_number)
            if supplier:
                self.current_supplier = supplier
                supplier_name = supplier.get('company') or f"{supplier.get('first_name', '')} {supplier.get('last_name', '')}"
                self.lbl_supplier_info.configure(
                    text=f"{supplier_name} - {supplier.get('id_number', '')}"
                )
                self.update_supplier_products_tree()
                # Habilitar interacción con productos
                self.supplier_products_tree.bind("<Button-1>", self.on_supplier_product_click)
            else:
                response = messagebox.askyesno(
                    "Proveedor no encontrado", 
                    "El proveedor no está registrado. ¿Desea registrarlo ahora?",
                    parent=self
                )
                if response:
                    self.register_new_supplier(id_number)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el proveedor: {str(e)}", parent=self)

    def register_new_supplier(self, id_number: str) -> None:
        """Abre el formulario para registrar un nuevo proveedor"""
        def on_supplier_created():
            # Después de crear el proveedor, intentar buscarlo nuevamente
            self.supplier_id_var.set(id_number)
            self.search_supplier()
        
        # Crear la ventana de CRUD para proveedor con cédula bloqueada
        crud = CrudSupplier(
            self,
            mode="create",
            initial_id_number=id_number,
            refresh_callback=on_supplier_created,
            lock_id_number=True  # Bloquear cédula cuando se crea desde ventas
        )
        # ... (resto del método igual)
        
        # Centrar la ventana
        window_width = 360
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        crud.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def update_supplier_products_tree(self) -> None:
        for item in self.supplier_products_tree.get_children():
            self.supplier_products_tree.delete(item)
        
        if not self.current_supplier:
            return
        
        all_products = InventoryItem.search_active()
        supplier_products = [
            p for p in all_products 
            if p.get('supplier_id') == self.current_supplier['id']
        ]
        
        for item in supplier_products:
            self.supplier_products_tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['quantity'],  # Mostrar quantity en lugar de stock
                f"{float(item['price']):.2f}" if item['price'] else "0.00"
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(supplier_products)} productos del proveedor")

    def on_supplier_product_click(self, event) -> None:
        if not self.current_supplier:
            self.show_no_supplier_warning()
            return
            
        selected = self.supplier_products_tree.identify_row(event.y)
        if not selected:
            return
            
        item_data = self.supplier_products_tree.item(selected)['values']
        self.show_product_quantity_dialog(item_data)

    def on_product_click(self, event) -> None:
        if not self.current_supplier:
            self.show_no_supplier_warning()
            return
    
    def show_no_supplier_warning(self) -> None:
        messagebox.showwarning(
            "Proveedor requerido", 
            "Debe seleccionar un proveedor antes de agregar productos al carrito.\n\n"
            "Por favor:\n"
            "1. Ingrese la cédula del proveedor\n"
            "2. Haga click en 'Buscar'\n"
            "3. Si no existe, regístrelo con el botón 'Buscar'",
            parent=self
        )
        self.entry_supplier.focus_set()
        self.entry_supplier.selection_range(0, tk.END)

    def show_product_quantity_dialog(self, item_data) -> None:
        item_id = item_data[0]
        product_name = item_data[2]
        quantity = int(item_data[3])  # Ahora usa quantity directamente
        price = float(item_data[4])
        
        # Verificar si el producto ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['id'] == item_id), None)
        
        # Crear ventana para seleccionar cantidad
        quantity_window = tk.Toplevel(self)
        quantity_window.title(f"Agregar {product_name}")
        
        # Calcular posición para centrar la ventana
        window_width = 350
        window_height = 250  # Reducida al eliminar elementos
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
            text=f"Cantidad: {quantity}",
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
        ).pack(side=tk.LEFT, padx=5)
        
        # Siempre mostrar 1 como valor inicial
        quantity_var = tk.StringVar(value="1")
        quantity_entry = CustomEntry(
            quantity_frame,
            textvariable=quantity_var,
            font=("Arial", 10),
            width=10,
            validate="key",
            validatecommand=(quantity_window.register(self.validate_quantity), '%P'
        ))
        quantity_entry.pack(side=tk.LEFT, padx=5)
        
        def add_to_cart():
            try:
                quantity = int(quantity_var.get())
                
                # Validación básica
                if quantity < 1:
                    messagebox.showwarning(
                        "Advertencia", 
                        "La cantidad mínima permitida es 1", 
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