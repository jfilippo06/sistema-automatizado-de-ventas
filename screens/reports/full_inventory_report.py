import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Optional, Callable
from sqlite_cli.models.inventory_report_model import InventoryReport
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_checkbutton import CustomCheckbutton
from reports.inventory_report_viewer import InventoryReportViewer
from utils.pdf_generator import PDFGenerator
from utils.field_formatter import FieldFormatter

class FullInventoryReportScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None],
        initial_search: Optional[str] = None
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")
        
        # Variables
        self.search_var = tk.StringVar(value=initial_search if initial_search else "")
        self.quantity_var = tk.StringVar()
        self.existencia_var = tk.StringVar()
        self.min_stock_var = tk.StringVar()
        self.max_stock_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.most_sold_var = tk.BooleanVar(value=False)
        
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self):
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = CustomLabel(
            header_frame,
            text="Reporte de productos",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Botón de regreso
        btn_back = CustomButton(
            header_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT, padx=20, pady=5)

        # Frame de filtros
        filters_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        filters_frame.pack(fill=tk.X)

        # Fila 1: Búsqueda de producto + botón Filtrar
        row1_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row1_frame.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            row1_frame,
            text="Buscar Producto:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        search_entry = CustomEntry(
            row1_frame,
            textvariable=self.search_var,
            width=30,
            font=("Arial", 10)
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(search_entry, 'first_name')
        
        btn_filter = CustomButton(
            row1_frame,
            text="Filtrar",
            command=self.apply_filters,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.LEFT, padx=5)
        
        btn_clear = CustomButton(
            row1_frame,
            text="Limpiar",
            command=self.clear_filters,
            padding=6,
            width=10
        )
        btn_clear.pack(side=tk.LEFT, padx=5)

        # Fila 2: Stock, Stock min y Stock max
        row2_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row2_frame.pack(fill=tk.X, pady=5)
        
        # Stock
        CustomLabel(
            row2_frame,
            text="Stock:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        existencia_entry = CustomEntry(
            row2_frame,
            textvariable=self.existencia_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        )
        existencia_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(existencia_entry, 'integer')
        
        # Stock mínimo
        CustomLabel(
            row2_frame,
            text="Stock Mín:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        min_stock_entry = CustomEntry(
            row2_frame,
            textvariable=self.min_stock_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        )
        min_stock_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(min_stock_entry, 'integer')
        
        # Stock máximo
        CustomLabel(
            row2_frame,
            text="Stock Máx:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        max_stock_entry = CustomEntry(
            row2_frame,
            textvariable=self.max_stock_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        )
        max_stock_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(max_stock_entry, 'integer')

        # Fila 3: Proveedor, Fechas y Checkbox
        row3_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row3_frame.pack(fill=tk.X, pady=5)
        
        # Proveedor
        CustomLabel(
            row3_frame,
            text="Proveedor:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        supplier_entry = CustomEntry(
            row3_frame,
            textvariable=self.supplier_var,
            width=15,
            font=("Arial", 10)
        )
        supplier_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(supplier_entry, 'first_name')
        
        # Fechas de vencimiento
        CustomLabel(
            row3_frame,
            text="Vencimiento Desde:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        start_date_entry = CustomEntry(
            row3_frame,
            textvariable=self.start_date_var,
            width=12,
            font=("Arial", 10)
        )
        start_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(start_date_entry, 'date')
        
        CustomLabel(
            row3_frame,
            text="Hasta:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        end_date_entry = CustomEntry(
            row3_frame,
            textvariable=self.end_date_var,
            width=12,
            font=("Arial", 10)
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(end_date_entry, 'date')
        
        # Checkbox para productos más vendidos
        most_sold_check = CustomCheckbutton(
            row3_frame,
            text="Mostrar más vendidos primero",
            variable=self.most_sold_var,
        )
        most_sold_check.pack(side=tk.LEFT, padx=10)

        # Botones de acción
        btn_frame = tk.Frame(row3_frame, bg="#f5f5f5")
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        btn_report = CustomButton(
            btn_frame,
            text="Ver Reporte",
            command=self.generate_report,
            padding=6,
            width=15
        )
        btn_report.pack(side=tk.LEFT, padx=5)
        
        btn_pdf = CustomButton(
            btn_frame,
            text="Generar PDF",
            command=self.generate_pdf,
            padding=6,
            width=15,
        )
        btn_pdf.pack(side=tk.LEFT, padx=5)

        # Treeview con scroll horizontal y vertical
        tree_container = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_container.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scroll horizontal
        h_scroll = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Scroll vertical
        v_scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_container,
            columns=("ID", "Código", "Producto", "Descripción", "Cantidad", 
                    "Stock", "Stock mínimo", "Stock máximo", 
                    "Precio compra", "Precio venta", "Proveedor", "Vencimiento", "Ventas"),
            show="headings",
            height=20,
            style="Custom.Treeview",
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 70, tk.CENTER),
            ("Stock", 80, tk.CENTER),
            ("Stock mínimo", 80, tk.CENTER),
            ("Stock máximo", 80, tk.CENTER),
            ("Precio compra", 90, tk.CENTER),
            ("Precio venta", 90, tk.CENTER),
            ("Proveedor", 120, tk.W),
            ("Vencimiento", 100, tk.CENTER),
            ("Ventas", 80, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.pack(fill=tk.BOTH, expand=True)
        h_scroll.config(command=self.tree.xview)
        v_scroll.config(command=self.tree.yview)

        # Contador de resultados
        self.count_label = CustomLabel(
            self,
            text="0 productos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def clear_filters(self):
        """Limpia todos los filtros y refresca los datos"""
        self.search_var.set("")
        self.quantity_var.set("")
        self.existencia_var.set("")
        self.min_stock_var.set("")
        self.max_stock_var.set("")
        self.supplier_var.set("")
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.most_sold_var.set(False)
        self.refresh_data()

    def apply_filters(self):
        """Aplica los filtros"""
        try:
            search_term = self.search_var.get() or None
            supplier = self.supplier_var.get() or None
            
            # Convertir valores numéricos
            quantity = int(self.quantity_var.get()) if self.quantity_var.get().isdigit() else None
            min_stock = int(self.min_stock_var.get()) if self.min_stock_var.get().isdigit() else None
            max_stock = int(self.max_stock_var.get()) if self.max_stock_var.get().isdigit() else None
            
            # Procesar fechas de vencimiento
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            
            if start_date:
                try:
                    # Convertir de DD/MM/AAAA a AAAA-MM-DD
                    day, month, year = start_date.split('/')
                    start_date = f"{year}-{month}-{day}"
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA", parent=self)
                    return
                    
            if end_date:
                try:
                    # Convertir de DD/MM/AAAA a AAAA-MM-DD
                    day, month, year = end_date.split('/')
                    end_date = f"{year}-{month}-{day}"
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA", parent=self)
                    return
            
            items = InventoryReport.get_inventory_report(
                search_term=search_term,
                supplier_id=supplier,
                min_quantity=quantity,
                max_quantity=quantity,
                min_stock=min_stock,
                max_stock=max_stock,
                start_date=start_date,
                end_date=end_date,
                order_by_sales=self.most_sold_var.get()
            )
            
            if items:
                self.update_table(items)
            else:
                messagebox.showinfo("Información", "No se encontraron coincidencias", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los filtros: {str(e)}", parent=self)

    def refresh_data(self):
        """Carga todos los datos iniciales"""
        items = InventoryReport.get_inventory_report()
        self.update_table(items)

    def update_table(self, items):
        """Actualiza la tabla"""
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['description'],
                item['quantity'],
                item['stock'],
                item['min_stock'],
                item['max_stock'],
                f"{item['cost']:.2f}",
                f"{item['price']:.2f}",
                item.get('supplier_company', ''),
                item.get('expiration_date', ''),
                item.get('sales_count', 0)
            ))
        self.count_label.config(text=f"{len(items)} productos encontrados")
        self.current_items = items

    def generate_report(self):
        """Genera el reporte visual"""
        if hasattr(self, 'current_items') and self.current_items:
            InventoryReportViewer(self, "Reporte de Inventario", self.current_items, "")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar reporte", parent=self)

    def generate_pdf(self):
        """Genera el reporte en PDF"""
        if hasattr(self, 'current_items') and self.current_items:
            PDFGenerator.generate_inventory_report(
                parent=self,
                title="Reporte de Inventario",
                items=self.current_items,
                filters=""
            )
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar PDF", parent=self)

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')
        self.open_previous_screen_callback()