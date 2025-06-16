import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from sqlite_cli.models.inventory_report_model import InventoryReport
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from reports.inventory_report_viewer import InventoryReportViewer
from reports.generate_pdf.invetory_report_pdf import InventoryReportPDF

class FullInventoryReportScreen(tk.Toplevel):
    def __init__(self, parent: tk.Widget, initial_search: Optional[str] = None):
        super().__init__(parent)
        self.title("Reporte Completo de Inventario")
        self.parent = parent
        self.configure(bg="#f5f5f5")
        
        self.resizable(True, True)
        self.state('zoomed')
        
        # Variables
        self.search_var = tk.StringVar(value=initial_search if initial_search else "")
        self.quantity_var = tk.StringVar()
        self.existencia_var = tk.StringVar()
        self.min_stock_var = tk.StringVar()
        self.max_stock_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        
        self.configure_ui()
        self.refresh_data()

    def configure_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de filtros (3 filas exactas)
        filters_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
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
        
        btn_filter = CustomButton(
            row1_frame,
            text="Filtrar",
            command=self.apply_filters,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.LEFT, padx=5)
        
        # Fila 2: Cantidad y Existencias
        row2_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row2_frame.pack(fill=tk.X, pady=5)
        
        # Cantidad
        CustomLabel(
            row2_frame,
            text="Cantidad:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        CustomEntry(
            row2_frame,
            textvariable=self.quantity_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        ).pack(side=tk.LEFT, padx=5)
        
        # Existencias
        CustomLabel(
            row2_frame,
            text="Existencias:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        CustomEntry(
            row2_frame,
            textvariable=self.existencia_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        ).pack(side=tk.LEFT, padx=5)
        
        # Fila 3: Stock mínimo, Stock máximo, Proveedor y botones
        row3_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row3_frame.pack(fill=tk.X, pady=5)
        
        # Stock mínimo
        CustomLabel(
            row3_frame,
            text="Stock Mín:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        CustomEntry(
            row3_frame,
            textvariable=self.min_stock_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        ).pack(side=tk.LEFT, padx=5)
        
        # Stock máximo
        CustomLabel(
            row3_frame,
            text="Stock Máx:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        CustomEntry(
            row3_frame,
            textvariable=self.max_stock_var,
            width=10,
            font=("Arial", 10),
            justify=tk.CENTER
        ).pack(side=tk.LEFT, padx=5)
        
        # Proveedor
        CustomLabel(
            row3_frame,
            text="Proveedor:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        CustomEntry(
            row3_frame,
            textvariable=self.supplier_var,
            width=15,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        # Botones de acción en la misma fila 3
        btn_pdf = CustomButton(
            row3_frame,
            text="Generar PDF",
            command=self.generate_pdf,
            padding=6,
            width=15,
        )
        btn_pdf.pack(side=tk.RIGHT, padx=5)
        
        btn_report = CustomButton(
            row3_frame,
            text="Generar Reporte",
            command=self.generate_report,
            padding=6,
            width=15
        )
        btn_report.pack(side=tk.RIGHT, padx=5)
        
        btn_back = CustomButton(
            row3_frame,
            text="Regresar",
            command=self.destroy,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT)
        
        # Treeview con scrollbars
        tree_container = tk.Frame(main_frame, bg="#f5f5f5")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        xscrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        yscrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (sin estado)
        self.tree = ttk.Treeview(
            tree_container,
            columns=("ID", "Código", "Producto", "Descripción", "Cantidad", 
                    "Existencias", "Stock mínimo", "Stock máximo", 
                    "Precio compra", "Precio venta", "Proveedor", "Vencimiento"),
            show="headings",
            height=20,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 70, tk.CENTER),
            ("Existencias", 80, tk.CENTER),
            ("Stock mínimo", 80, tk.CENTER),
            ("Stock máximo", 80, tk.CENTER),
            ("Precio compra", 90, tk.CENTER),
            ("Precio venta", 90, tk.CENTER),
            ("Proveedor", 120, tk.W),
            ("Vencimiento", 100, tk.CENTER)
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        # Contador de resultados
        self.count_label = CustomLabel(
            main_frame,
            text="0 productos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def apply_filters(self):
        """Aplica los filtros"""
        search_term = self.search_var.get() or None
        quantity = int(self.quantity_var.get()) if self.quantity_var.get().isdigit() else None
        min_stock = int(self.min_stock_var.get()) if self.min_stock_var.get().isdigit() else None
        max_stock = int(self.max_stock_var.get()) if self.max_stock_var.get().isdigit() else None
        supplier = self.supplier_var.get() or None
        
        items = InventoryReport.get_inventory_report(
            search_term=search_term,
            supplier_id=supplier,
            min_quantity=quantity,
            max_quantity=quantity,
            min_stock=min_stock,
            max_stock=max_stock
        )
        
        if items:
            self.update_table(items)
        else:
            messagebox.showinfo("Información", "No se encontraron coincidencias", parent=self)

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
                item.get('expiration_date', '')
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
            InventoryReportPDF.generate_inventory_report(
                parent=self,
                title="Reporte de Inventario",
                items=self.current_items,
                filters=""
            )
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar PDF", parent=self)