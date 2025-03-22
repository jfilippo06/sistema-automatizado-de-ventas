import tkinter as tk
from tkinter import ttk

class Inventory(tk.Frame):
    def __init__(self, parent, open_previous_screen_callback):
        super().__init__(parent)
        self.parent = parent  # Guardar referencia a la ventana principal
        self.open_previous_screen_callback = open_previous_screen_callback  # Callback para regresar a la pantalla anterior

        # Configurar la interfaz de usuario
        self.configure_ui()

    def pack(self, **kwargs):
        """
        Configura la ventana principal cuando se muestra la pantalla de inventario.
        """
        self.parent.geometry("800x600")  # Tamaño específico para el inventario
        self.parent.resizable(False, False)  # No redimensionable
        super().pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla

    def configure_ui(self):
        """
        Configura la interfaz de usuario de la pantalla de inventario.
        """
        # Crear un Frame para los botones superiores
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botón para regresar a la pantalla anterior (izquierda)
        btn_back = tk.Button(
            button_frame,
            text="Regresar",
            command=self.go_back
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Botones adicionales (derecha)
        btn_add = tk.Button(
            button_frame,
            text="Agregar",
            command=self.add_item
        )
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit = tk.Button(
            button_frame,
            text="Editar",
            command=self.edit_item
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable = tk.Button(
            button_frame,
            text="Deshabilitar",
            command=self.disable_item
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Crear un Treeview (tabla)
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        
        # Configurar las columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        
        # Ajustar el ancho de las columnas
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=200, anchor=tk.W)
        self.tree.column("Cantidad", width=150, anchor=tk.CENTER)
        self.tree.column("Precio", width=150, anchor=tk.E)
        
        # Insertar datos de ejemplo
        self.insert_sample_data()
        
        # Posicionar el Treeview en la pantalla
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def insert_sample_data(self):
        """
        Inserta datos de ejemplo en la tabla.
        """
        sample_data = [
            (1, "Producto 1", 10, 100.50),
            (2, "Producto 2", 5, 200.75),
            (3, "Producto 3", 20, 50.00),
            (4, "Producto 4", 15, 300.25),
        ]
        for data in sample_data:
            self.tree.insert("", tk.END, values=data)

    def go_back(self):
        """
        Método para regresar a la pantalla anterior.
        """
        self.open_previous_screen_callback()  # Llamar al callback para regresar

    def add_item(self):
        """
        Método para agregar un nuevo ítem al inventario.
        """
        print("Función: Agregar ítem")

    def edit_item(self):
        """
        Método para editar un ítem del inventario.
        """
        print("Función: Editar ítem")

    def disable_item(self):
        """
        Método para deshabilitar un ítem del inventario.
        """
        print("Función: Deshabilitar ítem")