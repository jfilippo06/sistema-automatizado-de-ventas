# screens/customers/customers.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.customers.reports_screen import CustomerReportsScreen
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry

class CustomersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')  # Pantalla completa
        super().pack(fill=tk.BOTH, expand=True)

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

        # Frame de botones y búsqueda
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botón Regresar
        btn_back = CustomButton(
            control_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Botón Reportes
        btn_reports = CustomButton(
            control_frame,
            text="Reportes",
            command=self.open_reports,
            padding=8,
            width=12
        )
        btn_reports.pack(side=tk.RIGHT, padx=5)

        # Frame de búsqueda
        search_frame = tk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        lbl_search = CustomLabel(
            search_frame,
            text="Buscar:",
            font=("Arial", 10),
            fg="#333"
        )
        lbl_search.pack(side=tk.LEFT, padx=5)

        self.entry_search = CustomEntry(
            search_frame,
            width=40
        )
        self.entry_search.pack(side=tk.LEFT, padx=5)
        self.entry_search.bind("<KeyRelease>", self.search_customers)

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Nombres", "Apellidos", "Cédula", "Email", 
            "Teléfono", "Dirección", "Estado"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Nombres", 120, tk.W),
            ("Apellidos", 120, tk.W),
            ("Cédula", 100, tk.CENTER),
            ("Email", 180, tk.W),
            ("Teléfono", 100, tk.CENTER),
            ("Dirección", 200, tk.W),
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
            text=f"Mostrando {len(Customer.all())} clientes",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.refresh_data()

    def refresh_data(self, customers: List[Dict] = None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            items = customers if customers is not None else Customer.all()
            for item in items:
                self.tree.insert("", tk.END, values=(
                    item['id'],
                    item['first_name'],
                    item['last_name'],
                    item['id_number'],
                    item.get('email', ''),
                    item.get('phone', ''),
                    item.get('address', ''),
                    item.get('status_name', 'Activo')
                ))
            self.status_bar.configure(text=f"Mostrando {len(items)} clientes")
        except Exception as e:
            self.status_bar.configure(text=f"Error al cargar datos: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}", parent=self)

    def search_customers(self, event=None) -> None:
        search_term = self.entry_search.get().lower()
        if not search_term:
            self.refresh_data()
            return
            
        try:
            all_customers = Customer.all()
            filtered = [
                c for c in all_customers
                if (search_term in str(c['id']).lower() or
                    search_term in c['first_name'].lower() or
                    search_term in c['last_name'].lower() or
                    search_term in c['id_number'].lower() or
                    search_term in c.get('email', '').lower() or
                    search_term in c.get('phone', '').lower() or
                    search_term in c.get('address', '').lower())
            ]
            self.refresh_data(filtered)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {str(e)}", parent=self)

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def open_reports(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Selección requerida", 
                "Por favor seleccione un cliente para generar el reporte",
                parent=self
            )
            return
        
        CustomerReportsScreen(self.parent)