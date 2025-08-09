import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Any, Union

class CustomLabel(ttk.Label):
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        font: Tuple[str, int] = ("Arial", 12),
        fg: str = "black",
        bg: Optional[str] = None,
        image_path: Optional[str] = None,
        image_size: Optional[Tuple[int, int]] = None,
        compound: str = "left",
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa una etiqueta personalizada con soporte para imágenes.

        :param parent: El widget padre al que pertenece esta etiqueta.
        :param text: El texto que se mostrará en la etiqueta.
        :param font: La fuente y el tamaño del texto (por defecto: Arial 12).
        :param fg: El color del texto (por defecto: negro).
        :param bg: El color de fondo de la etiqueta (opcional).
        :param image_path: Ruta a la imagen a mostrar (opcional).
        :param image_size: Tamaño para redimensionar la imagen (ancho, alto).
        :param compound: Posición de la imagen respecto al texto ('left', 'right', 'top', 'bottom').
        :param args: Argumentos adicionales para ttk.Label.
        :param kwargs: Argumentos clave adicionales para ttk.Label.
        """
        super().__init__(parent, *args, **kwargs)
        
        self._image = None  # Para mantener referencia a la imagen
        
        # Cargar imagen si se proporciona
        if image_path:
            self.load_image(image_path, image_size)
            self.configure(image=self._image, compound=compound)
        
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

    def load_image(self, image_path: str, size: Optional[Tuple[int, int]] = None) -> None:
        """Carga y opcionalmente redimensiona una imagen."""
        try:
            self._image = tk.PhotoImage(file=image_path)
            if size:
                self._image = self._image.subsample(size[0], size[1])
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self._image = None

    def configure_style(self, bg: str) -> None:
        """
        Configura el estilo del label si tiene un fondo personalizado.

        :param bg: El color de fondo de la etiqueta.
        """
        style = ttk.Style()
        style.configure("CustomLabel.TLabel", background=bg)