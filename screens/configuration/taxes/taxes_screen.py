import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class TaxesManagementScreen(tk.Frame):
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
        self.parent.geometry("700x600")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Impuestos",
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)

        # Frame para botones
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_back = CustomButton(
            button_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Contenido principal (vacío por ahora)
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Puedes agregar aquí los widgets específicos de gestión de impuestos cuando los desarrolles

    def go_back(self) -> None:
        self.open_previous_screen_callback()