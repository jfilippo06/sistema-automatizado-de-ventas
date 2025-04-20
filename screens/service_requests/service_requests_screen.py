# screens/service_requests/service_requests_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.service_requests.crud_service_request import CrudServiceRequest
from sqlite_cli.models.request_status_model import RequestStatus
from sqlite_cli.models.service_request_model import ServiceRequest
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class ServiceRequestsScreen(tk.Frame):
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
            text="Solicitudes de Servicio",
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
            "Número de solicitud",
            "Cliente",
            "Servicio",
            "Estado Solicitud",
            "Empleado"
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

        btn_add = CustomButton(
            action_frame,
            text="Agregar",
            command=self.add_item,
            padding=8,
            width=10
        )
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit = CustomButton(
            action_frame,
            text="Editar",
            command=self.edit_item,
            padding=8,
            width=10
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable = CustomButton(
            action_frame,
            text="Deshabilitar",
            command=self.disable_item,
            padding=8,
            width=12
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        btn_update_status = CustomButton(
            action_frame,
            text="Cambiar Estado",
            command=self.update_request_status,
            padding=8,
            width=15
        )
        btn_update_status.pack(side=tk.RIGHT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview para solicitudes
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Número de solicitud", "Empleado", "Cliente", "Servicio", "Descripción", "Cantidad", 
            "Total", "Estado Solicitud"
        ), show="headings")

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
            
        items = ServiceRequest.search_active(search_term, field if field != "Todos los campos" else None)
        
        # Mapeo de estados en inglés a español
        status_mapping = {
            "started": "Iniciado",
            "in_progress": "En progreso",
            "completed": "Completado",
        }
        
        for item in items:
            status = item['request_status_name']
            status_es = status_mapping.get(status, status)
            
            self.tree.insert("", tk.END, values=(
                item['id'],
                item['request_number'],
                item['employee_name'],
                item['customer_name'],
                item['service_name'],
                item['description'],
                item['quantity'],
                f"{item['total']:.2f}",
                status_es
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(items)} solicitudes")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def add_item(self) -> None:
        CrudServiceRequest(self, mode="create", refresh_callback=self.refresh_data)

    def edit_item(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        CrudServiceRequest(self, mode="edit", item_id=item_id, refresh_callback=self.refresh_data)

    def disable_item(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        service_name = self.tree.item(selected[0])['values'][4]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar la solicitud '{service_name}'?",
            parent=self
        )
        
        if response:
            try:
                ServiceRequest.deactivate(item_id)
                messagebox.showinfo("Éxito", "Solicitud deshabilitada correctamente", parent=self)
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar la solicitud: {str(e)}", parent=self)

    def update_request_status(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        current_status = self.tree.item(selected[0])['values'][8]
        
        status_window = tk.Toplevel(self)
        status_window.title("Cambiar Estado de Solicitud")
        status_window.geometry("300x200")
        status_window.resizable(False, False)
        status_window.transient(self)
        status_window.grab_set()
        
        tk.Label(
            status_window, 
            text=f"Estado actual: {current_status}",
            font=("Arial", 10)
        ).pack(pady=10)
        
        tk.Label(
            status_window, 
            text="Nuevo estado:",
            font=("Arial", 10)
        ).pack(pady=5)
        
        status_var = tk.StringVar()
        
        # Estados en español pero guardamos los valores en inglés
        status_options = {
            "Iniciado": "started",
            "En progreso": "in_progress",
            "Completado": "completed",
        }
        
        status_combobox = ttk.Combobox(
            status_window,
            textvariable=status_var,
            values=list(status_options.keys()),
            state="readonly"
        )
        status_combobox.pack(pady=5)
        
        def apply_status():
            new_status = status_var.get()
            if not new_status:
                messagebox.showwarning("Advertencia", "Seleccione un estado", parent=status_window)
                return
                
            try:
                status_english = status_options.get(new_status)
                if status_english:
                    status = RequestStatus.get_by_name(status_english)
                    if status:
                        ServiceRequest.update_request_status(item_id, status['id'])
                        messagebox.showinfo("Éxito", "Estado actualizado correctamente", parent=status_window)
                        self.refresh_data()
                        status_window.destroy()
                    else:
                        messagebox.showerror("Error", "Estado no válido", parent=status_window)
                else:
                    messagebox.showerror("Error", "Estado no válido", parent=status_window)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el estado: {str(e)}", parent=status_window)
        
        btn_frame = tk.Frame(status_window)
        btn_frame.pack(pady=10)
        
        CustomButton(
            btn_frame,
            text="Aplicar",
            command=apply_status,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=status_window.destroy,
            padding=6,
            width=10
        ).pack(side=tk.LEFT, padx=5)