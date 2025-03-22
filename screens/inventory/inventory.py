import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Any
from sqlite_cli.models.inventory_model import InventoryItem  # Importar el modelo de inventario

class Inventory(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        """
        Inicializa la pantalla de inventario.

        :param parent: El widget padre al que pertenece esta pantalla.
        :param open_previous_screen_callback: Función para regresar a la pantalla anterior.
        """
        super().__init__(parent)
        self.parent: tk.Widget = parent  # Guardar referencia a la ventana principal
        self.open_previous_screen_callback: Callable[[], None] = open_previous_screen_callback  # Callback para regresar a la pantalla anterior

        # Configurar la interfaz de usuario
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        """
        Configura la ventana principal cuando se muestra la pantalla de inventario.
        """
        self.parent.geometry("800x600")  # Tamaño específico para el inventario
        self.parent.resizable(False, False)  # No redimensionable
        super().pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla

    def configure_ui(self) -> None:
        """
        Configura la interfaz de usuario de la pantalla de inventario.
        """
        # Crear un Frame para los botones superiores
        button_frame: tk.Frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botón para regresar a la pantalla anterior (izquierda)
        btn_back: tk.Button = tk.Button(
            button_frame,
            text="Regresar",
            command=self.go_back
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Botones adicionales (derecha)
        btn_add: tk.Button = tk.Button(
            button_frame,
            text="Agregar",
            command=self.add_item
        )
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit: tk.Button = tk.Button(
            button_frame,
            text="Editar",
            command=self.edit_item
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable: tk.Button = tk.Button(
            button_frame,
            text="Deshabilitar",
            command=self.disable_item
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Crear un Treeview (tabla)
        self.tree: ttk.Treeview = ttk.Treeview(self, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        
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
        
        # Cargar datos desde la base de datos
        self.load_data()
        
        # Posicionar el Treeview en la pantalla
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self) -> None:
        """
        Carga los datos desde la base de datos y los inserta en la tabla.
        """
        # Obtener todos los ítems de la base de datos
        items: List[Tuple[int, str, int, float]] = InventoryItem.all()
        
        # Insertar los datos en la tabla
        for item in items:
            self.tree.insert("", tk.END, values=(item['id'], item['name'], item['quantity'], item['price']))

    def go_back(self) -> None:
        """
        Método para regresar a la pantalla anterior.
        """
        self.open_previous_screen_callback()  # Llamar al callback para regresar

    def add_item(self) -> None:
        """
        Método para agregar un nuevo ítem al inventario.
        """
        print("Función: Agregar ítem")

    def edit_item(self) -> None:
        """
        Método para editar un ítem del inventario.
        """
        print("Función: Editar ítem")

    def disable_item(self) -> None:
        """
        Método para deshabilitar un ítem del inventario.
        """
        print("Función: Deshabilitar ítem")