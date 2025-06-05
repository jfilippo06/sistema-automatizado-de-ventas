import tkinter as tk
from tkinter import ttk
from typing import Callable, Any
from datetime import datetime
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.purchase_order_report_model import PurchaseOrderReport
from sqlite_cli.models.supplier_model import Supplier
from reports.purchase_order_viewer import PurchaseOrderViewer

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
        self.supplier_var = tk.StringVar()
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

        # Back button
        btn_back = CustomButton(
            header_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT, padx=20, pady=5)

        # Filters frame
        filters_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        filters_frame.pack(fill=tk.X)

        # Date filter
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
        start_date_entry.insert(0, datetime.now().strftime("%Y-%m-01"))

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
        end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Bind date changes to refresh
        self.start_date_var.trace_add("write", lambda *args: self.refresh_data())
        self.end_date_var.trace_add("write", lambda *args: self.refresh_data())

        # Supplier filter
        supplier_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        supplier_frame.pack(side=tk.LEFT, padx=20)

        CustomLabel(
            supplier_frame,
            text="Proveedor:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        self.supplier_combobox = CustomCombobox(
            supplier_frame,
            textvariable=self.supplier_var,
            width=30,
            font=("Arial", 10)
        )
        self.supplier_combobox.pack(side=tk.LEFT, padx=5)
        self.load_suppliers()
        
        # Bind supplier changes to refresh
        self.supplier_var.trace_add("write", lambda *args: self.refresh_data())

        # Search field
        search_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        CustomLabel(
            search_frame,
            text="Buscar (N° Orden/Proveedor):",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            font=("Arial", 10)
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Bind search changes to refresh
        self.search_var.trace_add("write", lambda *args: self.refresh_data())

        # Treeview to show orders
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "N° Orden", "Fecha", "Proveedor", "Productos", "Subtotal", "IVA", "Total", "Estado", "Entrega"),
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
            ("Estado", 100, tk.CENTER),
            ("Entrega", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind double click to view order
        self.tree.bind("<Double-1>", self.view_order)

    def load_suppliers(self):
        """Load suppliers list into combobox"""
        suppliers = Supplier.search_active()
        supplier_list = [f"{s['company']} ({s['id_number']})" for s in suppliers]
        self.supplier_combobox['values'] = supplier_list

    def refresh_data(self) -> None:
        """Refresh report data based on filters"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        supplier = self.supplier_var.get()
        search_term = self.search_var.get()

        # Get supplier ID if selected
        supplier_id = None
        if supplier:
            try:
                id_number = supplier.split("(")[-1].rstrip(")")
                supplier_data = Supplier.get_by_id_number(id_number)
                if supplier_data:
                    supplier_id = supplier_data['id']
            except:
                pass

        # Get purchase orders report
        orders = PurchaseOrderReport.get_purchase_orders_report(
            start_date=start_date,
            end_date=end_date,
            supplier_id=supplier_id,
            search_term=search_term if search_term else None
        )

        # Update treeview
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
                order['status_name'],
                order['expected_delivery_date']
            ))

    def view_order(self, event) -> None:
        """View the selected purchase order"""
        selected = self.tree.selection()
        if not selected:
            return
            
        order_id = self.tree.item(selected[0])['values'][0]
        order_data = PurchaseOrderReport.get_order_details(order_id)
        
        # Prepare items for PurchaseOrderViewer
        items = []
        for item in order_data['items']:
            items.append({
                'code': item.get('product_code', ''),
                'description': item.get('product_name', item['product_name']),
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total': item['subtotal']
            })
        
        # Show the order
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

    def go_back(self) -> None:
        """Go back to previous screen"""
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()