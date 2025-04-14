import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class ConfigurationScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None],
        open_users_callback: Callable[[], None],
        open_currency_callback: Callable[[], None],
        open_taxes_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.open_users_callback = open_users_callback
        self.open_currency_callback = open_currency_callback
        self.open_taxes_callback = open_taxes_callback
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("500x370")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Configuración del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(pady=(0, 10))

        buttons = [
            ("Gestión de Usuarios", self.users_management),
            ("Gestión de Monedas", self.currency_management),
            ("Gestión de Impuestos", self.taxes_management),
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

    def users_management(self) -> None:
        self.open_users_callback()

    def currency_management(self) -> None:
        self.open_currency_callback()

    def taxes_management(self) -> None:
        self.open_taxes_callback()

    def go_back(self) -> None:
        self.open_previous_screen_callback()