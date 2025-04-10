import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.customers.crud_customer import CrudCustomer
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class CustomersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        # Forzar actualización de datos al mostrar la pantalla
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Clientes",
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
            "Nombres",
            "Apellidos",
            "Cédula",
            "Email",
            "Teléfono"
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

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview (sin columna de estado)
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Nombres", "Apellidos", "Cédula", "Email", "Teléfono", "Dirección"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Nombres", 150, tk.W),
            ("Apellidos", 150, tk.W),
            ("Cédula", 100, tk.CENTER),
            ("Email", 180, tk.W),
            ("Teléfono", 100, tk.CENTER),
            ("Dirección", 200, tk.W)
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
            
        customers = Customer.search_active(search_term, field if field != "Todos los campos" else None)
        
        for customer in customers:
            self.tree.insert("", tk.END, values=(
                customer['id'],
                customer['first_name'],
                customer['last_name'],
                customer['id_number'],
                customer.get('email', ''),
                customer.get('phone', ''),
                customer.get('address', '')
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(customers)} clientes")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()