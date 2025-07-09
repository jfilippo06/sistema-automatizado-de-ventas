import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Any, Union

class CustomCheckbutton(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        variable: Optional[tk.Variable] = None,
        command: Optional[Callable[[], None]] = None,
        width: Optional[int] = None,
        padding: Optional[int] = None,
        wraplength: Optional[int] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa un checkbutton personalizado.

        :param parent: El widget padre al que pertenece este checkbutton.
        :param text: El texto que se mostrará junto al checkbutton.
        :param variable: Variable de control para el estado del checkbutton (opcional).
        :param command: Función que se ejecutará al cambiar el estado (opcional).
        :param width: Ancho del widget en caracteres (opcional).
        :param padding: Relleno interno del widget (opcional).
        :param wraplength: Longitud máxima del texto antes de dividirlo (opcional).
        :param args: Argumentos adicionales para ttk.Frame.
        :param kwargs: Argumentos clave adicionales para ttk.Frame.
        """
        super().__init__(parent, *args, **kwargs)
        
        # Variables de instancia
        self.command: Optional[Callable[[], None]] = command
        self._variable: Union[tk.Variable, None] = variable
        
        # Crear variable interna si no se proporciona una
        if self._variable is None:
            self._variable = tk.BooleanVar(value=False)
        
        # Configurar el estilo
        self.style: ttk.Style = ttk.Style()
        self.style.configure("Custom.TCheckbutton", padding=padding if padding is not None else 5)
        
        # Frame contenedor
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Checkbutton
        self.checkbutton = ttk.Checkbutton(
            self.container,
            variable=self._variable,
            command=self._on_change
        )
        self.checkbutton.pack(side=tk.LEFT, padx=(0, 5))
        
        # Label para el texto
        self.label = ttk.Label(
            self.container,
            text=text,
            wraplength=wraplength,
            width=width if width is not None else 15,
            anchor="w",
            justify="left",
            padding=5
        )
        self.label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar eventos
        self.label.bind("<Button-1>", self._toggle)
        self.bind("<Button-1>", self._toggle)

    def _on_change(self) -> None:
        """Método interno para manejar cambios en el checkbutton."""
        if self.command:
            self.command()

    def _toggle(self, event: Optional[tk.Event] = None) -> None:
        """Alterna el estado del checkbutton."""
        current_value = self._variable.get()
        self._variable.set(not current_value)
        self._on_change()

    @property
    def variable(self) -> tk.Variable:
        """Devuelve la variable asociada al checkbutton."""
        return self._variable

    def get(self) -> Any:
        """Devuelve el valor actual del checkbutton."""
        return self._variable.get()

    def set(self, value: Any) -> None:
        """Establece el valor del checkbutton."""
        self._variable.set(value)

    def disable(self) -> None:
        """Deshabilita el checkbutton."""
        self.checkbutton.state(["disabled"])
        self.label.state(["disabled"])

    def enable(self) -> None:
        """Habilita el checkbutton."""
        self.checkbutton.state(["!disabled"])
        self.label.state(["!disabled"])

    def is_checked(self) -> bool:
        """Devuelve True si el checkbutton está marcado."""
        return bool(self._variable.get())