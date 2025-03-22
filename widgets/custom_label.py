import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Any

class CustomLabel(ttk.Label):
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        font: Tuple[str, int] = ("Arial", 12),
        fg: str = "black",
        bg: Optional[str] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa una etiqueta personalizada.

        :param parent: El widget padre al que pertenece esta etiqueta.
        :param text: El texto que se mostrará en la etiqueta.
        :param font: La fuente y el tamaño del texto (por defecto: Arial 12).
        :param fg: El color del texto (por defecto: negro).
        :param bg: El color de fondo de la etiqueta (opcional).
        :param args: Argumentos adicionales para ttk.Label.
        :param kwargs: Argumentos clave adicionales para ttk.Label.
        """
        super().__init__(parent, *args, **kwargs)
        
        # Configurar propiedades personalizadas
        self.configure(
            text=text,          # Texto del label
            font=font,          # Fuente y tamaño
            foreground=fg,      # Color del texto
            background=bg       # Color de fondo (opcional)
        )
        
        # Si se proporciona un color de fondo, configurar el estilo
        if bg:
            self.configure(style="CustomLabel.TLabel")
            self.configure_style(bg)

    def configure_style(self, bg: str) -> None:
        """
        Configura el estilo del label si tiene un fondo personalizado.

        :param bg: El color de fondo de la etiqueta.
        """
        style = ttk.Style()
        style.configure("CustomLabel.TLabel", background=bg)