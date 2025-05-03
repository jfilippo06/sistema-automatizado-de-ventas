import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class ReportsScreen(tk.Frame):
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
        self.parent.geometry("550x370")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Reportes del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        # Creamos un frame para contener las dos columnas
        columns_frame = tk.Frame(main_frame, bg="#f0f0f0")
        columns_frame.pack()

        # Frame para la columna izquierda
        left_column = tk.Frame(columns_frame, bg="#f0f0f0")
        left_column.pack(side=tk.LEFT, padx=10)

        # Frame para la columna derecha
        right_column = tk.Frame(columns_frame, bg="#f0f0f0")
        right_column.pack(side=tk.LEFT, padx=10)

        buttons = [
            ("Gestión de proveedores", self.suppliers_report),
            ("Inventario de productos", self.inventory_report),
            ("Gestión de compras", self.sales_report),
            ("Facturas", self.invoices_report),
            ("Clientes", self.customers_report),
            ("Solicitud de servicios", self.service_requests_report),
            ("Gestión de servicios", self.services_report),
            ("Regresar", self.go_back)
        ]

        # Distribuimos los botones en las dos columnas
        for i, (text, command) in enumerate(buttons):
            btn = CustomButton(
                left_column if i % 2 == 0 else right_column,  # Alternamos columnas
                text=text,
                command=command,
                padding=10,
                width=25  # Reducimos un poco el ancho para que quepan dos columnas
            )
            btn.pack(pady=5, ipady=10, ipadx=10)

    def suppliers_report(self) -> None:
        print("Generando reporte de proveedores")

    def inventory_report(self) -> None:
        print("Generando reporte de inventario")

    def sales_report(self) -> None:
        print("Generando reporte de compras")

    def invoices_report(self) -> None:
        print("Generando reporte de facturas")

    def customers_report(self) -> None:
        print("Generando reporte de clientes")

    def service_requests_report(self) -> None:
        print("Generando reporte de solicitudes de servicio")

    def services_report(self) -> None:
        print("Generando reporte de servicios")

    def go_back(self) -> None:
        self.open_previous_screen_callback()