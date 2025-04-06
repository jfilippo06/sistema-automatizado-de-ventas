# screens/service_requests/service_requests_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.service_requests.crud_service_request import CrudServiceRequest
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.status_model import Status
from sqlite_cli.models.request_status_model import RequestStatus
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel

class ServiceRequestsScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure_ui()

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

        # Botones de acción
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

        self.btn_update_status = CustomButton(
            control_frame,
            text="Cambiar Estado",
            command=self.update_request_status,
            padding=8,
            width=15
        )
        self.btn_update_status.pack(side=tk.RIGHT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview para solicitudes
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Cliente", "Servicio", "Descripción", "Cantidad", 
            "Total", "Estado Solicitud", "Estado"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Cliente", 150, tk.W),
            ("Servicio", 120, tk.W),
            ("Descripción", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Total", 100, tk.CENTER),
            ("Estado Solicitud", 120, tk.CENTER),
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
            text="",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.refresh_data()

    def refresh_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            items = ServiceRequest.all()
            for item in items:
                self.tree.insert("", tk.END, values=(
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
        item_name = self.tree.item(selected[0])['values'][2]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar la solicitud '{item_name}'?",
            parent=self
        )
        
        if response:
            try:
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    ServiceRequest.update_status(item_id, status_inactive['id'])
                    messagebox.showinfo("Éxito", "Solicitud deshabilitada correctamente", parent=self)
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar la solicitud: {str(e)}", parent=self)

    def update_request_status(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        current_status = self.tree.item(selected[0])['values'][6]
        
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
                    self.refresh_data()
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