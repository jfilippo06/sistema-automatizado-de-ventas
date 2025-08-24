import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from sqlite_cli.models.service_request_query import ServiceRequestQuery

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

        # Botón de historial
        btn_history = CustomButton(
            filters_frame,
            text="Ver Historial",
            command=self.open_history_screen,
            padding=6,
            width=15
        )
        btn_history.pack(side=tk.RIGHT, padx=5)
        self.btn_history = btn_history

        # Treeview para mostrar las solicitudes
        tree_frame = tk.Frame(self, bg="#f5f5f5", padx=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Número", "Empleado", "Cliente", "Servicio", "Estado", "Fecha"),
            show="headings",
            height=20
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Número", 120, tk.CENTER),
            ("Empleado", 150, tk.W),
            ("Cliente", 150, tk.W),
            ("Servicio", 120, tk.W),
            ("Estado", 120, tk.CENTER),
            ("Fecha", 120, tk.CENTER)
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
        selected = self.tree.selection()
        if selected:
            self.selected_item_id = self.tree.item(selected[0])['values'][0]

    def translate_status(self, status: str) -> str:
        """Traduce el estado del inglés al español"""
        status_translations = {
            "in_progress": "En Progreso",
            "started": "Iniciado",
            "completed": "Completado"
        }
        return status_translations.get(status, status)

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        search_term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        requests = ServiceRequestQuery.get_service_requests_report(
            search_term=search_term if search_term else None
        )
        
        for i, req in enumerate(requests):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            # Traducir el estado al español
            translated_status = self.translate_status(req['request_status'])
            
            self.tree.insert("", tk.END, values=(
                req['id'],
                req['request_number'],
                req['employee'],
                req['customer'],
                req['service'],
                translated_status,  # Usar el estado traducido
                req['created_at']
            ), tags=(tag,))

    def open_history_screen(self) -> None:
        """Abre la pantalla de historial para la solicitud seleccionada"""
        if not self.selected_item_id:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
        
        from .service_request_history_screen import ServiceRequestHistoryScreen
        self.pack_forget()
        ServiceRequestHistoryScreen(
            self.parent,
            self.selected_item_id,
            lambda: self.pack(fill=tk.BOTH, expand=True)
        ).pack(fill=tk.BOTH, expand=True)

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.open_previous_screen_callback()