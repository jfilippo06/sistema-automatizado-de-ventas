import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime
from sqlite_cli.models.inventory_report_model import InventoryReport
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from reports.inventory_report_viewer import InventoryReportViewer

class FullInventoryReportScreen(tk.Toplevel):
    def __init__(self, parent: tk.Widget, initial_search: Optional[str] = None):
        super().__init__(parent)
        self.title("Reporte Completo de Inventario")
        self.parent = parent
        self.configure(bg="#f5f5f5")
        
        self.resizable(False, False)
        self.state('zoomed')
        
        # Variables
        self.search_var = tk.StringVar(value=initial_search if initial_search else "")
        self.supplier_var = tk.StringVar()
        self.min_stock_var = tk.StringVar()
        self.max_stock_var = tk.StringVar()
        self.min_quantity_var = tk.StringVar()
        self.max_quantity_var = tk.StringVar()
        self.expired_only_var = tk.BooleanVar(value=False)
        
        self.configure_ui()
        self.refresh_data()

    def configure_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de filtros
        filters_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        filters_frame.pack(fill=tk.X)
        
        # Fila 1 de filtros
        row1_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row1_frame.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            row1_frame,
            text="Buscar:",
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
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())
        
        CustomLabel(
            row1_frame,
            text="Proveedor:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        supplier_entry = CustomEntry(
            row1_frame,
            textvariable=self.supplier_var,
            width=20,
            font=("Arial", 10)
        )
        supplier_entry.pack(side=tk.LEFT, padx=5)
        
        # Fila 2 de filtros
        row2_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row2_frame.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            row2_frame,
            text="Existencias Mín:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        min_stock_entry = CustomEntry(
            row2_frame,
            textvariable=self.min_stock_var,
            width=8,
            font=("Arial", 10)
        )
        min_stock_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            row2_frame,
            text="Existencias Máx:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        max_stock_entry = CustomEntry(
            row2_frame,
            textvariable=self.max_stock_var,
            width=8,
            font=("Arial", 10)
        )
        max_stock_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            row2_frame,
            text="Almacén Mín:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        min_quantity_entry = CustomEntry(
            row2_frame,
            textvariable=self.min_quantity_var,
            width=8,
            font=("Arial", 10)
        )
        min_quantity_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            row2_frame,
            text="Almacén Máx:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        max_quantity_entry = CustomEntry(
            row2_frame,
            textvariable=self.max_quantity_var,
            width=8,
            font=("Arial", 10)
        )
        max_quantity_entry.pack(side=tk.LEFT, padx=5)
        
        # Fila 3 de filtros
        row3_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row3_frame.pack(fill=tk.X, pady=5)
        
        tk.Checkbutton(
            row3_frame,
            text="Solo productos vencidos",
            variable=self.expired_only_var,
            bg="#f5f5f5",
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        # Botón de regresar
        btn_back = CustomButton(
            row3_frame,
            text="Regresar",
            command=self.destroy,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT, padx=5)
        
        # Botón de generar reporte
        btn_report = CustomButton(
            row3_frame,
            text="Generar Reporte",
            command=self.generate_report,
            padding=6,
            width=15
        )
        btn_report.pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(main_frame, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Código", "Producto", "Descripción", "Cantidad", "Existencias", 
                    "Stock mínimo", "Stock máximo", "Precio compra", "Precio venta", 
                    "Proveedor", "Vencimiento", "Estado"),
            show="headings",
            height=20
        )
        
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
            ("Proveedor", 150, tk.W),
            ("Vencimiento", 100, tk.CENTER),
            ("Estado", 100, tk.CENTER)
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
            
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Contador de resultados
        self.count_label = CustomLabel(
            main_frame,
            text="0 productos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def refresh_data(self):
        """Actualiza los datos según los filtros"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener valores de los filtros
        search_term = self.search_var.get() if self.search_var.get() else None
        supplier_id = self.supplier_var.get() if self.supplier_var.get() else None
        min_stock = int(self.min_stock_var.get()) if self.min_stock_var.get().isdigit() else None
        max_stock = int(self.max_stock_var.get()) if self.max_stock_var.get().isdigit() else None
        min_quantity = int(self.min_quantity_var.get()) if self.min_quantity_var.get().isdigit() else None
        max_quantity = int(self.max_quantity_var.get()) if self.max_quantity_var.get().isdigit() else None
        expired_only = self.expired_only_var.get()
        
        items = InventoryReport.get_inventory_report(
            search_term=search_term,
            supplier_id=supplier_id,
            min_stock=min_stock,
            max_stock=max_stock,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            expired_only=expired_only
        )
        
        for item in items:
            expiration_date = item['expiration_date'] if item['expiration_date'] else ""
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
                item['supplier_company'] if item['supplier_company'] else "",
                expiration_date,
                item['status']
            ))
        
        self.count_label.config(text=f"{len(items)} productos encontrados")
        self.current_items = items  # Store items for report generation

    def generate_report(self):
        """Genera el reporte visual de inventario"""
        if hasattr(self, 'current_items') and self.current_items:
            report_title = "Reporte Completo de Inventario"
            filters = self._get_current_filters()
            InventoryReportViewer(self, report_title, self.current_items, filters)
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar el reporte", parent=self)

    def _get_current_filters(self):
        """Obtiene los filtros actuales aplicados"""
        filters = []
        
        if self.search_var.get():
            filters.append(f"Búsqueda: {self.search_var.get()}")
        if self.supplier_var.get():
            filters.append(f"Proveedor: {self.supplier_var.get()}")
        if self.min_stock_var.get():
            filters.append(f"Existencias mín: {self.min_stock_var.get()}")
        if self.max_stock_var.get():
            filters.append(f"Existencias máx: {self.max_stock_var.get()}")
        if self.min_quantity_var.get():
            filters.append(f"Almacén mín: {self.min_quantity_var.get()}")
        if self.max_quantity_var.get():
            filters.append(f"Almacén máx: {self.max_quantity_var.get()}")
        if self.expired_only_var.get():
            filters.append("Solo productos vencidos")
            
        return ", ".join(filters) if filters else "Sin filtros aplicados"