import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable

class SystemInfoScreen(tk.Frame):
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
        # Tamaño de la ventana
        window_width = 560
        window_height = 400
        
        # Calcular posición para centrar
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # Configurar geometría centrada
        self.parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Información del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        info_frame = tk.Frame(main_frame, bg="#f0f0f0")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Información del sistema
        system_info = {
            "Nombre del Sistema": "Sistema automatizado de ventas y servicios",
            "Versión": "1.0.0",
            "Desarrollado por": "Diego Nieves",
            "Año": "2025",
            "Plataforma": "Python 3.13.2",
            "Interfaz": "Tkinter",
            "Base de Datos": "SQLite"
        }

        row = 0
        for key, value in system_info.items():
            label_key = CustomLabel(
                info_frame,
                text=f"{key}:",
                font=("Arial", 12, "bold"),
                fg="#333",
                bg="#f0f0f0",
                anchor="w"
            )
            label_key.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            label_value = CustomLabel(
                info_frame,
                text=value,
                font=("Arial", 12),
                fg="#555",
                bg="#f0f0f0",
                anchor="w"
            )
            label_value.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            row += 1

        # Botón de regreso
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        back_btn = CustomButton(
            btn_frame,
            text="Regresar",
            command=self.go_back,
            padding=10,
            width=20
        )
        back_btn.pack(pady=10, ipady=5)

    def go_back(self) -> None:
        self.open_previous_screen_callback()