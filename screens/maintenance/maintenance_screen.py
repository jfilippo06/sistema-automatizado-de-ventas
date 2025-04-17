import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class MaintenanceScreen(tk.Frame):
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
        self.parent.geometry("500x370")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Mantenimiento del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(pady=(0, 10))

        buttons = [
            ("Comprimir Base de Datos", self.compress_database),
            ("Exportar Base de Datos", self.export_database),
            ("Importar Base de Datos", self.import_database),
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

    def compress_database(self) -> None:
        print("Function: Comprimir Base de Datos")

    def export_database(self) -> None:
        print("Function: Exportar Base de Datos")

    def import_database(self) -> None:
        print("Function: Importar Base de Datos")

    def go_back(self) -> None:
        self.open_previous_screen_callback()