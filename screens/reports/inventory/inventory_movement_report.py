import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime
from sqlite_cli.models.inventory_report_model import InventoryReport
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from reports.inventory_movement_viewer import InventoryMovementViewer

class InventoryMovementReportScreen(tk.Toplevel):
    def __init__(self, parent: tk.Widget, inventory_id: int):
        super().__init__(parent)
        self.title("Historial de Movimientos")
        self.parent = parent
        self.inventory_id = inventory_id
        self.configure(bg="#f5f5f5")
        
        self.resizable(False, False)
        self.state('zoomed')
        
        # Variables
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.movement_type_var = tk.StringVar()
        
        self.configure_ui()
        self.load_product_info()
        self.refresh_data()

    def configure_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del producto
        product_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        product_frame.pack(fill=tk.X)
        
        self.product_label = CustomLabel(
            product_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        )
        self.product_label.pack(anchor=tk.W)
        
        # Frame de filtros
        filters_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        filters_frame.pack(fill=tk.X)
        
        # Fila 1 de filtros
        row1_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row1_frame.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            row1_frame,
            text="Desde:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        start_date_entry = CustomEntry(
            row1_frame,
            textvariable=self.start_date_var,
            width=12,
            font=("Arial", 10)
        )
        start_date_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            row1_frame,
            text="Hasta:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        end_date_entry = CustomEntry(
            row1_frame,
            textvariable=self.end_date_var,
            width=12,
            font=("Arial", 10)
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            row1_frame,
            text="Tipo de Movimiento:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        movement_types = ["Todos", "Entrada inicial", "Ajuste positivo", "Ajuste negativo", "Venta", "Compra"]
        movement_combobox = CustomCombobox(
            row1_frame,
            textvariable=self.movement_type_var,
            values=movement_types,
            width=15,
            font=("Arial", 10)
        )
        movement_combobox.pack(side=tk.LEFT, padx=5)
        movement_combobox.current(0)
        
        # Botón de regresar
        btn_back = CustomButton(
            row1_frame,
            text="Regresar",
            command=self.destroy,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT, padx=5)
        
        # Botón de generar reporte
        btn_report = CustomButton(
            row1_frame,
            text="Generar Reporte",
            command=self.generate_report,
            padding=6,
            width=15
        )
        btn_report.pack(side=tk.RIGHT, padx=5)
        
        # Botón de filtrar
        btn_filter = CustomButton(
            row1_frame,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(main_frame, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Fecha", "Tipo", "Cambio Stock", "Cambio Stock", 
                    "Anterior Stock", "Nuevo Stock", "Anterior Disp.", "Nuevo Disp.", 
                    "Usuario", "Referencia", "Notas"),
            show="headings",
            height=15
        )
        
        columns = [
            ("Fecha", 120, tk.CENTER),
            ("Tipo", 120, tk.CENTER),
            ("Cambio Stock", 100, tk.CENTER),
            ("Cambio Stock", 100, tk.CENTER),
            ("Anterior Stock", 100, tk.CENTER),
            ("Nuevo Stock", 100, tk.CENTER),
            ("Anterior Disp.", 100, tk.CENTER),
            ("Nuevo Disp.", 100, tk.CENTER),
            ("Usuario", 100, tk.CENTER),
            ("Referencia", 100, tk.CENTER),
            ("Notas", 200, tk.W)
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
            text="0 movimientos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def load_product_info(self):
        """Carga la información del producto seleccionado"""
        from sqlite_cli.models.inventory_model import InventoryItem
        product = InventoryItem.get_by_id(self.inventory_id)
        if product:
            self.product_label.config(
                text=f"Producto: {product['product']} ({product['code']}) - {product['description']}"
            )
            self.product_info = product

    def refresh_data(self):
        """Actualiza los datos según los filtros"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener valores de los filtros
        start_date = self.start_date_var.get() if self.start_date_var.get() else None
        end_date = self.end_date_var.get() if self.end_date_var.get() else None
        movement_type = self.movement_type_var.get() if self.movement_type_var.get() != "Todos" else None
        
        movements = InventoryReport.get_inventory_movements_report(
            inventory_id=self.inventory_id,
            start_date=start_date,
            end_date=end_date,
            movement_type=movement_type
        )
        
        for movement in movements:
            self.tree.insert("", tk.END, values=(
                movement['created_at'],
                movement['movement_type'],
                movement['quantity_change'],
                movement['stock_change'],
                movement['previous_quantity'],
                movement['new_quantity'],
                movement['previous_stock'],
                movement['new_stock'],
                movement['user'],
                f"{movement['reference_type']} #{movement['reference_id']}" if movement['reference_type'] else "",
                movement['notes']
            ))
        
        self.count_label.config(text=f"{len(movements)} movimientos encontrados")
        self.current_movements = movements  # Store movements for report generation

    def generate_report(self):
        """Genera el reporte visual de movimientos"""
        if hasattr(self, 'current_movements') and self.current_movements:
            report_title = f"Historial de Movimientos - {self.product_info['product']}"
            filters = self._get_current_filters()
            InventoryMovementViewer(self, report_title, self.product_info, self.current_movements, filters)
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar el reporte", parent=self)

    def _get_current_filters(self):
        """Obtiene los filtros actuales aplicados"""
        filters = []
        
        if self.start_date_var.get():
            filters.append(f"Desde: {self.start_date_var.get()}")
        if self.end_date_var.get():
            filters.append(f"Hasta: {self.end_date_var.get()}")
        if self.movement_type_var.get() != "Todos":
            filters.append(f"Tipo: {self.movement_type_var.get()}")
            
        return ", ".join(filters) if filters else "Sin filtros aplicados"