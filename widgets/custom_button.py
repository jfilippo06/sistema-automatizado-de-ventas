import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Any

class CustomButton(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable[[], None]] = None,
        width: Optional[int] = None,
        padding: Optional[int] = None,
        wraplength: Optional[int] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa un botón personalizado.

        :param parent: El widget padre al que pertenece este botón.
        :param text: El texto que se mostrará en el botón.
        :param command: La función que se ejecutará al hacer clic en el botón (opcional).
        :param width: El ancho del botón en caracteres (opcional).
        :param padding: El relleno interno del botón (opcional).
        :param wraplength: La longitud máxima del texto antes de dividirlo en varias líneas (opcional).
        :param args: Argumentos adicionales para ttk.Frame.
        :param kwargs: Argumentos clave adicionales para ttk.Frame.
        """
        super().__init__(parent, *args, **kwargs)
        
        # Guardar la función de comando
        self.command: Optional[Callable[[], None]] = command
        
        # Configurar el estilo del botón
        self.style: ttk.Style = ttk.Style()
        self.style.configure("Custom.TButton", padding=padding if padding is not None else 5)
        
        # Crear un Label para el texto del botón
        self.label: ttk.Label = ttk.Label(
            self,
            text=text,
            style="Custom.TButton",
            wraplength=wraplength,  # Dividir el texto si supera este ancho
            width=width if width is not None else 15,  # Ancho del botón
            anchor="center",  # Centrar el texto horizontalmente
            justify="center",  # Centrar el texto verticalmente
            padding=5
        )
        self.label.pack(fill=tk.BOTH, expand=True)  # Expandir el Label dentro del Frame
        
        # Configurar eventos de clic
        self.label.bind("<Button-1>", self.on_click)
        self.bind("<Button-1>", self.on_click)
        
        # Configurar el estilo para simular un botón
        self.configure(relief=tk.RAISED)  # Borde elevado como un botón
        self.label.configure(background="lightgray")  # Fondo del botón

    def on_click(self, event: tk.Event) -> None:
        """
        Método para manejar el evento de clic.

        :param event: El evento de clic.
        """
        if self.command:
            self.command()

    def disable(self) -> None:
        """
        Método para deshabilitar el botón.
        """
        self.label.state(["disabled"])
        self.configure(relief=tk.SUNKEN)  # Cambiar el borde para indicar deshabilitado

    def enable(self) -> None:
        """
        Método para habilitar el botón.
        """
        self.label.state(["!disabled"])
        self.configure(relief=tk.RAISED)  # Restaurar el borde elevado