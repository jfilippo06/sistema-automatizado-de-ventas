import tkinter as tk

class CustomText(tk.Text):
    def __init__(self, parent, height=1, width=25, *args, **kwargs):
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

    def get_text(self):
        """
        Método para obtener el texto de la caja.
        """
        return self.get("1.0", tk.END).strip()  # Obtener todo el texto y eliminar espacios en blanco

    def clear_text(self):
        """
        Método para limpiar el contenido de la caja.
        """
        self.delete("1.0", tk.END)