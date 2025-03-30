import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, Tuple

class CustomEntry(ttk.Entry):
    def __init__(
        self,
        parent: tk.Widget,
        textvariable: Optional[tk.Variable] = None,
        font: Tuple[str, int] = ("Arial", 10),
        width: int = 20,
        placeholder: Optional[str] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Widget Entry personalizado con estilo moderno y características adicionales.
        
        Args:
            parent: Widget padre contenedor
            textvariable: Variable opcional para enlazar con el entry
            font: Tupla con fuente (familia, tamaño)
            width: Ancho en caracteres
            placeholder: Texto de ejemplo opcional
            *args: Argumentos posicionales adicionales para ttk.Entry
            **kwargs: Argumentos clave adicionales para ttk.Entry
        """
        self._placeholder = placeholder
        self._placeholder_color = "gray"  # Color para texto de ejemplo
        self._default_fg = "black"       # Color normal del texto
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("CustomEntry.TEntry", 
                            font=font,
                            foreground=self._default_fg,
                            padding=5,
                            relief="solid",
                            borderwidth=1)
        
        super().__init__(
            parent,
            style="CustomEntry.TEntry",
            width=width,
            *args,
            **kwargs
        )
        
        # Enlazar variable si se proporciona
        if textvariable:
            self.configure(textvariable=textvariable)
        
        # Configurar placeholder si existe
        if placeholder:
            self._add_placeholder()
            self.bind("<FocusIn>", self._clear_placeholder)
            self.bind("<FocusOut>", self._add_placeholder_if_empty)
    
    def _add_placeholder(self) -> None:
        """Añade texto de ejemplo (placeholder) al entry."""
        if not self.get():
            self.style.configure("CustomEntry.TEntry", foreground=self._placeholder_color)
            if isinstance(self, ttk.Entry):
                self.insert(0, self._placeholder)
            else:
                self.delete(0, tk.END)
                self.insert(0, self._placeholder)
    
    def _clear_placeholder(self, event: Optional[tk.Event] = None) -> None:
        """Elimina el texto de ejemplo cuando el entry recibe foco."""
        if self._placeholder and self.get() == self._placeholder:
            self.style.configure("CustomEntry.TEntry", foreground=self._default_fg)
            self.delete(0, tk.END)
    
    def _add_placeholder_if_empty(self, event: Optional[tk.Event] = None) -> None:
        """Vuelve a mostrar el texto de ejemplo si el entry está vacío."""
        if self._placeholder and not self.get():
            self._add_placeholder()
    
    def get(self) -> str:
        """Obtiene el texto actual, ignorando el texto de ejemplo."""
        text = super().get()
        if self._placeholder and text == self._placeholder:
            return ""
        return text
    
    def set(self, value: str) -> None:
        """Establece el texto del entry."""
        self._clear_placeholder()
        if isinstance(self, ttk.Entry):
            self.delete(0, tk.END)
            self.insert(0, value)
        else:
            super().delete(0, tk.END)
            super().insert(0, value)
    
    def clear(self) -> None:
        """Limpia el contenido del entry."""
        self.delete(0, tk.END)
        if self._placeholder:
            self._add_placeholder()
    
    def disable(self) -> None:
        """Deshabilita el entry."""
        self.state(["disabled"])
        self.style.configure("CustomEntry.TEntry", foreground="gray")
    
    def enable(self) -> None:
        """Habilita el entry."""
        self.state(["!disabled"])
        self.style.configure("CustomEntry.TEntry", foreground=self._default_fg)
        if not self.get() and self._placeholder:
            self._add_placeholder()