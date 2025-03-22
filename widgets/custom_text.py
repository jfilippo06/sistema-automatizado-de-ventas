import tkinter as tk
from typing import Any

class CustomText(tk.Text):
    def __init__(
        self,
        parent: tk.Widget,
        height: int = 1,
        width: int = 25,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa una caja de texto personalizada.

        :param parent: El widget padre al que pertenece esta caja de texto.
        :param height: La altura de la caja de texto en líneas.
        :param width: El ancho de la caja de texto en caracteres.
        :param args: Argumentos adicionales para tk.Text.
        :param kwargs: Argumentos clave adicionales para tk.Text.
        """
        super().__init__(parent, *args, **kwargs)
        
        # Configurar propiedades por defecto
        self.configure(
            font=("Arial", 12),          # Fuente y tamaño
            wrap=tk.WORD,                # Ajuste de texto por palabras
            height=height,               # Altura en líneas
            width=width,                 # Ancho en caracteres
            bg="white",                  # Color de fondo
            fg="black",                 # Color del texto
            insertbackground="black",   # Color del cursor
            selectbackground="lightblue" # Color de selección
        )
        
        # Añadir un borde con estilo
        self.configure(relief=tk.SUNKEN, borderwidth=2)

    def get_text(self) -> str:
        """
        Obtiene el texto de la caja de texto.

        :return: El texto contenido en la caja de texto, sin espacios en blanco al inicio o final.
        """
        return self.get("1.0", tk.END).strip()  # Obtener todo el texto y eliminar espacios en blanco

    def clear_text(self) -> None:
        """
        Limpia el contenido de la caja de texto.
        """
        self.delete("1.0", tk.END)