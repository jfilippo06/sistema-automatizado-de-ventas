import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from .service_request_history_screen import ServiceRequestHistoryScreen  # Importar la pantalla de historial

class ServiceRequestsQueryScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.configure(bg="#f5f5f5")
        self.selected_item_id = None
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = CustomLabel(
            header_frame,
            text="Consulta de Solicitudes de Servicio",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Botón de regreso
        btn_back = CustomButton(
            header_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT, padx=20, pady=5)

        # Frame de filtros
        filters_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        filters_frame.pack(fill=tk.X)

        # Campo de búsqueda
        search_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        CustomLabel(
            search_frame,
            text="Buscar (Número/Cliente/Servicio):",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)

        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 10)
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

        # Botón de detalles
        btn_details = CustomButton(
            filters_frame,
            text="Ver Historial",
            command=self.open_movement_query,
            padding=6,
            width=15
        )
        btn_details.pack(side=tk.RIGHT, padx=5)
        self.btn_details = btn_details

        # Treeview para mostrar las solicitudes
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Número", "Cliente", "Servicio", "Estado", "Fecha Creación"),
            show="headings",
            height=20
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Número", 120, tk.CENTER),
            ("Cliente", 200, tk.W),
            ("Servicio", 150, tk.W),
            ("Estado", 120, tk.CENTER),
            ("Fecha Creación", 120, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('oddrow', background='#f0f0f0')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        """Manejador de selección de item en el treeview"""
        selected = self.tree.selection()
        if selected:
            self.selected_item_id = self.tree.item(selected[0])['values'][0]

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aquí iría la lógica para cargar los datos reales
        # Datos de ejemplo:
        example_data = [
            (1, "SR-2023-001", "Cliente Ejemplo 1", "Mantenimiento", "Pendiente", "2023-01-15"),
            (2, "SR-2023-002", "Cliente Ejemplo 2", "Reparación", "Completado", "2023-01-20")
        ]
        
        for i, item in enumerate(example_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=item, tags=(tag,))

    def open_movement_query(self) -> None:
        """Muestra el historial de la solicitud seleccionada"""
        if not self.selected_item_id:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
        
        # Ocultar la pantalla actual
        self.pack_forget()
        
        # Crear y mostrar la pantalla de historial
        history_screen = ServiceRequestHistoryScreen(
            parent=self.parent,
            service_request_id=self.selected_item_id,
            open_previous_screen_callback=lambda: self.pack()  # Callback para volver a esta pantalla
        )
        history_screen.pack()

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.open_previous_screen_callback()