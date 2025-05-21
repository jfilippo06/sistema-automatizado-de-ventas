import tkinter as tk
from tkinter import ttk
from typing import Any, Callable
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class PurchaseOrdersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header (manteniendo tu estilo)
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Órdenes de Compra",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Botones en el header
        buttons_frame = tk.Frame(header_frame, bg="#4a6fa5")
        buttons_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        # Botones adicionales junto a "Regresar"
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
            command=self.search_supplier,
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

        # Contenedor principal (formulario tipo documento)
        form_frame = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief=tk.SUNKEN)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Encabezado del documento
        doc_header_frame = tk.Frame(form_frame, bg="white")
        doc_header_frame.pack(fill=tk.X, pady=10)

        # Número de orden (derecha)
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
        self.order_number_entry.insert(0, "OC-0001")  # Ejemplo

        # Logo y datos empresa (izquierda)
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

        # Línea divisoria
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Sección Proveedor (estilo similar al catálogo)
        supplier_frame = tk.Frame(form_frame, bg="white")
        supplier_frame.pack(fill=tk.X, pady=10)

        CustomLabel(
            supplier_frame,
            text="PROVEEDOR:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        # Campos del proveedor en un grid (3 columnas)
        supplier_fields_frame = tk.Frame(supplier_frame, bg="white")
        supplier_fields_frame.pack(fill=tk.X, pady=5)

        # Columna 1
        col1 = tk.Frame(supplier_fields_frame, bg="white")
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fields_col1 = [
            ("Cédula/RIF:", "supplier_id", 20),
            ("Nombre:", "supplier_first_name", 20),
            ("Apellido:", "supplier_last_name", 20)
        ]

        for label, var_name, width in fields_col1:
            frame = tk.Frame(col1, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5)
            setattr(self, var_name, entry)

        # Columna 2
        col2 = tk.Frame(supplier_fields_frame, bg="white")
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fields_col2 = [
            ("Empresa:", "supplier_company", 25),
            ("Teléfono:", "supplier_phone", 15),
            ("Email:", "supplier_email", 25)
        ]

        for label, var_name, width in fields_col2:
            frame = tk.Frame(col2, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=10,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5)
            setattr(self, var_name, entry)

        # Columna 3
        col3 = tk.Frame(supplier_fields_frame, bg="white")
        col3.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fields_col3 = [
            ("Dirección:", "supplier_address", 30),
            ("Fecha Entrega:", "delivery_date", 15)
        ]

        for label, var_name, width in fields_col3:
            frame = tk.Frame(col3, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=width
            )
            entry.pack(side=tk.LEFT, padx=5)
            setattr(self, var_name, entry)

        # Línea divisoria
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Sección Productos (estilo similar al catálogo)
        products_frame = tk.Frame(form_frame, bg="white")
        products_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para agregar productos
        add_product_frame = tk.Frame(products_frame, bg="white")
        add_product_frame.pack(fill=tk.X, pady=10)

        CustomLabel(
            add_product_frame,
            text="AGREGAR PRODUCTOS:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        # Campos para producto en una fila
        product_fields_frame = tk.Frame(add_product_frame, bg="white")
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

        # Botón para agregar producto (en la misma línea)
        btn_add_product = CustomButton(
            product_fields_frame,
            text="Agregar",
            command=self.add_product,
            padding=6,
            width=10
        )
        btn_add_product.pack(side=tk.LEFT, padx=5)

        # Tabla de productos (estilo similar al catálogo)
        table_frame = tk.Frame(products_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado de tabla
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

        # Cuerpo de la tabla con scroll
        self.table_body = tk.Frame(table_frame, bg="white", bd=1, relief=tk.SUNKEN)
        self.table_body.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.table_body, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas para la tabla
        self.canvas = tk.Canvas(self.table_body, bg="white", yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        # Frame interno para los productos
        self.products_inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.products_inner_frame, anchor=tk.NW)

        # Configurar el scroll
        self.products_inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Totales
        totals_frame = tk.Frame(form_frame, bg="white")
        totals_frame.pack(fill=tk.X, pady=10)

        # Subtotal, IVA, Total (alineados a la derecha)
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

        # Botones de acción
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

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def create_order(self) -> None:
        self.status_bar.config(text="Orden creada exitosamente")

    def clear_form(self) -> None:
        # Limpiar campos de proveedor
        for field in ["supplier_id", "supplier_first_name", "supplier_last_name",
                     "supplier_company", "supplier_address", "supplier_phone",
                     "supplier_email", "delivery_date"]:
            getattr(self, field).delete(0, tk.END)
        
        # Limpiar campos de producto
        for field in ["product_code", "product_description", 
                     "product_quantity", "product_unit_price"]:
            getattr(self, field).delete(0, tk.END)
        
        # Limpiar tabla de productos
        for widget in self.products_inner_frame.winfo_children():
            widget.destroy()
        
        # Resetear totales
        for var in self.totals.values():
            var.set("0.00")
        
        self.status_bar.config(text="Formulario limpiado")

    def search_product(self) -> None:
        self.status_bar.config(text="Buscando producto...")

    def search_supplier(self) -> None:
        self.status_bar.config(text="Buscando proveedor...")

    def view_orders(self) -> None:
        self.status_bar.config(text="Mostrando órdenes existentes...")

    def add_product(self) -> None:
        # Obtener datos del producto
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
        
        # Crear fila en la tabla
        row_frame = tk.Frame(self.products_inner_frame, bg="white")
        row_frame.pack(fill=tk.X, pady=1)
        
        # Campos de la fila
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
        
        # Botón para eliminar
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
        
        # Actualizar totales
        self.update_totals(total, add=True)
        
        # Limpiar campos de producto
        self.product_code.delete(0, tk.END)
        self.product_description.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
        self.product_unit_price.delete(0, tk.END)
        
        self.status_bar.config(text="Producto agregado a la orden")

    def remove_product(self, row_frame: tk.Frame, total: float) -> None:
        row_frame.destroy()
        self.update_totals(total, add=False)
        self.status_bar.config(text="Producto eliminado de la orden")

    def update_totals(self, amount: float, add: bool = True) -> None:
        try:
            subtotal = float(self.totals["subtotal"].get())
            iva = float(self.totals["iva"].get())
            total = float(self.totals["total"].get())
            
            if add:
                subtotal += amount
            else:
                subtotal -= amount
            
            iva = subtotal * 0.16
            total = subtotal + iva
            
            self.totals["subtotal"].set(f"{subtotal:.2f}")
            self.totals["iva"].set(f"{iva:.2f}")
            self.totals["total"].set(f"{total:.2f}")
        except ValueError:
            self.status_bar.config(text="Error actualizando totales")