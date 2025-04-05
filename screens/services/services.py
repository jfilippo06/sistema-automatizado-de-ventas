# screens/services/services_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.services.crud_service import CrudService
from screens.services.crud_service_request import CrudServiceRequest
from sqlite_cli.models.service_model import Service
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.status_model import Status
from sqlite_cli.models.request_status_model import RequestStatus
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry

class ServicesScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.current_mode = "requests"  # "requests" or "services"
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
            text="Gestión de Servicios",
            font=("Arial", 16, "bold"),
            fg="#333"
        )
        title_label.pack(side=tk.LEFT)

        # Frame de botones de modo
        mode_frame = tk.Frame(self)
        mode_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        btn_requests = CustomButton(
            mode_frame,
            text="Solicitudes de Servicio",
            command=lambda: self.switch_mode("requests"),
            padding=8,
            width=20
        )
        btn_requests.pack(side=tk.LEFT, padx=5)

        btn_services = CustomButton(
            mode_frame,
            text="Servicios",
            command=lambda: self.switch_mode("services"),
            padding=8,
            width=20
        )
        btn_services.pack(side=tk.LEFT, padx=5)

        # Frame de botones de acción
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

        # Botones específicos del modo
        self.btn_add = CustomButton(
            control_frame,
            text="Crear",
            command=self.add_item,
            padding=8,
            width=10
        )
        self.btn_add.pack(side=tk.RIGHT, padx=5)

        self.btn_edit = CustomButton(
            control_frame,
            text="Editar",
            command=self.edit_item,
            padding=8,
            width=10
        )
        self.btn_edit.pack(side=tk.RIGHT, padx=5)

        self.btn_disable = CustomButton(
            control_frame,
            text="Deshabilitar",
            command=self.disable_item,
            padding=8,
            width=12
        )
        self.btn_disable.pack(side=tk.RIGHT, padx=5)

        # Botón específico para solicitudes
        self.btn_update_status = CustomButton(
            control_frame,
            text="Cambiar Estado",
            command=self.update_request_status,
            padding=8,
            width=15
        )
        self.btn_update_status.pack(side=tk.RIGHT, padx=5)
        self.btn_update_status.pack_forget()  # Ocultar inicialmente

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview para solicitudes
        self.tree_requests = ttk.Treeview(tree_frame, columns=(
            "ID", "Cliente", "Servicio", "Descripción", "Cantidad", 
            "Total", "Estado Solicitud", "Estado"
        ), show="headings")

        columns_requests = [
            ("ID", 50, tk.CENTER),
            ("Cliente", 150, tk.W),
            ("Servicio", 120, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Estado Solicitud", 120, tk.CENTER),
            ("Estado", 100, tk.CENTER)
        ]

        for col, width, anchor in columns_requests:
            self.tree_requests.heading(col, text=col)
            self.tree_requests.column(col, width=width, anchor=anchor)

        # Treeview para servicios
        self.tree_services = ttk.Treeview(tree_frame, columns=(
            "ID", "Nombre", "Precio", "Descripción", "Estado"
        ), show="headings")

        columns_services = [
            ("ID", 50, tk.CENTER),
            ("Nombre", 200, tk.W),
            ("Precio", 100, tk.CENTER),
            ("Descripción", 300, tk.W),
            ("Estado", 100, tk.CENTER)
        ]

        for col, width, anchor in columns_services:
            self.tree_services.heading(col, text=col)
            self.tree_services.column(col, width=width, anchor=anchor)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree_requests.configure(yscroll=self.scrollbar.set)
        self.tree_services.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mostrar el treeview inicial
        self.tree_requests.pack(fill=tk.BOTH, expand=True)
        self.tree_services.pack_forget()

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Inicializar con el modo de solicitudes
        self.switch_mode("requests")

    def switch_mode(self, mode: str) -> None:
        """Cambia entre los modos de solicitudes y servicios."""
        self.current_mode = mode
        
        if mode == "requests":
            self.tree_services.pack_forget()
            self.tree_requests.pack(fill=tk.BOTH, expand=True)
            self.btn_update_status.pack(side=tk.RIGHT, padx=5)
            self.refresh_requests_data()
        else:
            self.tree_requests.pack_forget()
            self.tree_services.pack(fill=tk.BOTH, expand=True)
            self.btn_update_status.pack_forget()
            self.refresh_services_data()

    def refresh_requests_data(self) -> None:
        """Actualiza los datos de solicitudes en el treeview."""
        for item in self.tree_requests.get_children():
            self.tree_requests.delete(item)
            
        try:
            items = ServiceRequest.all()
            for item in items:
                self.tree_requests.insert("", tk.END, values=(
                    item['id'],
                    item['customer_name'],
                    item['service_name'],
                    item['description'],
                    item['quantity'],
                    f"${item['total']:.2f}",
                    item['request_status_name'],
                    "Activo" if item['status_id'] == 1 else "Inactivo"
                ))
            self.status_bar.configure(text=f"Mostrando {len(items)} solicitudes")
        except Exception as e:
            self.status_bar.configure(text=f"Error al cargar solicitudes: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar las solicitudes: {str(e)}", parent=self)

    def refresh_services_data(self) -> None:
        """Actualiza los datos de servicios en el treeview."""
        for item in self.tree_services.get_children():
            self.tree_services.delete(item)
            
        try:
            items = Service.all()
            for item in items:
                self.tree_services.insert("", tk.END, values=(
                    item['id'],
                    item['name'],
                    f"${item['price']:.2f}",
                    item.get('description', ''),
                    "Activo" if item['status_id'] == 1 else "Inactivo"
                ))
            self.status_bar.configure(text=f"Mostrando {len(items)} servicios")
        except Exception as e:
            self.status_bar.configure(text=f"Error al cargar servicios: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar los servicios: {str(e)}", parent=self)

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def add_item(self) -> None:
        if self.current_mode == "requests":
            CrudServiceRequest(self, mode="create", refresh_callback=self.refresh_requests_data)
        else:
            CrudService(self, mode="create", refresh_callback=self.refresh_services_data)

    def edit_item(self) -> None:
        selected = self.get_selected_item()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un elemento", parent=self)
            return
            
        item_id = selected['values'][0]
        
        if self.current_mode == "requests":
            CrudServiceRequest(self, mode="edit", item_id=item_id, refresh_callback=self.refresh_requests_data)
        else:
            CrudService(self, mode="edit", item_id=item_id, refresh_callback=self.refresh_services_data)

    def disable_item(self) -> None:
        selected = self.get_selected_item()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un elemento", parent=self)
            return
            
        item_id = selected['values'][0]
        item_name = selected['values'][1] if self.current_mode == "services" else selected['values'][2]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar {'el servicio' if self.current_mode == 'services' else 'la solicitud'} '{item_name}'?",
            parent=self
        )
        
        if response:
            try:
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    if self.current_mode == "services":
                        Service.update_status(item_id, status_inactive['id'])
                    else:
                        ServiceRequest.update_status(item_id, status_inactive['id'])
                    
                    messagebox.showinfo("Éxito", "Operación realizada correctamente", parent=self)
                    if self.current_mode == "services":
                        self.refresh_services_data()
                    else:
                        self.refresh_requests_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar la operación: {str(e)}", parent=self)

    def update_request_status(self) -> None:
        if self.current_mode != "requests":
            return
            
        selected = self.tree_requests.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        item_id = self.tree_requests.item(selected[0])['values'][0]
        current_status = self.tree_requests.item(selected[0])['values'][6]
        
        # Crear ventana para seleccionar nuevo estado
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
        statuses = [s['name'] for s in RequestStatus.all()]
        status_combobox = ttk.Combobox(
            status_window,
            textvariable=status_var,
            values=statuses,
            state="readonly"
        )
        status_combobox.pack(pady=5)
        
        def apply_status():
            new_status = status_var.get()
            if not new_status:
                messagebox.showwarning("Advertencia", "Seleccione un estado", parent=status_window)
                return
                
            try:
                status = RequestStatus.get_by_name(new_status)
                if status:
                    ServiceRequest.update_request_status(item_id, status['id'])
                    messagebox.showinfo("Éxito", "Estado actualizado correctamente", parent=status_window)
                    self.refresh_requests_data()
                    status_window.destroy()
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

    def get_selected_item(self):
        """Obtiene el elemento seleccionado según el modo actual."""
        if self.current_mode == "requests":
            selected = self.tree_requests.selection()
            return self.tree_requests.item(selected[0]) if selected else None
        else:
            selected = self.tree_services.selection()
            return self.tree_services.item(selected[0]) if selected else None