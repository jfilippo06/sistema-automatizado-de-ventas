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
        self.configure(bg="#f5f5f5")
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Solicitudes de Servicio",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Frame para botón de regreso
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Frame principal para controles
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame de búsqueda
        search_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Campo de búsqueda
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 12)
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
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

        # Frame para los botones de acciones
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        btn_update_status = CustomButton(
            action_frame,
            text="Cambiar Estado",
            command=self.update_request_status,
            padding=8,
            width=15
        )
        btn_update_status.pack(side=tk.RIGHT, padx=5)

        btn_disable = CustomButton(
            action_frame,
            text="Deshabilitar",
            command=self.disable_item,
            padding=8,
            width=12,
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        btn_edit = CustomButton(
            action_frame,
            text="Editar",
            command=self.edit_item,
            padding=8,
            width=10,
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Treeview para solicitudes
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Número de solicitud", "Empleado", "Cliente", "Servicio", 
            "Descripción", "Cantidad", "Total", "Estado Solicitud"
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
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = ServiceRequest.search_active(search_term, field if field != "Todos los campos" else None)
        
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
                item.get('employee_name', 'Sin asignar'),
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
        status_window.geometry("400x200")
        status_window.resizable(False, False)
        status_window.configure(bg="#f5f5f5")
        status_window.transient(self)
        status_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(status_window, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = tk.Frame(main_frame, bg="#4a6fa5")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        CustomLabel(
            title_frame,
            text=f"Estado actual: {current_status}",
            font=("Arial", 12),
            fg="white",
            bg="#4a6fa5"
        ).pack(pady=10, padx=10, anchor="w")
        
        # Controles
        control_frame = tk.Frame(main_frame, bg="#f5f5f5")
        control_frame.pack(fill=tk.X, pady=5)
        
        CustomLabel(
            control_frame,
            text="Nuevo estado:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        status_var = tk.StringVar()
        
        status_options = {
            "Iniciado": "started",
            "En progreso": "in_progress",
            "Completado": "completed",
        }
        
        status_combobox = CustomCombobox(
            control_frame,
            textvariable=status_var,
            values=list(status_options.keys()),
            state="readonly",
            width=20
        )
        status_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
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
        
        # Frame de botones
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(pady=15, anchor="e")
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=status_window.destroy,
            padding=8,
            width=12
        ).pack(side=tk.RIGHT, padx=5)
        
        CustomButton(
            btn_frame,
            text="Aplicar",
            command=apply_status,
            padding=8,
            width=12
        ).pack(side=tk.RIGHT, padx=5)