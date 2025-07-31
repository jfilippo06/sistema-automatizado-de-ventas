import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_combobox import CustomCombobox
from widgets.custom_entry import CustomEntry
from utils.field_formatter import FieldFormatter
from sqlite_cli.models.service_request_query import ServiceRequestQuery

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
        self.event_type_var = tk.StringVar(value="Todos")
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
        
        # Información de la solicitud
        info_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        info_frame.pack(fill=tk.X)
        
        self.info_label = CustomLabel(
            info_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        )
        self.info_label.pack(anchor=tk.W)
        
        # Frame de filtros
        filters_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
        filters_frame.pack(fill=tk.X)
        
        # Fila 1 de filtros
        row1_frame = tk.Frame(filters_frame, bg="#f5f5f5")
        row1_frame.pack(fill=tk.X, pady=5)
        
        # Filtros de fecha
        CustomLabel(
            row1_frame,
            text="Desde:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        start_date_entry = CustomEntry(
            row1_frame,
            textvariable=self.start_date_var,
            width=12,
            font=("Arial", 10)
        )
        start_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(start_date_entry, 'date')
        
        CustomLabel(
            row1_frame,
            text="Hasta:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        end_date_entry = CustomEntry(
            row1_frame,
            textvariable=self.end_date_var,
            width=12,
            font=("Arial", 10)
        )
        end_date_entry.pack(side=tk.LEFT, padx=5)
        FieldFormatter.bind_validation(end_date_entry, 'date')
        
        # Filtro de tipo de evento
        CustomLabel(
            row1_frame,
            text="Tipo:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        event_types = ["Todos", "Creación", "Actualización", "Asignación", "Completado", "Cancelado"]
        event_combobox = CustomCombobox(
            row1_frame,
            textvariable=self.event_type_var,
            values=event_types,
            width=15,
            font=("Arial", 10)
        )
        event_combobox.pack(side=tk.LEFT, padx=5)
        event_combobox.current(0)
        
        # Botones Filtrar y Limpiar
        btn_filter = CustomButton(
            row1_frame,
            text="Filtrar",
            command=self.refresh_data,
            padding=6,
            width=10
        )
        btn_filter.pack(side=tk.LEFT, padx=(10, 5))
        
        btn_clear = CustomButton(
            row1_frame,
            text="Limpiar",
            command=self.clear_filters,
            padding=6,
            width=10
        )
        btn_clear.pack(side=tk.LEFT)
        
        # Botón de regreso (a la derecha)
        btn_back = CustomButton(
            row1_frame,
            text="Regresar",
            command=self.go_back,
            padding=6,
            width=10
        )
        btn_back.pack(side=tk.RIGHT)
        
        # Treeview y scrollbars
        tree_container = tk.Frame(main_frame, bg="#f5f5f5")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        xscrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        yscrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_container,
            columns=("Fecha", "Evento", "Usuario", "Estado Anterior", "Estado Nuevo", "Comentarios"),
            show="headings",
            height=15,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
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
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)
        
        # Contador de registros
        self.count_label = CustomLabel(
            main_frame,
            text="0 eventos encontrados",
            font=("Arial", 10),
            bg="#f5f5f5"
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def load_request_info(self):
        request = ServiceRequestQuery.get_service_request_details(self.service_request_id)
        if request:
            self.info_label.config(
                text=f"Solicitud: {request['request_number']} - Cliente: {request['customer']} - Servicio: {request['service']} - Estado: {request['request_status']}"
            )

    def refresh_data(self):
        """Actualiza los datos del historial según los filtros"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener valores de los filtros
        start_date = self.start_date_var.get().replace("/", "-") if self.start_date_var.get() else None
        end_date = self.end_date_var.get().replace("/", "-") if self.end_date_var.get() else None
        event_type = self.event_type_var.get() if self.event_type_var.get() != "Todos" else None
        
        movements = ServiceRequestQuery.get_service_request_movements_report(
            request_id=self.service_request_id,
            start_date=start_date,
            end_date=end_date,
            movement_type=event_type
        )
        
        for i, movement in enumerate(movements):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(
                movement['created_at'],
                movement['movement_type'],
                movement['user'],
                movement['previous_request_status'],
                movement['new_request_status'],
                movement['notes']
            ), tags=(tag,))
        
        self.count_label.config(text=f"{len(movements)} eventos encontrados")

    def clear_filters(self):
        """Limpia todos los filtros aplicados"""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.event_type_var.set("Todos")
        self.refresh_data()

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.open_previous_screen_callback()