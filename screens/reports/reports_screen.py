import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
from screens.reports.sales_report_screen import SalesReportScreen
from screens.reports.purchase_order_report_screen import PurchaseOrderReportScreen

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
        self.parent.geometry("500x400")  # Increased height for new button
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

        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(pady=(0, 10))

        buttons = [
            ("Inventario de productos", self.inventory_report),
            ("Ordenes de Compra", self.purchase_order_report_screen),
            ("Ventas", self.sales_report_screen),
            ("Regresar", self.go_back)
        ]

        for text, command in buttons:
            btn = CustomButton(
                options_frame,
                text=text,
                command=command,
                padding=10,
                width=30
            )
            btn.pack(pady=5, ipady=10, ipadx=10)

    def inventory_report(self) -> None:
        print("Generando reporte de inventario")

    def purchase_order_report_screen(self) -> None:
        """Abre la pantalla de reporte de órdenes de compra"""
        self.pack_forget()
        purchase_order_report_screen = PurchaseOrderReportScreen(
            self.parent,
            lambda: self.pack(fill=tk.BOTH, expand=True)
        )
        purchase_order_report_screen.pack(fill=tk.BOTH, expand=True)

    def sales_report_screen(self) -> None:
        """Abre la pantalla de reporte de ventas"""
        self.pack_forget()
        sales_report_screen = SalesReportScreen(
            self.parent,
            lambda: self.pack(fill=tk.BOTH, expand=True)
        )
        sales_report_screen.pack(fill=tk.BOTH, expand=True)

    def go_back(self) -> None:
        self.open_previous_screen_callback()