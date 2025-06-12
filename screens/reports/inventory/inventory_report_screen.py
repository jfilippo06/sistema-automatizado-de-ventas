import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from datetime import datetime
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from sqlite_cli.models.inventory_report_model import InventoryReport
from utils.session_manager import SessionManager
from screens.reports.inventory.inventory_movement_report import InventoryMovementReportScreen
from screens.reports.inventory.full_inventory_report import FullInventoryReportScreen

class InventoryReportScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.configure(bg="#f5f5f5")
        self.selected_item_id = None
        self.configure_ui()

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

        # Campo de búsqueda
        search_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        CustomLabel(
            search_frame,
            text="Buscar (Código/Nombre/Descripción):",
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
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

        # Botón de reporte completo
        btn_full_report = CustomButton(
            filters_frame,
            text="Reporte Completo",
            command=self.open_full_report,
            padding=6,
            width=20
        )
        btn_full_report.pack(side=tk.RIGHT, padx=5)

        # Botón de reporte de movimientos
        btn_movements = CustomButton(
            filters_frame,
            text="Historial del Producto",
            command=self.open_movement_report,
            padding=6,
            width=20
        )
        btn_movements.pack(side=tk.RIGHT, padx=5)
        self.btn_movements = btn_movements

        # Treeview para mostrar el inventario
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Código", "Producto", "Descripción", "Cantidad", "Existencias", 
                    "Stock mínimo", "Stock máximo", "Precio compra", "Precio venta", 
                    "Proveedor", "Vencimiento", "Estado"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 100, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 70, tk.CENTER),
            ("Existencias", 80, tk.CENTER),
            ("Stock mínimo", 70, tk.CENTER),
            ("Stock máximo", 70, tk.CENTER),
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

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_item_id = self.tree.item(selected[0])['values'][0]

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        search_term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = InventoryReport.get_inventory_report(search_term=search_term if search_term else None)
        
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

    def open_full_report(self) -> None:
        """Abre la pantalla de reporte completo"""
        FullInventoryReportScreen(self.parent, self.search_var.get())

    def open_movement_report(self) -> None:
        """Abre la pantalla de reporte de movimientos para el producto seleccionado"""
        if self.selected_item_id:
            InventoryMovementReportScreen(self.parent, self.selected_item_id)
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=self)

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()