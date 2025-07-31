import tkinter as tk
from tkinter import ttk
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry

class ServiceRequestHistoryScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        service_request_id: int,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.service_request_id = service_request_id
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")
        
        # Variables
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        
        self.configure_ui()
        self.load_request_info()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#4a6fa5")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = CustomLabel(
            header_frame,
            text=f"Historial de Solicitud de Servicio #{self.service_request_id}",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Información de la solicitud
        info_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        info_frame.pack(fill=tk.X)
        
        self.info_label = CustomLabel(
            info_frame,
            text="Cargando información...",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.info_label.pack(anchor=tk.W)
        
        # Frame de filtros
        filters_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        filters_frame.pack(fill=tk.X)
        
        # Filtros de fecha
        filter_row = tk.Frame(filters_frame, bg="#f5f5f5")
        filter_row.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            filter_row,
            text="Desde:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        start_date_entry = CustomEntry(
            filter_row,
            textvariable=self.start_date_var,
            width=12,
            font=("Arial", 10)
        )
        start_date_entry.pack(side=tk.LEFT, padx=5)
        
        CustomLabel(
            filter_row,
            text="Hasta:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        end_date_entry = CustomEntry(
            filter_row,
            textvariable=self.end_date_var,
            width=12,
            font=("Arial", 10)
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        
        # Botones
        btn_frame = tk.Frame(filter_row, bg="#f5f5f5")
        btn_frame.pack(side=tk.RIGHT)
        
        btn_filter = CustomButton(
            filter_row,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.LEFT, padx=(20, 5))
        
        btn_clear = CustomButton(
            filter_row,
            text="Limpiar",
            command=self.clear_filters,
            padding=6,
            width=10
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_back = CustomButton(
            filter_row,
            text="Regresar",
            command=self.go_back,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT)
        
        # Treeview para mostrar el historial
        tree_frame = tk.Frame(main_frame, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Fecha", "Evento", "Usuario", "Estado Anterior", "Estado Nuevo", "Comentarios"),
            show="headings",
            height=15,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        columns = [
            ("Fecha", 150, tk.CENTER),
            ("Evento", 120, tk.CENTER),
            ("Usuario", 120, tk.CENTER),
            ("Estado Anterior", 120, tk.CENTER),
            ("Estado Nuevo", 120, tk.CENTER),
            ("Comentarios", 250, tk.W)
        ]
        
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Contador de registros
        self.count_label = CustomLabel(
            main_frame,
            text="0 eventos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def load_request_info(self):
        """Carga la información básica de la solicitud"""
        # Aquí iría la lógica para cargar la información de la solicitud
        self.info_label.config(
            text=f"Solicitud #{self.service_request_id} - Cliente: Ejemplo Cliente - Servicio: Mantenimiento"
        )

    def refresh_data(self):
        """Actualiza los datos del historial según los filtros"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aquí iría la lógica para cargar el historial real
        # Datos de ejemplo:
        example_data = [
            ("2023-01-15 10:00", "Creación", "Admin", "", "Pendiente", "Solicitud creada"),
            ("2023-01-16 14:30", "Actualización", "Técnico", "Pendiente", "En Proceso", "Asignado a técnico"),
            ("2023-01-18 16:45", "Completado", "Técnico", "En Proceso", "Completado", "Servicio realizado")
        ]
        
        for i, item in enumerate(example_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=item, tags=(tag,))
        
        self.count_label.config(text=f"{len(example_data)} eventos encontrados")

    def clear_filters(self):
        """Limpia todos los filtros aplicados"""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.refresh_data()

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.open_previous_screen_callback()