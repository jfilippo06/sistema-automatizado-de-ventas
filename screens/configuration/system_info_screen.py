import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
from PIL import Image, ImageTk

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
        self.images = {}  # Diccionario para almacenar las imágenes
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Frame superior para las imágenes y el título en la misma línea
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, pady=(0, 20))

        # Imagen de la empresa (izquierda)
        try:
            img = Image.open("assets/empresa.png").resize((150, 70), Image.Resampling.LANCZOS)
            self.images["empresa"] = ImageTk.PhotoImage(img)
            img_label = tk.Label(top_frame, image=self.images["empresa"], bg="#f0f0f0")
            img_label.pack(side="left", anchor="w")
        except Exception as e:
            print(f"Error cargando imagen de empresa: {e}")
            # Fallback a texto si no se puede cargar la imagen
            company_frame = tk.Frame(top_frame, bg="#f0f0f0")
            company_frame.pack(side="left", anchor="w")
            tk.Label(company_frame, text="RN&M SERVICIOS INTEGRALES, C.A", 
                    font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#333").pack(anchor="w")
            tk.Label(company_frame, text="RIF: J-40339817-8", 
                    font=("Arial", 9), bg="#f0f0f0", fg="#555").pack(anchor="w")

        # Título centrado
        title = CustomLabel(
            top_frame,
            text="Información del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(side="left", expand=True, padx=10)

        # Imagen de la universidad (derecha)
        try:
            uni_img = Image.open("assets/universidad.png").resize((100, 50), Image.Resampling.LANCZOS)
            self.images["universidad"] = ImageTk.PhotoImage(uni_img)
            uni_label = tk.Label(top_frame, image=self.images["universidad"], bg="#f0f0f0")
            uni_label.pack(side="right", anchor="e")
        except Exception as e:
            print(f"Error cargando imagen de universidad: {e}")

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