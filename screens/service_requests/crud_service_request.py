import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any, List
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.user_model import User
from sqlite_cli.models.service_request_movement_type_model import ServiceRequestMovementType
from utils.session_manager import SessionManager
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_combobox import CustomCombobox

class CrudServiceRequest(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "edit", 
        item_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        self.employee_users = []
        
        self.title("Editar Solicitud")
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.employee_var = tk.StringVar()
        
        self.configure_ui()
        self.load_item_data()

    def configure_ui(self) -> None:
        # Frame principal con fondo gris claro
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título con estilo azul
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        title_label = CustomLabel(
            title_frame,
            text="Asignar Empleado",
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.pack(pady=10, padx=10, anchor="w")
        
        # Frame para campo de empleado
        field_frame = tk.Frame(main_frame, bg="#f5f5f5")
        field_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        field_label = CustomLabel(
            field_frame,
            text="Empleado:",
            font=("Arial", 10),
            fg="#333",
            bg="#f5f5f5",
            width=15,
            anchor="w"
        )
        field_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.employee_combobox = CustomCombobox(
            field_frame,
            textvariable=self.employee_var,
            values=[],
            state="readonly",
            width=25
        )
        self.employee_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(30, 10), sticky="e")
        
        # Botón Cancelar
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Botón Actualizar
        btn_action = CustomButton(
            btn_frame, 
            text="Actualizar", 
            command=self.update_item,
            padding=8,
            width=12
        )
        btn_action.pack(side=tk.RIGHT, padx=5)

    def get_employee_users(self) -> List[Dict]:
        """Obtiene solo los usuarios con rol de empleado"""
        all_users = User.all()
        employee_users = []
        
        for user in all_users:
            if user['role_name'].lower() == 'employee':
                employee_users.append({
                    'id': user['id'],
                    'name': f"{user['first_name']} {user['last_name']}"
                })
        
        return employee_users

    def load_item_data(self) -> None:
        try:
            if not self.item_id:
                raise ValueError("ID de solicitud no válido")
                
            request = ServiceRequest.get_by_id(self.item_id)
            if not request:
                raise ValueError("Solicitud no encontrada")
            
            self.employee_users = self.get_employee_users()
            employee_names = [emp['name'] for emp in self.employee_users]
            
            self.employee_combobox['values'] = employee_names
            
            if request['employee_name'] and request['employee_name'] != 'Sin asignar':
                self.employee_var.set(request['employee_name'])
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    def update_item(self) -> None:
        try:
            if not self.item_id:
                raise ValueError("ID de solicitud no válido")
                
            employee_name = self.employee_var.get()
            if not employee_name:
                messagebox.showwarning("Advertencia", "Seleccione un empleado", parent=self)
                return
                
            employee = next((emp for emp in self.employee_users if emp['name'] == employee_name), None)
            if not employee:
                raise ValueError("Debe seleccionar un empleado válido")
            
            # Obtener datos actuales antes de cambiar
            request = ServiceRequest.get_by_id(self.item_id)
            if not request:
                raise ValueError("Solicitud no encontrada")
            
            # Actualizar empleado
            ServiceRequest.update_employee(
                request_id=self.item_id,
                employee_id=employee['id']
            )
            
            # Registrar movimiento en el historial
            ServiceRequestMovementType.record_movement(
                request_id=self.item_id,
                movement_type_name="ASIGNACION_EMPLEADO",
                previous_employee_id=request['employee_id'],
                new_employee_id=employee['id'],
                notes=f"Empleado asignado: {employee_name}"
            )
            
            messagebox.showinfo("Éxito", "Empleado asignado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la solicitud: {str(e)}", parent=self)