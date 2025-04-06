# screens/customers/customers.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
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
        # Configura la ventana en pantalla completa al mostrarse
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Frame superior con el título
        header_frame = tk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Título de la pantalla
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Clientes",
            font=("Arial", 16, "bold"),
            fg="#333"
        )
        title_label.pack(side=tk.LEFT)

        # Frame de controles (botones y búsqueda)
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botón para regresar a la pantalla anterior
        btn_back = CustomButton(
            control_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        # Frame para la búsqueda de clientes
        search_frame = tk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # Etiqueta para el campo de búsqueda
        lbl_search = CustomLabel(
            search_frame,
            text="Buscar:",
            font=("Arial", 10),
            fg="#333"
        )
        lbl_search.pack(side=tk.LEFT, padx=5)

        # Campo de entrada para búsqueda
        self.entry_search = CustomEntry(
            search_frame,
            width=40
        )
        self.entry_search.pack(side=tk.LEFT, padx=5)
        # Configura la búsqueda mientras se escribe
        self.entry_search.bind("<KeyRelease>", self.search_customers)

        # Frame para la tabla de clientes
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla (Treeview)
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Nombres", "Apellidos", "Cédula", "Email", 
            "Teléfono", "Dirección", "Estado"
        ), show="headings")

        # Columnas de la tabla con sus configuraciones
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

        # Configura cada columna
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        # Barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de estado inferior
        self.status_bar = CustomLabel(
            self,
            text=f"Mostrando {len(Customer.all())} clientes",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Carga los datos iniciales
        self.refresh_data()

    def refresh_data(self, customers: List[Dict] = None) -> None:
        """Actualiza los datos mostrados en la tabla"""
        # Limpia la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Obtiene los clientes a mostrar (todos o los filtrados)
            items = customers if customers is not None else Customer.all()
            
            # Agrega cada cliente a la tabla
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
            
            # Actualiza el contador en la barra de estado
            self.status_bar.configure(text=f"Mostrando {len(items)} clientes")
        except Exception as e:
            # Manejo de errores al cargar los datos
            self.status_bar.configure(text=f"Error al cargar datos: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}", parent=self)

    def search_customers(self, event=None) -> None:
        """Filtra los clientes según el término de búsqueda"""
        search_term = self.entry_search.get().lower()
        
        # Si no hay término de búsqueda, muestra todos los clientes
        if not search_term:
            self.refresh_data()
            return
            
        try:
            # Obtiene todos los clientes y filtra según el término
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
            
            # Actualiza la tabla con los resultados filtrados
            self.refresh_data(filtered)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {str(e)}", parent=self)

    def go_back(self) -> None:
        """Regresa a la pantalla anterior"""
        # Restaura el tamaño normal de la ventana
        self.parent.state('normal')
        # Llama al callback para mostrar la pantalla anterior
        self.open_previous_screen_callback()