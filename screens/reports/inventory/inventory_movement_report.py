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
from utils.pdf_generator import PDFGenerator

class InventoryMovementReportScreen(tk.Toplevel):
    def __init__(self, parent: tk.Widget, inventory_id: int):
        super().__init__(parent)
        self.title("Historial de Movimientos")
        self.parent = parent
        self.inventory_id = inventory_id
        self.configure(bg="#f5f5f5")
        
        self.resizable(True, True)
        self.state('zoomed')
        
        # Variables
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.movement_type_var = tk.StringVar(value="Todos")
        
        self.configure_ui()
        self.load_product_info()
        self.refresh_data()

    def configure_ui(self):
        """Configura la interfaz de usuario"""
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
        
        # Filtros de fecha
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
            font=("Arial", 10),
            placeholder="DD/MM/AAAA"
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
            font=("Arial", 10),
            placeholder="DD/MM/AAAA"
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Filtro de tipo de movimiento
        CustomLabel(
            row1_frame,
            text="Tipo:",
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
        
        # Botones de acción
        btn_pdf = CustomButton(
            row1_frame,
            text="Generar PDF",
            command=self.generate_pdf,
            padding=6,
            width=15,
        )
        btn_pdf.pack(side=tk.RIGHT, padx=5)
        
        btn_filter = CustomButton(
            row1_frame,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.RIGHT, padx=5)
        
        btn_report = CustomButton(
            row1_frame,
            text="Ver Reporte",
            command=self.generate_report,
            padding=6,
            width=15
        )
        btn_report.pack(side=tk.RIGHT, padx=5)
        
        btn_back = CustomButton(
            row1_frame,
            text="Regresar",
            command=self.destroy,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT)
        
        # Contenedor para Treeview con scrollbars
        tree_container = tk.Frame(main_frame, bg="#f5f5f5")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        xscrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        yscrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview con columnas ajustadas
        self.tree = ttk.Treeview(
            tree_container,
            columns=("Fecha", "Tipo", "Cambio Cantidad", "Cambio Stock", 
                    "Anterior Cantidad", "Nuevo Cantidad", "Anterior Stock", "Nuevo Stock",
                    "Usuario", "Referencia", "Notas"),
            show="headings",
            height=15,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        
        # Configurar columnas
        columns = [
            ("Fecha", 120, tk.CENTER),
            ("Tipo", 120, tk.CENTER),
            ("Cambio Cantidad", 100, tk.CENTER),
            ("Cambio Stock", 100, tk.CENTER), 
            ("Anterior Cantidad", 100, tk.CENTER),
            ("Nuevo Cantidad", 100, tk.CENTER),
            ("Anterior Stock", 100, tk.CENTER),
            ("Nuevo Stock", 100, tk.CENTER),
            ("Usuario", 100, tk.CENTER),
            ("Referencia", 120, tk.CENTER),
            ("Notas", 200, tk.W)
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)
        
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
            product_name = product['product'] if product['product'] != "None" else "None"
            product_code = product['code'] if product['code'] != "None" else "None"
            product_desc = product['description'] if product['description'] != "None" else "None"
            self.product_label.config(
                text=f"Producto: {product_name} ({product_code}) - {product_desc}"
            )
            self.product_info = {
                'product': product_name,
                'code': product_code,
                'description': product_desc,
                'id': product['id']
            }

    def refresh_data(self):
        """Actualiza los datos según los filtros"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener valores de los filtros
        start_date = self._parse_date(self.start_date_var.get())
        end_date = self._parse_date(self.end_date_var.get())
        movement_type = self.movement_type_var.get() if self.movement_type_var.get() != "Todos" else None
        
        movements = InventoryReport.get_inventory_movements_report(
            inventory_id=self.inventory_id,
            start_date=start_date,
            end_date=end_date,
            movement_type=movement_type
        )
        
        for movement in movements:
            notes = movement['notes'] if movement['notes'] != "None" else "None"
            reference = f"{movement['reference_type']} #{movement['reference_id']}" if movement['reference_type'] != "None" else "None"
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
                reference,
                notes
            ))
        
        self.count_label.config(text=f"{len(movements)} movimientos encontrados")
        self.current_movements = movements

    def _parse_date(self, date_str):
        """Intenta parsear la fecha del formato DD/MM/AAAA"""
        if not date_str:
            return None
            
        try:
            day, month, year = map(int, date_str.split('/'))
            return f"{year}-{month:02d}-{day:02d}"
        except (ValueError, AttributeError):
            return None

    def generate_report(self):
        """Genera el reporte visual de movimientos"""
        if hasattr(self, 'current_movements') and self.current_movements:
            report_title = f"Historial de Movimientos - {self.product_info['product']}"
            filters = self._get_current_filters()
            InventoryMovementViewer(self, report_title, self.product_info, self.current_movements, filters)
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar el reporte", parent=self)

    def generate_pdf(self):
        """Genera directamente un PDF con los movimientos"""
        if hasattr(self, 'current_movements') and self.current_movements:
            report_title = f"Historial de Movimientos - {self.product_info['product']}"
            filters = self._get_current_filters()
            PDFGenerator.generate_movement_report(
                parent=self,
                title=report_title,
                product_info=self.product_info,
                movements=self.current_movements,
                filters=filters
            )
        else:
            messagebox.showwarning("Advertencia", "No hay datos para generar PDF", parent=self)

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