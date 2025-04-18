import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class RecoveryScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None],
        open_recovery_suppliers_callback: Callable[[], None],
        open_recovery_inventory_callback: Callable[[], None]  # Nuevo parámetro
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.open_recovery_suppliers_callback = open_recovery_suppliers_callback
        self.open_recovery_inventory_callback = open_recovery_inventory_callback  # Guardamos el callback
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("500x420")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Recuperación de Registros",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(pady=(0, 10))

        buttons = [
            ("Gestión de Proveedores", self.recover_suppliers),
            ("Inventario de Productos", self.recover_inventory),  # Actualizado
            ("Solicitudes de Servicio", self.recover_service_requests),
            ("Gestión de Servicios", self.recover_services),
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

    def recover_suppliers(self) -> None:
        self.open_recovery_suppliers_callback()

    def recover_inventory(self) -> None:
        self.open_recovery_inventory_callback()  # Usamos el callback para abrir la pantalla

    def recover_service_requests(self) -> None:
        print("Function: Recuperar Solicitudes de Servicio")

    def recover_services(self) -> None:
        print("Function: Recuperar Servicios")

    def go_back(self) -> None:
        self.open_previous_screen_callback()