import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from datetime import datetime
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.sales_report_model import SalesReport
from sqlite_cli.models.customer_model import Customer
from reports.InvoiceViewer import InvoiceViewer
from utils.session_manager import SessionManager
from utils.pdf_generator import PDFGenerator
from utils.field_formatter import FieldFormatter

class SalesReportScreen(tk.Frame):
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
            text="Reporte de Ventas",
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

        # Botón Ver Recibo
        btn_view = CustomButton(
            btn_frame,
            text="Ver Recibo",
            command=self.view_invoice,
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

        # Treeview para mostrar las ventas
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Fecha", "Cliente", "Cédula", "Tipo", "Productos", "Servicios", "Total"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 70, tk.CENTER),
            ("Fecha", 120, tk.CENTER),
            ("Cliente", 180, tk.W),
            ("Cédula", 100, tk.CENTER),
            ("Tipo", 80, tk.CENTER),
            ("Productos", 80, tk.CENTER),
            ("Servicios", 80, tk.CENTER),
            ("Total", 100, tk.CENTER)
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

        # Obtener reporte de ventas
        sales = SalesReport.get_sales_report(
            start_date=start_date,
            end_date=end_date,
            search_term=search_term if search_term else None
        )

        # Actualizar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for sale in sales:
            self.tree.insert("", tk.END, values=(
                sale['invoice_id'],
                sale['issue_date'],
                sale['customer_name'],
                sale['customer_id_number'],
                sale['invoice_type'],
                sale['product_count'],
                sale['service_count'],
                f"Bs. {sale['total']:,.2f}"
            ))

    def view_invoice(self, event=None) -> None:
        """Muestra el recibo de la venta seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una venta", parent=self)
            return
            
        invoice_id = self.tree.item(selected[0])['values'][0]
        invoice_data = SalesReport.get_invoice_details(invoice_id)
        
        # Preparar items para el InvoiceViewer
        items = []
        for item in invoice_data['items']:
            items.append({
                'id': item['product_id'] or item['service_request_id'],
                'name': item['item_name'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total': item['subtotal'],
                'is_service': item['item_type'] == 'service'
            })
        
        # Mostrar el recibo
        InvoiceViewer(
            self,
            invoice_id=invoice_data['id'],
            customer_info=f"{invoice_data['customer_name']} - {invoice_data['customer_id_number']}",
            items=items,
            subtotal=invoice_data['subtotal'],
            taxes=invoice_data['taxes'],
            total=invoice_data['total']
        )

    def generate_pdf(self) -> None:
        """Genera PDF del recibo seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una venta", parent=self)
            return
            
        invoice_id = self.tree.item(selected[0])['values'][0]
        invoice_data = SalesReport.get_invoice_details(invoice_id)
        
        # Preparar items para el PDF
        items = []
        for item in invoice_data['items']:
            items.append({
                'id': item['product_id'] or item['service_request_id'],
                'name': item['item_name'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total': item['subtotal'],
                'is_service': item['item_type'] == 'service'
            })
        
        # Obtener información del empleado
        current_user = SessionManager.get_current_user()
        employee_info = "No disponible"
        if current_user:
            if 'first_name' in current_user and 'last_name' in current_user:
                employee_info = f"{current_user['first_name']} {current_user['last_name']}"
                if current_user.get('username'):
                    employee_info += f" ({current_user['username']})"
            elif 'username' in current_user:
                employee_info = current_user['username']
            elif 'id' in current_user:
                employee_info = f"Empleado ID: {current_user['id']}"
        
        # Generar PDF
        PDFGenerator.generate_invoice(
            parent=self,
            invoice_id=invoice_data['id'],
            customer_info=f"{invoice_data['customer_name']} - {invoice_data['customer_id_number']}",
            items=items,
            subtotal=invoice_data['subtotal'],
            taxes=invoice_data['taxes'],
            total=invoice_data['total'],
            employee_info=employee_info
        )

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')
        self.open_previous_screen_callback()