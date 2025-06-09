import tkinter as tk
from tkinter import ttk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class InventoryReportScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("900x600")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title = CustomLabel(
            main_frame,
            text="Reporte de Inventario",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(0, 20))

        # Frame para controles de filtrado
        filter_frame = tk.Frame(main_frame, bg="#f0f0f0")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        # Filtros
        tk.Label(filter_frame, text="Filtrar por:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.category_var = tk.StringVar()
        categories = ["Todos", "Electrónicos", "Ropa", "Alimentos", "Herramientas"]
        tk.OptionMenu(filter_frame, self.category_var, *categories).pack(side=tk.LEFT, padx=5)
        
        self.stock_var = tk.StringVar()
        stock_options = ["Todos", "En stock", "Bajo stock", "Agotado"]
        tk.OptionMenu(filter_frame, self.stock_var, *stock_options).pack(side=tk.LEFT, padx=5)
        
        CustomButton(
            filter_frame,
            text="Aplicar Filtros",
            command=self.apply_filters,
            padding=5
        ).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar el reporte
        self.tree_frame = tk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "category", "price", "stock", "min_stock"),
            show="headings"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("category", text="Categoría")
        self.tree.heading("price", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("min_stock", text="Stock Mínimo")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150)
        self.tree.column("category", width=120)
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("stock", width=80, anchor="center")
        self.tree.column("min_stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Botones
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=(20, 0))

        CustomButton(
            button_frame,
            text="Exportar a Excel",
            command=self.export_to_excel,
            padding=10
        ).pack(side="left", padx=10)

        CustomButton(
            button_frame,
            text="Imprimir",
            command=self.print_report,
            padding=10
        ).pack(side="left", padx=10)

        CustomButton(
            button_frame,
            text="Regresar",
            command=self.go_back,
            padding=10
        ).pack(side="right", padx=10)

        # Cargar datos de ejemplo
        self.load_sample_data()

    def load_sample_data(self):
        # Datos de ejemplo - en una aplicación real esto vendría de la base de datos
        sample_data = [
            (1, "Laptop HP", "Electrónicos", 1200.00, 15, 5),
            (2, "Mouse inalámbrico", "Electrónicos", 25.99, 42, 10),
            (3, "Camisa manga larga", "Ropa", 35.50, 8, 5),
            (4, "Arroz 1kg", "Alimentos", 2.99, 120, 20),
            (5, "Destornillador", "Herramientas", 8.75, 3, 5)
        ]

        for item in sample_data:
            self.tree.insert("", "end", values=item)

    def apply_filters(self):
        # Aquí implementarías la lógica de filtrado
        print(f"Filtrando por categoría: {self.category_var.get()}")
        print(f"Filtrando por stock: {self.stock_var.get()}")

    def export_to_excel(self):
        print("Exportando a Excel...")

    def print_report(self):
        print("Imprimiendo reporte...")

    def go_back(self) -> None:
        self.open_previous_screen_callback()