import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from datetime import datetime
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from sqlite_cli.models.purchase_order_report_model import PurchaseOrderReport
from reports.purchase_order_viewer import PurchaseOrderViewer
from utils.pdf_generator import PDFGenerator
from utils.field_formatter import FieldFormatter

class PurchaseOrderReportScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.configure(bg="#f5f5f5")
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = CustomLabel(
            header_frame,
            text="Reporte de Órdenes de Compra",
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

        # Filtro por fechas
        date_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        date_frame.pack(side=tk.LEFT, padx=5)

        CustomLabel(
            date_frame,
            text="Desde:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        start_date_entry = CustomEntry(
            date_frame,
            textvariable=self.start_date_var,
            width=12,
            font=("Arial", 10)
        )
        start_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(start_date_entry, 'date')

        CustomLabel(
            date_frame,
            text="Hasta:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))

        end_date_entry = CustomEntry(
            date_frame,
            textvariable=self.end_date_var,
            width=12,
            font=("Arial", 10)
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(end_date_entry, 'date')

        # Campo de búsqueda y botones
        search_btn_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        search_btn_frame.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

        # Campo de búsqueda
        search_frame = tk.Frame(search_btn_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        CustomLabel(
            search_frame,
            text="Buscar:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 10)
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Botones de acción
        btn_frame = tk.Frame(search_btn_frame, bg="#f5f5f5")
        btn_frame.pack(side=tk.RIGHT, padx=5)

        # Botón Filtrar
        btn_filter = CustomButton(
            btn_frame,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10,
        )
        btn_filter.pack(side=tk.LEFT, padx=5)

        # Botón Limpiar
        btn_clear = CustomButton(
            btn_frame,
            text="Limpiar",
            command=self.clear_filters,
            padding=6,
            width=10,
        )
        btn_clear.pack(side=tk.LEFT, padx=5)

        # Botón Ver Orden
        btn_view = CustomButton(
            btn_frame,
            text="Ver Orden",
            command=self.view_order,
            padding=6,
            width=12,
        )
        btn_view.pack(side=tk.LEFT, padx=5)

        # Botón Generar PDF
        btn_pdf = CustomButton(
            btn_frame,
            text="Generar PDF",
            command=self.generate_pdf,
            padding=6,
            width=12,
        )
        btn_pdf.pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar las órdenes
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "N° Orden", "Fecha", "Proveedor", "Productos", "Subtotal", "IVA", "Total", "Entrega"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("N° Orden", 100, tk.CENTER),
            ("Fecha", 100, tk.CENTER),
            ("Proveedor", 200, tk.W),
            ("Productos", 80, tk.CENTER),
            ("Subtotal", 100, tk.CENTER),
            ("IVA", 80, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Entrega", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def clear_filters(self):
        """Limpia todos los filtros de búsqueda"""
        self.search_var.set("")
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.refresh_data()

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        start_date = self.start_date_var.get().replace("/", "-") if self.start_date_var.get() else None
        end_date = self.end_date_var.get().replace("/", "-") if self.end_date_var.get() else None
        search_term = self.search_var.get()

        # Obtener reporte de órdenes de compra
        orders = PurchaseOrderReport.get_purchase_orders_report(
            start_date=start_date,
            end_date=end_date,
            search_term=search_term if search_term else None
        )

        # Actualizar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for order in orders:
            self.tree.insert("", tk.END, values=(
                order['id'],
                order['order_number'],
                order['issue_date'],
                order['supplier_company'],
                order['product_count'],
                f"Bs. {order['subtotal']:,.2f}",
                f"Bs. {order['taxes']:,.2f}",
                f"Bs. {order['total']:,.2f}",
                order['expected_delivery_date']
            ))

    def view_order(self) -> None:
        """Muestra la orden de compra seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una orden", parent=self)
            return
            
        order_id = self.tree.item(selected[0])['values'][0]
        order_data = PurchaseOrderReport.get_order_details(order_id)
        
        # Preparar items para el visor
        items = []
        for item in order_data['items']:
            items.append({
                'code': item.get('product_code', ''),
                'description': item.get('product_name', item['product_name']),
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total': item['subtotal']
            })
        
        # Mostrar la orden
        PurchaseOrderViewer(
            self,
            order_number=order_data['order_number'],
            supplier_info=f"{order_data['supplier_company']} - {order_data['supplier_id_number']}",
            items=items,
            subtotal=order_data['subtotal'],
            taxes=order_data['taxes'],
            total=order_data['total'],
            delivery_date=order_data['expected_delivery_date'],
            created_by=order_data['created_by']
        )

    def generate_pdf(self) -> None:
        """Genera PDF de la orden seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una orden", parent=self)
            return
            
        order_id = self.tree.item(selected[0])['values'][0]
        order_data = PurchaseOrderReport.get_order_details(order_id)
        
        # Preparar items para el PDF
        items = []
        for item in order_data['items']:
            items.append({
                'code': item.get('product_code', ''),
                'description': item.get('product_name', item['product_name']),
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total': item['subtotal']
            })
        
        # Generar PDF
        PDFGenerator.generate_purchase_order(
            parent=self,
            order_number=order_data['order_number'],
            supplier_info=f"{order_data['supplier_company']} - {order_data['supplier_id_number']}",
            items=items,
            subtotal=order_data['subtotal'],
            taxes=order_data['taxes'],
            total=order_data['total'],
            delivery_date=order_data['expected_delivery_date'],
            created_by=order_data['created_by']
        )

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')
        self.open_previous_screen_callback()