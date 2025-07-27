import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry

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
            text="Ver Detalles",
            command=self.show_details,
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
            columns=("ID", "Número de solicitud", "Empleado", "Cliente", "Servicio", 
                    "Descripción", "Cantidad", "Total", "Estado Solicitud"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )

        columns = [
            ("ID", 50, tk.CENTER),
            ("Número de solicitud", 120, tk.CENTER),
            ("Empleado", 150, tk.W),
            ("Cliente", 150, tk.W),
            ("Servicio", 120, tk.W),
            ("Descripción", 180, tk.W),
            ("Cantidad", 70, tk.CENTER),
            ("Total", 90, tk.CENTER),
            ("Estado Solicitud", 120, tk.CENTER)
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

    def refresh_data(self) -> None:
        """Actualiza los datos del reporte según los filtros"""
        search_term = self.search_var.get()
        
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Aquí iría la lógica para obtener las solicitudes de servicio
        # Por ahora dejamos esta función vacía
        
        # Datos de ejemplo (eliminar esto cuando implementes la conexión real)
        example_data = [
            {
                'id': 1,
                'request_number': 'SR-2023-001',
                'employee': 'Juan Pérez',
                'customer': 'Cliente Ejemplo 1',
                'service': 'Mantenimiento Preventivo',
                'description': 'Servicio de mantenimiento programado',
                'quantity': 1,
                'total': 150.00,
                'status': 'En progreso'
            },
            {
                'id': 2,
                'request_number': 'SR-2023-002',
                'employee': 'María Gómez',
                'customer': 'Cliente Ejemplo 2',
                'service': 'Reparación de Equipo',
                'description': 'Reparación de laptop dañada',
                'quantity': 1,
                'total': 250.00,
                'status': 'Completado'
            }
        ]
        
        for i, item in enumerate(example_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(
                item['id'],
                item['request_number'],
                item['employee'],
                item['customer'],
                item['service'],
                item['description'],
                item['quantity'],
                f"{item['total']:.2f}",
                item['status']
            ), tags=(tag,))

    def show_details(self) -> None:
        """Muestra los detalles de la solicitud seleccionada"""
        if self.selected_item_id:
            # Aquí iría la lógica para mostrar los detalles
            # Por ahora mostramos un mensaje
            messagebox.showinfo(
                "Detalles de Solicitud", 
                f"Mostraría detalles para solicitud ID: {self.selected_item_id}",
                parent=self
            )
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        self.pack_forget()
        self.parent.state('normal')  # Reset window state before going back
        self.open_previous_screen_callback()