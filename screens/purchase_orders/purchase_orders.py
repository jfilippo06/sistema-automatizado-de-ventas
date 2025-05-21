import tkinter as tk
from tkinter import ttk
from typing import Any, Callable
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel

class PurchaseOrdersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Órdenes de Compra",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Botón de regreso
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Controles principales
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Botones de acciones
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        btn_new = CustomButton(
            action_frame,
            text="Nueva Orden",
            command=self.new_order,
            padding=8,
            width=12,
        )
        btn_new.pack(side=tk.LEFT, padx=5)

        btn_view = CustomButton(
            action_frame,
            text="Ver Detalle",
            command=self.view_order,
            padding=8,
            width=12,
        )
        btn_view.pack(side=tk.LEFT, padx=5)

        btn_edit = CustomButton(
            action_frame,
            text="Editar",
            command=self.edit_order,
            padding=8,
            width=10,
        )
        btn_edit.pack(side=tk.LEFT, padx=5)

        btn_delete = CustomButton(
            action_frame,
            text="Eliminar",
            command=self.delete_order,
            padding=8,
            width=10,
        )
        btn_delete.pack(side=tk.LEFT, padx=5)

        # Treeview para listar órdenes
        tree_frame = tk.Frame(self, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Número", "Proveedor", "Fecha", "Total", "Estado"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Número", 100, tk.CENTER),
            ("Proveedor", 200, tk.W),
            ("Fecha", 100, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Estado", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def new_order(self) -> None:
        # TODO: Implementar creación de nueva orden
        pass

    def view_order(self) -> None:
        # TODO: Implementar visualización de orden
        pass

    def edit_order(self) -> None:
        # TODO: Implementar edición de orden
        pass

    def delete_order(self) -> None:
        # TODO: Implementar eliminación de orden
        pass