import tkinter as tk
from typing import Any

class CustomText(tk.Text):
    def __init__(
        self,
        parent: tk.Widget,
        height: int = 1,
        width: int = 25,
        password_char: str = None,  # Nuevo parámetro para contraseñas
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Inicializa una caja de texto personalizada con soporte para contraseñas.
        
        Args:
            parent: Widget padre contenedor
            height: Altura en líneas
            width: Ancho en caracteres
            password_char: Carácter para mostrar en lugar del texto (para contraseñas)
            args: Argumentos adicionales
            kwargs: Argumentos clave adicionales
        """
        super().__init__(parent, *args, **kwargs)
        
        self.password_char = password_char
        self.real_content = ""  # Para almacenar el texto real cuando es contraseña
        
        # Configurar propiedades
        self.configure(
            font=("Arial", 12),
            wrap=tk.WORD,
            height=height,
            width=width,
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="lightblue",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        
        # Configurar eventos para manejar contraseñas
        if password_char:
            self.bind("<KeyPress>", self._handle_password_input)
            self.bind("<KeyRelease>", self._handle_password_input)
            self.bind("<BackSpace>", self._handle_backspace)

    def _handle_password_input(self, event: tk.Event) -> None:
        """Maneja la entrada de texto cuando es campo de contraseña."""
        if event.keysym not in ["BackSpace", "Delete"]:
            self.real_content += event.char
            self._update_password_display()
        
    def _handle_backspace(self, event: tk.Event) -> None:
        """Maneja la tecla backspace para campos de contraseña."""
        self.real_content = self.real_content[:-1]
        self._update_password_display()
        
    def _update_password_display(self) -> None:
        """Actualiza la visualización del texto con caracteres de contraseña."""
        self.delete("1.0", tk.END)
        self.insert("1.0", self.password_char * len(self.real_content))

    def get_text(self) -> str:
        """Obtiene el texto real (incluso para contraseñas)."""
        if self.password_char:
            return self.real_content.strip()
        return self.get("1.0", tk.END).strip()

    def clear_text(self) -> None:
        """Limpia el contenido del campo."""
        self.delete("1.0", tk.END)
        if self.password_char:
            self.real_content = ""