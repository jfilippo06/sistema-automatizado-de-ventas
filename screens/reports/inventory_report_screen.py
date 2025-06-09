import tkinter as tk
from tkinter import ttk
from typing import Callable, Any
from datetime import datetime
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.session_manager import SessionManager

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
        self.category_var = tk.StringVar()
        self.stock_status_var = tk.StringVar()
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = CustomLabel(
            header_frame,
            text="Reporte de Inventario",
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

        # Filtro por categoría
        category_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        category_frame.pack(side=tk.LEFT, padx=5)

        CustomLabel(
            category_frame,
            text="Categoría:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        self.category_combobox = CustomCombobox(
            category_frame,
            textvariable=self.category_var,
            width=20,
            font=("Arial", 10)
        )
        self.category_combobox.pack(side=tk.LEFT, padx=5)
        self.category_combobox['values'] = ["Todas", "Electrónicos", "Ropa", "Alimentos", "Herramientas"]
        self.category_combobox.current(0)

        # Filtro por estado de stock
        stock_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        stock_frame.pack(side=tk.LEFT, padx=20)

        CustomLabel(
            stock_frame,
            text="Estado de stock:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        self.stock_combobox = CustomCombobox(
            stock_frame,
            textvariable=self.stock_status_var,
            width=15,
            font=("Arial", 10)
        )
        self.stock_combobox.pack(side=tk.LEFT, padx=5)
        self.stock_combobox['values'] = ["Todos", "En stock", "Bajo stock", "Agotado"]
        self.stock_combobox.current(0)

        # Campo de búsqueda
        search_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        CustomLabel(
            search_frame,
            text="Buscar (ID/Nombre/Código):",
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
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

        # Botón de búsqueda
        btn_search = CustomButton(
            filters_frame,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10
        )
        btn_search.pack(side=tk.RIGHT, padx=5)

        # Botón de exportar
        btn_export = CustomButton(
            filters_frame,
            text="Exportar",
            command=self.export_report,
            padding=6,
            width=10
        )
        btn_export.pack(side=tk.RIGHT, padx=5)

        # Treeview para mostrar el inventario
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Código", "Nombre", "Categoría", "Precio", "Stock", "Stock Mínimo", "Estado"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 70, tk.CENTER),
            ("Código", 100, tk.CENTER),
            ("Nombre", 200, tk.W),
            ("Categoría", 120, tk.W),
            ("Precio", 100, tk.CENTER),
            ("Stock", 80, tk.CENTER),
            ("Stock Mínimo", 100, tk.CENTER),
            ("Estado", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar datos de ejemplo (solo para diseño)
        self.load_sample_data()

    def load_sample_data(self):
        """Carga datos de ejemplo para el diseño"""
        sample_data = [
            (1, "PROD-001", "Laptop HP EliteBook", "Electrónicos", "1,200.00", 15, 5, "En stock"),
            (2, "PROD-002", "Mouse inalámbrico", "Electrónicos", "25.99", 42, 10, "En stock"),
            (3, "PROD-003", "Camisa manga larga", "Ropa", "35.50", 8, 5, "Bajo stock"),
            (4, "PROD-004", "Arroz 1kg", "Alimentos", "2.99", 120, 20, "En stock"),
            (5, "PROD-005", "Destornillador", "Herramientas", "8.75", 3, 5, "Agotado")
        ]

        for item in sample_data:
            self.tree.insert("", tk.END, values=item)

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        # Función vacía como solicitaste
        pass

    def export_report(self) -> None:
        """Exporta el reporte a un archivo"""
        # Función vacía como solicitaste
        pass

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()