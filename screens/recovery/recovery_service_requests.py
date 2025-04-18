import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.request_status_model import RequestStatus
from widgets.custom_button import CustomButton
from widgets.custom_combobox import CustomCombobox
from widgets.custom_entry import CustomEntry
from widgets.custom_label import CustomLabel

class RecoveryServiceRequests(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Recuperación de Solicitudes de Servicio",
            font=("Arial", 16, "bold"),
            fg="#333"
        )
        title_label.pack(side=tk.LEFT)

        # Frame principal para botones y búsqueda
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Frame de botones (solo para el botón Regresar)
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT)

        btn_back = CustomButton(
            button_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Frame de búsqueda (a la derecha del botón Regresar)
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # Campo de búsqueda
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Combobox para seleccionar campo de búsqueda
        search_fields = [
            "Todos los campos",
            "ID",
            "Cliente",
            "Servicio",
            "Estado Solicitud"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_fields,
            state="readonly",
            width=20
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Frame para los botones de acciones (derecha)
        action_frame = tk.Frame(top_frame)
        action_frame.pack(side=tk.RIGHT)

        btn_enable = CustomButton(
            action_frame,
            text="Habilitar",
            command=self.enable_request,
            padding=8,
            width=12
        )
        btn_enable.pack(side=tk.RIGHT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Cliente", "Servicio", "Descripción", "Cantidad", 
            "Total", "Estado Solicitud"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Cliente", 150, tk.W),
            ("Servicio", 120, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Estado Solicitud", 120, tk.CENTER)
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
            text="",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.refresh_data()

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        requests = ServiceRequest.search_inactive(search_term, field if field != "Todos los campos" else None)
        
        for req in requests:
            self.tree.insert("", tk.END, values=(
                req['id'],
                req['customer_name'],
                req['service_name'],
                req['description'],
                req['quantity'],
                f"{req['total']:.2f}",
                req['request_status_name'],
                "Inactivo"
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(requests)} solicitudes deshabilitadas")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def enable_request(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        request_id = self.tree.item(selected[0])['values'][0]
        service_name = self.tree.item(selected[0])['values'][2]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea habilitar la solicitud '{service_name}'?",
            parent=self
        )
        
        if response:
            try:
                ServiceRequest.activate(request_id)
                messagebox.showinfo("Éxito", "Solicitud habilitada correctamente", parent=self)
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo habilitar la solicitud: {str(e)}", parent=self)